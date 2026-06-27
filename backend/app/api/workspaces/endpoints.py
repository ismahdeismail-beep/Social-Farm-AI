from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime, timezone
import secrets

from app.core.security import verify_token
from app.models import get_db, Organization, Workspace, OrganizationMember, WorkspaceMember, Invitation, User
from app.schemas import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.schemas import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse
from app.schemas import OrganizationMemberResponse, WorkspaceMemberResponse
from app.schemas import InvitationCreate, InvitationResponse, InvitationAccept

router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

@router.post("/", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    workspace_in: WorkspaceCreate,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Get organization_id from request body
    organization_id = workspace_in.organization_id
    
    # Check if workspace slug is unique
    existing_workspace = db.query(Workspace).filter(
        Workspace.slug == workspace_in.slug
    ).first()
    if existing_workspace:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Workspace with this slug already exists"
        )
    
    # Check if organization exists
    organization = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.deleted_at.is_(None)
    ).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check if user has permission to create workspace
    organization_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id,
        OrganizationMember.user_id == current_user_id,
        OrganizationMember.status == "active"
    ).first()
    
    if not organization_member or organization_member.role not in ["owner", "admin", "manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to create workspaces in this organization"
        )
    
    # Create new workspace
    db_workspace = Workspace(
        id=uuid.uuid4(),
        organization_id=organization_id,
        name=workspace_in.name,
        slug=workspace_in.slug,
        description=workspace_in.description,
        timezone=workspace_in.timezone,
        locale=workspace_in.locale,
        default_language=workspace_in.default_language,
        status="active"
    )
    
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    
    return db_workspace

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: uuid.UUID,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Find workspace by ID
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()
    
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )
    
    # Check if user has access to this workspace
    workspace_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user_id,
        WorkspaceMember.status == "active"
    ).first()
    
    if not workspace_member:
        # Also check organization membership
        org_member = db.query(OrganizationMember).filter(
            OrganizationMember.organization_id == workspace.organization_id,
            OrganizationMember.user_id == current_user_id,
            OrganizationMember.status == "active"
        ).first()
        
        if not org_member:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to access this workspace"
            )
    
    return workspace

@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: uuid.UUID,
    workspace_in: WorkspaceUpdate,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Find workspace by ID
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()
    
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )
    
    # Check if user has permission to update workspace
    workspace_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user_id,
        WorkspaceMember.status == "active"
    ).first()
    
    if not workspace_member or workspace_member.role not in ["member", "admin"]:
        # Check organization membership
        org_member = db.query(OrganizationMember).filter(
            OrganizationMember.organization_id == workspace.organization_id,
            OrganizationMember.user_id == current_user_id,
            OrganizationMember.status == "active"
        ).first()
        
        if not org_member or org_member.role not in ["owner", "admin", "manager"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to update this workspace"
            )
    
    # Update workspace fields
    if workspace_in.name is not None:
        workspace.name = workspace_in.name
    if workspace_in.slug is not None:
        # Check if slug is unique
        existing_workspace = db.query(Workspace).filter(
            Workspace.slug == workspace_in.slug,
            Workspace.id != workspace_id
        ).first()
        if existing_workspace:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Workspace with this slug already exists"
            )
        workspace.slug = workspace_in.slug
    
    if workspace_in.description is not None:
        workspace.description = workspace_in.description
    if workspace_in.timezone is not None:
        workspace.timezone = workspace_in.timezone
    if workspace_in.locale is not None:
        workspace.locale = workspace_in.locale
    if workspace_in.default_language is not None:
        workspace.default_language = workspace_in.default_language
    
    db.commit()
    db.refresh(workspace)
    
    return workspace

@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
    workspace_id: uuid.UUID,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Find workspace by ID
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()
    
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )
    
    # Check if user has permission to delete workspace
    workspace_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user_id,
        WorkspaceMember.status == "active"
    ).first()
    
    if not workspace_member or workspace_member.role not in ["admin", "owner"]:
        # Check organization membership
        org_member = db.query(OrganizationMember).filter(
            OrganizationMember.organization_id == workspace.organization_id,
            OrganizationMember.user_id == current_user_id,
            OrganizationMember.status == "active"
        ).first()
        
        if not org_member or org_member.role not in ["owner", "admin"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to delete this workspace"
            )
    
    # Soft delete workspace
    workspace.deleted_at = datetime.now(timezone.utc)
    db.commit()
    
    return

@router.post("/{workspace_id}/switch", status_code=status.HTTP_204_NO_CONTENT)
async def switch_active_workspace(
    workspace_id: uuid.UUID,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Find workspace by ID
    workspace = db.query(Workspace).filter(
        Workspace.id == workspace_id
    ).first()
    
    if not workspace:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )
    
    # Check if user is a member of the workspace
    workspace_member = db.query(WorkspaceMember).filter(
        WorkspaceMember.workspace_id == workspace_id,
        WorkspaceMember.user_id == current_user_id,
        WorkspaceMember.status == "active"
    ).first()
    
    if not workspace_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this workspace"
        )
    
    # In a real implementation, this would update the user's active workspace
    # For now, we just return success
    
    return
