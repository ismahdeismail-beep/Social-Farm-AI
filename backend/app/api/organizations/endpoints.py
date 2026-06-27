from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
import secrets
from datetime import datetime, timedelta, timezone

from app.core.security import verify_token
from app.models import get_db, Organization, Workspace, OrganizationMember, WorkspaceMember, Invitation, User
from app.schemas import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.schemas import WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse
from app.schemas import OrganizationMemberResponse, WorkspaceMemberResponse
from app.schemas import InvitationCreate, InvitationResponse, InvitationAccept

router = APIRouter(prefix="/organizations", tags=["Organizations"])

# Organization endpoints
@router.post("/", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization_in: OrganizationCreate,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    # Check if slug is unique
    db_organization = db.query(Organization).filter(Organization.slug == organization_in.slug).first()
    if db_organization:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with this slug already exists"
        )
    
    # Create new organization
    db_organization = Organization(
        id=uuid.uuid4(),
        name=organization_in.name,
        slug=organization_in.slug,
        description=organization_in.description,
        logo_url=organization_in.logo_url,
        website=organization_in.website,
        industry=organization_in.industry,
        owner_id=current_user_id,
        status="active"
    )
    
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    
    # Add owner as organization member
    organization_member = OrganizationMember(
        organization_id=db_organization.id,
        user_id=current_user_id,
        role="owner",
        invited_by=None,
        status="active"
    )
    db.add(organization_member)
    db.commit()
    db.refresh(organization_member)
    
    return db_organization

@router.get("/", response_model=List[OrganizationResponse])
async def list_organizations(
    skip: int = 0,
    limit: int = 100,
    status: str = "active",
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    organizations_query = db.query(Organization).filter(Organization.status == status, Organization.deleted_at.is_(None))
    organizations = organizations_query.offset(skip).limit(limit).all()
    return organizations

@router.get("/{organization_id}", response_model=OrganizationResponse)
async def get_organization(
    organization_id: uuid.UUID,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.deleted_at.is_(None)
    ).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check if user is a member of the organization
    organization_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id,
        OrganizationMember.user_id == current_user_id,
        OrganizationMember.status == "active"
    ).first()
    
    if not organization_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this organization"
        )
    
    return organization

@router.patch("/{organization_id}", response_model=OrganizationResponse)
async def update_organization(
    organization_id: uuid.UUID,
    organization_in: OrganizationUpdate,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.deleted_at.is_(None)
    ).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check if user has permission to update organization
    organization_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id,
        OrganizationMember.user_id == current_user_id,
        OrganizationMember.status == "active"
    ).first()
    
    if not organization_member or organization_member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this organization"
        )
    
    # Update organization fields
    if organization_in.name is not None:
        organization.name = organization_in.name
    if organization_in.slug is not None:
        # Check if slug is unique
        existing_organization = db.query(Organization).filter(
            Organization.slug == organization_in.slug,
            Organization.id != organization_id,
            Organization.deleted_at.is_(None)
        ).first()
        if existing_organization:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization with this slug already exists"
            )
        organization.slug = organization_in.slug
    
    if organization_in.description is not None:
        organization.description = organization_in.description
    if organization_in.logo_url is not None:
        organization.logo_url = organization_in.logo_url
    if organization_in.website is not None:
        organization.website = organization_in.website
    if organization_in.industry is not None:
        organization.industry = organization_in.industry
    
    db.commit()
    db.refresh(organization)
    
    return organization

@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: uuid.UUID,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.deleted_at.is_(None)
    ).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check if user has permission to delete organization
    if organization.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization owner can delete the organization"
        )
    
    # Soft delete organization
    organization.soft_delete()
    db.commit()
    
    return

