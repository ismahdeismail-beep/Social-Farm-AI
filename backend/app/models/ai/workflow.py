"""
AI Workflow Models

Defines workflows and workflow steps for the AI Orchestrator.
"""

from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Integer, Float, JSON as JSONType
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.models import Base, TimestampMixin, SoftDeleteMixin


class Workflow(Base, TimestampMixin, SoftDeleteMixin):
    """
    Represents a complex multi-step AI workflow.
    
    Workflows contain tasks that can be executed sequentially, in parallel,
    or with conditional branching.
    """
    __tablename__ = 'ai_workflows'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Definition
    name = Column(String(255), nullable=False)
    description = Column(Text)
    workflow_type = Column(String(100), nullable=False)  # campaign, content, research, analysis
    version = Column(Integer, default=1)
    
    # Template
    is_template = Column(Boolean, default=False)
    template_id = Column(UUID(as_uuid=True), ForeignKey('ai_workflows.id'))
    
    # Ownership
    created_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    organization_id = Column(UUID(as_uuid=True), ForeignKey('organizations.id'))
    workspace_id = Column(UUID(as_uuid=True), ForeignKey('workspaces.id'))
    
    # Execution
    status = Column(String(50), default='draft')  # draft, active, running, completed, failed, cancelled
    trigger_type = Column(String(50))  # manual, api, schedule, event
    trigger_config = Column(JSONType, default=dict)
    
    # Configuration
    config = Column(JSONType, default=dict)
    variables = Column(JSONType, default=dict)  # Dynamic variables for workflow
    
    # Scheduling
    scheduled_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    timeout_seconds = Column(Integer, default=3600)  # 1 hour default
    
    # Metrics
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)
    total_cost_usd = Column(Float, default=0.0)
    total_tokens = Column(Integer, default=0)
    
    # Relationships
    tasks = relationship('AgentTask', back_populates='workflow')
    steps = relationship('WorkflowStep', back_populates='workflow', cascade='all, delete-orphan')
    executions = relationship('WorkflowExecution', back_populates='workflow')
    parent_workflow = relationship('Workflow', remote_side=[id], backref='child_workflows')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'workflow_type': self.workflow_type,
            'version': self.version,
            'is_template': self.is_template,
            'template_id': self.template_id,
            'created_by': self.created_by,
            'organization_id': self.organization_id,
            'workspace_id': self.workspace_id,
            'status': self.status,
            'trigger_type': self.trigger_type,
            'trigger_config': self.trigger_config,
            'config': self.config,
            'variables': self.variables,
            'scheduled_at': self.scheduled_at,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'timeout_seconds': self.timeout_seconds,
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'total_cost_usd': self.total_cost_usd,
            'total_tokens': self.total_tokens,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'deleted_at': self.deleted_at
        }


class WorkflowStep(Base, TimestampMixin):
    """
    Defines a step in a workflow template.
    
    Steps define the structure of a workflow before execution.
    """
    __tablename__ = 'ai_workflow_steps'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('ai_workflows.id'), nullable=False)
    
    # Step definition
    name = Column(String(255), nullable=False)
    step_type = Column(String(50), nullable=False)  # task, parallel, conditional, approval
    description = Column(Text)
    sort_order = Column(Integer, default=0)
    
    # Task configuration (for task-type steps)
    task_type = Column(String(100))
    agent_type = Column(String(100))
    model_preference = Column(JSONType, default=list)
    prompt_template_id = Column(UUID(as_uuid=True), ForeignKey('ai_prompt_templates.id'))
    
    # Input/Output mapping
    input_mapping = Column(JSONType, default=dict)  # Maps workflow variables to task inputs
    output_mapping = Column(JSONType, default=dict)  # Maps task outputs to workflow variables
    
    # Conditions (for conditional steps)
    condition_expression = Column(JSONType)
    
    # Dependencies
    depends_on_steps = Column(JSONType, default=list)  # Step IDs this step depends on
    
    # Configuration
    config = Column(JSONType, default=dict)
    timeout_seconds = Column(Integer, default=300)
    retry_config = Column(JSONType, default={'max_retries': 3, 'backoff': 'exponential'})
    
    # Relationships
    workflow = relationship('Workflow', back_populates='steps')
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'name': self.name,
            'step_type': self.step_type,
            'description': self.description,
            'sort_order': self.sort_order,
            'task_type': self.task_type,
            'agent_type': self.agent_type,
            'model_preference': self.model_preference,
            'prompt_template_id': self.prompt_template_id,
            'input_mapping': self.input_mapping,
            'output_mapping': self.output_mapping,
            'condition_expression': self.condition_expression,
            'depends_on_steps': self.depends_on_steps,
            'config': self.config,
            'timeout_seconds': self.timeout_seconds,
            'retry_config': self.retry_config,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class WorkflowExecution(Base, TimestampMixin):
    """
    Tracks execution instances of a workflow.
    """
    __tablename__ = 'ai_workflow_executions'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workflow_id = Column(UUID(as_uuid=True), ForeignKey('ai_workflows.id'), nullable=False)
    
    # Execution
    status = Column(String(50), default='pending')  # pending, running, completed, failed, cancelled
    trigger_type = Column(String(50))  # manual, api, schedule, event
    triggered_by = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    
    # Context
    input_variables = Column(JSONType, default=dict)
    output_variables = Column(JSONType, default=dict)
    
    # Timing
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    duration_ms = Column(Float)
    
    # Metrics
    total_tasks = Column(Integer, default=0)
    completed_tasks = Column(Integer, default=0)
    failed_tasks = Column(Integer, default=0)
    total_cost_usd = Column(Float, default=0.0)
    total_tokens = Column(Integer, default=0)
    
    # Error
    error_message = Column(Text)
    error_details = Column(JSONType)
    
    # Relationships
    workflow = relationship('Workflow', back_populates='executions')
    
    def to_dict(self):
        return {
            'id': self.id,
            'workflow_id': self.workflow_id,
            'status': self.status,
            'trigger_type': self.trigger_type,
            'triggered_by': self.triggered_by,
            'input_variables': self.input_variables,
            'output_variables': self.output_variables,
            'started_at': self.started_at,
            'completed_at': self.completed_at,
            'duration_ms': self.duration_ms,
            'total_tasks': self.total_tasks,
            'completed_tasks': self.completed_tasks,
            'failed_tasks': self.failed_tasks,
            'total_cost_usd': self.total_cost_usd,
            'total_tokens': self.total_tokens,
            'error_message': self.error_message,
            'error_details': self.error_details,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
