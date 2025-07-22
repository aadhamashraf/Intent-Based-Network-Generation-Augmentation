import uuid
import random
from typing import Dict, Any, List
from typing import Dict, Any
from .Constants_Enums import NETWORK_FUNCTIONS
from .Parameter_Generator import ParameterGenerator
from .utilis_generator import current_timestamp, generate_unique_id, random_choice, random_int, random_float

class DeploymentIntentGenerator:
    """Generator for deployment intent records."""
    
    def __init__(self):
        # Import here to avoid circular imports
        try:
            from .Constraint_Engine import ConstraintEngine
            self.constraint_engine = ConstraintEngine()
        except ImportError:
            self.constraint_engine = None
    
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
        slice_category = self.constraint_engine.categorize_slice_type(slice_type)
        location_category = self.constraint_engine.categorize_location(location)
        
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
        slice_category = self.constraint_engine.categorize_slice_type(slice_type)
        
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
        slice_category = self.constraint_engine.categorize_slice_type(slice_type)
        
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
        slice_category = self.constraint_engine.categorize_slice_type(slice_type)
        
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
