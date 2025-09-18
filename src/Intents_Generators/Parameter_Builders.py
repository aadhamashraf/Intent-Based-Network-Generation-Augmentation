"""
Modular Parameter Builders

This module provides modular, reusable parameter building functions to replace
monolithic parameter dictionaries and improve maintainability.
"""

import random
import uuid
from typing import Dict, Any, List
from .utilis_generator import random_choice, random_int, random_float, current_timestamp


class SecurityParameterBuilder:
    """Builder for security-related parameters."""
    
    @staticmethod
    def build_authentication_block(security_level: str = 'STANDARD') -> Dict[str, Any]:
        """Build authentication parameter block."""
        if security_level == 'HIGH':
            return {
                "authentication_method": random_choice(['5G_AKA', 'EAP_AKA_Prime']),
                "multi_factor_enabled": True,
                "certificate_validation": 'STRICT',
                "session_timeout": f"{random_int(15, 60)}minutes"
            }
        else:
            return {
                "authentication_method": random_choice(['5G_AKA', 'EAP_TLS', 'Certificate_Based']),
                "multi_factor_enabled": random_choice([True, False]),
                "certificate_validation": random_choice(['STRICT', 'STANDARD']),
                "session_timeout": f"{random_int(60, 240)}minutes"
            }
    
    @staticmethod
    def build_encryption_block(security_level: str = 'STANDARD') -> Dict[str, Any]:
        """Build encryption parameter block."""
        if security_level == 'HIGH':
            return {
                "encryption_algorithm": random_choice(['256_NEA1', '256_NEA2']),
                "key_length": '256_bit',
                "key_rotation_interval": f"{random_int(1, 6)}hours",
                "perfect_forward_secrecy": True
            }
        else:
            return {
                "encryption_algorithm": random_choice(['128_NEA1', '128_NEA2', '256_NEA1']),
                "key_length": random_choice(['128_bit', '256_bit']),
                "key_rotation_interval": f"{random_int(6, 24)}hours",
                "perfect_forward_secrecy": random_choice([True, False])
            }
    
    @staticmethod
    def build_privacy_block(privacy_level: str = 'STANDARD') -> Dict[str, Any]:
        """Build privacy protection parameter block."""
        if privacy_level == 'HIGH':
            return {
                "supi_concealment": "ENABLED",
                "location_privacy": "FULL_PROTECTION",
                "temporary_identifiers": "5G_GUTI",
                "identity_anonymization": True
            }
        else:
            return {
                "supi_concealment": random_choice(["ENABLED", "DISABLED"]),
                "location_privacy": random_choice(["FULL_PROTECTION", "PARTIAL_PROTECTION"]),
                "temporary_identifiers": random_choice(["5G_GUTI", "5G_TMSI"]),
                "identity_anonymization": random_choice([True, False])
            }


class NetworkParameterBuilder:
    """Builder for network-related parameters."""
    
    @staticmethod
    def build_topology_block(slice_category: str, location_category: str) -> Dict[str, Any]:
        """Build network topology parameter block."""
        architecture_mapping = {
            'URLLC': 'Standalone_5G',
            'V2X': 'Standalone_5G',
            'eMBB': random_choice(['Standalone_5G', 'Non_Standalone_5G']),
            'mMTC': random_choice(['Non_Standalone_5G', 'Hybrid_4G_5G'])
        }
        
        scenario_mapping = {
            'urban': random_choice(['Urban_Macro', 'Urban_Micro', 'Dense_Urban']),
            'rural': 'Rural_Macro',
            'highway': 'Urban_Macro',
            'industrial': 'Indoor_Hotspot'
        }
        
        return {
            "network_architecture": architecture_mapping.get(slice_category, 'Standalone_5G'),
            "deployment_scenario": scenario_mapping.get(location_category, 'Urban_Macro'),
            "spectrum_allocation": NetworkParameterBuilder._build_spectrum_block(slice_category),
            "antenna_system": NetworkParameterBuilder._build_antenna_block(slice_category, location_category)
        }
    
    @staticmethod
    def _build_spectrum_block(slice_category: str) -> Dict[str, str]:
        """Build spectrum allocation block."""
        spectrum_mapping = {
            'URLLC': {
                "low_band": random_choice(['700MHz', '800MHz']),
                "mid_band": random_choice(['3.5GHz', '2.6GHz']),
                "high_band": random_choice(['28GHz', '39GHz'])
            },
            'V2X': {
                "low_band": random_choice(['700MHz', '800MHz']),
                "mid_band": random_choice(['3.5GHz', '2.6GHz']),
                "high_band": random_choice(['28GHz', '39GHz'])
            },
            'eMBB': {
                "low_band": random_choice(['600MHz', '700MHz']),
                "mid_band": random_choice(['1.8GHz', '2.1GHz']),
                "high_band": random_choice(['24GHz', '28GHz', '39GHz'])
            },
            'mMTC': {
                "low_band": random_choice(['600MHz', '700MHz', '800MHz']),
                "mid_band": random_choice(['1.8GHz', '2.1GHz']),
                "high_band": random_choice(['24GHz', '28GHz'])
            }
        }
        return spectrum_mapping.get(slice_category, spectrum_mapping['eMBB'])
    
    @staticmethod
    def _build_antenna_block(slice_category: str, location_category: str) -> Dict[str, str]:
        """Build antenna configuration block."""
        if slice_category in ['URLLC', 'V2X'] or location_category == 'industrial':
            return {
                "type": random_choice(['Massive_MIMO_64T64R', 'Massive_MIMO_32T32R']),
                "beamforming_capability": '3D_Beamforming',
                "sectorization": random_choice(['6_Sector', '12_Sector'])
            }
        else:
            return {
                "type": random_choice(['Massive_MIMO_32T32R', 'Traditional_MIMO_4T4R']),
                "beamforming_capability": random_choice(['3D_Beamforming', 'Horizontal_Beamforming']),
                "sectorization": random_choice(['3_Sector', '6_Sector'])
            }


