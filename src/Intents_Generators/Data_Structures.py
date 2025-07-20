import uuid
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional, List

@dataclass
class NetworkIntent:
    """Represents a complete 3GPP network intent record."""
    id: str
    intent_type: str
    description: str
    timestamp: str
    priority: str
    network_slice: Optional[str]
    location: Optional[str]
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]
    llm_metadata: Optional[Dict[str, Any]] = None

@dataclass
class EvaluationMetrics:
    """Metrics for evaluating intent quality."""
    technical_accuracy: float
    realism_score: float
    compliance_level: float
    research_value: float
    implementability: float
    overall_quality: float

@dataclass
class ValidationResult:
    """Result of a validation check."""
    criterion: str
    score: float
    feedback: str
    passed: bool

@dataclass
class SynthesisResult:
    """Result of LLM synthesis."""
    synthesized_data: Dict[str, Any]
    evaluation_score: float
    validation_results: List[ValidationResult]
    improvements: List[str]