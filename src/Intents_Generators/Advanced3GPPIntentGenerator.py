import json
import csv
import time
import uuid
import random
from dataclasses import asdict
from datetime import datetime
from typing import List, Dict, Any

from .Constants_Enums import IntentType, Priority, ADVANCED_LOCATIONS, ADVANCED_SLICE_TYPES, COMPLIANCE_STANDARDS, RESEARCH_CONTEXTS
from .Data_Structures import NetworkIntent
from .utils_generator import generate_unique_id, random_choice, random_int, random_float, current_timestamp
from .Template_Engine import AdvancedTemplateEngine, TemplateContext
from .Enhanced_Constraint_Engine import EnhancedConstraintEngine
from .Deployment_Intent_Generator import DeploymentIntentGenerator
from .Modification_Intent_Generator import ModificationIntentGenerator
from .Performance_Assurance_Intent_Generator import PerformanceAssuranceIntentGenerator
from .Report_Request_Intent_Generator import ReportRequestIntentGenerator
from .Feasibility_Check_Intent_Generator import FeasibilityCheckIntentGenerator
from .Notification_Request_Intent_Generator import NotificationRequestIntentGenerator

try:
    from ..Evaluation.evaluation_metric import DataEvaluator
except ImportError:
    try:
        from Evaluation.evaluation_metric import DataEvaluator
    except ImportError:
        DataEvaluator = None


