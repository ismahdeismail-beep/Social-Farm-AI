from pydantic import BaseModel
from typing import Optional, Dict, List, Any
from datetime import datetime, date
from uuid import UUID
from enum import Enum


class BrandStatus(str, Enum):
    ACTIVE = "active"
    ARCHIVED = "archived"
    DRAFT = "draft"


class Platform(str, Enum):
    TIKTOK = "TikTok"
    INSTAGRAM = "Instagram"
    FACEBOOK = "Facebook"
    THREADS = "Threads"
    LINKEDIN = "LinkedIn"
    PINTEREST = "Pinterest"
    YOUTUBE = "YouTube"
    X = "X"


class BrandAssetType(str, Enum):
    LOGO = "logo"
    ICON = "icon"
    PHOTO = "photo"
    VIDEO = "video"
    TEMPLATE = "template"
    BRAND_KIT = "brand_kit"
    FONT = "font"
    AUDIO = "audio"
    LEGAL_DOCUMENT = "legal_document"
    LICENSE = "license"


class SocialProfileStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    DEPRECATED = "deprecated"


class BrandGoalStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"


class BrandCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    industry: Optional[str] = None
    category_id: Optional[UUID] = None
    logo: Optional[str] = None
    cover_image: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    core_values: Optional[List[str]] = None
    brand_story: Optional[str] = None
    target_audience_id: Optional[UUID] = None
    primary_language: Optional[str] = None
    timezone: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    website: Optional[str] = None
    status: BrandStatus = BrandStatus.DRAFT
    workspace_id: UUID
    organization_id: Optional[UUID] = None


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    category_id: Optional[UUID] = None
    logo: Optional[str] = None
    cover_image: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    core_values: Optional[List[str]] = None
    brand_story: Optional[str] = None
    target_audience_id: Optional[UUID] = None
    primary_language: Optional[str] = None
    timezone: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    website: Optional[str] = None
    status: Optional[BrandStatus] = None
    workspace_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None


class BrandResponse(BaseModel):
    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    industry: Optional[str] = None
    logo: Optional[str] = None
    cover_image: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    core_values: Optional[List[str]] = None
    brand_story: Optional[str] = None
    primary_language: Optional[str] = None
    timezone: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    website: Optional[str] = None
    status: str
    owner_id: Optional[UUID] = None
    workspace_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            slug=obj.slug,
            description=obj.description,
            industry=obj.industry,
            logo=obj.logo,
            cover_image=obj.cover_image,
            mission=obj.mission,
            vision=obj.vision,
            core_values=obj.core_values,
            brand_story=obj.brand_story,
            primary_language=obj.primary_language,
            timezone=obj.timezone,
            country=obj.country,
            region=obj.region,
            website=obj.website,
            status=obj.status,
            owner_id=obj.owner_id,
            workspace_id=obj.workspace_id,
            organization_id=obj.organization_id,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            deleted_at=obj.deleted_at
        )


class BrandVoiceCreate(BaseModel):
    tone: Optional[str] = None
    writing_style: Optional[str] = None
    vocabulary: Optional[List[str]] = None
    reading_level: Optional[str] = None
    emoji_policy: Optional[str] = None
    cta_style: Optional[str] = None
    forbidden_words: Optional[List[str]] = None
    preferred_words: Optional[List[str]] = None
    brand_personality: Optional[str] = None
    ai_prompt_prefix: Optional[str] = None
    ai_prompt_suffix: Optional[str] = None
    content_constraints: Optional[Dict[str, Any]] = None


class BrandVoiceUpdate(BaseModel):
    tone: Optional[str] = None
    writing_style: Optional[str] = None
    vocabulary: Optional[List[str]] = None
    reading_level: Optional[str] = None
    emoji_policy: Optional[str] = None
    cta_style: Optional[str] = None
    forbidden_words: Optional[List[str]] = None
    preferred_words: Optional[List[str]] = None
    brand_personality: Optional[str] = None
    ai_prompt_prefix: Optional[str] = None
    ai_prompt_suffix: Optional[str] = None
    content_constraints: Optional[Dict[str, Any]] = None


