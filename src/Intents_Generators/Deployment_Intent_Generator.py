import uuid
import random
from typing import Dict, Any, List
from dataclasses import dataclass
from typing import Dict, Any
from .Constants_Enums import NETWORK_FUNCTIONS
from .Parameter_Generator import ParameterGenerator
from .utilis_generator import current_timestamp, generate_unique_id, random_choice, random_int, random_float

class DeploymentIntentGenerator:
    """Generator for deployment intent records."""
    
    def __init__(self):
        pass
    
    def _extract_extensive_parameters(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Extract extensive parameters from the comprehensive parameter set."""
        extracted = {}
        
        # Extract from nested parameter structures
        for key, value in params.items():
            if isinstance(value, dict):
                extracted.update(self._flatten_parameters(value, key))
            else:
                extracted[key] = value
        
        return extracted
    
    def _flatten_parameters(self, params: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """Flatten nested parameter structures for extensive utilization."""
        flattened = {}
        
        for key, value in params.items():
            new_key = f"{prefix}_{key}" if prefix else key
            
            if isinstance(value, dict):
                flattened.update(self._flatten_parameters(value, new_key))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        flattened.update(self._flatten_parameters(item, f"{new_key}_{i}"))
                    else:
                        flattened[f"{new_key}_{i}"] = item
            else:
                flattened[new_key] = value
        
        return flattened
    
    @staticmethod
    def generate_parameters() -> Dict[str, Any]:
        """Generate deployment-specific parameters."""
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
        
        # Add deployment-specific parameters
        deployment_params = {
            "deployment_specification": {
                "network_function": random_choice(NETWORK_FUNCTIONS),
                "vnf_descriptor": {
                    "vnfd_id": f"vnfd_{uuid.uuid4().hex[:12]}",
                    "vnfd_version": f"{random_int(1, 5)}.{random_int(0, 9)}.{random_int(0, 99)}",
                    "vnf_provider": random_choice(['Ericsson', 'Nokia', 'Huawei', 'Samsung', 'ZTE', 'Cisco']),
                    "vnf_product_name": f"{random_choice(NETWORK_FUNCTIONS)}_Advanced_{random_int(1000, 9999)}",
                    "vnf_software_version": f"SW_{random_int(1, 10)}.{random_int(0, 99)}.{random_int(0, 999)}",
                    "vnfd_invariant_id": f"invariant_{uuid.uuid4().hex[:16]}"
                },
                "deployment_flavor": {
                    "flavor_id": f"flavor_{uuid.uuid4().hex[:8]}",
                    "description": f"High_Performance_{random_choice(['Compute', 'Network', 'Storage'])}_Optimized",
                    "vdu_profile": {
                        "vdu_id": f"vdu_{uuid.uuid4().hex[:8]}",
                        "min_number_of_instances": random_int(1, 5),
                        "max_number_of_instances": random_int(10, 100),
                        "initial_number_of_instances": random_int(2, 10)
                    }
                },
                "instantiation_level_id": f"level_{random_int(1, 5)}",
                "additional_params": {
                    "lcm_operations_configuration": {
                        "instantiate": {
                            "timeout": f"{random_int(300, 3600)}seconds",
                            "rollback_on_failure": random_choice(['true', 'false']),
                            "skip_verification": random_choice(['true', 'false'])
                        },
                        "scale": {
                            "timeout": f"{random_int(60, 600)}seconds",
                            "scale_type": random_choice(['SCALE_OUT', 'SCALE_IN', 'SCALE_UP', 'SCALE_DOWN'])
                        },
                        "heal": {
                            "timeout": f"{random_int(120, 1200)}seconds",
                            "heal_type": random_choice(['RESTART', 'REBUILD', 'MIGRATE'])
                        }
                    },
                    "affinity_rules": {
                        "anti_affinity": random_choice(['HOST', 'ZONE', 'REGION']),
                        "affinity": random_choice(['SOFT', 'HARD', 'PREFERRED'])
                    }
                }
            },
            "orchestration_parameters": {
                "nfvo_id": f"nfvo_{uuid.uuid4().hex[:12]}",
                "vnfm_id": f"vnfm_{uuid.uuid4().hex[:12]}",
                "vim_id": f"vim_{uuid.uuid4().hex[:12]}",
                "orchestration_workflow": {
                    "workflow_id": f"workflow_{uuid.uuid4().hex[:16]}",
                    "workflow_version": f"{random_int(1, 3)}.{random_int(0, 9)}",
                    "execution_timeout": f"{random_int(600, 7200)}seconds",
                    "rollback_strategy": random_choice(['AUTOMATIC', 'MANUAL', 'CONDITIONAL'])
                }
            },
            "performance_requirements": {
                "throughput_requirement": f"{random_int(100, 100000)}Mbps",
                "latency_requirement": f"{random_float(0.1, 50)}ms",
                "availability_requirement": f"{random_float(99.9, 99.999)}%",
                "reliability_requirement": f"{random_float(99.5, 99.99)}%",
                "scalability_requirement": {
                    "horizontal_scaling": f"{random_int(1, 1000)}instances",
                    "vertical_scaling": f"{random_int(1, 64)}cores",
                    "auto_scaling_policy": random_choice(['CPU_BASED', 'MEMORY_BASED', 'NETWORK_BASED', 'CUSTOM_METRIC'])
                }
            }
        }
        
        return {**base_params, **deployment_params}
    
    def generate_extensive_parameters(self, slice_type: str, priority: str, location: str, complexity: int) -> Dict[str, Any]:
        """Generate extensive parameters utilizing much more of the available parameter space."""
        base_params = self.generate_constrained_parameters(slice_type, priority, location, complexity)
        
        # Add extensive additional parameters
        extensive_params = {
            "advanced_deployment_specification": {
                "multi_vendor_support": {
                    "primary_vendor": random.choice(['Ericsson', 'Nokia', 'Huawei', 'Samsung', 'ZTE']),
                    "secondary_vendor": random.choice(['Cisco', 'Juniper', 'Dell', 'HPE']),
                    "vendor_interoperability": random.choice(['FULL', 'PARTIAL', 'LIMITED']),
                    "vendor_lock_in_mitigation": random.choice(['ENABLED', 'DISABLED']),
                    "multi_vendor_orchestration": {
                        "orchestration_complexity": random.choice(['LOW', 'MEDIUM', 'HIGH', 'VERY_HIGH']),
                        "integration_testing_required": random.choice(['true', 'false']),
                        "compatibility_matrix": {
                            "network_functions": random.randint(10, 100),
                            "tested_combinations": random.randint(50, 500),
                            "certification_level": random.choice(['BASIC', 'ADVANCED', 'PREMIUM'])
                        }
                    }
                },
                "deployment_automation": {
                    "automation_level": random.choice(['MANUAL', 'SEMI_AUTOMATED', 'FULLY_AUTOMATED', 'AI_DRIVEN']),
                    "ci_cd_integration": {
                        "pipeline_stages": random.randint(5, 20),
                        "automated_testing": {
                            "unit_tests": random.choice(['true', 'false']),
                            "integration_tests": random.choice(['true', 'false']),
                            "performance_tests": random.choice(['true', 'false']),
                            "security_tests": random.choice(['true', 'false']),
                            "compliance_tests": random.choice(['true', 'false'])
                        },
                        "deployment_strategies": {
                            "blue_green": random.choice(['SUPPORTED', 'NOT_SUPPORTED']),
                            "canary": random.choice(['SUPPORTED', 'NOT_SUPPORTED']),
                            "rolling_update": random.choice(['SUPPORTED', 'NOT_SUPPORTED']),
                            "a_b_testing": random.choice(['SUPPORTED', 'NOT_SUPPORTED'])
                        }
                    },
                    "infrastructure_as_code": {
                        "iac_tool": random.choice(['Terraform', 'Ansible', 'CloudFormation', 'Pulumi']),
                        "configuration_management": random.choice(['Puppet', 'Chef', 'SaltStack', 'Ansible']),
                        "version_control": {
                            "repository_type": random.choice(['Git', 'SVN', 'Mercurial']),
                            "branching_strategy": random.choice(['GitFlow', 'GitHub Flow', 'GitLab Flow']),
                            "code_review_required": random.choice(['true', 'false'])
                        }
                    }
                },
                "cloud_native_features": {
                    "containerization": {
                        "container_runtime": random.choice(['Docker', 'Containerd', 'CRI-O', 'Podman']),
                        "image_registry": random.choice(['Docker Hub', 'Harbor', 'Quay', 'ECR', 'GCR']),
                        "image_scanning": {
                            "vulnerability_scanning": random.choice(['ENABLED', 'DISABLED']),
                            "compliance_scanning": random.choice(['ENABLED', 'DISABLED']),
                            "malware_scanning": random.choice(['ENABLED', 'DISABLED'])
                        },
                        "container_optimization": {
                            "multi_stage_builds": random.choice(['true', 'false']),
                            "distroless_images": random.choice(['true', 'false']),
                            "image_compression": random.choice(['true', 'false']),
                            "layer_caching": random.choice(['true', 'false'])
                        }
                    },
                    "service_mesh": {
                        "mesh_technology": random.choice(['Istio', 'Linkerd', 'Consul Connect', 'Envoy']),
                        "traffic_management": {
                            "load_balancing": random.choice(['ROUND_ROBIN', 'LEAST_CONN', 'WEIGHTED', 'CONSISTENT_HASH']),
                            "circuit_breaker": random.choice(['ENABLED', 'DISABLED']),
                            "retry_policy": {
                                "max_retries": random.randint(1, 10),
                                "retry_timeout": f"{random.randint(1, 30)}s",
                                "backoff_strategy": random.choice(['EXPONENTIAL', 'LINEAR', 'FIXED'])
                            },
                            "timeout_policy": {
                                "connection_timeout": f"{random.randint(1, 60)}s",
                                "request_timeout": f"{random.randint(1, 300)}s"
                            }
                        },
                        "security_policies": {
                            "mtls_enabled": random.choice(['true', 'false']),
                            "authorization_policies": random.randint(1, 50),
                            "network_policies": random.randint(1, 20)
                        },
                        "observability": {
                            "distributed_tracing": random.choice(['Jaeger', 'Zipkin', 'AWS X-Ray']),
                            "metrics_collection": random.choice(['Prometheus', 'DataDog', 'New Relic']),
                            "logging_aggregation": random.choice(['ELK Stack', 'Fluentd', 'Splunk'])
                        }
                    }
                }
            },
            "advanced_orchestration_parameters": {
                "multi_cloud_orchestration": {
                    "cloud_providers": random.sample(['AWS', 'Azure', 'GCP', 'IBM Cloud', 'Oracle Cloud'], random.randint(1, 3)),
                    "hybrid_cloud_strategy": random.choice(['CLOUD_FIRST', 'ON_PREMISE_FIRST', 'BALANCED']),
                    "cloud_bursting": {
                        "enabled": random.choice(['true', 'false']),
                        "burst_threshold": f"{random.randint(70, 90)}%",
                        "burst_cloud": random.choice(['AWS', 'Azure', 'GCP'])
                    },
                    "data_sovereignty": {
                        "data_residency_requirements": random.choice(['STRICT', 'MODERATE', 'FLEXIBLE']),
                        "cross_border_data_transfer": random.choice(['ALLOWED', 'RESTRICTED', 'PROHIBITED']),
                        "compliance_frameworks": random.sample(['GDPR', 'CCPA', 'HIPAA', 'SOX'], random.randint(1, 3))
                    }
                },
                "edge_orchestration": {
                    "edge_deployment_strategy": random.choice(['CENTRALIZED', 'DISTRIBUTED', 'FEDERATED']),
                    "edge_node_management": {
                        "node_discovery": random.choice(['AUTOMATIC', 'MANUAL', 'HYBRID']),
                        "node_health_monitoring": random.choice(['ENABLED', 'DISABLED']),
                        "node_failover": random.choice(['AUTOMATIC', 'MANUAL']),
                        "node_scaling": {
                            "horizontal_scaling": random.choice(['ENABLED', 'DISABLED']),
                            "vertical_scaling": random.choice(['ENABLED', 'DISABLED']),
                            "auto_scaling_triggers": random.sample(['CPU', 'MEMORY', 'NETWORK', 'CUSTOM'], random.randint(1, 3))
                        }
                    },
                    "edge_to_cloud_connectivity": {
                        "connectivity_type": random.choice(['VPN', 'DIRECT_CONNECT', 'SD_WAN']),
                        "bandwidth_allocation": f"{random.randint(10, 1000)}Mbps",
                        "latency_requirements": f"{random.uniform(1, 100)}ms",
                        "redundancy": random.choice(['ACTIVE_ACTIVE', 'ACTIVE_STANDBY', 'NONE'])
                    }
                },
                "workflow_orchestration": {
                    "workflow_engine": random.choice(['Airflow', 'Argo Workflows', 'Tekton', 'Jenkins']),
                    "workflow_complexity": {
                        "total_steps": random.randint(10, 100),
                        "parallel_execution": random.choice(['ENABLED', 'DISABLED']),
                        "conditional_logic": random.choice(['SIMPLE', 'COMPLEX', 'ADVANCED']),
                        "error_handling": {
                            "retry_mechanisms": random.choice(['ENABLED', 'DISABLED']),
                            "fallback_procedures": random.choice(['ENABLED', 'DISABLED']),
                            "manual_intervention": random.choice(['ALLOWED', 'NOT_ALLOWED'])
                        }
                    },
                    "workflow_optimization": {
                        "execution_time_optimization": random.choice(['ENABLED', 'DISABLED']),
                        "resource_optimization": random.choice(['ENABLED', 'DISABLED']),
                        "cost_optimization": random.choice(['ENABLED', 'DISABLED']),
                        "performance_monitoring": {
                            "execution_metrics": random.choice(['BASIC', 'DETAILED', 'COMPREHENSIVE']),
                            "bottleneck_detection": random.choice(['ENABLED', 'DISABLED']),
                            "performance_alerts": random.choice(['ENABLED', 'DISABLED'])
                        }
                    }
                }
            },
            "comprehensive_performance_requirements": {
                "detailed_sla_specifications": {
                    "availability_sla": {
                        "uptime_percentage": f"{random.uniform(99.0, 99.999)}%",
                        "planned_downtime": f"{random.randint(1, 24)}hours_per_month",
                        "unplanned_downtime": f"{random.randint(0, 4)}hours_per_month",
                        "availability_measurement": random.choice(['CALENDAR_TIME', 'BUSINESS_HOURS', 'CUSTOM']),
                        "penalty_clauses": {
                            "penalty_threshold": f"{random.uniform(98.0, 99.0)}%",
                            "penalty_rate": f"{random.uniform(1, 10)}%_of_monthly_fee",
                            "maximum_penalty": f"{random.uniform(10, 50)}%_of_monthly_fee"
                        }
                    },
                    "performance_sla": {
                        "response_time_sla": {
                            "average_response_time": f"{random.uniform(1, 100)}ms",
                            "95th_percentile": f"{random.uniform(10, 200)}ms",
                            "99th_percentile": f"{random.uniform(50, 500)}ms",
                            "maximum_response_time": f"{random.uniform(100, 1000)}ms"
                        },
                        "throughput_sla": {
                            "minimum_throughput": f"{random.randint(10, 1000)}Mbps",
                            "average_throughput": f"{random.randint(100, 10000)}Mbps",
                            "peak_throughput": f"{random.randint(1000, 100000)}Mbps",
                            "throughput_consistency": f"{random.uniform(90, 99)}%"
                        },
                        "scalability_sla": {
                            "horizontal_scaling_time": f"{random.randint(30, 300)}seconds",
                            "vertical_scaling_time": f"{random.randint(10, 120)}seconds",
                            "maximum_scale_out": f"{random.randint(10, 1000)}instances",
                            "scale_down_time": f"{random.randint(60, 600)}seconds"
                        }
                    }
                },
                "advanced_monitoring_requirements": {
                    "real_time_monitoring": {
                        "monitoring_frequency": f"{random.randint(1, 60)}seconds",
                        "metric_collection": random.choice(['PUSH', 'PULL', 'HYBRID']),
                        "data_retention": f"{random.randint(30, 365)}days",
                        "monitoring_coverage": {
                            "infrastructure_monitoring": random.choice(['BASIC', 'COMPREHENSIVE', 'ADVANCED']),
                            "application_monitoring": random.choice(['BASIC', 'COMPREHENSIVE', 'ADVANCED']),
                            "network_monitoring": random.choice(['BASIC', 'COMPREHENSIVE', 'ADVANCED']),
                            "security_monitoring": random.choice(['BASIC', 'COMPREHENSIVE', 'ADVANCED'])
                        }
                    },
                    "alerting_system": {
                        "alert_channels": random.sample(['EMAIL', 'SMS', 'SLACK', 'WEBHOOK', 'PAGERDUTY'], random.randint(2, 4)),
                        "alert_severity_levels": random.randint(3, 7),
                        "alert_correlation": random.choice(['ENABLED', 'DISABLED']),
                        "alert_suppression": {
                            "duplicate_suppression": random.choice(['ENABLED', 'DISABLED']),
                            "maintenance_mode": random.choice(['ENABLED', 'DISABLED']),
                            "intelligent_grouping": random.choice(['ENABLED', 'DISABLED'])
                        },
                        "escalation_procedures": {
                            "escalation_levels": random.randint(2, 5),
                            "escalation_timeouts": [f"{random.randint(5, 60)}minutes" for _ in range(3)],
                            "on_call_rotation": random.choice(['ENABLED', 'DISABLED'])
                        }
                    }
                }
            }
        }
        
        # Merge extensive parameters with base parameters
        merged_params = {**base_params, **extensive_params}
        
        return merged_params
    
    def generate_constrained_parameters(self, slice_type: str, priority: str, location: str, complexity: int) -> Dict[str, Any]:
        """Generate deployment parameters with realistic constraints."""
        base_params = {
            "timestamp": current_timestamp(),
            "request_id": f"REQ_{generate_unique_id()}",
            "correlation_id": f"CORR_{uuid.uuid4().hex[:16]}",
            "tenant_id": f"TENANT_{random_int(10000, 99999)}",
            "service_level": self._determine_service_level(priority, complexity),
            "network_topology": self._generate_constrained_topology(slice_type, location),
            "security_parameters": self._generate_constrained_security(slice_type, priority),
            "monitoring_parameters": self._generate_constrained_monitoring(complexity, priority)
        }
        
        # Add deployment-specific constrained parameters
        deployment_params = {
            "deployment_specification": {
                "network_function": self._select_appropriate_nf(slice_type),
                "vnf_descriptor": self._generate_vnf_descriptor(complexity, priority),
                "deployment_flavor": self._generate_deployment_flavor(slice_type, complexity),
                "instantiation_level_id": f"level_{min(5, max(1, complexity // 2))}",
                "additional_params": self._generate_additional_params(priority, complexity)
            },
            "orchestration_parameters": self._generate_orchestration_params(complexity),
            "performance_requirements": self._generate_performance_requirements(slice_type, priority)
        }
        
        return {**base_params, **deployment_params}
    
    def _determine_service_level(self, priority: str, complexity: int) -> str:
        """Determine service level based on priority and complexity."""
        if priority in ['EMERGENCY', 'CRITICAL'] and complexity >= 8:
            return 'PLATINUM_PLUS'
        elif priority in ['CRITICAL', 'HIGH'] and complexity >= 6:
            return 'PLATINUM'
        elif priority == 'HIGH' or complexity >= 7:
            return 'GOLD_PREMIUM'
        elif priority == 'MEDIUM' or complexity >= 5:
            return 'GOLD'
        elif complexity >= 3:
            return 'SILVER_PLUS'
        else:
            return 'SILVER'
    
    def _generate_constrained_topology(self, slice_type: str, location: str) -> Dict[str, Any]:
        """Generate network topology based on slice type and location constraints."""
        slice_category = self._categorize_slice_type(slice_type)
        location_category = self._categorize_location(location)
        
        # Select appropriate architecture
        if slice_category in ['URLLC', 'V2X']:
            architecture = 'Standalone_5G'  # SA for low latency
        elif location_category == 'rural':
            architecture = 'Non_Standalone_5G'  # NSA for coverage
        else:
            architecture = random.choice(['Standalone_5G', 'Non_Standalone_5G'])
        
        # Select deployment scenario based on location
        scenario_mapping = {
            'urban': random.choice(['Urban_Macro', 'Urban_Micro', 'Dense_Urban']),
            'rural': 'Rural_Macro',
            'highway': 'Urban_Macro',  # Wide coverage needed
            'industrial': 'Indoor_Hotspot'
        }
        
        return {
            "network_architecture": architecture,
            "deployment_scenario": scenario_mapping.get(location_category, 'Urban_Macro'),
            "spectrum_bands": self._select_spectrum_bands(slice_category),
            "antenna_configuration": self._select_antenna_config(slice_category, location_category),
            "backhaul": self._select_backhaul(location_category, slice_category)
        }
    
    def _categorize_slice_type(self, slice_type: str) -> str:
        """Categorize slice type into main domain categories."""
        slice_lower = slice_type.lower()
        if any(keyword in slice_lower for keyword in ['urllc', 'critical', 'autonomous', 'industrial']):
            if 'v2x' in slice_lower or 'vehicle' in slice_lower or 'autonomous' in slice_lower:
                return 'V2X'
            return 'URLLC'
        elif any(keyword in slice_lower for keyword in ['mmtc', 'iot', 'massive', 'agriculture', 'monitoring']):
            return 'mMTC'
        else:
            return 'eMBB'
    
    def _categorize_location(self, location: str) -> str:
        """Categorize location into main types."""
        location_lower = location.lower()
        if any(keyword in location_lower for keyword in ['highway', 'corridor', 'road']):
            return 'highway'
        elif any(keyword in location_lower for keyword in ['industrial', 'manufacturing', 'factory']):
            return 'industrial'
        elif any(keyword in location_lower for keyword in ['rural', 'farm', 'agriculture']):
            return 'rural'
        else:
            return 'urban'
    
    def _select_spectrum_bands(self, slice_category: str) -> Dict[str, str]:
        """Select appropriate spectrum bands for slice category."""
        if slice_category in ['URLLC', 'V2X']:
            # Prefer mid-band for balance of coverage and capacity
            return {
                "low_band": random.choice(['700MHz', '800MHz']),
                "mid_band": random.choice(['3.5GHz', '2.6GHz']),
                "high_band": random.choice(['28GHz', '39GHz'])
            }
        elif slice_category == 'eMBB':
            # Prefer high-band for capacity
            return {
                "low_band": random.choice(['600MHz', '700MHz']),
                "mid_band": random.choice(['1.8GHz', '2.1GHz']),
                "high_band": random.choice(['24GHz', '28GHz', '39GHz'])
            }
        else:  # mMTC
            # Prefer low-band for coverage
            return {
                "low_band": random.choice(['600MHz', '700MHz', '800MHz']),
                "mid_band": random.choice(['1.8GHz', '2.1GHz']),
                "high_band": random.choice(['24GHz', '28GHz'])
            }
    
    def _select_antenna_config(self, slice_category: str, location_category: str) -> Dict[str, str]:
        """Select appropriate antenna configuration."""
        if slice_category in ['URLLC', 'V2X'] or location_category == 'industrial':
            # High-performance antennas for critical applications
            return {
                "type": random.choice(['Massive_MIMO_64T64R', 'Massive_MIMO_32T32R']),
                "beamforming_capability": '3D_Beamforming',
                "sectorization": random.choice(['6_Sector', '12_Sector'])
            }
        else:
            return {
                "type": random.choice(['Massive_MIMO_32T32R', 'Traditional_MIMO_4T4R']),
                "beamforming_capability": random.choice(['3D_Beamforming', 'Horizontal_Beamforming']),
                "sectorization": random.choice(['3_Sector', '6_Sector'])
            }
    
    def _select_backhaul(self, location_category: str, slice_category: str) -> Dict[str, str]:
        """Select appropriate backhaul based on location and requirements."""
        if location_category == 'rural':
            backhaul_type = random.choice(['Microwave', 'Satellite', 'Hybrid_Fiber_Wireless'])
            capacity = f"{random_int(1, 10)}Gbps"
            latency = f"{random_float(2, 10)}ms"
        elif slice_category in ['URLLC', 'V2X']:
            backhaul_type = 'Fiber_Optic'  # Lowest latency
            capacity = f"{random_int(10, 100)}Gbps"
            latency = f"{random_float(0.1, 1)}ms"
        else:
            backhaul_type = random.choice(['Fiber_Optic', 'Microwave'])
            capacity = f"{random_int(5, 50)}Gbps"
            latency = f"{random_float(0.5, 5)}ms"
        
        return {
            "type": backhaul_type,
            "capacity": capacity,
            "latency": latency,
            "redundancy": "Active_Active" if slice_category in ['URLLC', 'V2X'] else random.choice(['Active_Active', 'Active_Standby'])
        }
    
    def _select_appropriate_nf(self, slice_type: str) -> str:
        """Select appropriate network function based on slice type."""
        slice_category = self._categorize_slice_type(slice_type)
        
        nf_preferences = {
            'URLLC': ['UPF', 'SMF', 'PCF', 'NWDAF'],
            'V2X': ['UPF', 'AMF', 'PCF', 'NWDAF'],
            'eMBB': ['UPF', 'SMF', 'AMF', 'PCF'],
            'mMTC': ['UPF', 'SMF', 'UDM', 'AUSF']
        }
        
        preferred_nfs = nf_preferences.get(slice_category, NETWORK_FUNCTIONS)
        return random.choice(preferred_nfs)
    
    def _generate_vnf_descriptor(self, complexity: int, priority: str) -> Dict[str, str]:
        """Generate VNF descriptor based on complexity and priority."""
        # Higher complexity and priority get more advanced versions
        version_major = min(5, max(1, complexity // 2))
        version_minor = random_int(0, 9)
        version_patch = random_int(0, 99)
        
        providers = ['Ericsson', 'Nokia', 'Huawei', 'Samsung', 'ZTE', 'Cisco']
        if priority in ['CRITICAL', 'EMERGENCY']:
            # Prefer established vendors for critical deployments
            providers = ['Ericsson', 'Nokia', 'Cisco']
        
        return {
            "vnfd_id": f"vnfd_{uuid.uuid4().hex[:12]}",
            "vnfd_version": f"{version_major}.{version_minor}.{version_patch}",
            "vnf_provider": random.choice(providers),
            "vnf_product_name": f"Advanced_NF_{random_int(1000, 9999)}",
            "vnf_software_version": f"SW_{version_major}.{version_minor}.{random_int(0, 999)}",
            "vnfd_invariant_id": f"invariant_{uuid.uuid4().hex[:16]}"
        }
    
    def _generate_deployment_flavor(self, slice_type: str, complexity: int) -> Dict[str, Any]:
        """Generate deployment flavor based on slice type and complexity."""
        slice_category = self.constraint_engine.categorize_slice_type(slice_type)
        
        # Determine optimization focus
        if slice_category in ['URLLC', 'V2X']:
            optimization = 'Network'  # Low latency focus
        elif slice_category == 'eMBB':
            optimization = 'Compute'  # High throughput focus
        else:
            optimization = 'Storage'  # Massive connections focus
        
        # Scale instances based on complexity
        base_instances = max(1, complexity // 2)
        
        return {
            "flavor_id": f"flavor_{uuid.uuid4().hex[:8]}",
            "description": f"High_Performance_{optimization}_Optimized",
            "vdu_profile": {
                "vdu_id": f"vdu_{uuid.uuid4().hex[:8]}",
                "min_number_of_instances": base_instances,
                "max_number_of_instances": base_instances * 10,
                "initial_number_of_instances": base_instances * 2
            }
        }
    
    def _generate_additional_params(self, priority: str, complexity: int) -> Dict[str, Any]:
        """Generate additional parameters based on priority and complexity."""
        # Timeout scales with complexity
        base_timeout = 300 + (complexity * 60)  # 300-900 seconds
        
        # Critical priorities get more conservative settings
        rollback_on_failure = priority in ['CRITICAL', 'EMERGENCY']
        skip_verification = priority not in ['CRITICAL', 'EMERGENCY'] and complexity < 5
        
        return {
            "lcm_operations_configuration": {
                "instantiate": {
                    "timeout": f"{base_timeout}seconds",
                    "rollback_on_failure": str(rollback_on_failure).lower(),
                    "skip_verification": str(skip_verification).lower()
                },
                "scale": {
                    "timeout": f"{base_timeout // 5}seconds",
                    "scale_type": random.choice(['SCALE_OUT', 'SCALE_UP'] if priority in ['HIGH', 'CRITICAL'] else ['SCALE_OUT', 'SCALE_IN', 'SCALE_UP', 'SCALE_DOWN'])
                },
                "heal": {
                    "timeout": f"{base_timeout // 3}seconds",
                    "heal_type": 'RESTART' if priority in ['CRITICAL', 'EMERGENCY'] else random.choice(['RESTART', 'REBUILD', 'MIGRATE'])
                }
            },
            "affinity_rules": {
                "anti_affinity": 'HOST' if priority in ['CRITICAL', 'EMERGENCY'] else random.choice(['HOST', 'ZONE', 'REGION']),
                "affinity": 'HARD' if priority in ['CRITICAL', 'EMERGENCY'] else random.choice(['SOFT', 'HARD', 'PREFERRED'])
            }
        }
    
    def _generate_orchestration_params(self, complexity: int) -> Dict[str, Any]:
        """Generate orchestration parameters based on complexity."""
        # More complex deployments get longer timeouts and more sophisticated rollback
        workflow_timeout = 600 + (complexity * 300)  # 600-3600 seconds
        
        rollback_strategy = 'AUTOMATIC' if complexity >= 7 else random.choice(['AUTOMATIC', 'MANUAL', 'CONDITIONAL'])
        
        return {
            "nfvo_id": f"nfvo_{uuid.uuid4().hex[:12]}",
            "vnfm_id": f"vnfm_{uuid.uuid4().hex[:12]}",
            "vim_id": f"vim_{uuid.uuid4().hex[:12]}",
            "orchestration_workflow": {
                "workflow_id": f"workflow_{uuid.uuid4().hex[:16]}",
                "workflow_version": f"{min(3, max(1, complexity // 3))}.{random_int(0, 9)}",
                "execution_timeout": f"{workflow_timeout}seconds",
                "rollback_strategy": rollback_strategy
            }
        }
    
    def _generate_performance_requirements(self, slice_type: str, priority: str) -> Dict[str, Any]:
        """Generate performance requirements based on slice type and priority."""
        slice_category = self._categorize_slice_type(slice_type)
        
        # Base requirements by slice category
        base_requirements = {
            'URLLC': {
                'throughput': (10, 100),
                'latency': (0.1, 5),
                'availability': (99.999, 99.9999),
                'reliability': (99.99, 99.999)
            },
            'V2X': {
                'throughput': (10, 1000),
                'latency': (1, 10),
                'availability': (99.99, 99.999),
                'reliability': (99.9, 99.99)
            },
            'eMBB': {
                'throughput': (100, 10000),
                'latency': (10, 50),
                'availability': (99.9, 99.99),
                'reliability': (99.5, 99.9)
            },
            'mMTC': {
                'throughput': (1, 10),
                'latency': (100, 1000),
                'availability': (99.0, 99.9),
                'reliability': (99.0, 99.5)
            }
        }
        
        reqs = base_requirements.get(slice_category, base_requirements['eMBB'])
        
        # Priority affects requirements
        priority_multiplier = {
            'EMERGENCY': 1.5,
            'CRITICAL': 1.3,
            'HIGH': 1.1,
            'MEDIUM': 1.0,
            'LOW': 0.8
        }.get(priority, 1.0)
        
        throughput = int(random.uniform(*reqs['throughput']) * priority_multiplier)
        latency = random.uniform(*reqs['latency']) / priority_multiplier
        availability = min(99.9999, random.uniform(*reqs['availability']) * (1 + (priority_multiplier - 1) * 0.001))
        reliability = min(99.999, random.uniform(*reqs['reliability']) * (1 + (priority_multiplier - 1) * 0.001))
        
        # Scaling requirements
        if priority in ['CRITICAL', 'EMERGENCY']:
            scaling_policy = 'CPU_BASED'  # Most responsive
            max_instances = random_int(100, 1000)
        else:
            scaling_policy = random.choice(['CPU_BASED', 'MEMORY_BASED', 'NETWORK_BASED', 'CUSTOM_METRIC'])
            max_instances = random_int(10, 100)
        
        return {
            "throughput_requirement": f"{throughput}Mbps",
            "latency_requirement": f"{latency:.1f}ms",
            "availability_requirement": f"{availability:.3f}%",
            "reliability_requirement": f"{reliability:.2f}%",
            "scalability_requirement": {
                "horizontal_scaling": f"{max_instances}instances",
                "vertical_scaling": f"{random_int(4, 64)}cores",
                "auto_scaling_policy": scaling_policy
            }
        }
    
    def _generate_constrained_security(self, slice_type: str, priority: str) -> Dict[str, Any]:
        """Generate security parameters based on slice type and priority."""
        slice_category = self._categorize_slice_type(slice_type)
        
        # Critical slices and high priority get stronger security
        if slice_category in ['URLLC', 'V2X'] or priority in ['CRITICAL', 'EMERGENCY']:
            encryption = random.choice(['256_NEA1', '256_NEA2'])
            integrity = random.choice(['256_NIA1', '256_NIA2'])
            key_length = '256_bit'
            rotation_interval = random_int(1, 6)  # More frequent rotation
        else:
            encryption = random.choice(['128_NEA1', '128_NEA2', '128_NEA3'])
            integrity = random.choice(['128_NIA1', '128_NIA2', '128_NIA3'])
            key_length = random.choice(['128_bit', '256_bit'])
            rotation_interval = random_int(6, 24)
        
        return {
            "authentication_method": random.choice(['5G_AKA', 'EAP_AKA_Prime']),
            "encryption_algorithm": encryption,
            "integrity_protection": integrity,
            "key_management": {
                "kdf": random.choice(['HMAC_SHA256', 'HMAC_SHA384', 'HMAC_SHA512']),
                "key_length": key_length,
                "key_rotation_interval": f"{rotation_interval}hours",
                "key_derivation_counter": random_int(1, 65535)
            },
            "privacy_protection": {
                "supi_concealment": "ENABLED",
                "temporary_identifiers": random.choice(['5G_GUTI', '5G_TMSI']),
                "location_privacy": "FULL_PROTECTION" if priority in ['CRITICAL', 'EMERGENCY'] else random.choice(['FULL_PROTECTION', 'PARTIAL_PROTECTION'])
            }
        }
    
    def _generate_constrained_monitoring(self, complexity: int, priority: str) -> Dict[str, Any]:
        """Generate monitoring parameters based on complexity and priority."""
        # More complex and critical deployments get more intensive monitoring
        if complexity >= 8 or priority in ['CRITICAL', 'EMERGENCY']:
            sampling_rate = random_int(80, 100)
            aggregation_interval = random_int(1, 10)
            retention_period = random_int(90, 365)
        elif complexity >= 5 or priority == 'HIGH':
            sampling_rate = random_int(50, 80)
            aggregation_interval = random_int(10, 30)
            retention_period = random_int(30, 90)
        else:
            sampling_rate = random_int(20, 50)
            aggregation_interval = random_int(30, 60)
            retention_period = random_int(7, 30)
        
        return {
            "kpi_metrics": {
                "collection_enabled": True,
                "sampling_rate": f"{sampling_rate}%",
                "key_metrics": self._select_key_metrics(complexity, priority)
            },
            "alerting_configuration": {
                "severity_levels": ['CRITICAL', 'MAJOR', 'MINOR', 'WARNING', 'INFO'],
                "escalation_policy": {
                    "level1": f"{random_int(1, 3)}minutes" if priority in ['CRITICAL', 'EMERGENCY'] else f"{random_int(1, 5)}minutes",
                    "level2": f"{random_int(3, 10)}minutes" if priority in ['CRITICAL', 'EMERGENCY'] else f"{random_int(5, 15)}minutes",
                    "level3": f"{random_int(10, 30)}minutes" if priority in ['CRITICAL', 'EMERGENCY'] else f"{random_int(15, 60)}minutes"
                }
            },
            "analytics_configuration": {
                "data_collection": {
                    "aggregation_interval": f"{aggregation_interval}seconds",
                    "retention_period": f"{retention_period}days",
                    "compression_enabled": complexity >= 5
                }
            }
        }
    
    def _select_key_metrics(self, complexity: int, priority: str) -> List[str]:
        """Select key metrics based on complexity and priority."""
        base_metrics = ['latency', 'throughput', 'availability', 'error_rate']
        
        if complexity >= 7:
            base_metrics.extend(['jitter', 'packet_loss', 'resource_utilization'])
        
        if priority in ['CRITICAL', 'EMERGENCY']:
            base_metrics.extend(['security_events', 'performance_degradation'])
        
        if complexity >= 8:
            base_metrics.extend(['predictive_analytics', 'anomaly_detection'])
        
        return base_metrics
    @staticmethod
    def generate_description(params: Dict[str, Any], location: str, slice_type: str) -> str:
        """Generate sophisticated deployment intent description."""
        nf = params.get("deployment_specification", {}).get("network_function", random_choice(NETWORK_FUNCTIONS))
        flavor = params.get("deployment_specification", {}).get("deployment_flavor", {}).get("description", "High_Performance")
        complexity = random_choice(['sophisticated', 'advanced', 'comprehensive', 'intelligent', 'adaptive'])
        
        return (f"Execute {complexity} deployment of {nf} network function with "
                f"{flavor.lower().replace('_', ' ')} configuration at {location} supporting "
                f"{slice_type.replace('_', ' ')} service requirements with advanced orchestration "
                f"capabilities, comprehensive security hardening, and intelligent resource "
                f"optimization algorithms for research-grade network performance analysis")
