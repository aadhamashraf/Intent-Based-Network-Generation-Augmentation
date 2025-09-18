import uuid
import random
from datetime import datetime, timedelta
from typing import Dict, Any
from .Parameter_Generator import ParameterGenerator
from .utilis_generator import current_timestamp, generate_unique_id, random_choice, random_int, random_float

from .BaseIntentGenerator import BaseIntentGenerator

class FeasibilityCheckIntentGenerator(BaseIntentGenerator):
    """Generator for feasibility check intent records."""
    def __init__(self, constraint_engine=None):
        super().__init__(constraint_engine)
    
    def generate_constrained_parameters(self, slice_type: str, priority: str, location: str, complexity: int) -> Dict[str, Any]:
        """Generate feasibility check parameters with realistic constraints."""
        constraint_engine = self.constraint_engine
        base_params = self.generate_base_params('FEASIBILITY_CHECK', {
            'slice_type': slice_type,
            'priority': priority,
            'location': location,
            'complexity': complexity
        })
        
        # Apply constraints based on context
        slice_category = constraint_engine.categorize_slice_type(slice_type)
        location_category = constraint_engine.categorize_location(location)
        
        # Adjust assessment scope based on complexity
        if complexity >= 8:
            base_params["feasibility_assessment"]["assessment_scope"] = "COMPREHENSIVE"
            base_params["feasibility_assessment"]["assessment_criteria"]["technical_feasibility"]["technology_maturity"]["implementation_readiness"] = random_choice(['PRODUCTION_READY', 'BETA'])
        elif complexity >= 5:
            base_params["feasibility_assessment"]["assessment_scope"] = random_choice(['COMPREHENSIVE', 'TECHNICAL_ONLY'])
            base_params["feasibility_assessment"]["assessment_criteria"]["technical_feasibility"]["technology_maturity"]["implementation_readiness"] = random_choice(['PRODUCTION_READY', 'BETA', 'ALPHA'])
        else:
            base_params["feasibility_assessment"]["assessment_scope"] = random_choice(['TECHNICAL_ONLY', 'ECONOMIC_ONLY'])
            base_params["feasibility_assessment"]["assessment_criteria"]["technical_feasibility"]["technology_maturity"]["implementation_readiness"] = random_choice(['PRODUCTION_READY', 'BETA', 'ALPHA', 'PROTOTYPE'])
        
        # Adjust resource availability based on slice category
        if slice_category in ['URLLC', 'V2X']:
            # Critical slices need higher resource availability
            base_params["feasibility_assessment"]["assessment_criteria"]["technical_feasibility"]["resource_availability"]["compute_resources"] = f"{random_int(80, 95)}%_available"
            base_params["feasibility_assessment"]["assessment_criteria"]["technical_feasibility"]["resource_availability"]["network_resources"] = f"{random_int(85, 95)}%_available"
        elif slice_category == 'eMBB':
            base_params["feasibility_assessment"]["assessment_criteria"]["technical_feasibility"]["resource_availability"]["compute_resources"] = f"{random_int(70, 90)}%_available"
            base_params["feasibility_assessment"]["assessment_criteria"]["technical_feasibility"]["resource_availability"]["network_resources"] = f"{random_int(75, 90)}%_available"
        else:  # mMTC
            base_params["feasibility_assessment"]["assessment_criteria"]["technical_feasibility"]["resource_availability"]["compute_resources"] = f"{random_int(60, 85)}%_available"
            base_params["feasibility_assessment"]["assessment_criteria"]["technical_feasibility"]["resource_availability"]["network_resources"] = f"{random_int(70, 85)}%_available"
        
        # Adjust economic feasibility based on priority
        if priority in ['CRITICAL', 'EMERGENCY']:
            # Higher budget allocation for critical services
            base_params["feasibility_assessment"]["assessment_criteria"]["economic_feasibility"]["cost_analysis"]["capital_expenditure"] = f"{random_int(100000, 10000000)}_USD"
            base_params["feasibility_assessment"]["assessment_criteria"]["economic_feasibility"]["budget_constraints"]["approval_required"] = random_choice(['TECHNICAL', 'FINANCIAL', 'EXECUTIVE'])
        elif priority == 'HIGH':
            base_params["feasibility_assessment"]["assessment_criteria"]["economic_feasibility"]["cost_analysis"]["capital_expenditure"] = f"{random_int(50000, 5000000)}_USD"
            base_params["feasibility_assessment"]["assessment_criteria"]["economic_feasibility"]["budget_constraints"]["approval_required"] = random_choice(['TECHNICAL', 'FINANCIAL'])
        else:
            base_params["feasibility_assessment"]["assessment_criteria"]["economic_feasibility"]["cost_analysis"]["capital_expenditure"] = f"{random_int(10000, 1000000)}_USD"
            base_params["feasibility_assessment"]["assessment_criteria"]["economic_feasibility"]["budget_constraints"]["approval_required"] = random_choice(['NONE', 'TECHNICAL'])
        
        # Adjust recommendation based on overall feasibility
        feasibility_factors = []
        if slice_category in ['URLLC', 'V2X'] and priority in ['CRITICAL', 'EMERGENCY']:
            feasibility_factors.append(0.9)  # High feasibility for critical URLLC/V2X
        elif complexity <= 5:
            feasibility_factors.append(0.8)  # Lower complexity is more feasible
        else:
            feasibility_factors.append(0.6)  # Default moderate feasibility
        
        avg_feasibility = sum(feasibility_factors) / len(feasibility_factors) * 100
        base_params["recommendation_engine"]["feasibility_score"] = avg_feasibility
        
        if avg_feasibility >= 80:
            base_params["recommendation_engine"]["recommendation"] = "PROCEED"
        elif avg_feasibility >= 60:
            base_params["recommendation_engine"]["recommendation"] = "PROCEED_WITH_CONDITIONS"
        elif avg_feasibility >= 40:
            base_params["recommendation_engine"]["recommendation"] = "DEFER"
        else:
            base_params["recommendation_engine"]["recommendation"] = "REJECT"
        
        return base_params
    
    def generate_parameters(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate feasibility check-specific parameters."""
        base_params = self.generate_base_params('FEASIBILITY_CHECK', context or {})
        
        # Add feasibility check-specific parameters
        feasibility_params = {
            "feasibility_assessment": {
                "assessment_scope": random_choice(['TECHNICAL_ONLY', 'ECONOMIC_ONLY', 'OPERATIONAL_ONLY', 'COMPREHENSIVE']),
                "assessment_criteria": {
                    "technical_feasibility": {
                        "resource_availability": {
                            "compute_resources": f"{random_int(60, 95)}%_available",
                            "network_resources": f"{random_int(70, 90)}%_available",
                            "storage_resources": f"{random_int(50, 85)}%_available"
                        },
                        "technology_maturity": {
                            "standards_compliance": random_choice(['FULL', 'PARTIAL', 'MINIMAL', 'NON_COMPLIANT']),
                            "implementation_readiness": random_choice(['PRODUCTION_READY', 'BETA', 'ALPHA', 'PROTOTYPE']),
                            "vendor_support": random_choice(['FULL_SUPPORT', 'LIMITED_SUPPORT', 'COMMUNITY_SUPPORT', 'NO_SUPPORT'])
                        },
                        "integration_complexity": {
                            "interface_compatibility": random_choice(['NATIVE', 'ADAPTER_REQUIRED', 'CUSTOM_INTEGRATION', 'NOT_COMPATIBLE']),
                            "data_format_alignment": random_choice(['PERFECT_MATCH', 'MINOR_TRANSFORMATION', 'MAJOR_TRANSFORMATION', 'INCOMPATIBLE']),
                            "protocol_support": random_choice(['NATIVE_SUPPORT', 'GATEWAY_REQUIRED', 'PROTOCOL_TRANSLATION', 'NOT_SUPPORTED'])
                        }
                    },
                    "economic_feasibility": {
                        "cost_analysis": {
                            "capital_expenditure": f"{random_int(10000, 10000000)}_USD",
                            "operational_expenditure": f"{random_int(1000, 100000)}_USD_per_month",
                            "total_cost_of_ownership": f"{random_int(50000, 50000000)}_USD_over_5_years",
                            "return_on_investment": f"{random_float(5, 50)}%_over_3_years"
                        },
                        "budget_constraints": {
                            "available_budget": f"{random_int(100000, 5000000)}_USD",
                            "budget_utilization": f"{random_float(60, 95)}%",
                            "funding_source": random_choice(['CAPEX', 'OPEX', 'MIXED', 'EXTERNAL_FUNDING']),
                            "approval_required": random_choice(['NONE', 'TECHNICAL', 'FINANCIAL', 'EXECUTIVE'])
                        },
                        "business_case": {
                            "revenue_impact": f"{random_int(-1000000, 5000000)}_USD_annually",
                            "cost_savings": f"{random_int(0, 2000000)}_USD_annually",
                            "risk_mitigation": f"{random_int(100000, 1000000)}_USD_risk_reduction",
                            "competitive_advantage": random_choice(['SIGNIFICANT', 'MODERATE', 'MINIMAL', 'NONE'])
                        }
                    },
                    "operational_feasibility": {
                        "skills_availability": {
                            "required_skills": [
                                random_choice(['5G_CORE', 'NETWORK_SLICING', 'EDGE_COMPUTING', 'AI_ML', 'SECURITY']),
                                random_choice(['ORCHESTRATION', 'AUTOMATION', 'DEVOPS', 'CLOUD_NATIVE', 'MICROSERVICES'])
                            ],
                            "current_capability": random_choice(['EXPERT', 'ADVANCED', 'INTERMEDIATE', 'BASIC', 'NONE']),
                            "training_required": f"{random_int(0, 200)}_hours",
                            "external_support": random_choice(['NOT_REQUIRED', 'CONSULTING', 'MANAGED_SERVICE', 'FULL_OUTSOURCING'])
                        },
                        "process_alignment": {
                            "current_process_maturity": random_choice(['OPTIMIZED', 'MANAGED', 'DEFINED', 'REPEATABLE', 'INITIAL']),
                            "process_changes_required": random_choice(['NONE', 'MINOR', 'MODERATE', 'MAJOR', 'COMPLETE_OVERHAUL']),
                            "change_management_effort": random_choice(['LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']),
                            "stakeholder_buy_in": random_choice(['FULL_SUPPORT', 'MAJORITY_SUPPORT', 'MIXED', 'RESISTANCE'])
                        },
                        "time_constraints": {
                            "required_delivery": (datetime.now() + timedelta(days=random_int(30, 365))).isoformat(),
                            "estimated_duration": f"{random_int(30, 730)}_days",
                            "critical_path": f"{random_int(20, 500)}_days",
                            "buffer_time": f"{random_int(5, 90)}_days"
                        }
                    }
                }
            },
            "risk_analysis": {
                "risk_categories": {
                    "technical_risks": [
                        {
                            "risk_id": f"TECH_RISK_{uuid.uuid4().hex[:8]}",
                            "description": 'Technology integration complexity higher than expected',
                            "probability": random_choice(['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']),
                            "impact": random_choice(['NEGLIGIBLE', 'MINOR', 'MODERATE', 'MAJOR', 'CATASTROPHIC']),
                            "mitigation_strategy": 'Proof of concept and phased implementation approach'
                        }
                    ],
                    "business_risks": [
                        {
                            "risk_id": f"BUS_RISK_{uuid.uuid4().hex[:8]}",
                            "description": 'Market conditions change affecting business case',
                            "probability": random_choice(['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']),
                            "impact": random_choice(['NEGLIGIBLE', 'MINOR', 'MODERATE', 'MAJOR', 'CATASTROPHIC']),
                            "mitigation_strategy": 'Regular market analysis and flexible implementation timeline'
                        }
                    ],
                    "operational_risks": [
                        {
                            "risk_id": f"OPS_RISK_{uuid.uuid4().hex[:8]}",
                            "description": 'Insufficient operational expertise for new technology',
                            "probability": random_choice(['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']),
                            "impact": random_choice(['NEGLIGIBLE', 'MINOR', 'MODERATE', 'MAJOR', 'CATASTROPHIC']),
                            "mitigation_strategy": 'Comprehensive training program and vendor support'
                        }
                    ]
                },
                "overall_risk_score": random_float(1, 10),
                "risk_tolerance": random_choice(['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']),
                "risk_mitigation_plan": {
                    "contingency_budget": f"{random_int(50000, 500000)}_USD",
                    "alternative_approaches": random_int(1, 5),
                    "rollback_plan": random_choice(['AVAILABLE', 'PARTIAL', 'NOT_AVAILABLE']),
                    "monitoring_plan": 'Weekly risk assessment and mitigation review'
                }
            },
            "recommendation_engine": {
                "feasibility_score": random_float(0, 100),
                "recommendation": random_choice(['PROCEED', 'PROCEED_WITH_CONDITIONS', 'DEFER', 'REJECT']),
                "confidence_level": random_float(60, 95),
                "alternative_options": [
                    {
                        "option_id": f"ALT_{uuid.uuid4().hex[:8]}",
                        "description": 'Phased implementation approach with reduced scope',
                        "feasibility_score": random_float(70, 90),
                        "estimated_cost": f"{random_int(50000, 500000)}_USD",
                        "estimated_duration": f"{random_int(60, 180)}_days"
                    }
                ],
                "next_steps": [
                    'Conduct detailed technical assessment',
                    'Prepare business case presentation',
                    'Initiate vendor evaluation process',
                    'Develop implementation roadmap'
                ]
            }
        }
        
        return {**base_params, **feasibility_params}
    
    @staticmethod
    def generate_description(params: Dict[str, Any], location: str, slice_type: str) -> str:
        """Generate sophisticated feasibility check intent description."""
        assessment_scope = params.get("feasibility_assessment", {}).get("assessment_scope", "COMPREHENSIVE")
        recommendation = params.get("recommendation_engine", {}).get("recommendation", "PROCEED")
        complexity = random_choice(['sophisticated', 'advanced', 'comprehensive', 'intelligent', 'adaptive'])
        
        return (f"Conduct {complexity} {assessment_scope.lower()} feasibility analysis for "
                f"{slice_type.replace('_', ' ')} implementation at {location} with advanced "
                f"risk modeling, economic impact assessment, and AI-driven recommendation engine "
                f"providing {recommendation.lower()} guidance for research-informed decision making")