class ResourceParameterBuilder:
    """Builder for resource allocation parameters."""
    
    @staticmethod
    def build_compute_block(complexity: int, priority: str) -> Dict[str, Any]:
        """Build compute resource parameter block."""
        base_multiplier = 0.5 + (complexity / 10) * 1.5  # 0.5 to 2.0
        
        if priority in ['CRITICAL', 'EMERGENCY']:
            base_multiplier *= 1.5
        
        base_cores = random_int(2, 16)
        base_memory = random_int(4, 64)
        
        return {
            "cpu_architecture": random_choice(['x86_64', 'ARM64']),
            "cpu_cores": int(base_cores * base_multiplier),
            "cpu_frequency": f"{random_float(2.0, 4.0)}GHz",
            "memory_size": f"{int(base_memory * base_multiplier)}GB",
            "memory_type": random_choice(['DDR4', 'DDR5']),
            "numa_topology": f"{random_int(1, 4)}_nodes" if complexity >= 7 else "single_node"
        }
    
    @staticmethod
    def build_storage_block(complexity: int, slice_category: str) -> Dict[str, Any]:
        """Build storage resource parameter block."""
        storage_requirements = {
            'URLLC': (100, 1000),
            'V2X': (200, 2000),
            'eMBB': (50, 500),
            'mMTC': (20, 200)
        }
        
        base_range = storage_requirements.get(slice_category, (50, 500))
        complexity_multiplier = 0.5 + (complexity / 10) * 1.5
        
        storage_size = int(random_int(*base_range) * complexity_multiplier)
        
        return {
            "storage_capacity": f"{storage_size}GB",
            "storage_type": random_choice(['NVMe_SSD', 'SATA_SSD']) if complexity >= 5 else 'SATA_SSD',
            "iops_requirement": f"{random_int(1000, 50000)}",
            "redundancy_level": "RAID_1" if complexity >= 7 else random_choice(["RAID_0", "RAID_1"])
        }
    
    @staticmethod
    def build_network_resources_block(slice_category: str, priority: str) -> Dict[str, Any]:
        """Build network resource parameter block."""
        bandwidth_ranges = {
            'URLLC': (10, 100),
            'V2X': (10, 1000),
            'eMBB': (100, 10000),
            'mMTC': (1, 10)
        }
        
        base_range = bandwidth_ranges.get(slice_category, (100, 1000))
        bandwidth = random_int(*base_range)
        
        if priority in ['CRITICAL', 'EMERGENCY']:
            bandwidth = int(bandwidth * 1.5)
        
        return {
            "bandwidth_allocation": f"{bandwidth}Mbps",
            "latency_requirement": f"{random_float(0.1, 100)}ms",
            "jitter_tolerance": f"{random_float(0.1, 10)}ms",
            "connection_density": f"{random_int(1000, 1000000)}_devices_per_km2"
        }


