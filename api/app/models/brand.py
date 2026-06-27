#!/usr/bin/env python
"""
Brand Management Database Models

This module contains all database models for the Brand Management system.
Implements all required entities with UUIDs and audit fields.
"""

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, JSON

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class TimestampMixin:
    """Mixin class to add created_at and updated_at fields to all models."""
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                       onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class SoftDeleteMixin:
    """Mixin class to add soft delete functionality."""
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.deleted_at = None


class Brand(Base, TimestampMixin, SoftDeleteMixin):
    """Main Brand entity containing all brand information and metadata."""
    __tablename__ = 'brands'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    industry = Column(String(100))
    category_id = Column(UUID(as_uuid=True), ForeignKey('brand_categories.id'))
    logo = Column(String(500))
    cover_image = Column(String(500))
    mission = Column(Text)
    vision = Column(Text)
    core_values = Column(JSONType)
    brand_story = Column(Text)
    target_audience_id = Column(UUID(as_uuid=True), ForeignKey('brand_audiences.id'))
    primary_language = Column(String(10))
    timezone = Column(String(50))
    country = Column(String(100))
    region = Column(String(100))
    website = Column(String(500))
    status = Column(String(20), default='active')  # active, archived, draft
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'))
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'))

    # Relationships
    category = relationship("BrandCategory", back_populates="brands")
    audience = relationship("BrandAudience", back_populates="brands")
    owner = relationship("User", back_populates="owned_brands")
    workspace = relationship("Workspace", back_populates="brands")
    organization = relationship("Organization", back_populates="brands")
    identity = relationship("BrandIdentity", back_populates="brand", uselist=False)
    voice = relationship("BrandVoice", back_populates="brand", uselist=False)
    assets = relationship("BrandAsset", back_populates="brand")
    social_profiles = relationship("BrandSocialProfile", back_populates="brand")
    competitors = relationship("BrandCompetitor", back_populates="brand")
    goals = relationship("BrandGoal", back_populates="brand")
    guidelines = relationship("BrandGuideline", back_populates="brand")
    approval_settings = relationship("BrandApprovalSettings", back_populates="brand", uselist=False)
    personas = relationship("BrandPersona", back_populates="brand")

    @property
    def social_accounts(self):
        """Return social profiles as a structured format."""
        return {
            'tiktok': self.get_social_profile('TikTok'),
            'instagram': self.get_social_profile('Instagram'),
            'facebook': self.get_social_profile('Facebook'),
            'threads': self.get_social_profile('Threads'),
            'linkedin': self.get_social_profile('LinkedIn'),
            'pinterest': self.get_social_profile('Pinterest'),
            'youtube': self.get_social_profile('YouTube'),
            'x': self.get_social_profile('X')
        }

    def get_social_profile(self, platform: str) -> Optional[Dict]:
        """Get a specific social profile."""
        for profile in self.social_profiles:
            if profile.platform == platform:
                return profile.to_dict()
        return None


