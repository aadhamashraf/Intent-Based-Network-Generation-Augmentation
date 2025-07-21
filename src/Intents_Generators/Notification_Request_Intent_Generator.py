import uuid
import random
from typing import Dict, Any
from .Constants_Enums import NETWORK_FUNCTIONS, ADVANCED_SLICE_TYPES, ADVANCED_LOCATIONS
from .Parameter_Generator import ParameterGenerator
from .utilis_generator import current_timestamp, generate_unique_id, random_choice, random_int

class NotificationRequestIntentGenerator:
    """Generator for notification request intent records."""
    
    def __init__(self):
        # Import here to avoid circular imports
        try:
            from .Constraint_Engine import ConstraintEngine
            self.constraint_engine = ConstraintEngine()
        except ImportError:
            self.constraint_engine = None
    
    def generate_constrained_parameters(self, slice_type: str, priority: str, location: str, complexity: int) -> Dict[str, Any]:
        """Generate notification request parameters with realistic constraints."""
        base_params = self.generate_parameters()
        
        # Apply constraints if constraint engine is available
        if self.constraint_engine:
            # Override with constrained parameters
            base_params["qos_parameters"] = self.constraint_engine.generate_constrained_qos_parameters(
                slice_type, priority, location
            )
            base_params["resource_allocation"] = self.constraint_engine.generate_constrained_resource_allocation(
                complexity, slice_type, priority
            )
        
        return base_params
    
    @staticmethod
    def generate_parameters() -> Dict[str, Any]:
        """Generate notification request-specific parameters."""
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
        
        # Add notification request-specific parameters
        notification_params = {
            "notification_configuration": {
                "subscription_details": {
                    "subscription_id": f"SUB_{generate_unique_id()}",
                    "subscription_type": random_choice(['EVENT_BASED', 'PERIODIC', 'THRESHOLD_BASED', 'HYBRID']),
                    "subscription_scope": {
                        "event_types": [
                            random_choice(['FAULT', 'PERFORMANCE', 'SECURITY', 'CONFIGURATION', 'LIFECYCLE']),
                            random_choice(['ALARM', 'NOTIFICATION', 'HEARTBEAT', 'STATUS_CHANGE'])
                        ],
                        "severity_filter": random_choice(['ALL', 'CRITICAL_MAJOR', 'CRITICAL_ONLY', 'CUSTOM']),
                        "source_filter": {
                            "network_functions": [random_choice(NETWORK_FUNCTIONS)],
                            "network_slices": [random_choice(ADVANCED_SLICE_TYPES)],
                            "geographical_areas": [random_choice(ADVANCED_LOCATIONS)]
                        }
                    },
                    "delivery_configuration": {
                        "frequency": random_choice(['REAL_TIME', 'EVERY_SECOND', 'EVERY_5_SECONDS', 'EVERY_MINUTE', 'EVERY_5_MINUTES', 'HOURLY', 'DAILY']),
                        "batching_enabled": random_choice(['true', 'false']),
                        "batch_size": random_int(1, 1000),
                        "batch_timeout": f"{random_int(1, 300)}seconds",
                        "compression_enabled": random_choice(['true', 'false'])
                    }
                },
                "delivery_mechanism": {
                    "primary_channel": {
                        "type": random_choice(['WEBHOOK', 'KAFKA', 'AMQP', 'MQTT', 'WEBSOCKET', 'gRPC']),
                        "endpoint": f"https://notifications.{uuid.uuid4().hex[:8]}.com/webhook/v1/events",
                        "authentication": {
                            "method": random_choice(['OAUTH2_CLIENT_CREDENTIALS', 'API_KEY', 'MUTUAL_TLS', 'JWT_BEARER']),
                            "credentials": {
                                "client_id": f"client_{uuid.uuid4().hex[:16]}",
                                "client_secret": f"secret_{uuid.uuid4().hex[:32]}",
                                "scope": random_choice(['read:notifications', 'write:notifications', 'admin:notifications'])
                            }
                        },
                        "headers": {
                            'Content-Type': 'application/json',
                            'X-API-Version': 'v1',
                            'X-Client-ID': f"client_{uuid.uuid4().hex[:12]}"
                        }
                    },
                    "fallback_channel": {
                        "type": random_choice(['EMAIL', 'SMS', 'SLACK', 'TEAMS', 'PAGERDUTY']),
                        "configuration": {
                            "recipients": [f"admin@{uuid.uuid4().hex[:8]}.com"],
                            "template": random_choice(['DETAILED', 'SUMMARY', 'MINIMAL', 'CUSTOM']),
                            "escalation_delay": f"{random_int(5, 60)}minutes"
                        }
                    }
                },
                "message_format": {
                    "schema": {
                        "version": '1.0',
                        "format": random_choice(['JSON_SCHEMA', 'AVRO', 'PROTOBUF', 'XML_SCHEMA']),
                        "content_encoding": random_choice(['UTF8', 'BASE64', 'GZIP']),
                        "message_structure": {
                            "header": {
                                "message_id": 'UUID',
                                "timestamp": 'ISO8601',
                                "source": 'STRING',
                                "event_type": 'ENUM',
                                "severity": 'ENUM'
                            },
                            "payload": {
                                "event_data": 'OBJECT',
                                "context": 'OBJECT',
                                "metadata": 'OBJECT'
                            }
                        }
                    },
                    "transformation": {
                        "enabled": random_choice(['true', 'false']),
                        "transformation_type": random_choice(['JOLT', 'XSLT', 'JAVASCRIPT', 'PYTHON']),
                        "transformation_rules": f"rule_{uuid.uuid4().hex[:12]}.json"
                    },
                    "enrichment": {
                        "enabled": random_choice(['true', 'false']),
                        "enrichment_sources": [
                            random_choice(['CMDB', 'INVENTORY', 'TOPOLOGY', 'CONFIGURATION'])
                        ],
                        "enrichment_fields": [
                            'location_details',
                            'service_impact',
                            'escalation_contacts',
                            'remediation_procedures'
                        ]
                    }
                },
                "quality_of_service": {
                    "delivery_guarantee": random_choice(['AT_MOST_ONCE', 'AT_LEAST_ONCE', 'EXACTLY_ONCE']),
                    "ordering_guarantee": random_choice(['NONE', 'PARTITION_ORDERED', 'GLOBAL_ORDERED']),
                    "durability": random_choice(['MEMORY_ONLY', 'DISK_BACKED', 'REPLICATED']),
                    "retry_policy": {
                        "max_retries": random_int(3, 20),
                        "retry_interval": f"{random_int(1, 60)}seconds",
                        "backoff_strategy": random_choice(['FIXED', 'LINEAR', 'EXPONENTIAL', 'FIBONACCI']),
                        "dead_letter_queue": random_choice(['ENABLED', 'DISABLED'])
                    },
                    "circuit_breaker": {
                        "enabled": random_choice(['true', 'false']),
                        "failure_threshold": random_int(5, 50),
                        "recovery_timeout": f"{random_int(30, 300)}seconds",
                        "half_open_max_calls": random_int(1, 10)
                    }
                },
                "monitoring": {
                    "metrics_collection": {
                        "enabled": random_choice(['true', 'false']),
                        "metrics": [
                            'delivery_success_rate',
                            'delivery_latency',
                            'message_throughput',
                            'error_rate',
                            'queue_depth'
                        ],
                        "aggregation_interval": f"{random_int(1, 60)}minutes",
                        "retention_period": f"{random_int(7, 90)}days"
                    },
                    "health_checks": {
                        "enabled": random_choice(['true', 'false']),
                        "check_interval": f"{random_int(10, 300)}seconds",
                        "timeout_threshold": f"{random_int(5, 30)}seconds",
                        "health_endpoint": '/health/notifications'
                    }
                }
            }
        }
        
        return {**base_params, **notification_params}
    
    @staticmethod
    def generate_description(params: Dict[str, Any], location: str, slice_type: str) -> str:
        """Generate sophisticated notification request intent description."""
        subscription_type = params.get("notification_configuration", {}).get("subscription_details", {}).get("subscription_type", "EVENT_BASED")
        delivery_type = params.get("notification_configuration", {}).get("delivery_mechanism", {}).get("primary_channel", {}).get("type", "WEBHOOK")
        complexity = random_choice(['sophisticated', 'advanced', 'comprehensive', 'intelligent', 'adaptive'])
        
        return (f"Configure {complexity} {subscription_type.lower().replace('_', ' ')} notification "
                f"system for {slice_type.replace('_', ' ')} monitoring at {location} with "
                f"{delivery_type.lower()} delivery mechanism, advanced message transformation, "
                f"and intelligent filtering capabilities for research-grade network event management")
