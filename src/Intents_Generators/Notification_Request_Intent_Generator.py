import uuid
import random
from typing import Dict, Any
from .Constants_Enums import NETWORK_FUNCTIONS, ADVANCED_SLICE_TYPES, ADVANCED_LOCATIONS
from .Parameter_Generator import ParameterGenerator
from .utilis_generator import current_timestamp, generate_unique_id, random_choice, random_int

from .BaseIntentGenerator import BaseIntentGenerator

class NotificationRequestIntentGenerator(BaseIntentGenerator):
    """Generator for notification request intent records."""
    def __init__(self, constraint_engine=None):
        super().__init__(constraint_engine)
    
    def generate_constrained_parameters(self, slice_type: str, priority: str, location: str, complexity: int) -> Dict[str, Any]:
        """Generate notification request parameters with realistic constraints."""
        constraint_engine = self.constraint_engine
        base_params = self.generate_base_params('NOTIFICATION_REQUEST', {
            'slice_type': slice_type,
            'priority': priority,
            'location': location,
            'complexity': complexity
        })
        
        # Apply constraints based on context
        slice_category = constraint_engine.categorize_slice_type(slice_type)
        location_category = constraint_engine.categorize_location(location)
        
        # Adjust subscription type based on slice category
        if slice_category in ['URLLC', 'V2X']:
            # Critical slices need real-time or threshold-based notifications
            base_params["notification_configuration"]["subscription_details"]["subscription_type"] = random_choice(['EVENT_BASED', 'THRESHOLD_BASED'])
            base_params["notification_configuration"]["subscription_details"]["delivery_configuration"]["frequency"] = random_choice(['REAL_TIME', 'EVERY_SECOND'])
            base_params["notification_configuration"]["subscription_details"]["subscription_scope"]["severity_filter"] = random_choice(['CRITICAL_ONLY', 'CRITICAL_MAJOR'])
        elif slice_category == 'eMBB':
            base_params["notification_configuration"]["subscription_details"]["subscription_type"] = random_choice(['EVENT_BASED', 'PERIODIC'])
            base_params["notification_configuration"]["subscription_details"]["delivery_configuration"]["frequency"] = random_choice(['EVERY_SECOND', 'EVERY_5_SECONDS', 'EVERY_MINUTE'])
        else:  # mMTC
            base_params["notification_configuration"]["subscription_details"]["subscription_type"] = random_choice(['PERIODIC', 'THRESHOLD_BASED'])
            base_params["notification_configuration"]["subscription_details"]["delivery_configuration"]["frequency"] = random_choice(['EVERY_5_MINUTES', 'HOURLY', 'DAILY'])
        
        # Adjust delivery mechanism based on priority
        if priority in ['CRITICAL', 'EMERGENCY']:
            # Multiple delivery channels for critical notifications
            base_params["notification_configuration"]["delivery_mechanism"]["primary_channel"]["type"] = random_choice(['WEBHOOK', 'WEBSOCKET', 'gRPC'])
            base_params["notification_configuration"]["delivery_mechanism"]["fallback_channel"]["type"] = random_choice(['SMS', 'PAGERDUTY'])
            base_params["notification_configuration"]["delivery_mechanism"]["fallback_channel"]["configuration"]["escalation_delay"] = f"{random_int(1, 5)}minutes"
        elif priority == 'HIGH':
            base_params["notification_configuration"]["delivery_mechanism"]["primary_channel"]["type"] = random_choice(['WEBHOOK', 'KAFKA', 'WEBSOCKET'])
            base_params["notification_configuration"]["delivery_mechanism"]["fallback_channel"]["configuration"]["escalation_delay"] = f"{random_int(5, 15)}minutes"
        else:
            base_params["notification_configuration"]["delivery_mechanism"]["primary_channel"]["type"] = random_choice(['WEBHOOK', 'KAFKA', 'AMQP', 'MQTT'])
            base_params["notification_configuration"]["delivery_mechanism"]["fallback_channel"]["configuration"]["escalation_delay"] = f"{random_int(15, 60)}minutes"
        
        # Adjust QoS based on complexity and priority
        if complexity >= 8 or priority in ['CRITICAL', 'EMERGENCY']:
            base_params["notification_configuration"]["quality_of_service"]["delivery_guarantee"] = "EXACTLY_ONCE"
            base_params["notification_configuration"]["quality_of_service"]["ordering_guarantee"] = random_choice(['PARTITION_ORDERED', 'GLOBAL_ORDERED'])
            base_params["notification_configuration"]["quality_of_service"]["durability"] = "REPLICATED"
            base_params["notification_configuration"]["quality_of_service"]["retry_policy"]["max_retries"] = random_int(10, 20)
        elif complexity >= 5 or priority == 'HIGH':
            base_params["notification_configuration"]["quality_of_service"]["delivery_guarantee"] = "AT_LEAST_ONCE"
            base_params["notification_configuration"]["quality_of_service"]["durability"] = random_choice(['DISK_BACKED', 'REPLICATED'])
            base_params["notification_configuration"]["quality_of_service"]["retry_policy"]["max_retries"] = random_int(5, 15)
        else:
            base_params["notification_configuration"]["quality_of_service"]["delivery_guarantee"] = random_choice(['AT_MOST_ONCE', 'AT_LEAST_ONCE'])
            base_params["notification_configuration"]["quality_of_service"]["durability"] = random_choice(['MEMORY_ONLY', 'DISK_BACKED'])
            base_params["notification_configuration"]["quality_of_service"]["retry_policy"]["max_retries"] = random_int(3, 10)
        
        # Adjust monitoring based on complexity
        if complexity >= 8:
            base_params["notification_configuration"]["monitoring"]["metrics_collection"]["enabled"] = "true"
            base_params["notification_configuration"]["monitoring"]["metrics_collection"]["aggregation_interval"] = f"{random_int(1, 5)}minutes"
            base_params["notification_configuration"]["monitoring"]["health_checks"]["enabled"] = "true"
            base_params["notification_configuration"]["monitoring"]["health_checks"]["check_interval"] = f"{random_int(10, 30)}seconds"
        elif complexity >= 5:
            base_params["notification_configuration"]["monitoring"]["metrics_collection"]["enabled"] = "true"
            base_params["notification_configuration"]["monitoring"]["metrics_collection"]["aggregation_interval"] = f"{random_int(5, 15)}minutes"
        else:
            base_params["notification_configuration"]["monitoring"]["metrics_collection"]["enabled"] = random_choice(["true", "false"])
            base_params["notification_configuration"]["monitoring"]["metrics_collection"]["aggregation_interval"] = f"{random_int(15, 60)}minutes"
        
        return base_params
    
    def generate_parameters(self, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate notification request-specific parameters."""
        base_params = self.generate_base_params('NOTIFICATION_REQUEST', context or {})
        
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
