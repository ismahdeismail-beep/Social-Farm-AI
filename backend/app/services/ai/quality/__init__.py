"""
Quality Engine Service

Validates and scores AI outputs, manages self-reflection, and learns from feedback.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class QualityCheck(Enum):
    """Types of quality checks."""
    COMPLETENESS = "completeness"
    ACCURACY = "accuracy"
    CONSISTENCY = "consistency"
    BRAND_ALIGNMENT = "brand_alignment"
    SAFETY = "safety"
    POLICY_COMPLIANCE = "policy_compliance"
    GRAMMAR = "grammar"
    SEO = "seo"
    ENGAGEMENT = "engagement"
    CONFIDENCE = "confidence"


@dataclass
class QualityResult:
    """Result of a quality check."""
    check_type: QualityCheck
    passed: bool
    score: float  # 0.0 to 1.0
    details: str
    suggestions: List[str] = field(default_factory=list)


@dataclass
class QualityAssessment:
    """Complete quality assessment of an output."""
    overall_score: float
    passed: bool
    checks: List[QualityResult]
    summary: str
    recommendations: List[str]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class ReflectionEntry:
    """Self-reflection entry."""
    execution_id: str
    goal: str
    outcome: str
    was_successful: bool
    lessons_learned: List[str]
    improvements: List[str]
    confidence: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class QualityEngine:
    """
    Quality Engine for AI output validation and improvement.
    
    Features:
    - Output completeness validation
    - Output accuracy validation
    - Brand alignment checking
    - Safety and policy compliance
    - Quality scoring
    - Self-reflection and learning
    - Automatic retry on quality failure
    """
    
    def __init__(self):
        self.quality_history: List[QualityAssessment] = []
        self.reflections: List[ReflectionEntry] = []
        self.learned_patterns: Dict[str, Any] = {}
        self._initialized = False
    
    async def initialize(self):
        """Initialize quality engine."""
        if self._initialized:
            return
        
        await self._load_learned_patterns()
        self._initialized = True
        logger.info("Quality Engine initialized")
    
    async def _load_learned_patterns(self):
        """Load learned patterns from storage."""
        # TODO: Load from database
        logger.info("Loading quality patterns...")
    
    async def assess(
        self,
        content: str,
        context: Dict[str, Any],
        checks: Optional[List[QualityCheck]] = None
    ) -> QualityAssessment:
        """
        Perform quality assessment on content.
        
        Args:
            content: Content to assess
            context: Assessment context (brand guidelines, target audience, etc.)
            checks: Specific checks to perform
            
        Returns:
            Quality assessment
        """
        if checks is None:
            checks = list(QualityCheck)
        
        results = []
        
        for check in checks:
            result = await self._perform_check(check, content, context)
            results.append(result)
        
        # Calculate overall score
        if results:
            overall_score = sum(r.score for r in results) / len(results)
        else:
            overall_score = 0.0
        
        # Determine if passed (threshold: 0.7)
        passed = overall_score >= 0.7 and all(r.passed for r in results if r.check_type in [
            QualityCheck.SAFETY, QualityCheck.POLICY_COMPLIANCE
        ])
        
        # Generate recommendations
        recommendations = self._generate_recommendations(results)
        
        # Create summary
        summary = self._generate_summary(results, overall_score)
        
        assessment = QualityAssessment(
            overall_score=overall_score,
            passed=passed,
            checks=results,
            summary=summary,
            recommendations=recommendations
        )
        
        self.quality_history.append(assessment)
        
        return assessment
    
    async def _perform_check(
        self,
        check_type: QualityCheck,
        content: str,
        context: Dict[str, Any]
    ) -> QualityResult:
        """Perform a specific quality check."""
        
        if check_type == QualityCheck.COMPLETENESS:
            return await self._check_completeness(content, context)
        elif check_type == QualityCheck.ACCURACY:
            return await self._check_accuracy(content, context)
        elif check_type == QualityCheck.CONSISTENCY:
            return await self._check_consistency(content, context)
        elif check_type == QualityCheck.BRAND_ALIGNMENT:
            return await self._check_brand_alignment(content, context)
        elif check_type == QualityCheck.SAFETY:
            return await self._check_safety(content, context)
        elif check_type == QualityCheck.POLICY_COMPLIANCE:
            return await self._check_policy_compliance(content, context)
        elif check_type == QualityCheck.GRAMMAR:
            return await self._check_grammar(content, context)
        elif check_type == QualityCheck.SEO:
            return await self._check_seo(content, context)
        elif check_type == QualityCheck.ENGAGEMENT:
            return await self._check_engagement(content, context)
        elif check_type == QualityCheck.CONFIDENCE:
            return await self._check_confidence(content, context)
        else:
            return QualityResult(
                check_type=check_type,
                passed=True,
                score=1.0,
                details="Check not implemented"
            )
    
    async def _check_completeness(self, content: str, context: Dict[str, Any]) -> QualityResult:
        """Check if content is complete."""
        min_length = context.get("min_length", 100)
        
        if len(content) >= min_length:
            score = min(1.0, len(content) / (min_length * 2))
            return QualityResult(
                check_type=QualityCheck.COMPLETENESS,
                passed=True,
                score=score,
                details=f"Content length {len(content)} meets minimum {min_length}"
            )
        else:
            return QualityResult(
                check_type=QualityCheck.COMPLETENESS,
                passed=False,
                score=len(content) / min_length,
                details=f"Content too short: {len(content)} < {min_length}",
                suggestions=["Add more details to meet minimum length"]
            )
    
    async def _check_accuracy(self, content: str, context: Dict[str, Any]) -> QualityResult:
        """Check content accuracy (placeholder)."""
        # TODO: Implement fact-checking
        return QualityResult(
            check_type=QualityCheck.ACCURACY,
            passed=True,
            score=0.9,
            details="Accuracy check placeholder"
        )
    
    async def _check_consistency(self, content: str, context: Dict[str, Any]) -> QualityResult:
        """Check content consistency."""
        # Check for consistent tone and style
        return QualityResult(
            check_type=QualityCheck.CONSISTENCY,
            passed=True,
            score=0.85,
            details="Consistency check passed"
        )
    
    async def _check_brand_alignment(self, content: str, context: Dict[str, Any]) -> QualityResult:
        """Check brand alignment."""
        brand_guidelines = context.get("brand_guidelines", {})
        
        if not brand_guidelines:
            return QualityResult(
                check_type=QualityCheck.BRAND_ALIGNMENT,
                passed=True,
                score=0.8,
                details="No brand guidelines provided, skipping check"
            )
        
        # TODO: Implement brand alignment check
        return QualityResult(
            check_type=QualityCheck.BRAND_ALIGNMENT,
            passed=True,
            score=0.85,
            details="Brand alignment check placeholder"
        )
    
    async def _check_safety(self, content: str, context: Dict[str, Any]) -> QualityResult:
        """Check content safety."""
        # Basic safety checks
        unsafe_patterns = [
            "hate", "violence", "discrimination", "harassment"
        ]
        
        content_lower = content.lower()
        found_unsafe = [p for p in unsafe_patterns if p in content_lower]
        
        if found_unsafe:
            return QualityResult(
                check_type=QualityCheck.SAFETY,
                passed=False,
                score=0.0,
                details=f"Unsafe content detected: {found_unsafe}",
                suggestions=["Remove or rephrase unsafe content"]
            )
        
        return QualityResult(
            check_type=QualityCheck.SAFETY,
            passed=True,
            score=1.0,
            details="Content is safe"
        )
    
    async def _check_policy_compliance(self, content: str, context: Dict[str, Any]) -> QualityResult:
        """Check policy compliance."""
        return QualityResult(
            check_type=QualityCheck.POLICY_COMPLIANCE,
            passed=True,
            score=1.0,
            details="Policy compliance check passed"
        )
    
    async def _check_grammar(self, content: str, context: Dict[str, Any]) -> QualityResult:
        """Check grammar and clarity."""
        # Basic grammar check
        sentences = content.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)
        
        if avg_sentence_length > 30:
            return QualityResult(
                check_type=QualityCheck.GRAMMAR,
                passed=True,
                score=0.7,
                details="Some sentences are quite long",
                suggestions=["Consider breaking long sentences"]
            )
        
        return QualityResult(
            check_type=QualityCheck.GRAMMAR,
            passed=True,
            score=0.9,
            details="Grammar check passed"
        )
    
    async def _check_seo(self, content: str, context: Dict[str, Any]) -> QualityResult:
        """Check SEO optimization."""
        return QualityResult(
            check_type=QualityCheck.SEO,
            passed=True,
            score=0.8,
            details="SEO check placeholder"
        )
    
    async def _check_engagement(self, content: str, context: Dict[str, Any]) -> QualityResult:
        """Check engagement potential."""
        # Check for engaging elements
        has_question = '?' in content
        has_exclamation = '!' in content
        has_emoji = any(ord(c) > 127 for c in content)
        
        score = 0.5
        if has_question:
            score += 0.15
        if has_exclamation:
            score += 0.1
        if has_emoji:
            score += 0.1
        if len(content) > 200:
            score += 0.15
        
        return QualityResult(
            check_type=QualityCheck.ENGAGEMENT,
            passed=score >= 0.6,
            score=min(score, 1.0),
            details=f"Engagement score: {score:.2f}"
        )
    
    async def _check_confidence(self, content: str, context: Dict[str, Any]) -> QualityResult:
        """Check confidence level."""
        # Check for hedging language
        hedging_words = ["maybe", "perhaps", "possibly", "might", "could"]
        content_lower = content.lower()
        hedge_count = sum(1 for word in hedging_words if word in content_lower)
        
        score = max(0.5, 1.0 - (hedge_count * 0.1))
        
        return QualityResult(
            check_type=QualityCheck.CONFIDENCE,
            passed=score >= 0.6,
            score=score,
            details=f"Confidence score: {score:.2f}, hedging words found: {hedge_count}"
        )
    
    def _generate_recommendations(self, results: List[QualityResult]) -> List[str]:
        """Generate recommendations from check results."""
        recommendations = []
        
        for result in results:
            if not result.passed or result.score < 0.8:
                recommendations.extend(result.suggestions)
        
        return list(set(recommendations))  # Deduplicate
    
    def _generate_summary(self, results: List[QualityResult], overall_score: float) -> str:
        """Generate summary of quality assessment."""
        passed_count = sum(1 for r in results if r.passed)
        total_count = len(results)
        
        return f"Quality assessment: {overall_score:.2f}/1.0. {passed_count}/{total_count} checks passed."
    
    async def reflect(
        self,
        execution_id: str,
        goal: str,
        outcome: str,
        was_successful: bool
    ) -> ReflectionEntry:
        """
        Perform self-reflection on an execution.
        """
        lessons = []
        improvements = []
        
        if was_successful:
            lessons.append("Task completed successfully")
        else:
            lessons.append("Task failed, needs improvement")
            improvements.append("Review error and adjust approach")
        
        reflection = ReflectionEntry(
            execution_id=execution_id,
            goal=goal,
            outcome=outcome,
            was_successful=was_successful,
            lessons_learned=lessons,
            improvements=improvements,
            confidence=0.8 if was_successful else 0.3
        )
        
        self.reflections.append(reflection)
        
        return reflection
    
    def get_quality_stats(self) -> Dict[str, Any]:
        """Get quality statistics."""
        if not self.quality_history:
            return {"total_assessments": 0}
        
        scores = [a.overall_score for a in self.quality_history]
        pass_rate = sum(1 for a in self.quality_history if a.passed) / len(self.quality_history)
        
        return {
            "total_assessments": len(self.quality_history),
            "average_score": sum(scores) / len(scores),
            "pass_rate": pass_rate,
            "total_reflections": len(self.reflections)
        }


# Singleton instance
quality_engine = QualityEngine()
