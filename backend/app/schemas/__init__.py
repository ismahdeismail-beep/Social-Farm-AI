"""
Schema models for Social Farm AI.

Re-exports all Pydantic schemas for convenient importing.
"""

from app.schemas.user import UserBase, UserCreate, User as UserSchema
from app.schemas.rbac import (
    PermissionCreate, PermissionUpdate, PermissionResponse,
    PermissionGroupCreate, PermissionGroupUpdate, PermissionGroupResponse,
    RoleCreate, RoleUpdate, RoleResponse,
    RoleTemplateCreate, RoleTemplateUpdate, RoleTemplateResponse,
    UserRoleCreate, UserRoleResponse,
)
from app.schemas.brand import (
    BrandCreate, BrandUpdate, BrandResponse,
    BrandVoiceCreate, BrandVoiceUpdate, BrandVoiceResponse,
    BrandIdentityCreate, BrandIdentityUpdate, BrandIdentityResponse,
)
from app.schemas.research import (
    ResearchSourceCreate, ResearchSourceUpdate, ResearchSourceResponse,
    ResearchQueryCreate, ResearchQueryUpdate, ResearchQueryResponse,
    ResearchDocumentCreate, ResearchDocumentUpdate, ResearchDocumentResponse,
    ResearchCollectionCreate, ResearchCollectionUpdate, ResearchCollectionResponse,
    ResearchTopicCreate, ResearchTopicUpdate, ResearchTopicResponse,
    ResearchSummaryCreate, ResearchSummaryUpdate, ResearchSummaryResponse,
    ResearchCitationCreate, ResearchCitationUpdate, ResearchCitationResponse,
    ResearchInsightCreate, ResearchInsightUpdate, ResearchInsightResponse,
    ResearchFactCreate, ResearchFactUpdate, ResearchFactResponse,
    ResearchKeywordCreate, ResearchKeywordUpdate, ResearchKeywordResponse,
    ResearchEntityCreate, ResearchEntityUpdate, ResearchEntityResponse,
    ResearchScoreCreate, ResearchScoreUpdate, ResearchScoreResponse,
    ResearchJobCreate, ResearchJobUpdate, ResearchJobResponse,
    ResearchReportCreate, ResearchReportUpdate, ResearchReportResponse,
    ResearchAlertCreate, ResearchAlertUpdate, ResearchAlertResponse,
)

# Organization / Workspace / Invitation minimal schemas
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid


class OrganizationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None


class OrganizationResponse(BaseModel):
    id: str
    name: str
    slug: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    owner_id: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WorkspaceCreate(BaseModel):
    organization_id: str
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    timezone: str = "UTC"
    locale: str = "en"
    default_language: str = "en"


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    timezone: Optional[str] = None
    locale: Optional[str] = None
    default_language: Optional[str] = None


class WorkspaceResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    slug: str
    description: Optional[str] = None
    timezone: str
    locale: str
    default_language: str
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class OrganizationMemberResponse(BaseModel):
    organization_id: str
    user_id: str
    role: str
    status: str
    joined_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class WorkspaceMemberResponse(BaseModel):
    workspace_id: str
    user_id: str
    role: str
    joined_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class InvitationCreate(BaseModel):
    email: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None


class InvitationUpdate(BaseModel):
    status: Optional[str] = None


class InvitationResponse(BaseModel):
    id: str
    email: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    token: str
    status: str
    expires_at: Optional[datetime] = None
    accepted_at: Optional[datetime] = None
    invited_by: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class InvitationAccept(BaseModel):
    token: str