@router.get("/{organization_id}/members", response_model=List[OrganizationMemberResponse])
async def list_organization_members(
    organization_id: uuid.UUID,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.deleted_at.is_(None)
    ).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check if user is a member of the organization
    organization_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id,
        OrganizationMember.user_id == current_user_id,
        OrganizationMember.status == "active"
    ).first()
    
    if not organization_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to access this organization"
        )
    
    members = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id,
        OrganizationMember.status == "active"
    ).all()
    
    return members

@router.post("/{organization_id}/invite", response_model=InvitationResponse)
async def invite_member(
    organization_id: uuid.UUID,
    invitation_in: InvitationCreate,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.deleted_at.is_(None)
    ).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check if user has permission to invite members
    organization_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id,
        OrganizationMember.user_id == current_user_id,
        OrganizationMember.status == "active"
    ).first()
    
    if not organization_member or organization_member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to invite members to this organization"
        )
    
    # Check if user is already a member
    existing_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id,
        OrganizationMember.user_id == invitation_in.email,
        OrganizationMember.status == "active"
    ).first()
    
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a member of this organization"
        )
    
    # Create invitation
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    
    invitation = Invitation(
        id=uuid.uuid4(),
        email=invitation_in.email,
        organization_id=organization_id,
        workspace_id=invitation_in.workspace_id,
        token=token,
        expires_at=expires_at,
        invited_by=current_user_id,
        status="pending"
    )
    
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    
    return invitation

@router.delete("/{organization_id}/members/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_member(
    organization_id: uuid.UUID,
    user_id: uuid.UUID,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    organization = db.query(Organization).filter(
        Organization.id == organization_id,
        Organization.deleted_at.is_(None)
    ).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    # Check if current user has permission to remove members
    organization_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id,
        OrganizationMember.user_id == current_user_id,
        OrganizationMember.status == "active"
    ).first()
    
    if not organization_member or organization_member.role not in ["owner", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to remove members from this organization"
        )
    
    # Cannot remove yourself
    if user_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot remove yourself from the organization"
        )
    
    # Cannot remove organization owner
    if user_id == organization.owner_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot remove organization owner"
        )
    
    # Remove member from organization
    organization_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == organization_id,
        OrganizationMember.user_id == user_id,
        OrganizationMember.status == "active"
    ).first()
    
    if not organization_member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    organization_member.status = "inactive"
    db.commit()
    
    # Remove workspace memberships
    db.query(WorkspaceMember).filter(
        WorkspaceMember.user_id == user_id
    ).delete()
    
    db.commit()
    
    return

@router.post("/invitations/accept", response_model=OrganizationResponse)
async def accept_invitation(
    invitation_in: InvitationAccept,
    current_user_id: str = Depends(verify_token),
    db: Session = Depends(get_db)
):
    invitation = db.query(Invitation).filter(
        Invitation.token == invitation_in.token,
        Invitation.status == "pending"
    ).first()
    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found or already used"
        )
    
    # Check if invitation expired
    if datetime.now(timezone.utc) > invitation.expires_at:
        invitation.status = "expired"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invitation has expired"
        )
    
    # Accept invitation
    invitation.status = "accepted"
    invitation.accepted_at = datetime.now(timezone.utc)
    db.commit()
    
    # Check if user is already a member
    existing_member = db.query(OrganizationMember).filter(
        OrganizationMember.organization_id == invitation.organization_id,
        OrganizationMember.user_id == current_user_id,
        OrganizationMember.status == "active"
    ).first()
    
    if existing_member:
        return existing_member.organization
    
    # Add user to organization
    organization_member = OrganizationMember(
        organization_id=invitation.organization_id,
        user_id=current_user_id,
        role="member",
        invited_by=invitation.invited_by,
        status="active"
    )
    
    db.add(organization_member)
    db.commit()
    db.refresh(organization_member)
    
    # Add user to workspace if provided
    if invitation.workspace_id:
        workspace_member = WorkspaceMember(
            workspace_id=invitation.workspace_id,
            user_id=current_user_id,
            role="member"
        )
        db.add(workspace_member)
        db.commit()
    
    return organization_member.organization
