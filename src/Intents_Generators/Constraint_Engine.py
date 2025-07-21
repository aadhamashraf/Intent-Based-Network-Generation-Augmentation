"""
Constraint Engine for Realistic Intent Generation

This module implements sophisticated constraint-based generation ensuring
logical consistency, domain-specific validity, and realistic interdependencies
between all intent parameters.
"""

import random
import uuid
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
from .Constants_Enums import IntentType, Priority, NETWORK_FUNCTIONS, ADVANCED_SLICE_TYPES, ADVANCED_LOCATIONS

@dataclass
class ConstraintRule:
    """Represents a constraint rule for parameter generation."""
    condition: str
    parameter: str
    value_generator: callable
    weight: float = 1.0

@dataclass
class DomainProfile:
    """Domain-specific parameter profiles."""
    latency_range: Tuple[float, float]
    throughput_range: Tuple[int, int]
    reliability_range: Tuple[float, float]
    complexity_bias: float
    priority_bias: float
    compliance_standards: List[str]

class ConstraintEngine:
    """Advanced constraint engine for realistic intent generation."""
    
    def __init__(self):
        self.domain_profiles = self._initialize_domain_profiles()
        self.slice_constraints = self._initialize_slice_constraints()
        self.location_constraints = self._initialize_location_constraints()
        self.interdependency_rules = self._initialize_interdependency_rules()
        
    def _initialize_domain_profiles(self) -> Dict[str, DomainProfile]:
        """Initialize domain-specific parameter profiles."""
        return {
            'URLLC': DomainProfile(
                latency_range=(0.1, 5.0),
                throughput_range=(1, 100),
                reliability_range=(99.999, 99.9999),
                complexity_bias=0.8,  # Higher complexity
                priority_bias=0.9,    # Higher priority
                compliance_standards=['3GPP_TS_23.501', '3GPP_TS_28.312', 'ETSI_NFV_SOL_001']
            ),
            'eMBB': DomainProfile(
                latency_range=(10, 50),
                throughput_range=(100, 10000),
                reliability_range=(99.9, 99.99),
                complexity_bias=0.5,
                priority_bias=0.4,
                compliance_standards=['3GPP_TS_23.502', '3GPP_TS_28.313', 'ITU_T_Y.3011']
            ),
            'mMTC': DomainProfile(
                latency_range=(100, 1000),
                throughput_range=(1, 10),
                reliability_range=(99.0, 99.9),
                complexity_bias=0.3,
                priority_bias=0.2,
                compliance_standards=['3GPP_TS_23.503', 'ITU_T_Y.3012', 'IETF_RFC_8309']
            ),
            'V2X': DomainProfile(
                latency_range=(1, 10),
                throughput_range=(10, 1000),
                reliability_range=(99.99, 99.999),
                complexity_bias=0.9,
                priority_bias=0.95,
                compliance_standards=['3GPP_TS_23.287', '3GPP_TS_22.186', 'ETSI_EN_302_637']
            )
        }
    
    def _initialize_slice_constraints(self) -> Dict[str, Dict[str, Any]]:
        """Initialize slice-specific constraints."""
        return {
            'eMBB_Ultra_HD_Streaming': {
                'domain_category': 'eMBB',
                'min_throughput': 100,
                'max_latency': 20,
                'min_reliability': 99.9,
                'complexity_range': (4, 7),
                'priority_weights': {'HIGH': 0.4, 'MEDIUM': 0.5, 'LOW': 0.1},
                'preferred_locations': ['urban', 'stadium', 'mall'],
                'required_nfs': ['UPF', 'SMF', 'AMF']
            },
            'URLLC_Autonomous_Vehicles': {
                'domain_category': 'V2X',
                'min_throughput': 10,
                'max_latency': 5,
                'min_reliability': 99.999,
                'complexity_range': (8, 10),
                'priority_weights': {'CRITICAL': 0.6, 'HIGH': 0.3, 'EMERGENCY': 0.1},
                'preferred_locations': ['highway', 'urban', 'intersection'],
                'required_nfs': ['UPF', 'AMF', 'PCF', 'NWDAF']
            },
            'URLLC_Industrial_Automation': {
                'domain_category': 'URLLC',
                'min_throughput': 1,
                'max_latency': 1,
                'min_reliability': 99.9999,
                'complexity_range': (7, 10),
                'priority_weights': {'CRITICAL': 0.5, 'HIGH': 0.4, 'EMERGENCY': 0.1},
                'preferred_locations': ['industrial', 'manufacturing', 'factory'],
                'required_nfs': ['UPF', 'SMF', 'PCF', 'NWDAF']
            },
            'mMTC_Smart_Agriculture': {
                'domain_category': 'mMTC',
                'min_throughput': 0.1,
                'max_latency': 1000,
                'min_reliability': 99.0,
                'complexity_range': (2, 5),
                'priority_weights': {'MEDIUM': 0.5, 'LOW': 0.4, 'HIGH': 0.1},
                'preferred_locations': ['rural', 'agricultural', 'farm'],
                'required_nfs': ['UPF', 'SMF', 'UDM']
            }
        }
    
    def _initialize_location_constraints(self) -> Dict[str, Dict[str, Any]]:
        """Initialize location-specific constraints."""
        return {
            'highway': {
                'mobility_factor': 0.9,
                'coverage_complexity': 0.8,
                'preferred_slices': ['V2X', 'URLLC'],
                'latency_penalty': 0.8,  # Lower latency required
                'reliability_boost': 1.2
            },
            'urban': {
                'mobility_factor': 0.6,
                'coverage_complexity': 0.7,
                'preferred_slices': ['eMBB', 'URLLC'],
                'latency_penalty': 0.9,
                'reliability_boost': 1.1
            },
            'industrial': {
                'mobility_factor': 0.1,
                'coverage_complexity': 0.9,
                'preferred_slices': ['URLLC', 'mMTC'],
                'latency_penalty': 0.5,  # Very low latency
                'reliability_boost': 1.3
            },
            'rural': {
                'mobility_factor': 0.3,
                'coverage_complexity': 0.4,
                'preferred_slices': ['mMTC', 'eMBB'],
                'latency_penalty': 1.2,  # Higher latency acceptable
                'reliability_boost': 0.9
            }
        }
    
    def _initialize_interdependency_rules(self) -> List[ConstraintRule]:
        """Initialize interdependency rules between parameters."""
        return [
            # Priority-Latency correlation
            ConstraintRule(
                condition="priority in ['CRITICAL', 'EMERGENCY']",
                parameter="latency_multiplier",
                value_generator=lambda: random.uniform(0.3, 0.7),
                weight=0.9
            ),
            # Complexity-Resource correlation
            ConstraintRule(
                condition="technical_complexity >= 8",
                parameter="resource_multiplier",
                value_generator=lambda: random.uniform(1.5, 3.0),
                weight=0.8
            ),
            # Slice-Priority correlation
            ConstraintRule(
                condition="slice_category == 'V2X'",
                parameter="priority_boost",
                value_generator=lambda: random.uniform(0.8, 1.0),
                weight=0.9
            )
        ]
    
    def categorize_slice_type(self, slice_type: str) -> str:
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
    
    def categorize_location(self, location: str) -> str:
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
    
    def generate_constrained_priority(self, slice_type: str, location: str, intent_type: str) -> str:
        """Generate priority based on slice type, location, and intent type constraints."""
        slice_category = self.categorize_slice_type(slice_type)
        location_category = self.categorize_location(location)
        
        # Get base weights from slice constraints
        slice_constraints = self.slice_constraints.get(slice_type, {})
        priority_weights = slice_constraints.get('priority_weights', {
            'LOW': 0.3, 'MEDIUM': 0.4, 'HIGH': 0.2, 'CRITICAL': 0.08, 'EMERGENCY': 0.02
        })
        
        # Adjust weights based on location
        location_constraints = self.location_constraints.get(location_category, {})
        if location_category in ['highway', 'industrial']:
            # Boost higher priorities for critical locations
            priority_weights['CRITICAL'] = priority_weights.get('CRITICAL', 0.1) * 2
            priority_weights['HIGH'] = priority_weights.get('HIGH', 0.2) * 1.5
        
        # Adjust weights based on intent type
        if intent_type in ['PERFORMANCE_ASSURANCE', 'FEASIBILITY_CHECK']:
            priority_weights['HIGH'] = priority_weights.get('HIGH', 0.2) * 1.3
            priority_weights['CRITICAL'] = priority_weights.get('CRITICAL', 0.1) * 1.2
        
        # Normalize weights
        total_weight = sum(priority_weights.values())
        normalized_weights = {k: v/total_weight for k, v in priority_weights.items()}
        
        # Weighted random selection
        priorities = list(normalized_weights.keys())
        weights = list(normalized_weights.values())
        return random.choices(priorities, weights=weights)[0]
    
    def generate_constrained_complexity(self, slice_type: str, priority: str, intent_type: str) -> int:
        """Generate technical complexity based on constraints."""
        slice_constraints = self.slice_constraints.get(slice_type, {})
        complexity_range = slice_constraints.get('complexity_range', (3, 7))
        
        # Base complexity from slice type
        base_complexity = random.randint(*complexity_range)
        
        # Adjust based on priority
        priority_adjustments = {
            'EMERGENCY': 2,
            'CRITICAL': 1,
            'HIGH': 0,
            'MEDIUM': -1,
            'LOW': -2
        }
        base_complexity += priority_adjustments.get(priority, 0)
        
        # Adjust based on intent type
        intent_adjustments = {
            'FEASIBILITY_CHECK': 2,
            'PERFORMANCE_ASSURANCE': 1,
            'DEPLOYMENT': 0,
            'MODIFICATION': 1,
            'REPORT_REQUEST': -1,
            'NOTIFICATION_REQUEST': -1
        }
        base_complexity += intent_adjustments.get(intent_type, 0)
        
        # Ensure within valid range
        return max(1, min(10, base_complexity))
    
    def generate_constrained_qos_parameters(self, slice_type: str, priority: str, location: str) -> Dict[str, Any]:
        """Generate QoS parameters with realistic constraints."""
        slice_category = self.categorize_slice_type(slice_type)
        location_category = self.categorize_location(location)
        
        # Get domain profile
        domain_profile = self.domain_profiles.get(slice_category, self.domain_profiles['eMBB'])
        location_constraints = self.location_constraints.get(location_category, {})
        
        # Generate latency with constraints
        base_latency_range = domain_profile.latency_range
        latency_penalty = location_constraints.get('latency_penalty', 1.0)
        
        # Priority affects latency requirements
        priority_latency_multiplier = {
            'EMERGENCY': 0.3,
            'CRITICAL': 0.5,
            'HIGH': 0.7,
            'MEDIUM': 1.0,
            'LOW': 1.3
        }.get(priority, 1.0)
        
        adjusted_latency_range = (
            base_latency_range[0] * latency_penalty * priority_latency_multiplier,
            base_latency_range[1] * latency_penalty * priority_latency_multiplier
        )
        
        latency = round(random.uniform(*adjusted_latency_range), 2)
        
        # Generate throughput with constraints
        base_throughput_range = domain_profile.throughput_range
        throughput = random.randint(*base_throughput_range)
        
        # Priority affects throughput requirements
        if priority in ['CRITICAL', 'EMERGENCY']:
            throughput = int(throughput * random.uniform(1.2, 2.0))
        
        # Generate reliability with constraints
        base_reliability_range = domain_profile.reliability_range
        reliability_boost = location_constraints.get('reliability_boost', 1.0)
        
        reliability = min(99.9999, base_reliability_range[1] * reliability_boost)
        if priority in ['CRITICAL', 'EMERGENCY']:
            reliability = min(99.9999, reliability * 1.001)  # Slight boost for critical
        
        # Generate other QoS parameters
        packet_error_rate = self._generate_packet_error_rate(slice_category, priority)
        jitter = self._generate_jitter(latency, slice_category)
        
        return {
            "qos_flow_identifier": self._get_appropriate_5qi(slice_category),
            "guaranteed_bit_rate": f"{max(1, throughput // 10)}Mbps",
            "maximum_bit_rate": f"{throughput}Mbps",
            "packet_delay_budget": f"{latency}ms",
            "packet_error_rate": f"{packet_error_rate}",
            "priority_level": self._get_priority_level(priority),
            "preemption_capability": "MAY_PREEMPT" if priority in ['CRITICAL', 'EMERGENCY'] else "SHALL_NOT_PREEMPT",
            "preemption_vulnerability": "NOT_PREEMPTABLE" if priority in ['CRITICAL', 'EMERGENCY'] else "PREEMPTABLE",
            "reflective_qos": "ENABLED" if slice_category in ['URLLC', 'V2X'] else "DISABLED",
            "jitter_tolerance": f"{jitter}ms"
        }
    
    def _generate_packet_error_rate(self, slice_category: str, priority: str) -> str:
        """Generate realistic packet error rate."""
        base_rates = {
            'URLLC': (1e-6, 1e-5),
            'V2X': (1e-6, 1e-5),
            'eMBB': (1e-4, 1e-3),
            'mMTC': (1e-3, 1e-2)
        }
        
        rate_range = base_rates.get(slice_category, base_rates['eMBB'])
        rate = random.uniform(*rate_range)
        
        # Priority affects error rate requirements
        if priority in ['CRITICAL', 'EMERGENCY']:
            rate *= 0.1  # Much lower error rate
        
        return f"{rate:.2e}"
    
    def _generate_jitter(self, latency: float, slice_category: str) -> float:
        """Generate realistic jitter based on latency and slice category."""
        # Jitter is typically 10-20% of latency for URLLC, higher for others
        jitter_factors = {
            'URLLC': (0.05, 0.1),
            'V2X': (0.05, 0.15),
            'eMBB': (0.1, 0.3),
            'mMTC': (0.2, 0.5)
        }
        
        factor_range = jitter_factors.get(slice_category, jitter_factors['eMBB'])
        factor = random.uniform(*factor_range)
        
        return round(latency * factor, 2)
    
    def _get_appropriate_5qi(self, slice_category: str) -> str:
        """Get appropriate 5QI based on slice category."""
        qqi_mappings = {
            'URLLC': ['5QI_82_Discrete_Automation_Small_Packets', '5QI_83_Discrete_Automation_Large_Packets'],
            'V2X': ['5QI_75_V2X_Messages', '5QI_79_V2X_Video'],
            'eMBB': ['5QI_7_Voice_Video_Gaming', '5QI_8_Video_TCP_Premium'],
            'mMTC': ['5QI_9_Video_TCP_Background', '5QI_6_Video_TCP']
        }
        
        return random.choice(qqi_mappings.get(slice_category, qqi_mappings['eMBB']))
    
    def _get_priority_level(self, priority: str) -> int:
        """Map priority to 3GPP priority level."""
        priority_levels = {
            'EMERGENCY': 1,
            'CRITICAL': random.randint(1, 5),
            'HIGH': random.randint(5, 15),
            'MEDIUM': random.randint(15, 50),
            'LOW': random.randint(50, 127)
        }
        
        return priority_levels.get(priority, 50)
    
    def generate_constrained_resource_allocation(self, complexity: int, slice_type: str, priority: str) -> Dict[str, Any]:
        """Generate resource allocation based on complexity and requirements."""
        slice_category = self.categorize_slice_type(slice_type)
        
        # Base resource requirements
        base_resources = {
            'URLLC': {'cpu_cores': (4, 16), 'memory_gb': (8, 64), 'storage_gb': (100, 1000)},
            'V2X': {'cpu_cores': (8, 32), 'memory_gb': (16, 128), 'storage_gb': (200, 2000)},
            'eMBB': {'cpu_cores': (2, 8), 'memory_gb': (4, 32), 'storage_gb': (50, 500)},
            'mMTC': {'cpu_cores': (1, 4), 'memory_gb': (2, 16), 'storage_gb': (20, 200)}
        }
        
        resources = base_resources.get(slice_category, base_resources['eMBB'])
        
        # Scale based on complexity
        complexity_multiplier = 0.5 + (complexity / 10) * 1.5  # 0.5 to 2.0
        
        cpu_cores = int(random.randint(*resources['cpu_cores']) * complexity_multiplier)
        memory_gb = int(random.randint(*resources['memory_gb']) * complexity_multiplier)
        storage_gb = int(random.randint(*resources['storage_gb']) * complexity_multiplier)
        
        # Priority affects resource allocation
        if priority in ['CRITICAL', 'EMERGENCY']:
            cpu_cores = int(cpu_cores * 1.5)
            memory_gb = int(memory_gb * 1.5)
        
        return {
            "compute_resources": {
                "cpu_architecture": random.choice(['x86_64', 'ARM64']),
                "cpu_cores": cpu_cores,
                "cpu_frequency": f"{random.uniform(2.0, 4.0):.1f}GHz",
                "memory_size": f"{memory_gb}GB",
                "memory_type": random.choice(['DDR4', 'DDR5']),
                "storage_capacity": f"{storage_gb}GB",
                "storage_type": random.choice(['NVMe_SSD', 'SATA_SSD'])
            },
            "network_resources": {
                "bandwidth_allocation": f"{random.randint(100, 10000)}Mbps",
                "latency_requirement": f"{random.uniform(0.1, 100)}ms",
                "connection_density": f"{random.randint(1000, 1000000)}_devices_per_km2"
            }
        }
    
    def generate_constrained_compliance_standards(self, slice_type: str, intent_type: str, domain: str) -> List[str]:
        """Generate appropriate compliance standards based on context."""
        slice_category = self.categorize_slice_type(slice_type)
        
        # Get base standards from domain profile
        domain_profile = self.domain_profiles.get(slice_category, self.domain_profiles['eMBB'])
        base_standards = domain_profile.compliance_standards.copy()
        
        # Add intent-specific standards
        intent_standards = {
            'DEPLOYMENT': ['3GPP_TS_28.312', 'ETSI_NFV_SOL_001'],
            'MODIFICATION': ['3GPP_TS_28.313', 'TM_Forum_IG1176'],
            'PERFORMANCE_ASSURANCE': ['3GPP_TS_28.314', 'ITU_T_Y.3011'],
            'REPORT_REQUEST': ['3GPP_TS_28.315', 'TM_Forum_IG1177'],
            'FEASIBILITY_CHECK': ['ETSI_NFV_SOL_002', 'ONF_TR_526'],
            'NOTIFICATION_REQUEST': ['IETF_RFC_8309', 'IETF_RFC_8329']
        }
        
        base_standards.extend(intent_standards.get(intent_type, []))
        
        # Add domain-specific standards
        if 'security' in slice_type.lower() or 'audit' in slice_type.lower():
            base_standards.extend(['ISO_27001', 'NIST_CYBERSECURITY_FRAMEWORK'])
        
        if slice_category == 'V2X':
            base_standards.extend(['ETSI_EN_302_637', '3GPP_TS_22.186'])
        
        # Remove duplicates and return subset
        unique_standards = list(set(base_standards))
        return random.sample(unique_standards, min(len(unique_standards), random.randint(2, 4)))
    
    def generate_constrained_research_context(self, slice_type: str, complexity: int, priority: str) -> str:
        """Generate appropriate research context based on parameters."""
        slice_category = self.categorize_slice_type(slice_type)
        
        research_contexts = {
            'URLLC': [
                'Ultra_Reliable_Low_Latency_Communication_Study',
                'Industrial_IoT_Network_Optimization',
                'Critical_Infrastructure_Protection_Research',
                'Real_Time_Control_Systems_Analysis'
            ],
            'V2X': [
                'Vehicular_Communication_Networks_Research',
                'Autonomous_Vehicle_Connectivity_Study',
                'Intelligent_Transportation_Systems_Analysis',
                'Connected_Vehicle_Safety_Research'
            ],
            'eMBB': [
                'Enhanced_Mobile_Broadband_Optimization',
                'High_Throughput_Applications_Study',
                'Multimedia_Service_Quality_Research',
                'Bandwidth_Intensive_Applications_Analysis'
            ],
            'mMTC': [
                'Massive_Machine_Type_Communication_Study',
                'IoT_Scalability_Research',
                'Sensor_Network_Optimization',
                'Large_Scale_Device_Connectivity_Analysis'
            ]
        }
        
        contexts = research_contexts.get(slice_category, research_contexts['eMBB'])
        
        # Add complexity-based modifiers
        if complexity >= 8:
            contexts = [ctx.replace('Study', 'Advanced_Study').replace('Research', 'Advanced_Research') 
                       for ctx in contexts]
        
        # Add priority-based modifiers
        if priority in ['CRITICAL', 'EMERGENCY']:
            contexts = [ctx.replace('Analysis', 'Critical_Analysis').replace('Study', 'Mission_Critical_Study') 
                       for ctx in contexts]
        
        return random.choice(contexts)