class BrandVoiceResponse(BaseModel):
    id: UUID
    tone: Optional[str] = None
    writing_style: Optional[str] = None
    vocabulary: Optional[List[str]] = None
    reading_level: Optional[str] = None
    emoji_policy: Optional[str] = None
    cta_style: Optional[str] = None
    forbidden_words: Optional[List[str]] = None
    preferred_words: Optional[List[str]] = None
    brand_personality: Optional[str] = None
    ai_prompt_prefix: Optional[str] = None
    ai_prompt_suffix: Optional[str] = None
    content_constraints: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            tone=obj.tone,
            writing_style=obj.writing_style,
            vocabulary=obj.vocabulary,
            reading_level=obj.reading_level,
            emoji_policy=obj.emoji_policy,
            cta_style=obj.cta_style,
            forbidden_words=obj.forbidden_words,
            preferred_words=obj.preferred_words,
            brand_personality=obj.brand_personality,
            ai_prompt_prefix=obj.ai_prompt_prefix,
            ai_prompt_suffix=obj.ai_prompt_suffix,
            content_constraints=obj.content_constraints,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class BrandIdentityCreate(BaseModel):
    primary_colors: Optional[Dict[str, str]] = None
    secondary_colors: Optional[Dict[str, str]] = None
    accent_colors: Optional[Dict[str, str]] = None
    typography: Optional[Dict[str, Any]] = None
    spacing_rules: Optional[Dict[str, Any]] = None
    logo_rules: Optional[Dict[str, Any]] = None
    photography_style: Optional[str] = None
    video_style: Optional[str] = None
    icon_style: Optional[str] = None
    illustration_style: Optional[str] = None
    accessibility_rules: Optional[str] = None


class BrandIdentityUpdate(BaseModel):
    primary_colors: Optional[Dict[str, str]] = None
    secondary_colors: Optional[Dict[str, str]] = None
    accent_colors: Optional[Dict[str, str]] = None
    typography: Optional[Dict[str, Any]] = None
    spacing_rules: Optional[Dict[str, Any]] = None
    logo_rules: Optional[Dict[str, Any]] = None
    photography_style: Optional[str] = None
    video_style: Optional[str] = None
    icon_style: Optional[str] = None
    illustration_style: Optional[str] = None
    accessibility_rules: Optional[str] = None


class BrandIdentityResponse(BaseModel):
    id: UUID
    primary_colors: Optional[Dict[str, str]] = None
    secondary_colors: Optional[Dict[str, str]] = None
    accent_colors: Optional[Dict[str, str]] = None
    typography: Optional[Dict[str, Any]] = None
    spacing_rules: Optional[Dict[str, Any]] = None
    logo_rules: Optional[Dict[str, Any]] = None
    photography_style: Optional[str] = None
    video_style: Optional[str] = None
    icon_style: Optional[str] = None
    illustration_style: Optional[str] = None
    accessibility_rules: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            primary_colors=obj.primary_colors,
            secondary_colors=obj.secondary_colors,
            accent_colors=obj.accent_colors,
            typography=obj.typography,
            spacing_rules=obj.spacing_rules,
            logo_rules=obj.logo_rules,
            photography_style=obj.photography_style,
            video_style=obj.video_style,
            icon_style=obj.icon_style,
            illustration_style=obj.illustration_style,
            accessibility_rules=obj.accessibility_rules,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class BrandSocialProfileCreate(BaseModel):
    platform: Platform
    username: str
    display_name: Optional[str] = None
    url: Optional[str] = None
    platform_id: Optional[str] = None
    status: SocialProfileStatus = SocialProfileStatus.ACTIVE
    oauth_ready: bool = False
    publishing_permissions: Optional[Dict[str, Any]] = None


class BrandSocialProfileUpdate(BaseModel):
    platform: Optional[Platform] = None
    username: Optional[str] = None
    display_name: Optional[str] = None
    url: Optional[str] = None
    platform_id: Optional[str] = None
    status: Optional[SocialProfileStatus] = None
    oauth_ready: Optional[bool] = None
    publishing_permissions: Optional[Dict[str, Any]] = None


