from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


class PermissionGroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    display_name: str = Field(..., min_length=1, max_length=255)
    icon: Optional[str] = None
    sort_order: int = 0
    is_active: bool = True


class PermissionGroupCreate(PermissionGroupBase):
    pass


class PermissionGroupUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    display_name: Optional[str] = Field(None, min_length=1, max_length=255)
    icon: Optional[str] = None
    sort_order: Optional[int] = None
    is_active: Optional[bool] = None


class PermissionGroupResponse(PermissionGroupBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    display_name: str = Field(..., min_length=1, max_length=255)
    resource: str = Field(..., min_length=1, max_length=100)
    action: str = Field(..., min_length=1, max_length=50)
    group_id: Optional[UUID] = None
    is_active: bool = True


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    display_name: Optional[str] = Field(None, min_length=1, max_length=255)
    resource: Optional[str] = Field(None, min_length=1, max_length=100)
    action: Optional[str] = Field(None, min_length=1, max_length=50)
    group_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class PermissionResponse(PermissionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    display_name: str = Field(..., min_length=1, max_length=255)
    level: int = 0
    is_system: bool = False
    is_active: bool = True
    organization_id: Optional[UUID] = None
    parent_role_id: Optional[UUID] = None
    max_users: Optional[int] = None


class RoleCreate(RoleBase):
    permission_ids: List[UUID] = []


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    display_name: Optional[str] = Field(None, min_length=1, max_length=255)
    level: Optional[int] = None
    is_system: Optional[bool] = None
    is_active: Optional[bool] = None
    parent_role_id: Optional[UUID] = None
    max_users: Optional[int] = None


class RoleResponse(RoleBase):
    id: UUID
    created_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RoleDetailResponse(RoleResponse):
    permissions: List[PermissionResponse] = []
    parent_role: Optional['RoleResponse'] = None
    child_roles: List['RoleResponse'] = []


class RolePermissionBase(BaseModel):
    role_id: UUID
    permission_id: UUID


class RolePermissionCreate(BaseModel):
    permission_id: UUID


class RolePermissionResponse(BaseModel):
    role_id: UUID
    permission_id: UUID
    granted_by: Optional[UUID] = None
    granted_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserRoleBase(BaseModel):
    user_id: UUID
    role_id: UUID
    organization_id: Optional[UUID] = None
    expires_at: Optional[datetime] = None
    is_active: bool = True


class UserRoleCreate(BaseModel):
    role_id: UUID
    organization_id: Optional[UUID] = None
    expires_at: Optional[datetime] = None


class UserRoleResponse(BaseModel):
    user_id: UUID
    role_id: UUID
    organization_id: Optional[UUID] = None
    assigned_by: Optional[UUID] = None
    assigned_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserRoleDetailResponse(UserRoleResponse):
    role: RoleResponse


class RoleTemplateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    display_name: str = Field(..., min_length=1, max_length=255)
    role_id: Optional[UUID] = None
    is_system: bool = False
    is_active: bool = True


class RoleTemplateCreate(RoleTemplateBase):
    permission_ids: List[UUID] = []


class RoleTemplateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    display_name: Optional[str] = Field(None, min_length=1, max_length=255)
    is_active: Optional[bool] = None


class RoleTemplateResponse(RoleTemplateBase):
    id: UUID
    usage_count: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PermissionEvaluationRequest(BaseModel):
    resource: str
    action: str
    organization_id: Optional[UUID] = None


class PermissionEvaluationResponse(BaseModel):
    has_permission: bool
    permissions: List[str] = []
    roles: List[str] = []


class BulkRoleAssignment(BaseModel):
    user_ids: List[UUID]
    role_id: UUID
    organization_id: Optional[UUID] = None
    expires_at: Optional[datetime] = None


class BulkRoleAssignmentResponse(BaseModel):
    assigned: int
    failed: int
    errors: List[str] = []


class PermissionMatrixResponse(BaseModel):
    roles: List[RoleResponse]
    permissions: List[PermissionResponse]
    matrix: dict
