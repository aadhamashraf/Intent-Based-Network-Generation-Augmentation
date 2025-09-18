import uuid
import random
from typing import Dict, Any
from .Constants_Enums import NETWORK_FUNCTIONS, ADVANCED_SLICE_TYPES, PERFORMANCE_METRICS
from .Parameter_Generator import ParameterGenerator
from .utilis_generator import current_timestamp, generate_unique_id, random_choice, random_int, random_float, random_timestamp_within_days

class ReportRequestIntentGenerator:
    """Generator for report request intent records."""
    
    def __init__(self):
        # Remove old constraint engine dependency - now handled by main generator
        pass
    
    def generate_constrained_parameters(self, slice_type: str, priority: str, location: str, complexity: int) -> Dict[str, Any]:
        """Generate report request parameters with realistic constraints."""
        # Import constraint engine for consistent constraint application
        from .Enhanced_Constraint_Engine import EnhancedConstraintEngine
        constraint_engine = EnhancedConstraintEngine()
        
        # Generate base parameters
        base_params = self.generate_parameters()
        
        # Apply constraints based on context
        slice_category = constraint_engine.categorize_slice_type(slice_type)
        location_category = constraint_engine.categorize_location(location)
        
        # Adjust report type based on slice category
        if slice_category in ['URLLC', 'V2X']:
            base_params["report_specification"]["report_type"] = random_choice(['PERFORMANCE_ANALYTICS', 'FAULT_ANALYSIS'])
            base_params["report_specification"]["data_requirements"]["filter_criteria"]["severity_level"] = random_choice(['CRITICAL_ONLY', 'MAJOR_AND_ABOVE'])
        elif slice_category == 'eMBB':
            base_params["report_specification"]["report_type"] = random_choice(['PERFORMANCE_ANALYTICS', 'RESOURCE_UTILIZATION'])
        else:  # mMTC
            base_params["report_specification"]["report_type"] = random_choice(['RESOURCE_UTILIZATION', 'COMPLIANCE_ASSESSMENT'])
        
        # Adjust temporal scope based on priority
        if priority in ['CRITICAL', 'EMERGENCY']:
            # More frequent, detailed reporting for critical services
            base_params["report_specification"]["report_scope"]["temporal_scope"]["granularity"] = random_choice(['1_MINUTE', '5_MINUTES'])
            base_params["output_configuration"]["delivery"]["retry_policy"]["max_retries"] = random_int(5, 10)
        elif priority == 'HIGH':
            base_params["report_specification"]["report_scope"]["temporal_scope"]["granularity"] = random_choice(['5_MINUTES', '15_MINUTES'])
            base_params["output_configuration"]["delivery"]["retry_policy"]["max_retries"] = random_int(3, 7)
        else:
            base_params["report_specification"]["report_scope"]["temporal_scope"]["granularity"] = random_choice(['15_MINUTES', '1_HOUR', '1_DAY'])
            base_params["output_configuration"]["delivery"]["retry_policy"]["max_retries"] = random_int(1, 5)
        
        # Adjust data requirements based on complexity
        if complexity >= 8:
            # More comprehensive metrics for complex scenarios
            base_params["report_specification"]["data_requirements"]["aggregation_methods"] = [
                random_choice(['AVERAGE', 'MEDIAN', 'P95', 'P99']),
                random_choice(['MIN', 'MAX', 'SUM', 'COUNT'])
            ]
            base_params["quality_assurance"]["data_validation"]["accuracy_threshold"] = f"{random_float(98, 99.9)}%"
        elif complexity >= 5:
            base_params["report_specification"]["data_requirements"]["aggregation_methods"] = [
                random_choice(['AVERAGE', 'MEDIAN', 'P95'])
            ]
            base_params["quality_assurance"]["data_validation"]["accuracy_threshold"] = f"{random_float(95, 98)}%"
        else:
            base_params["report_specification"]["data_requirements"]["aggregation_methods"] = [
                random_choice(['AVERAGE', 'MEDIAN'])
            ]
            base_params["quality_assurance"]["data_validation"]["accuracy_threshold"] = f"{random_float(90, 95)}%"
        
        # Adjust security based on slice category and priority
        if slice_category in ['URLLC', 'V2X'] or priority in ['CRITICAL', 'EMERGENCY']:
            base_params["output_configuration"]["encryption"]["enabled"] = "true"
            base_params["output_configuration"]["encryption"]["algorithm"] = "AES_256_GCM"
            base_params["output_configuration"]["delivery"]["authentication"]["type"] = random_choice(['OAUTH2', 'MUTUAL_TLS'])
        else:
            base_params["output_configuration"]["encryption"]["enabled"] = random_choice(["true", "false"])
            if base_params["output_configuration"]["encryption"]["enabled"] == "true":
                base_params["output_configuration"]["encryption"]["algorithm"] = random_choice(['AES_256_GCM', 'AES_128_GCM'])
        
        return base_params
    
    @staticmethod
    def generate_parameters() -> Dict[str, Any]:
        """Generate report request-specific parameters."""
        base_params = {
            "timestamp": current_timestamp(),
            "request_id": f"REQ_{generate_unique_id()}",
            "correlation_id": f"CORR_{uuid.uuid4().hex[:16]}",
            "tenant_id": f"TENANT_{random_int(10000, 99999)}",
            "service_level": random_choice(['PLATINUM_PLUS', 'PLATINUM', 'GOLD_PREMIUM', 'GOLD', 'SILVER_PLUS', 'SILVER', 'BRONZE']),
            "network_topology": ParameterGenerator.generate_network_topology(),
            "qos_parameters": ParameterGenerator.generate_qos_parameters(),
            "security_parameters": ParameterGenerator.generate_security_parameters(),
            "resource_allocation": ParameterGenerator.generate_resource_allocation(),
            "monitoring_parameters": ParameterGenerator.generate_monitoring_parameters()
        }
        
        # Add report request-specific parameters
        report_params = {
            "report_specification": {
                "report_type": random_choice(['PERFORMANCE_ANALYTICS', 'SECURITY_AUDIT', 'COMPLIANCE_ASSESSMENT', 'RESOURCE_UTILIZATION', 'FAULT_ANALYSIS']),
                "report_scope": {
                    "temporal_scope": {
                        "start_time": random_timestamp_within_days(90),
                        "end_time": current_timestamp(),
                        "time_zone": random_choice(['UTC', 'EST', 'PST', 'CET', 'JST']),
                        "granularity": random_choice(['1_MINUTE', '5_MINUTES', '15_MINUTES', '1_HOUR', '1_DAY'])
                    },
                    "spatial_scope": {
                        "network_elements": random_choice(NETWORK_FUNCTIONS),
                        "geographical_region": random_choice(['GLOBAL', 'REGIONAL', 'NATIONAL', 'METROPOLITAN', 'LOCAL']),
                        "network_slices": [random_choice(ADVANCED_SLICE_TYPES)],
                        "service_instances": [f"service_{uuid.uuid4().hex[:12]}"]
                    },
                    "functional_scope": {
                        "domains": random_choice(['RAN', 'CORE', 'TRANSPORT', 'MANAGEMENT', 'SECURITY']),
                        "layers": random_choice(['PHYSICAL', 'NETWORK', 'SERVICE', 'APPLICATION', 'BUSINESS']),
                        "aspects": random_choice(['PERFORMANCE', 'AVAILABILITY', 'SECURITY', 'COMPLIANCE', 'COST'])
                    }
                },
                "data_requirements": {
                    "metrics_of_interest": random.sample(PERFORMANCE_METRICS, random_int(3, 8)),
                    "aggregation_methods": [
                        random_choice(['AVERAGE', 'MEDIAN', 'P95', 'P99', 'MIN', 'MAX', 'SUM', 'COUNT'])
                    ],
                    "filter_criteria": {
                        "severity_level": random_choice(['ALL', 'CRITICAL_ONLY', 'MAJOR_AND_ABOVE', 'MINOR_AND_ABOVE']),
                        "event_types": [random_choice(['ALARM', 'EVENT', 'NOTIFICATION', 'MEASUREMENT'])],
                        "source_filters": [random_choice(NETWORK_FUNCTIONS)]
                    }
                }
            },
            "output_configuration": {
                "format": random_choice(['JSON', 'XML', 'CSV', 'PARQUET', 'AVRO', 'YAML']),
                "compression": random_choice(['GZIP', 'BZIP2', 'LZ4', 'SNAPPY', 'NONE']),
                "encryption": {
                    "enabled": random_choice(['true', 'false']),
                    "algorithm": random_choice(['AES_256_GCM', 'AES_128_GCM', 'ChaCha20_Poly1305']),
                    "key_management": random_choice(['HSM', 'KMS', 'LOCAL_KEY'])
                },
                "delivery": {
                    "method": random_choice(['REST_API', 'SFTP', 'S3_BUCKET', 'KAFKA_TOPIC', 'EMAIL']),
                    "endpoint": f"https://reports.{random_choice(['internal', 'external'])}.{uuid.uuid4().hex[:8]}.com/api/v1/reports",
                    "authentication": {
                        "type": random_choice(['OAUTH2', 'API_KEY', 'MUTUAL_TLS', 'BASIC_AUTH']),
                        "credentials": f"cred_{uuid.uuid4().hex[:16]}"
                    },
                    "retry_policy": {
                        "max_retries": random_int(3, 10),
                        "backoff_strategy": random_choice(['EXPONENTIAL', 'LINEAR', 'FIXED']),
                        "timeout": f"{random_int(30, 300)}seconds"
                    }
                }
            },
            "quality_assurance": {
                "data_validation": {
                    "completeness_check": random_choice(['ENABLED', 'DISABLED']),
                    "consistency_check": random_choice(['ENABLED', 'DISABLED']),
                    "accuracy_threshold": f"{random_float(95, 99.9)}%",
                    "freshness_requirement": f"{random_int(1, 60)}minutes"
                },
                "report_validation": {
                    "schema_validation": random_choice(['STRICT', 'LENIENT', 'DISABLED']),
                    "business_rule_validation": random_choice(['ENABLED', 'DISABLED']),
                    "cross_reference_validation": random_choice(['ENABLED', 'DISABLED'])
                }
            }
        }
        
        return {**base_params, **report_params}
    
    @staticmethod
    def generate_description(params: Dict[str, Any], location: str, slice_type: str) -> str:
        """Generate sophisticated report request intent description."""
        report_type = params.get("report_specification", {}).get("report_type", "PERFORMANCE_ANALYTICS")
        scope = params.get("report_specification", {}).get("report_scope", {}).get("functional_scope", {}).get("domains", "CORE")
        complexity = random_choice(['sophisticated', 'advanced', 'comprehensive', 'intelligent', 'adaptive'])
        
        return (f"Generate {complexity} {report_type.lower().replace('_', ' ')} report covering "
                f"{scope.lower()} domain operations at {location} for {slice_type.replace('_', ' ')} "
                f"with advanced data analytics, multi-dimensional correlation analysis, and "
                f"research-grade statistical modeling for comprehensive network intelligence gathering")