class MonitoringParameterBuilder:
    """Builder for monitoring and observability parameters."""
    
    @staticmethod
    def build_metrics_collection_block(complexity: int, priority: str) -> Dict[str, Any]:
        """Build metrics collection parameter block."""
        if complexity >= 8 or priority in ['CRITICAL', 'EMERGENCY']:
            sampling_rate = random_int(80, 100)
            collection_interval = random_int(1, 10)
        elif complexity >= 5 or priority == 'HIGH':
            sampling_rate = random_int(50, 80)
            collection_interval = random_int(10, 30)
        else:
            sampling_rate = random_int(20, 50)
            collection_interval = random_int(30, 60)
        
        return {
            "sampling_rate": f"{sampling_rate}%",
            "collection_interval": f"{collection_interval}seconds",
            "metrics_retention": f"{random_int(7, 365)}days",
            "compression_enabled": complexity >= 5,
            "real_time_processing": complexity >= 7
        }
    
    @staticmethod
    def build_alerting_block(priority: str, complexity: int) -> Dict[str, Any]:
        """Build alerting configuration parameter block."""
        if priority in ['CRITICAL', 'EMERGENCY']:
            escalation_times = [f"{random_int(1, 3)}minutes", f"{random_int(3, 10)}minutes"]
        elif priority == 'HIGH':
            escalation_times = [f"{random_int(1, 5)}minutes", f"{random_int(5, 15)}minutes"]
        else:
            escalation_times = [f"{random_int(5, 15)}minutes", f"{random_int(15, 60)}minutes"]
        
        return {
            "severity_levels": ['CRITICAL', 'MAJOR', 'MINOR', 'WARNING', 'INFO'],
            "escalation_policy": {
                "level1": escalation_times[0],
                "level2": escalation_times[1],
                "level3": f"{random_int(30, 120)}minutes"
            },
            "notification_channels": MonitoringParameterBuilder._select_notification_channels(priority),
            "correlation_enabled": complexity >= 6
        }
    
    @staticmethod
    def _select_notification_channels(priority: str) -> List[str]:
        """Select appropriate notification channels based on priority."""
        if priority in ['CRITICAL', 'EMERGENCY']:
            return ['EMAIL', 'SMS', 'PAGERDUTY', 'WEBHOOK']
        elif priority == 'HIGH':
            return ['EMAIL', 'SLACK', 'WEBHOOK']
        else:
            return ['EMAIL', 'WEBHOOK']


class QoSParameterBuilder:
    """Builder for Quality of Service parameters."""
    
    @staticmethod
    def build_qos_flow_block(slice_category: str, priority: str) -> Dict[str, Any]:
        """Build QoS flow parameter block."""
        # Base QoS parameters by slice category
        qos_mappings = {
            'URLLC': {
                'latency_range': (0.1, 5.0),
                'throughput_range': (1, 100),
                'reliability_range': (99.999, 99.9999),
                'qfi': ['5QI_82_Discrete_Automation_Small_Packets', '5QI_83_Discrete_Automation_Large_Packets']
            },
            'V2X': {
                'latency_range': (1, 10),
                'throughput_range': (10, 1000),
                'reliability_range': (99.99, 99.999),
                'qfi': ['5QI_75_V2X_Messages', '5QI_79_V2X_Video']
            },
            'eMBB': {
                'latency_range': (10, 50),
                'throughput_range': (100, 10000),
                'reliability_range': (99.9, 99.99),
                'qfi': ['5QI_7_Voice_Video_Gaming', '5QI_8_Video_TCP_Premium']
            },
            'mMTC': {
                'latency_range': (100, 1000),
                'throughput_range': (1, 10),
                'reliability_range': (99.0, 99.9),
                'qfi': ['5QI_9_Video_TCP_Background', '5QI_6_Video_TCP']
            }
        }
        
        mapping = qos_mappings.get(slice_category, qos_mappings['eMBB'])
        
        # Priority affects QoS requirements
        priority_multiplier = {
            'EMERGENCY': 1.5,
            'CRITICAL': 1.3,
            'HIGH': 1.1,
            'MEDIUM': 1.0,
            'LOW': 0.8
        }.get(priority, 1.0)
        
        latency = random_float(*mapping['latency_range']) / priority_multiplier
        throughput = int(random_int(*mapping['throughput_range']) * priority_multiplier)
        
        return {
            "qos_flow_identifier": random_choice(mapping['qfi']),
            "guaranteed_bit_rate": f"{max(1, throughput // 10)}Mbps",
            "maximum_bit_rate": f"{throughput}Mbps",
            "packet_delay_budget": f"{latency:.2f}ms",
            "packet_error_rate": QoSParameterBuilder._calculate_error_rate(slice_category, priority),
            "priority_level": QoSParameterBuilder._get_priority_level(priority),
            "preemption_capability": "MAY_PREEMPT" if priority in ['CRITICAL', 'EMERGENCY'] else "SHALL_NOT_PREEMPT",
            "reflective_qos": "ENABLED" if slice_category in ['URLLC', 'V2X'] else "DISABLED"
        }
    
    @staticmethod
    def _calculate_error_rate(slice_category: str, priority: str) -> str:
        """Calculate appropriate packet error rate."""
        base_rates = {
            'URLLC': (1e-6, 1e-5),
            'V2X': (1e-6, 1e-5),
            'eMBB': (1e-4, 1e-3),
            'mMTC': (1e-3, 1e-2)
        }
        
        rate_range = base_rates.get(slice_category, base_rates['eMBB'])
        rate = random_float(*rate_range, 6)
        
        if priority in ['CRITICAL', 'EMERGENCY']:
            rate *= 0.1
        
        return f"{rate:.2e}"
    
    @staticmethod
    def _get_priority_level(priority: str) -> int:
        """Map priority to 3GPP priority level."""
        priority_levels = {
            'EMERGENCY': 1,
            'CRITICAL': random_int(1, 5),
            'HIGH': random_int(5, 15),
            'MEDIUM': random_int(15, 50),
            'LOW': random_int(50, 127)
        }
        return priority_levels.get(priority, 50)