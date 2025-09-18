import uuid
import random
from typing import Dict, Any
from .Parameter_Generator import ParameterGenerator
from .utilis_generator import current_timestamp, generate_unique_id, random_choice, random_int, random_float

from .BaseIntentGenerator import BaseIntentGenerator

class ModificationIntentGenerator(BaseIntentGenerator):
    """Generator for modification intent records."""
    def __init__(self, constraint_engine=None):
        super().__init__(constraint_engine)
    
    def generate_constrained_parameters(self, slice_type: str, priority: str, location: str, complexity: int) -> Dict[str, Any]:
        """Generate modification parameters with realistic constraints."""
        constraint_engine = self.constraint_engine
        base_params = self.generate_base_params('MODIFICATION', {
            'slice_type': slice_type,
            'priority': priority,
            'location': location,
            'complexity': complexity
        })
        
        # Apply constraints based on context
        slice_category = constraint_engine.categorize_slice_type(slice_type)
        location_category = constraint_engine.categorize_location(location)
        
        # Adjust modification operations based on priority and complexity
        if priority in ['CRITICAL', 'EMERGENCY']:
            # Critical modifications need more conservative approaches
            base_params["modification_specification"]["change_pattern"] = "BLUE_GREEN"
            base_params["modification_specification"]["rollback_configuration"]["rollback_enabled"] = "true"
            base_params["modification_specification"]["rollback_configuration"]["rollback_timeout"] = "300seconds"
        elif priority == 'HIGH':
            base_params["modification_specification"]["change_pattern"] = random_choice(["BLUE_GREEN", "CANARY"])
            base_params["modification_specification"]["rollback_configuration"]["rollback_enabled"] = "true"
        else:
            base_params["modification_specification"]["change_pattern"] = random_choice(["ROLLING_UPDATE", "CANARY", "IMMEDIATE"])
        
        # Adjust impact analysis based on complexity
        if complexity >= 8:
            base_params["impact_analysis"]["affected_services"] = random_int(20, 50)
            base_params["impact_analysis"]["estimated_downtime"] = f"{random_int(60, 300)}seconds"
            base_params["impact_analysis"]["risk_assessment"]["technical_risk"] = random_choice(['HIGH', 'VERY_HIGH'])
        elif complexity >= 5:
            base_params["impact_analysis"]["affected_services"] = random_int(5, 20)
            base_params["impact_analysis"]["estimated_downtime"] = f"{random_int(10, 60)}seconds"
            base_params["impact_analysis"]["risk_assessment"]["technical_risk"] = random_choice(['MEDIUM', 'HIGH'])
        else:
            base_params["impact_analysis"]["affected_services"] = random_int(1, 5)
            base_params["impact_analysis"]["estimated_downtime"] = f"{random_int(0, 10)}seconds"
            base_params["impact_analysis"]["risk_assessment"]["technical_risk"] = random_choice(['LOW', 'MEDIUM'])
        
        # Adjust validation criteria based on slice category
        if slice_category in ['URLLC', 'V2X']:
            base_params["validation_criteria"]["performance_validation"]["latency_threshold"] = f"{random_float(0.1, 5)}ms"
            base_params["validation_criteria"]["performance_validation"]["error_rate_threshold"] = f"{random_float(0.001, 0.01)}%"
            base_params["validation_criteria"]["performance_validation"]["availability_threshold"] = f"{random_float(99.99, 99.999)}%"
        elif slice_category == 'eMBB':
            base_params["validation_criteria"]["performance_validation"]["latency_threshold"] = f"{random_float(5, 50)}ms"
            base_params["validation_criteria"]["performance_validation"]["throughput_threshold"] = f"{random_int(100, 10000)}Mbps"
        else:  # mMTC
            base_params["validation_criteria"]["performance_validation"]["latency_threshold"] = f"{random_float(50, 1000)}ms"
            base_params["validation_criteria"]["performance_validation"]["error_rate_threshold"] = f"{random_float(0.1, 1)}%"
        
        return base_params
    
    def generate_parameters(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate modification-specific parameters."""
        base_params = self.generate_base_params('MODIFICATION', context or {})
        
        # Add modification-specific parameters
        modification_params = {
            "modification_specification": {
                "target_resource": {
                    "resource_type": random_choice(['VNF_INSTANCE', 'NETWORK_SLICE', 'QOS_FLOW', 'PDU_SESSION']),
                    "resource_id": f"resource_{uuid.uuid4().hex[:16]}",
                    "resource_version": f"{random_int(1, 10)}.{random_int(0, 99)}",
                    "current_state": random_choice(['INSTANTIATED', 'STARTED', 'STOPPED', 'CONFIGURED'])
                },
                "modification_operations": [
                    {
                        "operation_type": random_choice(['MODIFY_INFO', 'CHANGE_FLAVOUR', 'CHANGE_EXT_CONN', 'OPERATE']),
                        "operation_params": {
                            "change_type": random_choice(['ADDED', 'REMOVED', 'MODIFIED', 'TEMPORARY']),
                            "modify_vnf_info_data": {
                                "vnf_instance_name": f"modified_instance_{uuid.uuid4().hex[:8]}",
                                "vnf_instance_description": f"Modified for {random_choice(['Performance', 'Security', 'Compliance', 'Optimization'])} enhancement",
                                "vnf_configurable_properties": {
                                    "is_auto_scale_enabled": random_choice(['true', 'false']),
                                    "is_auto_heal_enabled": random_choice(['true', 'false']),
                                    "max_instances": random_int(10, 1000),
                                    "min_instances": random_int(1, 10)
                                }
                            }
                        }
                    }
                ],
                "change_pattern": random_choice(['ROLLING_UPDATE', 'BLUE_GREEN', 'CANARY', 'IMMEDIATE']),
                "rollback_configuration": {
                    "rollback_enabled": random_choice(['true', 'false']),
                    "rollback_timeout": f"{random_int(300, 1800)}seconds",
                    "rollback_triggers": [
                        random_choice(['PERFORMANCE_DEGRADATION', 'ERROR_RATE_THRESHOLD', 'MANUAL_TRIGGER', 'HEALTH_CHECK_FAILURE'])
                    ]
                }
            },
            "impact_analysis": {
                "affected_services": random_int(1, 50),
                "estimated_downtime": f"{random_int(0, 300)}seconds",
                "risk_assessment": {
                    "technical_risk": random_choice(['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']),
                    "business_risk": random_choice(['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']),
                    "operational_risk": random_choice(['VERY_LOW', 'LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH'])
                },
                "dependency_analysis": {
                    "upstream_dependencies": random_int(0, 20),
                    "downstream_dependencies": random_int(0, 30),
                    "critical_path": random_choice(['true', 'false'])
                }
            },
            "validation_criteria": {
                "functional_validation": [
                    'Service_Continuity_Check',
                    'Performance_Baseline_Validation',
                    'Security_Compliance_Verification',
                    'Integration_Testing'
                ],
                "performance_validation": {
                    "latency_threshold": f"{random_float(1, 100)}ms",
                    "throughput_threshold": f"{random_int(10, 10000)}Mbps",
                    "error_rate_threshold": f"{random_float(0.01, 1)}%",
                    "availability_threshold": f"{random_float(99, 99.99)}%"
                }
            }
        }
        
        return {**base_params, **modification_params}
    
    @staticmethod
    def generate_description(params: Dict[str, Any], location: str, slice_type: str) -> str:
        """Generate sophisticated modification intent description."""
        target = params.get("modification_specification", {}).get("target_resource", {}).get("resource_type", "VNF_INSTANCE")
        operation = params.get("modification_specification", {}).get("modification_operations", [{}])[0].get("operation_type", "MODIFY_INFO")
        complexity = random_choice(['sophisticated', 'advanced', 'comprehensive', 'intelligent', 'adaptive'])
        
        return (f"Implement {complexity} modification of {target.lower().replace('_', ' ')} through "
                f"{operation.lower().replace('_', ' ')} operation at {location} for "
                f"{slice_type.replace('_', ' ')} with advanced impact analysis, intelligent rollback "
                f"mechanisms, and comprehensive validation procedures for research-oriented "
                f"network optimization studies")
