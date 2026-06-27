"""
Prompt Library Service

Version-controlled prompt template management.
"""

from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from dataclasses import dataclass
from enum import Enum
import logging
import re

logger = logging.getLogger(__name__)


class PromptCategory(Enum):
    """Prompt template categories."""
    SYSTEM = "system"
    TASK = "task"
    WORKFLOW = "workflow"
    QUALITY = "quality"
    AGENT = "agent"


@dataclass
class PromptVariable:
    """Definition of a prompt variable."""
    name: str
    description: str
    required: bool = True
    default: Optional[str] = None
    type: str = "string"  # string, number, boolean, json


@dataclass
class PromptTemplate:
    """Prompt template with versioning."""
    id: str
    name: str
    display_name: str
    description: str
    category: PromptCategory
    template: str
    system_prompt: Optional[str]
    variables: List[PromptVariable]
    tags: List[str]
    agent_types: List[str]
    task_types: List[str]
    version: int
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    is_system: bool = False
    avg_quality_score: float = 0.0
    usage_count: int = 0


class PromptLibrary:
    """
    Prompt Library for version-controlled prompt management.
    
    Features:
    - Template storage and retrieval
    - Variable interpolation
    - Version control
    - A/B testing support
    - Performance tracking
    """
    
    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self.templates_by_name: Dict[str, str] = {}  # name -> id
        self._initialized = False
    
    async def initialize(self):
        """Initialize prompt library."""
        if self._initialized:
            return
        
        await self._load_templates()
        await self._create_default_templates()
        self._initialized = True
        logger.info("Prompt Library initialized")
    
    async def _load_templates(self):
        """Load templates from database, falling back to defaults."""
        try:
            from app.db.session import SessionLocal
            from app.models.ai.prompt import PromptTemplate as PromptModel
            
            db = SessionLocal()
            try:
                db_templates = db.query(PromptModel).filter(
                    PromptModel.is_active == True
                ).all()
                
                for tmpl in db_templates:
                    try:
                        category = PromptCategory(tmpl.category) if hasattr(tmpl, 'category') else PromptCategory.SYSTEM
                    except ValueError:
                        category = PromptCategory.SYSTEM
                    
                    template = PromptTemplate(
                        id=str(tmpl.id),
                        name=tmpl.name,
                        display_name=tmpl.display_name,
                        description=tmpl.description or "",
                        category=category,
                        template=tmpl.template,
                        system_prompt=getattr(tmpl, 'system_prompt', None),
                        variables=[],  # Load from separate table if available
                        tags=getattr(tmpl, 'tags', []) or [],
                        agent_types=getattr(tmpl, 'agent_types', []) or [],
                        task_types=getattr(tmpl, 'task_types', []) or [],
                        version=getattr(tmpl, 'version', 1),
                        created_at=tmpl.created_at,
                        updated_at=tmpl.updated_at,
                        is_active=tmpl.is_active,
                        is_system=getattr(tmpl, 'is_system', False),
                    )
                    self.templates[template.id] = template
                    self.templates_by_name[template.name] = template.id
                
                if db_templates:
                    logger.info(f"Loaded {len(db_templates)} templates from database")
                    return
            finally:
                db.close()
        except Exception as e:
            logger.warning(f"Could not load templates from database: {e}")
        
        logger.info("No templates in database, will use defaults")
    
    async def _create_default_templates(self):
        """Create default system templates."""
        default_templates = [
            {
                "name": "system_assistant",
                "display_name": "System Assistant",
                "category": PromptCategory.SYSTEM,
                "template": "You are a helpful AI assistant for Social Farm AI OS.",
                "system_prompt": None,
                "variables": [],
                "agent_types": ["*"],
                "task_types": ["*"],
                "is_system": True
            },
            {
                "name": "content_creator",
                "display_name": "Content Creator",
                "category": PromptCategory.AGENT,
                "template": """You are a content creation expert for {{brand_name}}.

Brand Voice: {{brand_voice}}
Target Audience: {{target_audience}}
Platform: {{platform}}

Create engaging content that aligns with the brand guidelines.""",
                "system_prompt": "You are a creative content writer specializing in social media.",
                "variables": [
                    PromptVariable(name="brand_name", description="Brand name", required=True),
                    PromptVariable(name="brand_voice", description="Brand voice description", required=True),
                    PromptVariable(name="target_audience", description="Target audience", required=True),
                    PromptVariable(name="platform", description="Target platform", required=True),
                ],
                "agent_types": ["content", "script"],
                "task_types": ["content_creation", "script_writing"],
                "is_system": False
            },
            {
                "name": "trend_analyst",
                "display_name": "Trend Analyst",
                "category": PromptCategory.AGENT,
                "template": """Analyze the following trends for {{industry}} industry:

{{trends_data}}

Provide:
1. Key insights
2. Opportunities
3. Recommended actions
4. Risk assessment""",
                "system_prompt": "You are a trend analysis expert with deep industry knowledge.",
                "variables": [
                    PromptVariable(name="industry", description="Industry to analyze", required=True),
                    PromptVariable(name="trends_data", description="Raw trend data", required=True),
                ],
                "agent_types": ["trend", "research"],
                "task_types": ["trend_analysis", "market_research"],
                "is_system": False
            },
            {
                "name": "quality_reviewer",
                "display_name": "Quality Reviewer",
                "category": PromptCategory.QUALITY,
                "template": """Review the following content for quality:

Content: {{content}}
Brand Guidelines: {{brand_guidelines}}
Target Audience: {{target_audience}}

Evaluate:
1. Brand alignment (1-10)
2. Engagement potential (1-10)
3. Grammar and clarity (1-10)
4. SEO optimization (1-10)
5. Safety compliance (pass/fail)

Provide detailed feedback and overall score.""",
                "system_prompt": "You are a content quality reviewer with expertise in brand compliance.",
                "variables": [
                    PromptVariable(name="content", description="Content to review", required=True),
                    PromptVariable(name="brand_guidelines", description="Brand guidelines", required=False, default="No specific guidelines"),
                    PromptVariable(name="target_audience", description="Target audience", required=True),
                ],
                "agent_types": ["quality"],
                "task_types": ["quality_review", "content_review"],
                "is_system": False
            },
        ]
        
        import uuid
        for template_data in default_templates:
            if template_data["name"] not in self.templates_by_name:
                template_id = str(uuid.uuid4())
                template = PromptTemplate(
                    id=template_id,
                    name=template_data["name"],
                    display_name=template_data["display_name"],
                    description="",
                    category=template_data["category"],
                    template=template_data["template"],
                    system_prompt=template_data["system_prompt"],
                    variables=template_data["variables"],
                    tags=[],
                    agent_types=template_data["agent_types"],
                    task_types=template_data["task_types"],
                    version=1,
                    created_at=datetime.now(timezone.utc),
                    updated_at=datetime.now(timezone.utc),
                    is_system=template_data.get("is_system", False)
                )
                self.templates[template_id] = template
                self.templates_by_name[template_data["name"]] = template_id
    
    async def create_template(
        self,
        name: str,
        display_name: str,
        template: str,
        category: PromptCategory,
        system_prompt: Optional[str] = None,
        variables: Optional[List[PromptVariable]] = None,
        tags: Optional[List[str]] = None,
        agent_types: Optional[List[str]] = None,
        task_types: Optional[List[str]] = None,
        description: str = ""
    ) -> str:
        """Create a new prompt template."""
        import uuid
        
        template_id = str(uuid.uuid4())
        
        prompt_template = PromptTemplate(
            id=template_id,
            name=name,
            display_name=display_name,
            description=description,
            category=category,
            template=template,
            system_prompt=system_prompt,
            variables=variables or [],
            tags=tags or [],
            agent_types=agent_types or [],
            task_types=task_types or [],
            version=1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        
        self.templates[template_id] = prompt_template
        self.templates_by_name[name] = template_id
        
        logger.info(f"Created template: {name} ({template_id})")
        
        return template_id
    
    async def get_template(
        self,
        template_id: Optional[str] = None,
        name: Optional[str] = None
    ) -> Optional[PromptTemplate]:
        """Get a prompt template by ID or name."""
        if template_id:
            return self.templates.get(template_id)
        if name:
            template_id = self.templates_by_name.get(name)
            if template_id:
                return self.templates.get(template_id)
        return None
    
    async def render(
        self,
        template_id: str,
        variables: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Render a template with variables.
        
        Returns:
            Dict with 'prompt' and optionally 'system_prompt'
        """
        template = self.templates.get(template_id)
        if not template:
            raise ValueError(f"Template not found: {template_id}")
        
        # Validate required variables
        for var in template.variables:
            if var.required and var.name not in variables:
                if var.default is None:
                    raise ValueError(f"Missing required variable: {var.name}")
                variables[var.name] = var.default
        
        # Render template
        rendered_prompt = self._interpolate(template.template, variables)
        
        result = {"prompt": rendered_prompt}
        
        if template.system_prompt:
            result["system_prompt"] = self._interpolate(template.system_prompt, variables)
        
        # Update usage count
        template.usage_count += 1
        
        return result
    
    def _interpolate(self, template: str, variables: Dict[str, str]) -> str:
        """Interpolate variables in template."""
        def replace_var(match):
            var_name = match.group(1)
            return variables.get(var_name, match.group(0))
        
        return re.sub(r'\{\{(\w+)\}\}', replace_var, template)
    
    async def update_template(
        self,
        template_id: str,
        template: Optional[str] = None,
        system_prompt: Optional[str] = None,
        variables: Optional[List[PromptVariable]] = None,
        changelog: Optional[str] = None
    ) -> bool:
        """Update a template (creates new version)."""
        if template_id not in self.templates:
            return False
        
        existing = self.templates[template_id]
        
        # Create new version
        import uuid
        new_id = str(uuid.uuid4())
        
        new_template = PromptTemplate(
            id=new_id,
            name=existing.name,
            display_name=existing.display_name,
            description=existing.description,
            category=existing.category,
            template=template or existing.template,
            system_prompt=system_prompt if system_prompt is not None else existing.system_prompt,
            variables=variables or existing.variables,
            tags=existing.tags,
            agent_types=existing.agent_types,
            task_types=existing.task_types,
            version=existing.version + 1,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
            is_active=True,
            is_system=existing.is_system
        )
        
        # Deactivate old version
        existing.is_active = False
        
        # Store new version
        self.templates[new_id] = new_template
        self.templates_by_name[existing.name] = new_id
        
        logger.info(f"Updated template {existing.name} to version {new_template.version}")
        
        return True
    
    async def list_templates(
        self,
        category: Optional[PromptCategory] = None,
        agent_type: Optional[str] = None,
        task_type: Optional[str] = None,
        active_only: bool = True
    ) -> List[PromptTemplate]:
        """List templates with optional filters."""
        results = []
        
        for template in self.templates.values():
            if active_only and not template.is_active:
                continue
            if category and template.category != category:
                continue
            if agent_type and agent_type not in template.agent_types and "*" not in template.agent_types:
                continue
            if task_type and task_type not in template.task_types and "*" not in template.task_types:
                continue
            
            results.append(template)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """Get library statistics."""
        active_templates = sum(1 for t in self.templates.values() if t.is_active)
        total_usage = sum(t.usage_count for t in self.templates.values())
        
        return {
            "total_templates": len(self.templates),
            "active_templates": active_templates,
            "total_usage": total_usage,
            "by_category": {
                cat.value: sum(1 for t in self.templates.values() if t.category == cat)
                for cat in PromptCategory
            }
        }


# Singleton instance
prompt_library = PromptLibrary()