class BrandIdentity(Base, TimestampMixin):
    """Brand visual identity guidelines."""
    __tablename__ = 'brand_identities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    primary_colors = Column(JSONType)
    secondary_colors = Column(JSONType)
    accent_colors = Column(JSONType)
    typography = Column(JSONType)
    spacing_rules = Column(JSONType)
    logo_rules = Column(JSONType)
    photography_style = Column(String(500))
    video_style = Column(String(500))
    icon_style = Column(String(500))
    illustration_style = Column(String(500))
    accessibility_rules = Column(Text)

    brand = relationship("Brand", back_populates="identity")

    def to_dict(self):
        return {
            'id': self.id,
            'primary_colors': self.primary_colors,
            'secondary_colors': self.secondary_colors,
            'accent_colors': self.accent_colors,
            'typography': self.typography,
            'spacing_rules': self.spacing_rules,
            'logo_rules': self.logo_rules,
            'photography_style': self.photography_style,
            'video_style': self.video_style,
            'icon_style': self.icon_style,
            'illustration_style': self.illustration_style,
            'accessibility_rules': self.accessibility_rules,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandVoice(Base, TimestampMixin):
    """Brand voice and personality guidelines."""
    __tablename__ = 'brand_voices'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    tone = Column(String(100))
    writing_style = Column(String(500))
    vocabulary = Column(JSONType)
    reading_level = Column(String(50))
    emoji_policy = Column(String(100))
    cta_style = Column(String(500))
    forbidden_words = Column(JSONType)
    preferred_words = Column(JSONType)
    brand_personality = Column(String(500))
    ai_prompt_prefix = Column(Text)
    ai_prompt_suffix = Column(Text)
    content_constraints = Column(JSONType)

    brand = relationship("Brand", back_populates="voice")

    def to_dict(self):
        return {
            'id': self.id,
            'tone': self.tone,
            'writing_style': self.writing_style,
            'vocabulary': self.vocabulary,
            'reading_level': self.reading_level,
            'emoji_policy': self.emoji_policy,
            'cta_style': self.cta_style,
            'forbidden_words': self.forbidden_words,
            'preferred_words': self.preferred_words,
            'brand_personality': self.brand_personality,
            'ai_prompt_prefix': self.ai_prompt_prefix,
            'ai_prompt_suffix': self.ai_prompt_suffix,
            'content_constraints': self.content_constraints,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandGuideline(Base, TimestampMixin):
    """Brand guidelines and rules."""
    __tablename__ = 'brand_guidelines'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    rules = Column(JSONType)
    exceptions = Column(JSONType)

    brand = relationship("Brand", back_populates="guidelines")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rules': self.rules,
            'exceptions': self.exceptions,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandColorPalette(Base, TimestampMixin):
    """Brand color palette."""
    __tablename__ = 'brand_color_palettes'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    name = Column(String(255), nullable=False)
    primary = Column(JSONType)
    secondary = Column(JSONType)
    accent = Column(JSONType)
    neutral = Column(JSONType)

    brand = relationship("Brand")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'primary': self.primary,
            'secondary': self.secondary,
            'accent': self.accent,
            'neutral': self.neutral,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandTypography(Base, TimestampMixin):
    """Brand typography specifications."""
    __tablename__ = 'brand_typography'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    headings = Column(JSONType)
    body = Column(JSONType)
    monospace = Column(JSONType)
    font_imports = Column(Text)

    brand = relationship("Brand")

    def to_dict(self):
        return {
            'id': self.id,
            'headings': self.headings,
            'body': self.body,
            'monospace': self.monospace,
            'font_imports': self.font_imports,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandSocialProfile(Base, TimestampMixin):
    """Brand social media profiles."""
    __tablename__ = 'brand_social_profiles'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    platform = Column(String(50), nullable=False)  # TikTok, Instagram, Facebook, etc.
    username = Column(String(255), nullable=False)
    display_name = Column(String(255))
    url = Column(String(500))
    platform_id = Column(String(255))
    status = Column(String(50), default='active')  # active, paused, deprecated
    oauth_ready = Column(Boolean, default=False)
    publishing_permissions = Column(JSONType)

    brand = relationship("Brand", back_populates="social_profiles")

    def to_dict(self):
        return {
            'id': self.id,
            'platform': self.platform,
            'username': self.username,
            'display_name': self.display_name,
            'url': self.url,
            'platform_id': self.platform_id,
            'status': self.status,
            'oauth_ready': self.oauth_ready,
            'publishing_permissions': self.publishing_permissions,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandCompetitor(Base, TimestampMixin):
    """Brand competitors and market intelligence."""
    __tablename__ = 'brand_competitors'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    website = Column(String(500))
    market_share = Column(String(100))

    brand = relationship("Brand", back_populates="competitors")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'website': self.website,
            'market_share': self.market_share,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandAudience(Base, TimestampMixin):
    """Target audience profiles."""
    __tablename__ = 'brand_audiences'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    demographics = Column(JSONType)
    psychographics = Column(JSONType)
    pain_points = Column(JSONType)
    preferred_platforms = Column(JSONType)

    brands = relationship("Brand", back_populates="audience")
    personas = relationship("BrandPersona", back_populates="audience")

    def to_dict(self):
        return {
            'id': self.id,
            'demographics': self.demographics,
            'psychographics': self.psychographics,
            'pain_points': self.pain_points,
            'preferred_platforms': self.preferred_platforms,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandGoal(Base, TimestampMixin):
    """Brand goals and metrics."""
    __tablename__ = 'brand_goals'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    target_metric = Column(String(255))
    current_progress = Column(Integer, default=0)
    target_progress = Column(Integer, default=100)
    deadline = Column(DateTime)
    status = Column(String(50), default='active')  # active, completed, paused

    brand = relationship("Brand", back_populates="goals")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'target_metric': self.target_metric,
            'current_progress': self.current_progress,
            'target_progress': self.target_progress,
            'deadline': self.deadline,
            'status': self.status,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandPersona(Base, TimestampMixin):
    """Brand personas and user profiles."""
    __tablename__ = 'brand_personas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    characteristics = Column(JSONType)
    pain_points = Column(JSONType)
    motivations = Column(JSONType)
    preferred_channels = Column(JSONType)
    audience_id = Column(UUID(as_uuid=True), ForeignKey('brand_audiences.id'))

    brand = relationship("Brand", back_populates="personas")
    audience = relationship("BrandAudience", back_populates="personas")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'characteristics': self.characteristics,
            'pain_points': self.pain_points,
            'motivations': self.motivations,
            'preferred_channels': self.preferred_channels,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandTag(Base, TimestampMixin):
    """Brand tags for categorization."""
    __tablename__ = 'brand_tags'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    color = Column(String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'color': self.color,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandCategory(Base, TimestampMixin):
    """Brand categories."""
    __tablename__ = 'brand_categories'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)

    brands = relationship("Brand", back_populates="category")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandAsset(Base, TimestampMixin, SoftDeleteMixin):
    """Brand assets and digital resources."""
    __tablename__ = 'brand_assets'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)  # logo, icon, photo, video, etc.
    file_path = Column(String(500), nullable=False)
    mime_type = Column(String(100))
    size = Column(Integer)  # File size in bytes
    description = Column(Text)
    tags = Column(JSONType)
    collections = Column(JSONType)
    version = Column(Integer, default=1)
    previous_version_id = Column(UUID(as_uuid=True), ForeignKey('brand_assets.id'))
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    brand = relationship("Brand", back_populates="assets")
    previous_version = relationship("BrandAsset", remote_side=[id])
    uploader = relationship("User", back_populates="uploaded_assets")

    def to_dict(self):
        return {
            'id': self.id,
            'brand_id': self.brand_id,
            'name': self.name,
            'type': self.type,
            'file_path': self.file_path,
            'mime_type': self.mime_type,
            'size': self.size,
            'description': self.description,
            'tags': self.tags,
            'collections': self.collections,
            'version': self.version,
            'previous_version_id': self.previous_version_id,
            'uploaded_by': self.uploaded_by,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class BrandApprovalSettings(Base, TimestampMixin):
    """Brand approval workflow settings."""
    __tablename__ = 'brand_approval_settings'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    require_approval = Column(Boolean, default=True)
    approver_roles = Column(JSONType)
    auto_publish = Column(Boolean, default=False)

    brand = relationship("Brand", back_populates="approval_settings")

    def to_dict(self):
        return {
            'id': self.id,
            'brand_id': self.brand_id,
            'require_approval': self.require_approval,
            'approver_roles': self.approver_roles,
            'auto_publish': self.auto_publish,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class BrandGuideline(Base, TimestampMixin):
    """Brand guidelines and rules."""
    __tablename__ = 'brand_guidelines'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brand_id = Column(UUID(as_uuid=True), ForeignKey('brands.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    rules = Column(JSONType)
    exceptions = Column(JSONType)

    brand = relationship("Brand", back_populates="guidelines")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'rules': self.rules,
            'exceptions': self.exceptions,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class User(Base, TimestampMixin, SoftDeleteMixin):
    """User model for authentication and ownership."""
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(500), nullable=False)
    full_name = Column(String(500))
    avatar_url = Column(String(500))
    role = Column(String(50), default='user')  # user, admin, workspace_admin

    # Relationships
    owned_brands = relationship("Brand", back_populates="owner")
    uploaded_assets = relationship("BrandAsset", back_populates="uploader")

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'full_name': self.full_name,
            'avatar_url': self.avatar_url,
            'role': self.role,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class Workspace(Base, TimestampMixin):
    """Workspace for organizing brands."""
    __tablename__ = 'workspaces'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    brands = relationship("Brand", back_populates="workspace")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'owner_id': self.owner_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class Organization(Base, TimestampMixin):
    """Organization for enterprise-level brand management."""
    __tablename__ = 'organizations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    website = Column(String(500))

    brands = relationship("Brand", back_populates="organization")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'website': self.website,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
