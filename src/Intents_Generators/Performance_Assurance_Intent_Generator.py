import uuid
import random
from typing import Dict, Any
from .Parameter_Generator import ParameterGenerator
from .utilis_generator import current_timestamp, generate_unique_id, random_choice, random_int, random_float

from .BaseIntentGenerator import BaseIntentGenerator

class PerformanceAssuranceIntentGenerator(BaseIntentGenerator):
    """Generator for performance assurance intent records."""
    def __init__(self, constraint_engine=None):
        super().__init__(constraint_engine)
    
    def generate_constrained_parameters(self, slice_type: str, priority: str, location: str, complexity: int) -> Dict[str, Any]:
        """Generate performance assurance parameters with realistic constraints."""
        constraint_engine = self.constraint_engine
        base_params = self.generate_base_params('PERFORMANCE_ASSURANCE', {
            'slice_type': slice_type,
            'priority': priority,
            'location': location,
            'complexity': complexity
        })
        
        # Apply constraints based on context
        slice_category = constraint_engine.categorize_slice_type(slice_type)
        location_category = constraint_engine.categorize_location(location)
        
        # Adjust SLA commitments based on slice category and priority
        if slice_category in ['URLLC', 'V2X']:
            base_params["performance_objectives"]["service_level"]["commitments"]["availability"] = f"{random_float(99.99, 99.999)}%"
            base_params["performance_objectives"]["service_level"]["commitments"]["mean_time_to_repair"] = f"{random_int(5, 30)}minutes"
            base_params["performance_objectives"]["kpi_targets"]["network_kpis"]["end_to_end_latency"]["target"] = f"{random_float(0.1, 5)}ms"
            base_params["performance_objectives"]["kpi_targets"]["network_kpis"]["packet_loss_rate"]["target"] = f"{random_float(0.0001, 0.001)}%"
        elif slice_category == 'eMBB':
            base_params["performance_objectives"]["service_level"]["commitments"]["availability"] = f"{random_float(99.5, 99.9)}%"
            base_params["performance_objectives"]["kpi_targets"]["network_kpis"]["end_to_end_latency"]["target"] = f"{random_float(5, 50)}ms"
            base_params["performance_objectives"]["kpi_targets"]["network_kpis"]["throughput"]["target"] = f"{random_int(100, 10000)}Mbps"
        else:  # mMTC
            base_params["performance_objectives"]["service_level"]["commitments"]["availability"] = f"{random_float(99.0, 99.5)}%"
            base_params["performance_objectives"]["kpi_targets"]["network_kpis"]["end_to_end_latency"]["target"] = f"{random_float(50, 1000)}ms"
        
        # Adjust assurance actions based on priority
        if priority in ['CRITICAL', 'EMERGENCY']:
            # More aggressive proactive actions for critical services
            base_params["assurance_actions"]["proactive_actions"][0]["parameters"]["prediction_horizon"] = f"{random_int(1, 15)}minutes"
            base_params["assurance_actions"]["proactive_actions"][0]["parameters"]["confidence_level"] = f"{random_int(90, 99)}%"
            base_params["assurance_actions"]["reactive_actions"][0]["parameters"]["max_reroute_attempts"] = random_int(5, 10)
        elif priority == 'HIGH':
            base_params["assurance_actions"]["proactive_actions"][0]["parameters"]["prediction_horizon"] = f"{random_int(15, 30)}minutes"
            base_params["assurance_actions"]["proactive_actions"][0]["parameters"]["confidence_level"] = f"{random_int(85, 95)}%"
        else:
            base_params["assurance_actions"]["proactive_actions"][0]["parameters"]["prediction_horizon"] = f"{random_int(30, 60)}minutes"
            base_params["assurance_actions"]["proactive_actions"][0]["parameters"]["confidence_level"] = f"{random_int(80, 90)}%"
        
        # Adjust monitoring frequency based on complexity
        if complexity >= 8:
            base_params["monitoring_configuration"]["data_collection"]["collection_interval"] = f"{random_int(1, 5)}seconds"
            base_params["monitoring_configuration"]["data_collection"]["aggregation_window"] = f"{random_int(1, 5)}minutes"
        elif complexity >= 5:
            base_params["monitoring_configuration"]["data_collection"]["collection_interval"] = f"{random_int(5, 30)}seconds"
            base_params["monitoring_configuration"]["data_collection"]["aggregation_window"] = f"{random_int(5, 10)}minutes"
        else:
            base_params["monitoring_configuration"]["data_collection"]["collection_interval"] = f"{random_int(30, 60)}seconds"
            base_params["monitoring_configuration"]["data_collection"]["aggregation_window"] = f"{random_int(10, 15)}minutes"
        
        return base_params
    
    def generate_parameters(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate performance assurance-specific parameters."""
        base_params = self.generate_base_params('PERFORMANCE_ASSURANCE', context or {})
        
        # Add performance assurance-specific parameters
        performance_params = {
            "performance_objectives": {
                "service_level": {
                    "sla_id": f"sla_{uuid.uuid4().hex[:12]}",
                    "sla_version": f"{random_int(1, 5)}.{random_int(0, 9)}",
                    "sla_type": random_choice(['GOLD_TIER', 'SILVER_TIER', 'BRONZE_TIER', 'CUSTOM_TIER']),
                    "commitments": {
                        "availability": f"{random_float(99.5, 99.999)}%",
                        "mean_time_to_repair": f"{random_int(15, 240)}minutes",
                        "mean_time_between_failures": f"{random_int(720, 8760)}hours",
                        "response_time": f"{random_float(0.1, 10)}seconds"
                    }
                },
                "kpi_targets": {
                    "network_kpis": {
                        "end_to_end_latency": {
                            "target": f"{random_float(1, 50)}ms",
                            "threshold": f"{random_float(10, 100)}ms",
                            "measurement": 'P95_PERCENTILE'
                        },
                        "packet_loss_rate": {
                            "target": f"{random_float(0.001, 0.1)}%",
                            "threshold": f"{random_float(0.1, 1)}%",
                            "measurement": 'AVERAGE'
                        },
                        "jitter": {
                            "target": f"{random_float(0.1, 5)}ms",
                            "threshold": f"{random_float(1, 20)}ms",
                            "measurement": 'P99_PERCENTILE'
                        },
                        "throughput": {
                            "target": f"{random_int(100, 10000)}Mbps",
                            "threshold": f"{random_int(50, 5000)}Mbps",
                            "measurement": 'SUSTAINED_RATE'
                        }
                    },
                    "service_kpis": {
                        "session_setup_time": {
                            "target": f"{random_float(100, 2000)}ms",
                            "threshold": f"{random_float(500, 5000)}ms",
                            "measurement": 'P90_PERCENTILE'
                        },
                        "handover_success_rate": {
                            "target": f"{random_float(98, 99.9)}%",
                            "threshold": f"{random_float(95, 98)}%",
                            "measurement": 'SUCCESS_RATIO'
                        },
                        "call_drop_rate": {
                            "target": f"{random_float(0.1, 2)}%",
                            "threshold": f"{random_float(2, 5)}%",
                            "measurement": 'FAILURE_RATIO'
                        }
                    }
                }
            },
            "assurance_actions": {
                "proactive_actions": [
                    {
                        "action_type": 'PREDICTIVE_SCALING',
                        "trigger": 'LOAD_PREDICTION_THRESHOLD',
                        "parameters": {
                            "prediction_horizon": f"{random_int(5, 60)}minutes",
                            "confidence_level": f"{random_int(80, 95)}%",
                            "scaling_factor": random_float(1.1, 3.0)
                        }
                    },
                    {
                        "action_type": 'RESOURCE_OPTIMIZATION',
                        "trigger": 'EFFICIENCY_DEGRADATION',
                        "parameters": {
                            "optimization_algorithm": random_choice(['GENETIC_ALGORITHM', 'SIMULATED_ANNEALING', 'PARTICLE_SWARM']),
                            "optimization_target": random_choice(['COST', 'PERFORMANCE', 'ENERGY', 'BALANCED'])
                        }
                    }
                ],
                "reactive_actions": [
                    {
                        "action_type": 'TRAFFIC_REROUTING',
                        "trigger": 'CONGESTION_DETECTED',
                        "parameters": {
                            "rerouting_strategy": random_choice(['SHORTEST_PATH', 'LOAD_BALANCED', 'QOS_AWARE']),
                            "max_reroute_attempts": random_int(3, 10)
                        }
                    },
                    {
                        "action_type": 'RESOURCE_SCALING',
                        "trigger": 'PERFORMANCE_THRESHOLD_BREACH',
                        "parameters": {
                            "scaling_direction": random_choice(['SCALE_OUT', 'SCALE_UP', 'SCALE_IN', 'SCALE_DOWN']),
                            "scaling_increment": random_int(1, 10)
                        }
                    }
                ]
            },
            "monitoring_configuration": {
                "data_collection": {
                    "collection_interval": f"{random_int(1, 60)}seconds",
                    "aggregation_window": f"{random_int(1, 15)}minutes",
                    "retention_policy": f"{random_int(30, 365)}days",
                    "sampling_strategy": random_choice(['UNIFORM', 'ADAPTIVE', 'STRATIFIED', 'SYSTEMATIC'])
                },
                "alerting_rules": [
                    {
                        "rule_name": f"Performance_Degradation_{uuid.uuid4().hex[:8]}",
                        "condition": 'latency > threshold OR packet_loss > threshold',
                        "severity": random_choice(['CRITICAL', 'MAJOR', 'MINOR', 'WARNING']),
                        "cooldown_period": f"{random_int(60, 600)}seconds"
                    }
                ]
            }
        }
        
        return {**base_params, **performance_params}
    
    @staticmethod
    def generate_description(params: Dict[str, Any], location: str, slice_type: str) -> str:
        """Generate sophisticated performance assurance intent description."""
        sla_type = params.get("performance_objectives", {}).get("service_level", {}).get("sla_type", "GOLD_TIER")
        availability = params.get("performance_objectives", {}).get("service_level", {}).get("commitments", {}).get("availability", "99.9%")
        complexity = random_choice(['sophisticated', 'advanced', 'comprehensive', 'intelligent', 'adaptive'])
        
        return (f"Establish {complexity} performance assurance framework for "
                f"{slice_type.replace('_', ' ')} at {location} with "
                f"{sla_type.lower().replace('_', ' ')} service level guaranteeing {availability} "
                f"availability through predictive analytics, machine learning-based optimization, "
                f"and autonomous remediation capabilities for advanced network research applications")