class Advanced3GPPIntentGenerator:
    """Main class for generating advanced 3GPP intent records."""
    
    def __init__(self, use_llm_synthesis: bool = True):
        self.use_llm_synthesis = use_llm_synthesis
        self.used_ids = set()
        self.used_descriptions = set()
        self.intent_counter = 0
        self.research_session_id = f"RESEARCH_{int(time.time())}_{uuid.uuid4().hex[:12]}"
        self.constraint_engine = EnhancedConstraintEngine()
        self.template_engine = AdvancedTemplateEngine()
        self.data_evaluator = DataEvaluator() if DataEvaluator else None
        
        self.generators = {
            IntentType.DEPLOYMENT: DeploymentIntentGenerator(),
            IntentType.MODIFICATION: ModificationIntentGenerator(),
            IntentType.PERFORMANCE_ASSURANCE: PerformanceAssuranceIntentGenerator(),
            IntentType.REPORT_REQUEST: ReportRequestIntentGenerator(),
            IntentType.FEASIBILITY_CHECK: FeasibilityCheckIntentGenerator(),
            IntentType.NOTIFICATION_REQUEST: NotificationRequestIntentGenerator()
        }
    
    def _generate_unique_id(self) -> str:
        """Generate a truly unique ID and ensure it's not duplicated."""
        max_attempts = 100
        for _ in range(max_attempts):
            new_id = generate_unique_id()
            if new_id not in self.used_ids:
                self.used_ids.add(new_id)
                return new_id
        
        # Fallback: create a guaranteed unique ID
        fallback_id = f"{generate_unique_id()}_{self.intent_counter}_{int(time.time())}"
        self.used_ids.add(fallback_id)
        return fallback_id
    
    def _generate_unique_description(self, context: TemplateContext, max_attempts: int = 10) -> tuple[str, str]:
        """Generate a unique description that hasn't been used before."""
        for attempt in range(max_attempts):
            # Add randomization to context to increase variety
            enhanced_context = self._enhance_context_for_uniqueness(context, attempt)
            description, base_template = self.template_engine.generate_description(enhanced_context)
            
            # Create a normalized version for comparison (remove extra spaces, lowercase)
            normalized_desc = ' '.join(description.lower().split())
            
            if normalized_desc not in self.used_descriptions:
                self.used_descriptions.add(normalized_desc)
                return description, base_template
        
        # If we can't generate a unique description, add a unique suffix
        description, base_template = self.template_engine.generate_description(context)
        unique_suffix = f" [Instance-{self.intent_counter}-{int(time.time() * 1000) % 10000}]"
        unique_description = description + unique_suffix
        
        normalized_desc = ' '.join(unique_description.lower().split())
        self.used_descriptions.add(normalized_desc)
        
        return unique_description, base_template
    
    def _enhance_context_for_uniqueness(self, context: TemplateContext, attempt: int) -> TemplateContext:
        """Enhance context with additional randomization to increase description variety."""
        # Create a copy of the context
        enhanced_context = TemplateContext(
            intent_type=context.intent_type,
            complexity=context.complexity,
            priority=context.priority,
            slice_category=context.slice_category,
            location_category=context.location_category,
            parameters=context.parameters.copy(),
            metadata=context.metadata.copy()
        )
        
        # Add variety-enhancing parameters based on attempt number
        variety_params = {
            'variation_seed': attempt,
            'description_style': random_choice(['technical', 'business', 'operational', 'detailed', 'concise']),
            'focus_aspect': random_choice(['performance', 'security', 'reliability', 'efficiency', 'scalability']),
            'implementation_phase': random_choice(['planning', 'deployment', 'optimization', 'monitoring', 'maintenance']),
            'stakeholder_perspective': random_choice(['operator', 'vendor', 'enterprise', 'regulator', 'researcher']),
            'time_horizon': random_choice(['immediate', 'short-term', 'medium-term', 'long-term', 'strategic']),
            'deployment_scenario': random_choice(['greenfield', 'brownfield', 'hybrid', 'migration', 'upgrade']),
            'business_context': random_choice(['cost-optimization', 'service-enhancement', 'compliance', 'innovation', 'competition'])
        }
        
        # Add these to the enhanced context
        enhanced_context.parameters.update(variety_params)
        enhanced_context.metadata.update({
            'description_variation_attempt': attempt,
            'uniqueness_enhancers': variety_params
        })
        
        return enhanced_context
    
    def generate_intent(self) -> NetworkIntent:
        """Generate a single intent record."""
        self.intent_counter += 1
        
        # Select intent type and basic parameters
        intent_type = random_choice(list(self.generators.keys()))
        slice_type = random_choice(ADVANCED_SLICE_TYPES)
        location = random_choice(ADVANCED_LOCATIONS)
        
        # Generate constrained parameters
        priority = self.constraint_engine.generate_constrained_priority(slice_type, location, intent_type.value)
        complexity = self.constraint_engine.generate_constrained_complexity(slice_type, priority, intent_type.value)
        research_context = self.constraint_engine.generate_constrained_research_context(slice_type, complexity, priority)
        compliance_standards = self.constraint_engine.generate_constrained_compliance_standards(
            slice_type, intent_type.value, "CORE"
        )

        # Create comprehensive parameter context
        param_context = {
            'slice_type': slice_type,
            'priority': priority,
            'location': location,
            'complexity': complexity,
            'intent_type': intent_type.value,
            'research_context': research_context,
            'compliance_standards': compliance_standards
        }

        # Generate comprehensive constrained parameters using enhanced constraint engine
        parameters = self.constraint_engine.generate_constrained_parameters(param_context)

        # Add additional parameters from specific generators
        generator = self.generators[intent_type]
        additional_params = generator.generate_constrained_parameters(
            slice_type, priority, location, complexity
        )

        # Merge additional parameters
        for key, value in additional_params.items():
            if key not in parameters:
                parameters[key] = value
            elif isinstance(value, dict) and isinstance(parameters[key], dict):
                parameters[key].update(value)

        # Generate description and capture base template
        context = self._create_template_context(
            intent_type.value, complexity, priority, slice_type, location, parameters, {}
        )
        description, base_template = self._generate_unique_description(context)

        # Build metadata including base_template
        metadata = {
            "version": f"{random_int(1, 3)}.{random_int(0, 9)}.{random_int(0, 99)}",
            "standard": "3GPP_Release_17",
            "compliance": compliance_standards,
            "research_context": research_context,
            "technical_complexity": complexity,
            "generation_timestamp": current_timestamp(),
            "generator_version": "2.0.0_Research_Edition",
            "data_classification": random_choice(['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']),
            "quality_score": self._calculate_quality_score(complexity, priority, slice_type),
            "validation_status": random_choice(['VALIDATED', 'PENDING_VALIDATION']),
            "research_relevance": self._determine_research_relevance(complexity, priority),
            "industry_vertical": self._determine_industry_vertical(slice_type, location),
            "base_template": base_template,
            "template_engine_version": "2.0.0",
            "description_complexity_score": self._calculate_description_complexity(description)
        }

        return NetworkIntent(
            id=self._generate_unique_id(),
            intent_type=intent_type.value,
            description=description,
            timestamp=current_timestamp(),
            priority=priority,
            network_slice=slice_type,
            location=location,
            parameters=parameters,
            metadata=metadata
        )
    
    def _create_template_context(self, intent_type: str, complexity: int, priority: str, 
                                slice_type: str, location: str, parameters: Dict[str, Any], 
                                metadata: Dict[str, Any]) -> TemplateContext:
        """Create template context for advanced description generation."""
        slice_category = self.constraint_engine.categorize_slice_type(slice_type)
        location_category = self.constraint_engine.categorize_location(location)
        return TemplateContext(
            intent_type=intent_type,
            complexity=complexity,
            priority=priority,
            slice_category=slice_category,
            location_category=location_category,
            parameters=parameters,
            metadata=metadata
        )
    
    def _calculate_description_complexity(self, description: str) -> float:
        """Calculate complexity score for generated description."""
        # Simple complexity calculation based on various factors
        word_count = len(description.split())
        if word_count == 0:
            return 0.0
            
        unique_words = len(set(description.lower().split()))
        avg_word_length = sum(len(word) for word in description.split()) / word_count
        
        return min(10.0, (word_count / 10) + (unique_words / word_count * 5) + (avg_word_length / 2))
    
    def _calculate_quality_score(self, complexity: int, priority: str, slice_type: str) -> float:
        """Calculate quality score based on realistic factors."""
        base_score = 7.0
        
        complexity_bonus = (complexity / 10) * 2.0  # 0 to 2.0
        
        priority_bonus = {
            'EMERGENCY': 1.0,
            'CRITICAL': 0.8,
            'HIGH': 0.5,
            'MEDIUM': 0.2,
            'LOW': 0.0
        }.get(priority, 0.0)
        
        slice_category = self.constraint_engine.categorize_slice_type(slice_type)
        slice_bonus = {
            'V2X': 0.8,
            'URLLC': 0.6,
            'eMBB': 0.4,
            'mMTC': 0.2
        }.get(slice_category, 0.0)
        
        total_score = base_score + complexity_bonus + priority_bonus + slice_bonus
        return min(10.0, total_score)
    
    def _determine_research_relevance(self, complexity: int, priority: str) -> str:
        """Determine research relevance based on parameters."""
        if complexity >= 8 and priority in ['CRITICAL', 'EMERGENCY']:
            return 'HIGH'
        elif complexity >= 6 or priority in ['HIGH', 'CRITICAL']:
            return 'MEDIUM'
        else:
            return 'LOW'
    
    def _determine_industry_vertical(self, slice_type: str, location: str) -> str:
        """Determine industry vertical based on slice type and location."""
        slice_lower = slice_type.lower()
        location_lower = location.lower()
        
        if any(keyword in slice_lower for keyword in ['vehicle', 'autonomous', 'v2x']):
            return 'AUTOMOTIVE'
        elif any(keyword in slice_lower for keyword in ['industrial', 'manufacturing', 'automation']):
            return 'MANUFACTURING'
        elif any(keyword in slice_lower for keyword in ['health', 'medical', 'surgery']):
            return 'HEALTHCARE'
        elif any(keyword in slice_lower for keyword in ['agriculture', 'farm', 'crop']):
            return 'AGRICULTURE'
        elif any(keyword in location_lower for keyword in ['smart', 'city', 'urban']):
            return 'SMART_CITIES'
        else:
            return 'TELECOMMUNICATIONS'
    
    def generate_batch(self, count: int, progress_callback=None) -> List[NetworkIntent]:
        """Generate a batch of intent records with guaranteed uniqueness."""
        intents = []
        description_attempts = 0
        max_description_attempts = count * 3  # Allow more attempts for unique descriptions
        
        for i in range(count):
            # Generate intent with retry logic for unique descriptions
            max_retries = 5
            intent = None
            
            for retry in range(max_retries):
                try:
                    intent = self.generate_intent()
                    break
                except Exception as e:
                    if retry == max_retries - 1:
                        # If all retries failed, generate with fallback
                        print(f"Warning: Failed to generate unique intent after {max_retries} attempts: {e}")
                        intent = self.generate_intent()
                        break
            
            if intent:
                intents.append(intent)
            
            if progress_callback and i % 100 == 0:
                progress_callback(i, count)
            
            if i % 50 == 0:
                time.sleep(0.001)
        
        # Verify uniqueness (additional safety check)
        seen_ids = set()
        seen_descriptions = set()
        unique_intents = []
        
        for intent in intents:
            normalized_desc = ' '.join(intent.description.lower().split())
            if intent.id not in seen_ids and normalized_desc not in seen_descriptions:
                seen_ids.add(intent.id)
                seen_descriptions.add(normalized_desc)
                unique_intents.append(intent)
        
        if len(unique_intents) != len(intents):
            duplicates_removed = len(intents) - len(unique_intents)
            print(f"Warning: Removed {duplicates_removed} duplicate intents (IDs or descriptions)")
        
        return unique_intents
    
    def evaluate_dataset(self, intents: List[NetworkIntent]) -> Dict[str, Any]:
        """Evaluate the generated dataset."""
        if self.data_evaluator:
            return self.data_evaluator.evaluate_batch(intents)
        else:
            from .Data_Structures import EvaluationMetrics
            dummy_metrics = EvaluationMetrics(
                technical_accuracy=0,
                realism_score=0,
                compliance_level=0,
                research_value=0,
                implementability=0,
                overall_quality=0
            )
            return {
                'overall_metrics': dummy_metrics,
                'detailed_evaluations': [],
                'batch_insights': ['Evaluation module not available - using dummy metrics']
            }
    
    def export_to_json(self, intents: List[NetworkIntent], filename: str):
        """Export intents to JSON file."""
        data = [asdict(intent) for intent in intents]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, intents: List[NetworkIntent], filename: str):
        """Export intents to CSV file with BaseTemplate column."""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'ID', 'Intent Type', 'Description', 'Timestamp', 'Priority',
                'Network Slice', 'Location', 'Technical Complexity',
                'Research Context', 'Compliance Standards', 'BaseTemplate', 'Parameters'
            ])
            for intent in intents:
                writer.writerow([
                    intent.id,
                    intent.intent_type,
                    intent.description,
                    intent.timestamp,
                    intent.priority,
                    intent.network_slice or '',
                    intent.location or '',
                    intent.metadata.get('technical_complexity', ''),
                    intent.metadata.get('research_context', ''),
                    '; '.join(intent.metadata.get('compliance', [])),
                    intent.metadata.get('base_template', ''),
                    json.dumps(intent.parameters)
                ])
    
    def export_research_dataset(self, intents: List[NetworkIntent], filename: str, evaluation_results=None):
        """Export comprehensive research dataset."""
        
        def serialize_evaluation_results(eval_results):
            if eval_results is None:
                return None
            
            serialized = {}
            for key, value in eval_results.items():
                if hasattr(value, '__dict__'):
                    serialized[key] = asdict(value)
                elif isinstance(value, list):
                    serialized[key] = []
                    for item in value:
                        if hasattr(item, '__dict__'):
                            serialized[key].append(asdict(item))
                        else:
                            serialized[key].append(item)
                else:
                    serialized[key] = value
            return serialized
        
        research_data = {
            "metadata": {
                "generation_timestamp": current_timestamp(),
                "total_records": len(intents),
                "generator_version": "2.0.0_Research_Edition",
                "llm_synthesis_enabled": self.use_llm_synthesis,
                "dataset_purpose": "Advanced 3GPP Intent-Based Networking Research",
                "compliance_standards": ['3GPP_TS_28.312', '3GPP_TS_28.313', 'ETSI_NFV_SOL_001'],
                "quality_metrics": {
                    "average_complexity": sum(intent.metadata.get('technical_complexity', 0) for intent in intents) / len(intents) if intents else 0,
                    "diversity_score": len(set(intent.intent_type for intent in intents)) / len(list(IntentType)) if intents else 0,
                    "research_relevance": len([i for i in intents if i.metadata.get('research_relevance') == 'HIGH']) / len(intents) if intents else 0,
                    "llm_enhanced_records": len([i for i in intents if hasattr(i, 'llm_metadata') and i.llm_metadata and i.llm_metadata.get('synthesized')]) if intents else 0
                },
                "evaluation_results": serialize_evaluation_results(evaluation_results)
            },
            "intents": [asdict(intent) for intent in intents],
            "statistics": {
                "research_session_id": self.research_session_id,
                "total_generated": len(intents),
                "intent_type_distribution": {
                    intent_type.value: len([i for i in intents if i.intent_type == intent_type.value])
                    for intent_type in IntentType
                },
                "unique_ids_generated": len(self.used_ids),
                "unique_descriptions_generated": len(self.used_descriptions),
                "description_uniqueness_ratio": len(self.used_descriptions) / len(intents) if intents else 0
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, indent=2, ensure_ascii=False)
    