class BrandSocialProfileResponse(BaseModel):
    id: UUID
    platform: str
    username: str
    display_name: Optional[str] = None
    url: Optional[str] = None
    platform_id: Optional[str] = None
    status: str
    oauth_ready: bool
    publishing_permissions: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            platform=obj.platform,
            username=obj.username,
            display_name=obj.display_name,
            url=obj.url,
            platform_id=obj.platform_id,
            status=obj.status,
            oauth_ready=obj.oauth_ready,
            publishing_permissions=obj.publishing_permissions,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class BrandGoalCreate(BaseModel):
    title: str
    description: Optional[str] = None
    target_metric: Optional[str] = None
    current_progress: int = 0
    target_progress: int = 100
    deadline: Optional[date] = None
    status: BrandGoalStatus = BrandGoalStatus.ACTIVE


class BrandGoalUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    target_metric: Optional[str] = None
    current_progress: Optional[int] = None
    target_progress: Optional[int] = None
    deadline: Optional[date] = None
    status: Optional[BrandGoalStatus] = None


class BrandGoalResponse(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    target_metric: Optional[str] = None
    current_progress: int
    target_progress: int
    deadline: Optional[date] = None
    status: str
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            title=obj.title,
            description=obj.description,
            target_metric=obj.target_metric,
            current_progress=obj.current_progress,
            target_progress=obj.target_progress,
            deadline=obj.deadline,
            status=obj.status,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class BrandCompetitorCreate(BaseModel):
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    market_share: Optional[str] = None


class BrandCompetitorUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None
    market_share: Optional[str] = None


class BrandCompetitorResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    market_share: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            website=obj.website,
            market_share=obj.market_share,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class BrandAudienceCreate(BaseModel):
    demographics: Optional[Dict[str, Any]] = None
    psychographics: Optional[Dict[str, Any]] = None
    pain_points: Optional[List[str]] = None
    preferred_platforms: Optional[List[str]] = None


class BrandAudienceUpdate(BaseModel):
    demographics: Optional[Dict[str, Any]] = None
    psychographics: Optional[Dict[str, Any]] = None
    pain_points: Optional[List[str]] = None
    preferred_platforms: Optional[List[str]] = None


class BrandAudienceResponse(BaseModel):
    id: UUID
    demographics: Optional[Dict[str, Any]] = None
    psychographics: Optional[Dict[str, Any]] = None
    pain_points: Optional[List[str]] = None
    preferred_platforms: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            demographics=obj.demographics,
            psychographics=obj.psychographics,
            pain_points=obj.pain_points,
            preferred_platforms=obj.preferred_platforms,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class BrandAssetCreate(BaseModel):
    brand_id: Optional[UUID] = None
    name: str
    type: BrandAssetType
    file_path: str
    mime_type: Optional[str] = None
    size: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    collections: Optional[List[str]] = None
    version: int = 1
    previous_version_id: Optional[UUID] = None
    uploaded_by: Optional[UUID] = None


class BrandAssetUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[BrandAssetType] = None
    file_path: Optional[str] = None
    mime_type: Optional[str] = None
    size: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    collections: Optional[List[str]] = None
    version: Optional[int] = None
    previous_version_id: Optional[UUID] = None
    uploaded_by: Optional[UUID] = None


class BrandAssetResponse(BaseModel):
    id: UUID
    brand_id: Optional[UUID] = None
    name: str
    type: str
    file_path: str
    mime_type: Optional[str] = None
    size: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    collections: Optional[List[str]] = None
    version: int
    previous_version_id: Optional[UUID] = None
    uploaded_by: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            brand_id=obj.brand_id,
            name=obj.name,
            type=obj.type,
            file_path=obj.file_path,
            mime_type=obj.mime_type,
            size=obj.size,
            description=obj.description,
            tags=obj.tags,
            collections=obj.collections,
            version=obj.version,
            previous_version_id=obj.previous_version_id,
            uploaded_by=obj.uploaded_by,
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            deleted_at=obj.deleted_at
        )


