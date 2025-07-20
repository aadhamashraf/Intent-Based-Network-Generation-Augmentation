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
from .utilis_generator import generate_unique_id, random_choice, random_int, random_float, current_timestamp
from .Deployment_Intent_Generator import DeploymentIntentGenerator
from .Modification_Intent_Generator import ModificationIntentGenerator
from .Performance_Assurance_Intent_Generator import PerformanceAssuranceIntentGenerator
from .Report_Request_Intent_Generator import ReportRequestIntentGenerator
from .Feasibility_Check_Intent_Generator import FeasibilityCheckIntentGenerator
from .Notification_Request_Intent_Generator import NotificationRequestIntentGenerator

class Advanced3GPPIntentGenerator:
    """Main class for generating advanced 3GPP intent records."""
    
    def __init__(self, use_llm_synthesis: bool = True):
        self.use_llm_synthesis = use_llm_synthesis
        self.used_ids = set()
        self.intent_counter = 0
        self.research_session_id = f"RESEARCH_{int(time.time())}_{uuid.uuid4().hex[:12]}"
        self.llm_synthesizer = LLMDataSynthesizer()
        self.data_evaluator = DataEvaluator()
        
        # Intent generators
        self.generators = {
            IntentType.DEPLOYMENT: DeploymentIntentGenerator(),
            IntentType.MODIFICATION: ModificationIntentGenerator(),
            IntentType.PERFORMANCE_ASSURANCE: PerformanceAssuranceIntentGenerator(),
            IntentType.REPORT_REQUEST: ReportRequestIntentGenerator(),
            IntentType.FEASIBILITY_CHECK: FeasibilityCheckIntentGenerator(),
            IntentType.NOTIFICATION_REQUEST: NotificationRequestIntentGenerator()
        }
    
    def generate_metadata(self, intent_type: str) -> Dict[str, Any]:
        """Generate metadata for an intent record."""
        complexity = random_int(1, 10)
        
        return {
            "version": f"{random_int(1, 3)}.{random_int(0, 9)}.{random_int(0, 99)}",
            "standard": "3GPP_Release_17",
            "compliance": random.sample(COMPLIANCE_STANDARDS, 2),
            "research_context": random_choice(RESEARCH_CONTEXTS),
            "technical_complexity": complexity,
            "generation_timestamp": current_timestamp(),
            "generator_version": "2.0.0_Research_Edition",
            "data_classification": random_choice(['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED']),
            "quality_score": random_float(7.5, 10.0),
            "validation_status": random_choice(['VALIDATED', 'PENDING_VALIDATION', 'VALIDATION_FAILED']),
            "research_relevance": random_choice(['HIGH', 'MEDIUM', 'LOW']),
            "industry_vertical": random_choice(['TELECOMMUNICATIONS', 'AUTOMOTIVE', 'HEALTHCARE', 'MANUFACTURING', 'ENERGY', 'SMART_CITIES'])
        }
    
    def generate_intent(self) -> NetworkIntent:
        """Generate a single intent record."""
        intent_type = random_choice(list(IntentType))
        generator = self.generators[intent_type]
        
        # Generate base parameters
        parameters = generator.generate_parameters()
        
        # Apply LLM synthesis if enabled
        llm_metadata = None
        if self.use_llm_synthesis:
            synthesis_result = self.llm_synthesizer.synthesize_intent_data(
                intent_type.value, parameters
            )
            parameters = synthesis_result.synthesized_data
            llm_metadata = {
                "evaluation_score": synthesis_result.evaluation_score,
                "validation_results": [asdict(vr) for vr in synthesis_result.validation_results],
                "improvements": synthesis_result.improvements,
                "synthesized": True
            }
        
        # Generate description
        location = random_choice(ADVANCED_LOCATIONS)
        slice_type = random_choice(ADVANCED_SLICE_TYPES)
        description = generator.generate_description(parameters, location, slice_type)
        
        # Generate metadata
        metadata = self.generate_metadata(intent_type.value)
        
        return NetworkIntent(
            id=generate_unique_id(),
            intent_type=intent_type.value,
            description=description,
            timestamp=current_timestamp(),
            priority=random_choice(list(Priority)).value,
            network_slice=slice_type,
            location=location,
            parameters=parameters,
            metadata=metadata,
            llm_metadata=llm_metadata
        )
    
    def generate_batch(self, count: int, progress_callback=None) -> List[NetworkIntent]:
        """Generate a batch of intent records."""
        intents = []
        
        for i in range(count):
            intent = self.generate_intent()
            intents.append(intent)
            
            if progress_callback and i % 100 == 0:
                progress_callback(i, count)
            
            # Brief pause every 50 records for timestamp uniqueness
            if i % 50 == 0:
                time.sleep(0.001)
        
        return intents
    
    def evaluate_dataset(self, intents: List[NetworkIntent]) -> Dict[str, Any]:
        """Evaluate the generated dataset."""
        return self.data_evaluator.evaluate_batch(intents)
    
    def export_to_json(self, intents: List[NetworkIntent], filename: str):
        """Export intents to JSON file."""
        data = [asdict(intent) for intent in intents]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def export_to_csv(self, intents: List[NetworkIntent], filename: str):
        """Export intents to CSV file."""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'ID', 'Intent Type', 'Description', 'Timestamp', 'Priority',
                'Network Slice', 'Location', 'Technical Complexity',
                'Research Context', 'Compliance Standards', 'Parameters'
            ])
            
            # Write data
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
                    json.dumps(intent.parameters)
                ])
    
    def export_research_dataset(self, intents: List[NetworkIntent], filename: str, evaluation_results=None):
        """Export comprehensive research dataset."""
        research_data = {
            "metadata": {
                "generation_timestamp": current_timestamp(),
                "total_records": len(intents),
                "generator_version": "2.0.0_Research_Edition",
                "llm_synthesis_enabled": self.use_llm_synthesis,
                "dataset_purpose": "Advanced 3GPP Intent-Based Networking Research",
                "compliance_standards": ['3GPP_TS_28.312', '3GPP_TS_28.313', 'ETSI_NFV_SOL_001'],
                "quality_metrics": {
                    "average_complexity": sum(intent.metadata.get('technical_complexity', 0) for intent in intents) / len(intents),
                    "diversity_score": len(set(intent.intent_type for intent in intents)) / len(list(IntentType)),
                    "research_relevance": len([i for i in intents if i.metadata.get('research_relevance') == 'HIGH']) / len(intents),
                    "llm_enhanced_records": len([i for i in intents if i.llm_metadata and i.llm_metadata.get('synthesized')])
                },
                "evaluation_results": evaluation_results
            },
            "intents": [asdict(intent) for intent in intents],
            "statistics": {
                "research_session_id": self.research_session_id,
                "total_generated": len(intents),
                "intent_type_distribution": {
                    intent_type.value: len([i for i in intents if i.intent_type == intent_type.value])
                    for intent_type in IntentType
                }
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, indent=2, ensure_ascii=False)

