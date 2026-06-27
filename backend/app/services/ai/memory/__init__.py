"""
Memory Engine Service

Provides context persistence for AI agents.
Supports conversation, brand, project, campaign, and performance memory.
"""

import re
import math
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass
from enum import Enum
from collections import Counter
import logging
import json

from app.services.ai.gateway import gateway, AIRequest

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Types of memory."""
    CONVERSATION = "conversation"
    BRAND = "brand"
    PROJECT = "project"
    CAMPAIGN = "campaign"
    USER = "user"
    PERFORMANCE = "performance"
    KNOWLEDGE = "knowledge"


@dataclass
class MemoryEntry:
    """A single memory entry."""
    id: str
    memory_type: MemoryType
    content: str
    summary: Optional[str]
    importance: float
    tags: List[str]
    metadata: Dict[str, Any]
    created_at: datetime
    expires_at: Optional[datetime]
    access_count: int = 0


@dataclass
class MemoryQuery:
    """Query for memory retrieval."""
    query: str
    memory_types: Optional[List[MemoryType]] = None
    tags: Optional[List[str]] = None
    min_importance: float = 0.0
    max_results: int = 10
    include_expired: bool = False


class MemoryEngine:
    """
    Memory Engine for AI context persistence.
    
    Manages:
    - Conversation memory (short-term, long-term)
    - Brand memory (guidelines, voice, identity)
    - Project memory (context, history)
    - Campaign memory (performance, learnings)
    - User memory (preferences, history)
    - Performance memory (metrics, learnings)
    """
    
    def __init__(self):
        self.memories: Dict[str, MemoryEntry] = {}
        self.indexes: Dict[MemoryType, List[str]] = {
            mt: [] for mt in MemoryType
        }
        self._initialized = False
    
    async def initialize(self):
        """Initialize memory engine."""
        if self._initialized:
            return
        
        await self._load_memories()
        self._initialized = True
        logger.info("Memory Engine initialized")
    
    async def _load_memories(self):
        """Load memories from database."""
        # Attempt to load from database via the Memory model
        try:
            from app.db.session import SessionLocal
            from app.models.ai.memory import MemoryEntry as MemoryModel
            
            db = SessionLocal()
            try:
                db_entries = db.query(MemoryModel).filter(
                    MemoryModel.is_active == True
                ).all()
                
                for entry in db_entries:
                    memory_entry = MemoryEntry(
                        id=str(entry.id),
                        memory_type=MemoryType(entry.memory_type),
                        content=entry.content,
                        summary=entry.summary,
                        importance=entry.importance or 0.5,
                        tags=entry.tags or [],
                        metadata=entry.metadata or {},
                        created_at=entry.created_at,
                        expires_at=entry.expires_at,
                        access_count=entry.access_count or 0,
                    )
                    self.memories[memory_entry.id] = memory_entry
                    self.indexes[memory_entry.memory_type].append(memory_entry.id)
                
                logger.info(f"Loaded {len(db_entries)} memories from database")
            finally:
                db.close()
        except Exception as e:
            logger.warning(f"Could not load memories from database: {e}")
            logger.info("Starting with empty memory store")
    
    async def store(
        self,
        memory_type: MemoryType,
        content: str,
        tags: Optional[List[str]] = None,
        importance: float = 0.5,
        metadata: Optional[Dict[str, Any]] = None,
        ttl_days: Optional[int] = None,
        reference_id: Optional[str] = None
    ) -> str:
        """
        Store a new memory.
        
        Args:
            memory_type: Type of memory
            content: Memory content
            tags: Tags for categorization
            importance: Importance score (0.0 to 1.0)
            metadata: Additional metadata
            ttl_days: Time to live in days
            reference_id: Reference to source entity
            
        Returns:
            Memory ID
        """
        if not self._initialized:
            await self.initialize()
        
        import uuid
        memory_id = str(uuid.uuid4())
        
        expires_at = None
        if ttl_days:
            expires_at = datetime.now(timezone.utc) + timedelta(days=ttl_days)
        
        entry = MemoryEntry(
            id=memory_id,
            memory_type=memory_type,
            content=content,
            summary=None,
            importance=importance,
            tags=tags or [],
            metadata=metadata or {},
            created_at=datetime.now(timezone.utc),
            expires_at=expires_at
        )
        
        self.memories[memory_id] = entry
        self.indexes[memory_type].append(memory_id)
        
        # Generate summary if content is long
        if len(content) > 500:
            entry.summary = await self._generate_summary(content)
        
        logger.debug(f"Stored memory {memory_id} of type {memory_type.value}")
        
        return memory_id
    
    async def retrieve(
        self,
        query: MemoryQuery
    ) -> List[MemoryEntry]:
        """
        Retrieve memories matching query.
        
        Uses:
        1. Exact keyword matching (baseline)
        2. TF-IDF relevance scoring (semantic-like)
        3. Recency and importance boosting
        
        Args:
            query: Memory query
            
        Returns:
            List of matching memory entries, sorted by relevance
        """
        if not self._initialized:
            await self.initialize()
        
        results: List[Tuple[MemoryEntry, float]] = []
        query_terms = set(self._tokenize(query.query.lower()))
        
        for memory_id, entry in self.memories.items():
            # Check expiry
            if not query.include_expired and entry.expires_at:
                if entry.expires_at < datetime.now(timezone.utc):
                    continue
            
            # Check memory type
            if query.memory_types and entry.memory_type not in query.memory_types:
                continue
            
            # Check importance
            if entry.importance < query.min_importance:
                continue
            
            # Check tags
            if query.tags:
                if not set(query.tags) & set(entry.tags):
                    continue
            
            # Compute relevance score
            content_lower = entry.content.lower()
            
            # 1. Exact substring match (baseline)
            exact_match = query.query.lower() in content_lower
            
            if not exact_match and not query_terms:
                continue
            
            # 2. TF-IDF-like scoring
            if query_terms:
                content_terms = self._tokenize(content_lower)
                content_term_freq = Counter(content_terms)
                
                # Term frequency score
                tf_score = 0.0
                for term in query_terms:
                    if term in content_term_freq:
                        tf = content_term_freq[term] / max(len(content_terms), 1)
                        # Inverse doc frequency (simplified: rarer terms score higher)
                        idf = math.log((len(self.memories) + 1) / max(self._term_doc_count.get(term, 1), 1))
                        tf_score += tf * idf
                
                # Normalize by query length
                tf_score /= max(len(query_terms), 1)
            else:
                tf_score = 0.5  # Pure keyword match
            
            # 3. Importance boost
            importance_boost = entry.importance * 0.3
            
            # 4. Recency boost (more recent = higher score)
            age_hours = (datetime.now(timezone.utc) - entry.created_at).total_seconds() / 3600
            recency_boost = math.exp(-age_hours / 720) * 0.2  # Half-life ~30 days
            
            combined_score = (
                (1.0 if exact_match else 0.0) * 0.3 +
                tf_score * 0.3 +
                importance_boost +
                recency_boost
            )
            
            if combined_score > 0:
                entry.access_count += 1
                results.append((entry, combined_score))
        
        # Sort by combined score (descending)
        results.sort(key=lambda e: e[1], reverse=True)
        
        return [entry for entry, score in results[:query.max_results]]
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words for search."""
        # Split on non-alphanumeric characters, filter short words
        tokens = re.findall(r'\b[a-zA-Z]{3,}\b', text)
        return [t.lower() for t in tokens if len(t) >= 3]
    
    @property
    def _term_doc_count(self) -> Dict[str, int]:
        """Count how many documents each term appears in (for IDF)."""
        counts: Dict[str, int] = {}
        for entry in self.memories.values():
            terms = set(self._tokenize(entry.content.lower()))
            for term in terms:
                counts[term] = counts.get(term, 0) + 1
        return counts
    
    async def get_conversation_history(
        self,
        session_id: str,
        max_messages: int = 50
    ) -> List[MemoryEntry]:
        """Get conversation history for a session."""
        query = MemoryQuery(
            query=session_id,
            memory_types=[MemoryType.CONVERSATION],
            max_results=max_messages,
            include_expired=False
        )
        return await self.retrieve(query)
    
    async def get_brand_context(
        self,
        brand_id: str
    ) -> Optional[MemoryEntry]:
        """Get brand context memory."""
        query = MemoryQuery(
            query=brand_id,
            memory_types=[MemoryType.BRAND],
            max_results=1
        )
        results = await self.retrieve(query)
        return results[0] if results else None
    
    async def get_project_context(
        self,
        project_id: str
    ) -> List[MemoryEntry]:
        """Get project context memories."""
        query = MemoryQuery(
            query=project_id,
            memory_types=[MemoryType.PROJECT],
            max_results=20
        )
        return await self.retrieve(query)
    
    async def update_importance(
        self,
        memory_id: str,
        importance: float
    ):
        """Update memory importance score."""
        if memory_id in self.memories:
            self.memories[memory_id].importance = max(0.0, min(1.0, importance))
    
    async def compress(
        self,
        memory_id: str
    ) -> Optional[str]:
        """
        Compress a memory entry.
        
        Returns compressed summary.
        """
        if memory_id not in self.memories:
            return None
        
        entry = self.memories[memory_id]
        
        if entry.summary:
            return entry.summary
        
        # Generate summary
        summary = await self._generate_summary(entry.content)
        entry.summary = summary
        
        return summary
    
    async def _generate_summary(self, content: str) -> str:
        """Generate a summary of content using the AI gateway."""
        if len(content) <= 200:
            return content
        
        try:
            ai_request = AIRequest(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": f"Summarize the following content in 1-2 sentences:\n\n{content[:4000]}"
                }],
                temperature=0.3,
                max_tokens=150,
            )
            
            response = await gateway.execute(ai_request)
            summary = response.content.strip()
            
            if summary:
                return summary
        except Exception as e:
            logger.warning(f"AI summary generation failed, using truncation: {e}")
        
        # Fallback: return truncated content
        return content[:200] + "..."
    
    async def cleanup_expired(self):
        """Remove expired memories."""
        now = datetime.now(timezone.utc)
        expired_ids = [
            mid for mid, entry in self.memories.items()
            if entry.expires_at and entry.expires_at < now
        ]
        
        for mid in expired_ids:
            entry = self.memories.pop(mid)
            self.indexes[entry.memory_type].remove(mid)
        
        if expired_ids:
            logger.info(f"Cleaned up {len(expired_ids)} expired memories")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        stats = {
            "total_memories": len(self.memories),
            "by_type": {},
            "avg_importance": 0.0,
            "total_access_count": 0
        }
        
        total_importance = 0
        for memory_type in MemoryType:
            count = len(self.indexes[memory_type])
            stats["by_type"][memory_type.value] = count
        
        for entry in self.memories.values():
            total_importance += entry.importance
            stats["total_access_count"] += entry.access_count
        
        if self.memories:
            stats["avg_importance"] = total_importance / len(self.memories)
        
        return stats


# Singleton instance
memory_engine = MemoryEngine()
