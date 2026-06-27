#!/usr/bin/env python
"""
Research Engine Database Models

This module contains all database models for the Research Engine system.
Implements 23 entities with UUIDs, audit fields, indexes, and foreign keys.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import (
    Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float,
    JSON as JSONType, Index, Enum as SAEnum, UniqueConstraint, Table
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


# ---------------------------------------------------------------------------
# Mixins
# ---------------------------------------------------------------------------

class TimestampMixin:
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                       onupdate=lambda: datetime.now(timezone.utc), nullable=False)


class SoftDeleteMixin:
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def soft_delete(self):
        self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.deleted_at = None


class AuditMixin:
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SourceType(str, enum.Enum):
    GOOGLE_SEARCH = 'google_search'
    GOOGLE_NEWS = 'google_news'
    RSS_FEED = 'rss_feed'
    WIKIPEDIA = 'wikipedia'
    YOUTUBE = 'youtube'
    REDDIT = 'reddit'
    GOVERNMENT = 'government'
    ACADEMIC = 'academic'
    COMPANY = 'company'
    BLOG = 'blog'
    INDUSTRY_REPORT = 'industry_report'
    USER_UPLOAD = 'user_upload'
    KNOWLEDGE_BASE = 'knowledge_base'
    CUSTOM = 'custom'


class QueryStatus(str, enum.Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'


class DocumentType(str, enum.Enum):
    ARTICLE = 'article'
    NEWS = 'news'
    VIDEO = 'video'
    PDF = 'pdf'
    DOCUMENT = 'document'
    REPORT = 'report'
    SOCIAL = 'social'
    ACADEMIC = 'academic'
    WEBPAGE = 'webpage'
    OTHER = 'other'


class EntityType(str, enum.Enum):
    PERSON = 'person'
    BRAND = 'brand'
    COMPANY = 'company'
    PRODUCT = 'product'
    EVENT = 'event'
    LOCATION = 'location'
    TOPIC = 'topic'
    KEYWORD = 'keyword'
    INDUSTRY = 'industry'
    COMPETITOR = 'competitor'
    ORGANIZATION = 'organization'
    CONCEPT = 'concept'
    TECHNOLOGY = 'technology'


class RelationshipType(str, enum.Enum):
    RELATED_TO = 'related_to'
    MENTIONS = 'mentions'
    COMPETES_WITH = 'competes_with'
    PARTNER_OF = 'partner_of'
    SUBSIDIARY_OF = 'subsidiary_of'
    PARENT_OF = 'parent_of'
    ACQUIRED_BY = 'acquired_by'
    ACQUIRED = 'acquired'
    LOCATED_IN = 'located_in'
    EMPLOYS = 'employs'
    PRODUCES = 'produces'
    USES = 'uses'
    INFLUENCES = 'influences'
    PRECEDES = 'precedes'
    FOLLOWS = 'follows'
    SIMILAR_TO = 'similar_to'
    CONTRADICTS = 'contradicts'
    SUPPORTS = 'supports'


class JobStatus(str, enum.Enum):
    PENDING = 'pending'
    QUEUED = 'queued'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    CANCELLED = 'cancelled'
    RETRYING = 'retrying'


class ConfidenceLevel(str, enum.Enum):
    VERY_HIGH = 'very_high'
    HIGH = 'high'
    MEDIUM = 'medium'
    LOW = 'low'
    VERY_LOW = 'very_low'
    UNVERIFIED = 'unverified'


# ===========================================================================
# 1. ResearchSource — Configurable data source connectors
# ===========================================================================

class ResearchSource(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Configurable data source connector metadata."""
    __tablename__ = 'research_sources'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False)
    source_type = Column(String(50), nullable=False)  # SourceType enum value
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    config = Column(JSONType, default=dict)  # Connector-specific configuration (API keys, URLs, etc.)
    rate_limit = Column(Integer, default=60)  # Requests per minute
    priority = Column(Integer, default=50)  # Lower = higher priority
    health_status = Column(String(50), default='unknown')  # healthy, degraded, down, unknown
    last_checked_at = Column(DateTime(timezone=True))
    last_success_at = Column(DateTime(timezone=True))
    error_count = Column(Integer, default=0)
    total_queries = Column(Integer, default=0)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=True)

    # Relationships
    queries = relationship("ResearchQuery", back_populates="source")
    documents = relationship("ResearchDocument", back_populates="source")

    __table_args__ = (
        Index('idx_research_source_type', 'source_type'),
        Index('idx_research_source_org', 'organization_id'),
        Index('idx_research_source_active', 'is_active'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'source_type': self.source_type,
            'description': self.description,
            'is_active': self.is_active,
            'config': self.config,
            'rate_limit': self.rate_limit,
            'priority': self.priority,
            'health_status': self.health_status,
            'last_checked_at': self.last_checked_at,
            'last_success_at': self.last_success_at,
            'error_count': self.error_count,
            'total_queries': self.total_queries,
            'organization_id': self.organization_id,
            'workspace_id': self.workspace_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 2. ResearchQuery — A research query/request
# ===========================================================================

class ResearchQuery(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """A research query capturing what was asked and how."""
    __tablename__ = 'research_queries'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    query_text = Column(Text, nullable=False)
    query_type = Column(String(50), default='keyword')  # keyword, semantic, boolean, entity, topic
    status = Column(String(50), default=QueryStatus.PENDING)
    parameters = Column(JSONType, default=dict)  # Boolean operators, filters, etc.
    filters = Column(JSONType, default=dict)  # Date range, language, region, etc.
    result_count = Column(Integer, default=0)
    execution_time_ms = Column(Integer)
    error_message = Column(Text)
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    source_id = Column(UUID(as_uuid=True), ForeignKey('research_sources.id'), nullable=True)
    collection_id = Column(UUID(as_uuid=True), ForeignKey('research_collections.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=True)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=True)

    # Relationships
    source = relationship("ResearchSource", back_populates="queries")
    collection = relationship("ResearchCollection", back_populates="queries")
    documents = relationship("ResearchDocument", secondary="research_query_documents", back_populates="queries")
    history = relationship("ResearchHistory", back_populates="query")
    cache_entries = relationship("ResearchCache", back_populates="query")

    __table_args__ = (
        Index('idx_research_query_status', 'status'),
        Index('idx_research_query_source', 'source_id'),
        Index('idx_research_query_org', 'organization_id'),
        Index('idx_research_query_created', 'created_at'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'query_text': self.query_text,
            'query_type': self.query_type,
            'status': self.status,
            'parameters': self.parameters,
            'filters': self.filters,
            'result_count': self.result_count,
            'execution_time_ms': self.execution_time_ms,
            'error_message': self.error_message,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'source_id': self.source_id,
            'collection_id': self.collection_id,
            'organization_id': self.organization_id,
            'workspace_id': self.workspace_id,
            'project_id': self.project_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# Association table: ResearchQuery <-> ResearchDocument
ResearchQueryDocument = Base.metadata.tables.get('research_query_documents')
if ResearchQueryDocument is None:
    ResearchQueryDocument = Table(
        'research_query_documents', Base.metadata,
        Column('query_id', UUID(as_uuid=True), ForeignKey('research_queries.id'), primary_key=True),
        Column('document_id', UUID(as_uuid=True), ForeignKey('research_documents.id'), primary_key=True),
        Column('relevance_score', Float, default=0.0),
        Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
    )


# ===========================================================================
# 3. ResearchDocument — A collected document/source
# ===========================================================================

class ResearchDocument(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """A document or piece of content collected during research."""
    __tablename__ = 'research_documents'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    url = Column(String(2000))
    content = Column(Text)  # Full text content
    content_hash = Column(String(64), unique=True)  # SHA-256 hash for dedup
    summary = Column(Text)
    document_type = Column(String(50), default=DocumentType.WEBPAGE)
    source_type = Column(String(50))
    language = Column(String(10))
    author = Column(String(255))
    published_at = Column(DateTime(timezone=True))
    fetched_at = Column(DateTime(timezone=True))
    word_count = Column(Integer, default=0)
    reading_time_minutes = Column(Integer)
    source_credibility = Column(Float, default=0.5)  # 0.0 - 1.0
    relevance_score = Column(Float, default=0.0)
    is_duplicate = Column(Boolean, default=False)
    duplicate_of_id = Column(UUID(as_uuid=True), ForeignKey('research_documents.id'), nullable=True)
    metadata = Column(JSONType, default=dict)  # Source-specific metadata
    source_id = Column(UUID(as_uuid=True), ForeignKey('research_sources.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=True)

    # Relationships
    source = relationship("ResearchSource", back_populates="documents")
    duplicate_of = relationship("ResearchDocument", remote_side=[id], backref="duplicates")
    queries = relationship("ResearchQuery", secondary="research_query_documents", back_populates="documents")
    citations = relationship("ResearchCitation", back_populates="document")
    facts = relationship("ResearchFact", back_populates="document")
    keywords = relationship("ResearchKeyword", back_populates="document")
    entities = relationship("ResearchEntity", back_populates="document")
    scores = relationship("ResearchScore", back_populates="document")

    __table_args__ = (
        Index('idx_research_doc_hash', 'content_hash'),
        Index('idx_research_doc_type', 'document_type'),
        Index('idx_research_doc_source', 'source_id'),
        Index('idx_research_doc_lang', 'language'),
        Index('idx_research_doc_published', 'published_at'),
        Index('idx_research_doc_org', 'organization_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'content_hash': self.content_hash,
            'summary': self.summary,
            'document_type': self.document_type,
            'source_type': self.source_type,
            'language': self.language,
            'author': self.author,
            'published_at': self.published_at,
            'fetched_at': self.fetched_at,
            'word_count': self.word_count,
            'reading_time_minutes': self.reading_time_minutes,
            'source_credibility': self.source_credibility,
            'relevance_score': self.relevance_score,
            'is_duplicate': self.is_duplicate,
            'duplicate_of_id': self.duplicate_of_id,
            'metadata': self.metadata,
            'source_id': self.source_id,
            'organization_id': self.organization_id,
            'workspace_id': self.workspace_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 4. ResearchCollection — Grouping of documents/queries
# ===========================================================================

class ResearchCollection(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """A curated collection of research documents and queries."""
    __tablename__ = 'research_collections'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    color = Column(String(50))
    is_public = Column(Boolean, default=False)
    is_shared = Column(Boolean, default=False)
    parent_id = Column(UUID(as_uuid=True), ForeignKey('research_collections.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=True)

    # Relationships
    parent = relationship("ResearchCollection", remote_side=[id], backref="children")
    queries = relationship("ResearchQuery", back_populates="collection")
    insights = relationship("ResearchInsight", back_populates="collection")
    reports = relationship("ResearchReport", back_populates="collection")

    __table_args__ = (
        Index('idx_research_collection_org', 'organization_id'),
        Index('idx_research_collection_parent', 'parent_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'is_public': self.is_public,
            'is_shared': self.is_shared,
            'parent_id': self.parent_id,
            'organization_id': self.organization_id,
            'workspace_id': self.workspace_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 5. ResearchTopic — Identified topics from research
# ===========================================================================

class ResearchTopic(Base, TimestampMixin, SoftDeleteMixin):
    """A topic identified through research analysis."""
    __tablename__ = 'research_topics'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    relevance_score = Column(Float, default=0.0)
    frequency = Column(Integer, default=1)  # How often this topic appears
    parent_id = Column(UUID(as_uuid=True), ForeignKey('research_topics.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    parent = relationship("ResearchTopic", remote_side=[id], backref="subtopics")

    __table_args__ = (
        Index('idx_research_topic_name', 'name'),
        Index('idx_research_topic_org', 'organization_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'relevance_score': self.relevance_score,
            'frequency': self.frequency,
            'parent_id': self.parent_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 6. ResearchSummary — AI-generated summary of research
# ===========================================================================

class ResearchSummary(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """An AI-generated summary of research findings."""
    __tablename__ = 'research_summaries'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    summary_type = Column(String(50), default='executive')  # executive, detailed, bullet, narrative
    content = Column(Text, nullable=False)
    key_findings = Column(JSONType, default=list)
    word_count = Column(Integer, default=0)
    confidence_score = Column(Float, default=0.0)
    model_used = Column(String(100))
    document_ids = Column(ARRAY(UUID(as_uuid=True)), default=list)
    query_id = Column(UUID(as_uuid=True), ForeignKey('research_queries.id'), nullable=True)
    collection_id = Column(UUID(as_uuid=True), ForeignKey('research_collections.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    query = relationship("ResearchQuery")
    collection = relationship("ResearchCollection", back_populates="insights")

    __table_args__ = (
        Index('idx_research_summary_type', 'summary_type'),
        Index('idx_research_summary_query', 'query_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'summary_type': self.summary_type,
            'content': self.content,
            'key_findings': self.key_findings,
            'word_count': self.word_count,
            'confidence_score': self.confidence_score,
            'model_used': self.model_used,
            'document_ids': self.document_ids,
            'query_id': self.query_id,
            'collection_id': self.collection_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 7. ResearchCitation — Citation linking a document to a fact/claim
# ===========================================================================

class ResearchCitation(Base, TimestampMixin):
    """A citation linking a document, fact, or claim to its source."""
    __tablename__ = 'research_citations'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    citation_text = Column(Text, nullable=False)
    citation_style = Column(String(50), default='apa')  # apa, mla, chicago, custom
    url = Column(String(2000))
    access_date = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    verified = Column(Boolean, default=False)
    verified_at = Column(DateTime(timezone=True))
    verification_method = Column(String(100))
    confidence = Column(String(50), default=ConfidenceLevel.UNVERIFIED)
    document_id = Column(UUID(as_uuid=True), ForeignKey('research_documents.id'), nullable=False)
    fact_id = Column(UUID(as_uuid=True), ForeignKey('research_facts.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    document = relationship("ResearchDocument", back_populates="citations")
    fact = relationship("ResearchFact", back_populates="citations")

    __table_args__ = (
        Index('idx_research_citation_doc', 'document_id'),
        Index('idx_research_citation_fact', 'fact_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'citation_text': self.citation_text,
            'citation_style': self.citation_style,
            'url': self.url,
            'access_date': self.access_date,
            'verified': self.verified,
            'verified_at': self.verified_at,
            'verification_method': self.verification_method,
            'confidence': self.confidence,
            'document_id': self.document_id,
            'fact_id': self.fact_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# 8. ResearchInsight — Generated insight/analysis
# ===========================================================================

class ResearchInsight(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """An AI-generated insight derived from research data."""
    __tablename__ = 'research_insights'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    insight_type = Column(String(50), nullable=False)  # trend, audience, competitor, risk, opportunity, industry
    title = Column(String(500), nullable=False)
    content = Column(Text, nullable=False)
    supporting_evidence = Column(JSONType, default=list)
    contradictory_evidence = Column(JSONType, default=list)
    confidence_score = Column(Float, default=0.0)
    impact_score = Column(Float, default=0.0)  # 0.0 - 1.0
    urgency_score = Column(Float, default=0.0)  # 0.0 - 1.0
    tags = Column(ARRAY(String), default=list)
    source_document_ids = Column(ARRAY(UUID(as_uuid=True)), default=list)
    collection_id = Column(UUID(as_uuid=True), ForeignKey('research_collections.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    collection = relationship("ResearchCollection", back_populates="insights")

    __table_args__ = (
        Index('idx_research_insight_type', 'insight_type'),
        Index('idx_research_insight_collection', 'collection_id'),
        Index('idx_research_insight_confidence', 'confidence_score'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'insight_type': self.insight_type,
            'title': self.title,
            'content': self.content,
            'supporting_evidence': self.supporting_evidence,
            'contradictory_evidence': self.contradictory_evidence,
            'confidence_score': self.confidence_score,
            'impact_score': self.impact_score,
            'urgency_score': self.urgency_score,
            'tags': self.tags,
            'source_document_ids': self.source_document_ids,
            'collection_id': self.collection_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 9. ResearchFact — A verified/extracted fact
# ===========================================================================

class ResearchFact(Base, TimestampMixin, SoftDeleteMixin):
    """A fact extracted and verified from research."""
    __tablename__ = 'research_facts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fact_text = Column(Text, nullable=False)
    category = Column(String(100))  # statistic, quote, date, definition, claim
    confidence = Column(String(50), default=ConfidenceLevel.UNVERIFIED)
    is_verified = Column(Boolean, default=False)
    verification_notes = Column(Text)
    source_count = Column(Integer, default=1)  # Number of sources supporting this fact
    contradiction_count = Column(Integer, default=0)
    document_id = Column(UUID(as_uuid=True), ForeignKey('research_documents.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    document = relationship("ResearchDocument", back_populates="facts")
    citations = relationship("ResearchCitation", back_populates="fact")

    __table_args__ = (
        Index('idx_research_fact_doc', 'document_id'),
        Index('idx_research_fact_confidence', 'confidence'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'fact_text': self.fact_text,
            'category': self.category,
            'confidence': self.confidence,
            'is_verified': self.is_verified,
            'verification_notes': self.verification_notes,
            'source_count': self.source_count,
            'contradiction_count': self.contradiction_count,
            'document_id': self.document_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 10. ResearchKeyword — Extracted keywords
# ===========================================================================

class ResearchKeyword(Base, TimestampMixin):
    """A keyword extracted from a research document."""
    __tablename__ = 'research_keywords'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    keyword = Column(String(255), nullable=False)
    frequency = Column(Integer, default=1)
    relevance_score = Column(Float, default=0.0)
    is_entity = Column(Boolean, default=False)  # Whether this keyword is also an entity
    document_id = Column(UUID(as_uuid=True), ForeignKey('research_documents.id'), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    document = relationship("ResearchDocument", back_populates="keywords")

    __table_args__ = (
        Index('idx_research_keyword_word', 'keyword'),
        Index('idx_research_keyword_doc', 'document_id'),
        Index('idx_research_keyword_freq', 'frequency'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'keyword': self.keyword,
            'frequency': self.frequency,
            'relevance_score': self.relevance_score,
            'is_entity': self.is_entity,
            'document_id': self.document_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# 11. ResearchEntity — Named entity extracted from research
# ===========================================================================

class ResearchEntity(Base, TimestampMixin, SoftDeleteMixin):
    """A named entity identified in research content."""
    __tablename__ = 'research_entities'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(500), nullable=False)
    entity_type = Column(String(50), nullable=False)  # EntityType enum value
    description = Column(Text)
    canonical_name = Column(String(500))  # Normalized form
    aliases = Column(ARRAY(String), default=list)  # Alternative names
    metadata = Column(JSONType, default=dict)
    confidence = Column(Float, default=0.0)
    mention_count = Column(Integer, default=1)
    first_seen_at = Column(DateTime(timezone=True))
    last_seen_at = Column(DateTime(timezone=True))
    document_id = Column(UUID(as_uuid=True), ForeignKey('research_documents.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    document = relationship("ResearchDocument", back_populates="entities")
    relationships_as_source = relationship(
        "ResearchRelationship",
        foreign_keys="ResearchRelationship.source_entity_id",
        back_populates="source_entity"
    )
    relationships_as_target = relationship(
        "ResearchRelationship",
        foreign_keys="ResearchRelationship.target_entity_id",
        back_populates="target_entity"
    )

    __table_args__ = (
        Index('idx_research_entity_name', 'name'),
        Index('idx_research_entity_type', 'entity_type'),
        Index('idx_research_entity_doc', 'document_id'),
        Index('idx_research_entity_canonical', 'canonical_name'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'entity_type': self.entity_type,
            'description': self.description,
            'canonical_name': self.canonical_name,
            'aliases': self.aliases,
            'metadata': self.metadata,
            'confidence': self.confidence,
            'mention_count': self.mention_count,
            'first_seen_at': self.first_seen_at,
            'last_seen_at': self.last_seen_at,
            'document_id': self.document_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 12. ResearchRelationship — Relationship between two entities
# ===========================================================================

class ResearchRelationship(Base, TimestampMixin):
    """A semantic relationship between two entities."""
    __tablename__ = 'research_relationships'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    relationship_type = Column(String(50), nullable=False)  # RelationshipType enum value
    label = Column(String(255))
    strength = Column(Float, default=0.5)  # 0.0 - 1.0
    context = Column(Text)  # Context in which the relationship was observed
    source_entity_id = Column(UUID(as_uuid=True), ForeignKey('research_entities.id'), nullable=False)
    target_entity_id = Column(UUID(as_uuid=True), ForeignKey('research_entities.id'), nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey('research_documents.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    source_entity = relationship(
        "ResearchEntity", foreign_keys=[source_entity_id],
        back_populates="relationships_as_source"
    )
    target_entity = relationship(
        "ResearchEntity", foreign_keys=[target_entity_id],
        back_populates="relationships_as_target"
    )

    __table_args__ = (
        Index('idx_research_rel_type', 'relationship_type'),
        Index('idx_research_rel_source', 'source_entity_id'),
        Index('idx_research_rel_target', 'target_entity_id'),
        Index('idx_research_rel_pair', 'source_entity_id', 'target_entity_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'relationship_type': self.relationship_type,
            'label': self.label,
            'strength': self.strength,
            'context': self.context,
            'source_entity_id': self.source_entity_id,
            'target_entity_id': self.target_entity_id,
            'document_id': self.document_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# 13. ResearchScore — Scoring/rubric for documents
# ===========================================================================

class ResearchScore(Base, TimestampMixin):
    """Quality/ranking score for a research document."""
    __tablename__ = 'research_scores'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    score_type = Column(String(50), nullable=False)  # relevance, credibility, quality, freshness, authority
    score_value = Column(Float, nullable=False)  # 0.0 - 1.0
    weight = Column(Float, default=1.0)
    reason = Column(Text)  # Why this score was assigned
    scorer = Column(String(100), default='system')  # system, ai_model, human
    document_id = Column(UUID(as_uuid=True), ForeignKey('research_documents.id'), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    document = relationship("ResearchDocument", back_populates="scores")

    __table_args__ = (
        Index('idx_research_score_doc', 'document_id'),
        Index('idx_research_score_type', 'score_type'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'score_type': self.score_type,
            'score_value': self.score_value,
            'weight': self.weight,
            'reason': self.reason,
            'scorer': self.scorer,
            'document_id': self.document_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# 14. ResearchSnapshot — Point-in-time snapshot of research
# ===========================================================================

class ResearchSnapshot(Base, TimestampMixin, AuditMixin):
    """A point-in-time snapshot of a research state."""
    __tablename__ = 'research_snapshots'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    snapshot_type = Column(String(50), default='auto')  # auto, manual, scheduled
    data = Column(JSONType, nullable=False)  # Snapshot payload
    document_count = Column(Integer, default=0)
    entity_count = Column(Integer, default=0)
    relationship_count = Column(Integer, default=0)
    tag = Column(String(100))  # Version tag
    query_id = Column(UUID(as_uuid=True), ForeignKey('research_queries.id'), nullable=True)
    collection_id = Column(UUID(as_uuid=True), ForeignKey('research_collections.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    __table_args__ = (
        Index('idx_research_snapshot_query', 'query_id'),
        Index('idx_research_snapshot_type', 'snapshot_type'),
        Index('idx_research_snapshot_created', 'created_at'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'snapshot_type': self.snapshot_type,
            'data': self.data,
            'document_count': self.document_count,
            'entity_count': self.entity_count,
            'relationship_count': self.relationship_count,
            'tag': self.tag,
            'query_id': self.query_id,
            'collection_id': self.collection_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# 15. ResearchCache — Cached research results
# ===========================================================================

class ResearchCache(Base, TimestampMixin):
    """Cache entry for research results to avoid redundant queries."""
    __tablename__ = 'research_caches'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    cache_key = Column(String(500), unique=True, nullable=False)
    cache_type = Column(String(50), default='query')  # query, source, document, summary
    data = Column(JSONType, nullable=False)
    ttl_seconds = Column(Integer, default=3600)  # Time-to-live
    expires_at = Column(DateTime(timezone=True), nullable=False)
    hit_count = Column(Integer, default=0)
    size_bytes = Column(Integer, default=0)
    query_id = Column(UUID(as_uuid=True), ForeignKey('research_queries.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    query = relationship("ResearchQuery", back_populates="cache_entries")

    __table_args__ = (
        Index('idx_research_cache_key', 'cache_key'),
        Index('idx_research_cache_expires', 'expires_at'),
        Index('idx_research_cache_type', 'cache_type'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'cache_key': self.cache_key,
            'cache_type': self.cache_type,
            'data': self.data,
            'ttl_seconds': self.ttl_seconds,
            'expires_at': self.expires_at,
            'hit_count': self.hit_count,
            'size_bytes': self.size_bytes,
            'query_id': self.query_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# 16. ResearchJob — Background job tracking
# ===========================================================================

class ResearchJob(Base, TimestampMixin):
    """Tracking for background research jobs."""
    __tablename__ = 'research_jobs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_type = Column(String(50), nullable=False)  # query, collection, summarization, insight, snapshot, export
    status = Column(String(50), default=JobStatus.PENDING)
    priority = Column(Integer, default=0)
    payload = Column(JSONType, default=dict)
    result = Column(JSONType, nullable=True)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    progress = Column(Float, default=0.0)  # 0.0 - 1.0
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    scheduled_at = Column(DateTime(timezone=True))
    scheduled_by = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    query_id = Column(UUID(as_uuid=True), ForeignKey('research_queries.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=True)

    __table_args__ = (
        Index('idx_research_job_status', 'status'),
        Index('idx_research_job_type', 'job_type'),
        Index('idx_research_job_query', 'query_id'),
        Index('idx_research_job_scheduled', 'scheduled_at'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'job_type': self.job_type,
            'status': self.status,
            'priority': self.priority,
            'payload': self.payload,
            'result': self.result,
            'error_message': self.error_message,
            'retry_count': self.retry_count,
            'max_retries': self.max_retries,
            'progress': self.progress,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'scheduled_at': self.scheduled_at,
            'scheduled_by': self.scheduled_by,
            'query_id': self.query_id,
            'organization_id': self.organization_id,
            'workspace_id': self.workspace_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# 17. ResearchHistory — History of research activity
# ===========================================================================

class ResearchHistory(Base, TimestampMixin):
    """Historical record of research queries and actions."""
    __tablename__ = 'research_history'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action = Column(String(100), nullable=False)  # query_executed, document_added, collection_created, etc.
    description = Column(Text)
    metadata = Column(JSONType, default=dict)
    query_id = Column(UUID(as_uuid=True), ForeignKey('research_queries.id'), nullable=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey('research_documents.id'), nullable=True)
    collection_id = Column(UUID(as_uuid=True), ForeignKey('research_collections.id'), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    query = relationship("ResearchQuery", back_populates="history")

    __table_args__ = (
        Index('idx_research_history_action', 'action'),
        Index('idx_research_history_query', 'query_id'),
        Index('idx_research_history_user', 'user_id'),
        Index('idx_research_history_created', 'created_at'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'action': self.action,
            'description': self.description,
            'metadata': self.metadata,
            'query_id': self.query_id,
            'document_id': self.document_id,
            'collection_id': self.collection_id,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# 18. ResearchBookmark — User bookmarks for research items
# ===========================================================================

class ResearchBookmark(Base, TimestampMixin):
    """User bookmark for a research document or query."""
    __tablename__ = 'research_bookmarks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500))
    notes = Column(Text)
    item_type = Column(String(50), nullable=False)  # document, query, collection, insight, report
    item_id = Column(UUID(as_uuid=True), nullable=False)
    folder_id = Column(UUID(as_uuid=True), ForeignKey('research_folders.id'), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    folder = relationship("ResearchFolder", back_populates="bookmarks")
    user = relationship("User")

    __table_args__ = (
        Index('idx_research_bookmark_user', 'user_id'),
        Index('idx_research_bookmark_item', 'item_type', 'item_id'),
        Index('idx_research_bookmark_folder', 'folder_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'notes': self.notes,
            'item_type': self.item_type,
            'item_id': self.item_id,
            'folder_id': self.folder_id,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# 19. ResearchFolder — Folder for organizing bookmarks
# ===========================================================================

class ResearchFolder(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Folder for organizing research bookmarks."""
    __tablename__ = 'research_folders'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    icon = Column(String(50))
    color = Column(String(50))
    parent_id = Column(UUID(as_uuid=True), ForeignKey('research_folders.id'), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    parent = relationship("ResearchFolder", remote_side=[id], backref="subfolders")
    bookmarks = relationship("ResearchBookmark", back_populates="folder")

    __table_args__ = (
        Index('idx_research_folder_user', 'user_id'),
        Index('idx_research_folder_parent', 'parent_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'icon': self.icon,
            'color': self.color,
            'parent_id': self.parent_id,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 20. ResearchTag — Tags for categorizing research items
# ===========================================================================

class ResearchTag(Base, TimestampMixin):
    """Tag for categorizing research items."""
    __tablename__ = 'research_tags'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    slug = Column(String(100), nullable=False)
    color = Column(String(50))
    description = Column(Text)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    __table_args__ = (
        Index('idx_research_tag_slug', 'slug'),
        Index('idx_research_tag_name', 'name'),
        Index('idx_research_tag_org', 'organization_id'),
        UniqueConstraint('slug', 'organization_id', name='uq_research_tag_org_slug'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'color': self.color,
            'description': self.description,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# 21. ResearchReport — Generated research report
# ===========================================================================

class ResearchReport(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """A comprehensive research report generated from collected data."""
    __tablename__ = 'research_reports'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(500), nullable=False)
    report_type = Column(String(50), default='standard')  # standard, deep_dive, competitive, trend, custom
    content = Column(Text)
    executive_summary = Column(Text)
    key_findings = Column(JSONType, default=list)
    sections = Column(JSONType, default=list)  # Structured sections
    methodology = Column(Text)
    conclusion = Column(Text)
    recommendations = Column(JSONType, default=list)
    document_count = Column(Integer, default=0)
    source_count = Column(Integer, default=0)
    fact_count = Column(Integer, default=0)
    insight_count = Column(Integer, default=0)
    confidence_score = Column(Float, default=0.0)
    version = Column(Integer, default=1)
    published = Column(Boolean, default=False)
    published_at = Column(DateTime(timezone=True))
    template = Column(String(100))
    format = Column(String(50), default='markdown')  # markdown, html, pdf, docx
    collection_id = Column(UUID(as_uuid=True), ForeignKey('research_collections.id'), nullable=True)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'), nullable=True)

    collection = relationship("ResearchCollection", back_populates="reports")

    __table_args__ = (
        Index('idx_research_report_type', 'report_type'),
        Index('idx_research_report_collection', 'collection_id'),
        Index('idx_research_report_org', 'organization_id'),
        Index('idx_research_report_published', 'published'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'report_type': self.report_type,
            'content': self.content,
            'executive_summary': self.executive_summary,
            'key_findings': self.key_findings,
            'sections': self.sections,
            'methodology': self.methodology,
            'conclusion': self.conclusion,
            'recommendations': self.recommendations,
            'document_count': self.document_count,
            'source_count': self.source_count,
            'fact_count': self.fact_count,
            'insight_count': self.insight_count,
            'confidence_score': self.confidence_score,
            'version': self.version,
            'published': self.published,
            'published_at': self.published_at,
            'template': self.template,
            'format': self.format,
            'collection_id': self.collection_id,
            'organization_id': self.organization_id,
            'workspace_id': self.workspace_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 22. ResearchAlert — Alert/watch for research conditions
# ===========================================================================

class ResearchAlert(Base, TimestampMixin, SoftDeleteMixin, AuditMixin):
    """Alert or watch for specific research conditions."""
    __tablename__ = 'research_alerts'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    alert_type = Column(String(50), nullable=False)  # new_topic, mention, trend_change, source_update
    conditions = Column(JSONType, nullable=False)  # Alert trigger conditions
    frequency = Column(String(50), default='realtime')  # realtime, hourly, daily, weekly
    last_triggered_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    notify_via = Column(ARRAY(String), default=['email'])  # email, slack, webhook, in_app
    channel_config = Column(JSONType, default=dict)
    query_id = Column(UUID(as_uuid=True), ForeignKey('research_queries.id'), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    user = relationship("User")

    __table_args__ = (
        Index('idx_research_alert_type', 'alert_type'),
        Index('idx_research_alert_user', 'user_id'),
        Index('idx_research_alert_active', 'is_active'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'alert_type': self.alert_type,
            'conditions': self.conditions,
            'frequency': self.frequency,
            'last_triggered_at': self.last_triggered_at,
            'is_active': self.is_active,
            'notify_via': self.notify_via,
            'channel_config': self.channel_config,
            'query_id': self.query_id,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at,
        }


# ===========================================================================
# 23. ResearchFeedback — User feedback on research quality
# ===========================================================================

class ResearchFeedback(Base, TimestampMixin):
    """User feedback on research results quality."""
    __tablename__ = 'research_feedback'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rating = Column(Integer, nullable=False)  # 1-5
    feedback_text = Column(Text)
    feedback_type = Column(String(50), default='general')  # general, accuracy, relevance, completeness
    is_helpful = Column(Boolean, default=True)
    item_type = Column(String(50), nullable=False)  # document, query, summary, insight, report
    item_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'), nullable=True)

    user = relationship("User")

    __table_args__ = (
        Index('idx_research_feedback_user', 'user_id'),
        Index('idx_research_feedback_item', 'item_type', 'item_id'),
        Index('idx_research_feedback_rating', 'rating'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'feedback_text': self.feedback_text,
            'feedback_type': self.feedback_type,
            'is_helpful': self.is_helpful,
            'item_type': self.item_type,
            'item_id': self.item_id,
            'user_id': self.user_id,
            'organization_id': self.organization_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
        }


# ===========================================================================
# Association tables
# ===========================================================================

# Document-Tag association
ResearchDocumentTag = Base.metadata.tables.get('research_document_tags')
if ResearchDocumentTag is None:
    ResearchDocumentTag = Table(
        'research_document_tags', Base.metadata,
        Column('document_id', UUID(as_uuid=True), ForeignKey('research_documents.id'), primary_key=True),
        Column('tag_id', UUID(as_uuid=True), ForeignKey('research_tags.id'), primary_key=True),
        Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
    )

# Entity-Document association (many-to-many)
ResearchEntityDocument = Base.metadata.tables.get('research_entity_documents')
if ResearchEntityDocument is None:
    ResearchEntityDocument = Table(
        'research_entity_documents', Base.metadata,
        Column('entity_id', UUID(as_uuid=True), ForeignKey('research_entities.id'), primary_key=True),
        Column('document_id', UUID(as_uuid=True), ForeignKey('research_documents.id'), primary_key=True),
        Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
    )

# Report-Document association
ResearchReportDocument = Base.metadata.tables.get('research_report_documents')
if ResearchReportDocument is None:
    ResearchReportDocument = Table(
        'research_report_documents', Base.metadata,
        Column('report_id', UUID(as_uuid=True), ForeignKey('research_reports.id'), primary_key=True),
        Column('document_id', UUID(as_uuid=True), ForeignKey('research_documents.id'), primary_key=True),
        Column('created_at', DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)),
    )
