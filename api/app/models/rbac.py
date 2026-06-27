from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Table, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from typing import Optional
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class PermissionGroup(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'permission_groups'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    display_name = Column(String(255), nullable=False)
    icon = Column(String(100))
    sort_order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    permissions = relationship('Permission', back_populates='group', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'display_name': self.display_name,
            'icon': self.icon,
            'sort_order': self.sort_order,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class Permission(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'permissions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    display_name = Column(String(255), nullable=False)
    resource = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey('permission_groups.id'))
    is_active = Column(Boolean, default=True)

    group = relationship('PermissionGroup', back_populates='permissions')
    role_permissions = relationship('RolePermission', back_populates='permission', cascade='all, delete-orphan')

    __table_args__ = (
        Index('idx_permission_resource_action', 'resource', 'action'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'display_name': self.display_name,
            'resource': self.resource,
            'action': self.action,
            'group_id': self.group_id,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class Role(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'roles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    display_name = Column(String(255), nullable=False)
    level = Column(Integer, default=0)
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'))
    parent_role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'))
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    max_users = Column(Integer)

    organization = relationship('Organization', back_populates='roles')
    parent_role = relationship('Role', remote_side=[id], backref='child_roles')
    creator = relationship('User', foreign_keys=[created_by])
    role_permissions = relationship('RolePermission', back_populates='role', cascade='all, delete-orphan')
    user_roles = relationship('UserRole', back_populates='role', cascade='all, delete-orphan')
    template_roles = relationship('RoleTemplate', back_populates='role', cascade='all, delete-orphan')

    __table_args__ = (
        Index('idx_role_organization', 'organization_id'),
        Index('idx_role_parent', 'parent_role_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'display_name': self.display_name,
            'level': self.level,
            'is_system': self.is_system,
            'is_active': self.is_active,
            'organization_id': self.organization_id,
            'parent_role_id': self.parent_role_id,
            'created_by': self.created_by,
            'max_users': self.max_users,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class RolePermission(Base, TimestampMixin):
    __tablename__ = 'role_permissions'

    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True)
    permission_id = Column(UUID(as_uuid=True), ForeignKey('permissions.id'), primary_key=True)
    granted_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    granted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    role = relationship('Role', back_populates='role_permissions')
    permission = relationship('Permission', back_populates='role_permissions')
    granter = relationship('User', foreign_keys=[granted_by])

    __table_args__ = (
        Index('idx_role_permission_role', 'role_id'),
        Index('idx_role_permission_permission', 'permission_id'),
    )

    def to_dict(self):
        return {
            'role_id': self.role_id,
            'permission_id': self.permission_id,
            'granted_by': self.granted_by,
            'granted_at': self.granted_at,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class UserRole(Base, TimestampMixin):
    __tablename__ = 'user_roles'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'), primary_key=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'))
    assigned_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    assigned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)

    user = relationship('User', back_populates='user_roles')
    role = relationship('Role', back_populates='user_roles')
    organization = relationship('Organization', back_populates='user_roles')
    assigner = relationship('User', foreign_keys=[assigned_by])

    __table_args__ = (
        Index('idx_user_role_user', 'user_id'),
        Index('idx_user_role_role', 'role_id'),
        Index('idx_user_role_organization', 'organization_id'),
    )

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'role_id': self.role_id,
            'organization_id': self.organization_id,
            'assigned_by': self.assigned_by,
            'assigned_at': self.assigned_at,
            'expires_at': self.expires_at,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class RoleTemplate(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = 'role_templates'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    display_name = Column(String(255), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'))
    is_system = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)

    role = relationship('Role', back_populates='template_roles')

    __table_args__ = (
        Index('idx_role_template_name', 'name'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'display_name': self.display_name,
            'role_id': self.role_id,
            'is_system': self.is_system,
            'is_active': self.is_active,
            'usage_count': self.usage_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }
