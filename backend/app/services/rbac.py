from typing import Optional, List, Dict, Set
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.models.rbac import (
    Permission, PermissionGroup, Role, RolePermission,
    UserRole, RoleTemplate
)
from app.models import User, Organization


class RBACService:
    def __init__(self, db: Session):
        self.db = db
        self._permission_cache: Dict[str, Set[str]] = {}

    def _get_cache_key(self, user_id: UUID, organization_id: Optional[UUID] = None) -> str:
        return f"user:{user_id}:org:{organization_id}"

    def _invalidate_cache(self, user_id: UUID, organization_id: Optional[UUID] = None):
        key = self._get_cache_key(user_id, organization_id)
        self._permission_cache.pop(key, None)

    async def get_user_permissions(
        self, user_id: UUID, organization_id: Optional[UUID] = None
    ) -> Set[str]:
        cache_key = self._get_cache_key(user_id, organization_id)
        if cache_key in self._permission_cache:
            return self._permission_cache[cache_key]

        query = (
            self.db.query(Permission.name)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .join(UserRole, UserRole.role_id == RolePermission.role_id)
            .where(
                and_(
                    UserRole.user_id == user_id,
                    UserRole.is_active == True,
                    Permission.is_active == True,
                    or_(
                        UserRole.expires_at.is_(None),
                        UserRole.expires_at > datetime.now(timezone.utc)
                    )
                )
            )
        )

        if organization_id:
            query = query.where(UserRole.organization_id == organization_id)

        permissions = {row[0] for row in query.all()}

        parent_roles = self._get_inherited_role_permissions(user_id, organization_id)
        permissions.update(parent_roles)

        self._permission_cache[cache_key] = permissions
        return permissions

    def _get_inherited_role_permissions(
        self, user_id: UUID, organization_id: Optional[UUID] = None
    ) -> Set[str]:
        permissions = set()
        visited = set()

        role_ids = (
            self.db.query(UserRole.role_id)
            .filter(
                and_(
                    UserRole.user_id == user_id,
                    UserRole.is_active == True
                )
            )
            .all()
        )

        for (role_id,) in role_ids:
            self._collect_inherited_permissions(role_id, permissions, visited)

        return permissions

    def _collect_inherited_permissions(
        self, role_id: UUID, permissions: Set[str], visited: Set[UUID]
    ):
        if role_id in visited:
            return
        visited.add(role_id)

        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role or not role.is_active:
            return

        role_perms = (
            self.db.query(Permission.name)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .filter(RolePermission.role_id == role_id)
            .all()
        )
        permissions.update([p[0] for p in role_perms])

        if role.parent_role_id:
            self._collect_inherited_permissions(role.parent_role_id, permissions, visited)

    async def check_permission(
        self,
        user_id: UUID,
        permission_name: str,
        organization_id: Optional[UUID] = None
    ) -> bool:
        user = self.db.query(User).filter(User.id == user_id).first()
        if user and user.role == 'admin':
            return True

        permissions = await self.get_user_permissions(user_id, organization_id)
        return permission_name in permissions

    async def check_any_permission(
        self,
        user_id: UUID,
        permission_names: List[str],
        organization_id: Optional[UUID] = None
    ) -> bool:
        permissions = await self.get_user_permissions(user_id, organization_id)
        return bool(permissions.intersection(permission_names))

    async def check_all_permissions(
        self,
        user_id: UUID,
        permission_names: List[str],
        organization_id: Optional[UUID] = None
    ) -> bool:
        permissions = await self.get_user_permissions(user_id, organization_id)
        return permissions.issuperset(permission_names)

    async def assign_role_to_user(
        self,
        user_id: UUID,
        role_id: UUID,
        organization_id: Optional[UUID] = None,
        assigned_by: Optional[UUID] = None,
        expires_at: Optional[datetime] = None
    ) -> UserRole:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise ValueError("Role not found")
        if not role.is_active:
            raise ValueError("Role is not active")

        if role.max_users:
            current_count = (
                self.db.query(UserRole)
                .filter(
                    and_(
                        UserRole.role_id == role_id,
                        UserRole.is_active == True
                    )
                )
                .count()
            )
            if current_count >= role.max_users:
                raise ValueError("Role has reached maximum user limit")

        existing = (
            self.db.query(UserRole)
            .filter(
                and_(
                    UserRole.user_id == user_id,
                    UserRole.role_id == role_id,
                    UserRole.organization_id == organization_id
                )
            )
            .first()
        )

        if existing:
            if existing.is_active:
                return existing
            existing.is_active = True
            existing.expires_at = expires_at
            self.db.commit()
            self._invalidate_cache(user_id, organization_id)
            return existing

        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            organization_id=organization_id,
            assigned_by=assigned_by,
            expires_at=expires_at,
            is_active=True
        )
        self.db.add(user_role)
        self.db.commit()
        self._invalidate_cache(user_id, organization_id)
        return user_role

    async def remove_role_from_user(
        self,
        user_id: UUID,
        role_id: UUID,
        organization_id: Optional[UUID] = None
    ) -> bool:
        user_role = (
            self.db.query(UserRole)
            .filter(
                and_(
                    UserRole.user_id == user_id,
                    UserRole.role_id == role_id,
                    UserRole.organization_id == organization_id
                )
            )
            .first()
        )

        if not user_role:
            return False

        user_role.is_active = False
        self.db.commit()
        self._invalidate_cache(user_id, organization_id)
        return True

    async def create_role(
        self,
        name: str,
        display_name: str,
        description: Optional[str] = None,
        level: int = 0,
        organization_id: Optional[UUID] = None,
        parent_role_id: Optional[UUID] = None,
        created_by: Optional[UUID] = None,
        permission_ids: Optional[List[UUID]] = None
    ) -> Role:
        existing = self.db.query(Role).filter(Role.name == name).first()
        if existing:
            raise ValueError(f"Role with name '{name}' already exists")

        if parent_role_id:
            parent = self.db.query(Role).filter(Role.id == parent_role_id).first()
            if not parent:
                raise ValueError("Parent role not found")

        role = Role(
            name=name,
            display_name=display_name,
            description=description,
            level=level,
            organization_id=organization_id,
            parent_role_id=parent_role_id,
            created_by=created_by,
            is_system=False,
            is_active=True
        )
        self.db.add(role)
        self.db.flush()

        if permission_ids:
            for perm_id in permission_ids:
                perm = self.db.query(Permission).filter(Permission.id == perm_id).first()
                if perm:
                    role_perm = RolePermission(
                        role_id=role.id,
                        permission_id=perm_id,
                        granted_by=created_by
                    )
                    self.db.add(role_perm)

        self.db.commit()
        return role

    async def update_role(
        self,
        role_id: UUID,
        name: Optional[str] = None,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
        level: Optional[int] = None,
        parent_role_id: Optional[UUID] = None,
        max_users: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> Role:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise ValueError("Role not found")

        if role.is_system:
            raise ValueError("Cannot modify system role")

        if name and name != role.name:
            existing = self.db.query(Role).filter(Role.name == name).first()
            if existing:
                raise ValueError(f"Role with name '{name}' already exists")
            role.name = name

        if display_name is not None:
            role.display_name = display_name
        if description is not None:
            role.description = description
        if level is not None:
            role.level = level
        if parent_role_id is not None:
            if parent_role_id == role_id:
                raise ValueError("Role cannot be its own parent")
            role.parent_role_id = parent_role_id
        if max_users is not None:
            role.max_users = max_users
        if is_active is not None:
            role.is_active = is_active

        self.db.commit()
        return role

    async def delete_role(self, role_id: UUID) -> bool:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise ValueError("Role not found")

        if role.is_system:
            raise ValueError("Cannot delete system role")

        active_users = (
            self.db.query(UserRole)
            .filter(
                and_(
                    UserRole.role_id == role_id,
                    UserRole.is_active == True
                )
            )
            .count()
        )
        if active_users > 0:
            raise ValueError("Cannot delete role with active users")

        role.soft_delete()
        self.db.commit()
        return True

    async def clone_role(
        self,
        role_id: UUID,
        new_name: str,
        new_display_name: str,
        created_by: Optional[UUID] = None
    ) -> Role:
        source_role = self.db.query(Role).filter(Role.id == role_id).first()
        if not source_role:
            raise ValueError("Source role not found")

        new_role = await self.create_role(
            name=new_name,
            display_name=new_display_name,
            description=f"Cloned from {source_role.display_name}",
            level=source_role.level,
            organization_id=source_role.organization_id,
            parent_role_id=source_role.parent_role_id,
            created_by=created_by
        )

        source_permissions = (
            self.db.query(RolePermission.permission_id)
            .filter(RolePermission.role_id == role_id)
            .all()
        )

        for (perm_id,) in source_permissions:
            role_perm = RolePermission(
                role_id=new_role.id,
                permission_id=perm_id,
                granted_by=created_by
            )
            self.db.add(role_perm)

        self.db.commit()
        return new_role

    async def assign_permission_to_role(
        self,
        role_id: UUID,
        permission_id: UUID,
        granted_by: Optional[UUID] = None
    ) -> RolePermission:
        role = self.db.query(Role).filter(Role.id == role_id).first()
        if not role:
            raise ValueError("Role not found")

        permission = self.db.query(Permission).filter(Permission.id == permission_id).first()
        if not permission:
            raise ValueError("Permission not found")

        existing = (
            self.db.query(RolePermission)
            .filter(
                and_(
                    RolePermission.role_id == role_id,
                    RolePermission.permission_id == permission_id
                )
            )
            .first()
        )

        if existing:
            return existing

        role_perm = RolePermission(
            role_id=role_id,
            permission_id=permission_id,
            granted_by=granted_by
        )
        self.db.add(role_perm)
        self.db.commit()
        return role_perm

    async def remove_permission_from_role(
        self,
        role_id: UUID,
        permission_id: UUID
    ) -> bool:
        role_perm = (
            self.db.query(RolePermission)
            .filter(
                and_(
                    RolePermission.role_id == role_id,
                    RolePermission.permission_id == permission_id
                )
            )
            .first()
        )

        if not role_perm:
            return False

        self.db.delete(role_perm)
        self.db.commit()
        return True

    async def get_role_permissions(self, role_id: UUID) -> List[Permission]:
        permissions = (
            self.db.query(Permission)
            .join(RolePermission, RolePermission.permission_id == Permission.id)
            .filter(
                and_(
                    RolePermission.role_id == role_id,
                    Permission.is_active == True
                )
            )
            .all()
        )
        return permissions

    async def get_user_roles(
        self, user_id: UUID, organization_id: Optional[UUID] = None
    ) -> List[UserRole]:
        query = (
            self.db.query(UserRole)
            .filter(
                and_(
                    UserRole.user_id == user_id,
                    UserRole.is_active == True,
                    or_(
                        UserRole.expires_at.is_(None),
                        UserRole.expires_at > datetime.now(timezone.utc)
                    )
                )
            )
        )

        if organization_id:
            query = query.filter(UserRole.organization_id == organization_id)

        return query.all()

    async def get_role_users(self, role_id: UUID) -> List[UserRole]:
        return (
            self.db.query(UserRole)
            .filter(
                and_(
                    UserRole.role_id == role_id,
                    UserRole.is_active == True
                )
            )
            .all()
        )

    async def get_all_roles(
        self,
        organization_id: Optional[UUID] = None,
        include_system: bool = True
    ) -> List[Role]:
        query = self.db.query(Role).filter(Role.is_active == True)

        if not include_system:
            query = query.filter(Role.is_system == False)

        if organization_id:
            query = query.filter(
                or_(
                    Role.organization_id == organization_id,
                    Role.organization_id.is_(None)
                )
            )

        return query.all()

    async def get_all_permissions(self, group_id: Optional[UUID] = None) -> List[Permission]:
        query = self.db.query(Permission).filter(Permission.is_active == True)

        if group_id:
            query = query.filter(Permission.group_id == group_id)

        return query.all()

    async def get_permission_groups(self) -> List[PermissionGroup]:
        return (
            self.db.query(PermissionGroup)
            .filter(PermissionGroup.is_active == True)
            .order_by(PermissionGroup.sort_order)
            .all()
        )

    async def get_permission_matrix(
        self, organization_id: Optional[UUID] = None
    ) -> Dict:
        roles = await self.get_all_roles(organization_id)
        permissions = await self.get_all_permissions()

        matrix = {}
        for role in roles:
            role_perms = await self.get_role_permissions(role.id)
            matrix[str(role.id)] = {str(p.id): True for p in role_perms}

        return {
            "roles": roles,
            "permissions": permissions,
            "matrix": matrix
        }

    async def bulk_assign_roles(
        self,
        user_ids: List[UUID],
        role_id: UUID,
        organization_id: Optional[UUID] = None,
        assigned_by: Optional[UUID] = None
    ) -> Dict:
        assigned = 0
        failed = 0
        errors = []

        for user_id in user_ids:
            try:
                await self.assign_role_to_user(
                    user_id=user_id,
                    role_id=role_id,
                    organization_id=organization_id,
                    assigned_by=assigned_by
                )
                assigned += 1
            except Exception as e:
                failed += 1
                errors.append(f"User {user_id}: {str(e)}")

        return {
            "assigned": assigned,
            "failed": failed,
            "errors": errors
        }

    async def create_default_roles(self, organization_id: UUID, created_by: UUID):
        default_roles = [
            {
                "name": "super_admin",
                "display_name": "Super Admin",
                "description": "Full system access with all permissions",
                "level": 100,
                "is_system": True
            },
            {
                "name": "org_owner",
                "display_name": "Organization Owner",
                "description": "Full organization management access",
                "level": 90,
                "is_system": True
            },
            {
                "name": "org_admin",
                "display_name": "Organization Admin",
                "description": "Organization administration access",
                "level": 80,
                "is_system": True
            },
            {
                "name": "workspace_manager",
                "display_name": "Workspace Manager",
                "description": "Workspace management access",
                "level": 70,
                "is_system": True
            },
            {
                "name": "editor",
                "display_name": "Editor",
                "description": "Content editing access",
                "level": 60,
                "is_system": True
            },
            {
                "name": "creator",
                "display_name": "Creator",
                "description": "Content creation access",
                "level": 50,
                "is_system": True
            },
            {
                "name": "analyst",
                "display_name": "Analyst",
                "description": "Analytics and reporting access",
                "level": 40,
                "is_system": True
            },
            {
                "name": "viewer",
                "display_name": "Viewer",
                "description": "Read-only access",
                "level": 10,
                "is_system": True
            }
        ]

        created_roles = []
        for role_data in default_roles:
            existing = self.db.query(Role).filter(Role.name == role_data["name"]).first()
            if not existing:
                role = Role(
                    **role_data,
                    organization_id=organization_id,
                    created_by=created_by
                )
                self.db.add(role)
                created_roles.append(role)

        self.db.commit()
        return created_roles