class BrandApprovalSettingsCreate(BaseModel):
    brand_id: Optional[UUID] = None
    require_approval: bool = True
    approver_roles: Optional[List[str]] = None
    auto_publish: bool = False


class BrandApprovalSettingsUpdate(BaseModel):
    require_approval: Optional[bool] = None
    approver_roles: Optional[List[str]] = None
    auto_publish: Optional[bool] = None


class BrandApprovalSettingsResponse(BaseModel):
    id: UUID
    brand_id: Optional[UUID] = None
    require_approval: bool
    approver_roles: Optional[List[str]] = None
    auto_publish: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            brand_id=obj.brand_id,
            require_approval=obj.require_approval,
            approver_roles=obj.approver_roles,
            auto_publish=obj.auto_publish,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class BrandGuidelineCreate(BaseModel):
    name: str
    description: Optional[str] = None
    rules: Optional[Dict[str, Any]] = None
    exceptions: Optional[Dict[str, Any]] = None


class BrandGuidelineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    rules: Optional[Dict[str, Any]] = None
    exceptions: Optional[Dict[str, Any]] = None


class BrandGuidelineResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    rules: Optional[Dict[str, Any]] = None
    exceptions: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            rules=obj.rules,
            exceptions=obj.exceptions,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class BrandColorPaletteCreate(BaseModel):
    name: str
    primary: Optional[Dict[str, str]] = None
    secondary: Optional[Dict[str, str]] = None
    accent: Optional[Dict[str, str]] = None
    neutral: Optional[Dict[str, str]] = None


class BrandColorPaletteUpdate(BaseModel):
    name: Optional[str] = None
    primary: Optional[Dict[str, str]] = None
    secondary: Optional[Dict[str, str]] = None
    accent: Optional[Dict[str, str]] = None
    neutral: Optional[Dict[str, str]] = None


class BrandColorPaletteResponse(BaseModel):
    id: UUID
    name: str
    primary: Optional[Dict[str, str]] = None
    secondary: Optional[Dict[str, str]] = None
    accent: Optional[Dict[str, str]] = None
    neutral: Optional[Dict[str, str]] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            primary=obj.primary,
            secondary=obj.secondary,
            accent=obj.accent,
            neutral=obj.neutral,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class BrandTypographyCreate(BaseModel):
    headings: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    monospace: Optional[Dict[str, Any]] = None
    font_imports: Optional[str] = None


class BrandTypographyUpdate(BaseModel):
    headings: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    monospace: Optional[Dict[str, Any]] = None
    font_imports: Optional[str] = None


class BrandTypographyResponse(BaseModel):
    id: UUID
    headings: Optional[Dict[str, Any]] = None
    body: Optional[Dict[str, Any]] = None
    monospace: Optional[Dict[str, Any]] = None
    font_imports: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            headings=obj.headings,
            body=obj.body,
            monospace=obj.monospace,
            font_imports=obj.font_imports,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )


class BrandPersonaCreate(BaseModel):
    name: str
    description: Optional[str] = None
    characteristics: Optional[Dict[str, Any]] = None
    pain_points: Optional[List[str]] = None
    motivations: Optional[List[str]] = None
    preferred_channels: Optional[List[str]] = None
    audience_id: Optional[UUID] = None


class BrandPersonaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    characteristics: Optional[Dict[str, Any]] = None
    pain_points: Optional[List[str]] = None
    motivations: Optional[List[str]] = None
    preferred_channels: Optional[List[str]] = None
    audience_id: Optional[UUID] = None


class BrandPersonaResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str] = None
    characteristics: Optional[Dict[str, Any]] = None
    pain_points: Optional[List[str]] = None
    motivations: Optional[List[str]] = None
    preferred_channels: Optional[List[str]] = None
    audience_id: Optional[UUID] = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            name=obj.name,
            description=obj.description,
            characteristics=obj.characteristics,
            pain_points=obj.pain_points,
            motivations=obj.motivations,
            preferred_channels=obj.preferred_channels,
            audience_id=obj.audience_id,
            created_at=obj.created_at,
            updated_at=obj.updated_at
        )
