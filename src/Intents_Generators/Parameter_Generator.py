import random
import uuid
from typing import Dict, Any
from .Constants_Enums import (
    QOS_FLOW_IDENTIFIERS, NETWORK_FUNCTIONS, ADVANCED_SLICE_TYPES,
    RADIO_PARAMETERS, PROTOCOL_PARAMETERS, PERFORMANCE_METRICS
)
from .utilis_generator import random_choice, random_int, random_float

class ParameterGenerator: 
    @staticmethod
    def generate_network_topology() -> Dict[str, Any]:
        """Generate advanced network topology parameters."""
        return {
            "network_architecture": random_choice(['Standalone_5G', 'Non_Standalone_5G', 'Hybrid_4G_5G']),
            "deployment_scenario": random_choice(['Urban_Macro', 'Urban_Micro', 'Rural_Macro', 'Indoor_Hotspot', 'Dense_Urban']),
            "spectrum_bands": {
                "low_band": random_choice(['600MHz', '700MHz', '800MHz', '900MHz']),
                "mid_band": random_choice(['1.8GHz', '2.1GHz', '2.6GHz', '3.5GHz']),
                "high_band": random_choice(['24GHz', '28GHz', '39GHz', '60GHz'])
            },
            "antenna_configuration": {
                "type": random_choice(['Massive_MIMO_64T64R', 'Massive_MIMO_32T32R', 'Traditional_MIMO_4T4R', 'Beamforming_8T8R']),
                "beamforming_capability": random_choice(['3D_Beamforming', 'Horizontal_Beamforming', 'Vertical_Beamforming']),
                "sectorization": random_choice(['3_Sector', '6_Sector', '12_Sector', 'Omni_Directional'])
            },
            "backhaul": {
                "type": random_choice(['Fiber_Optic', 'Microwave', 'Satellite', 'Hybrid_Fiber_Wireless']),
                "capacity": f"{random_int(1, 100)}Gbps",
                "latency": f"{random_float(0.1, 5.0)}ms",
                "redundancy": random_choice(['Active_Active', 'Active_Standby', 'Load_Balanced'])
            }
        }
    
    @staticmethod
    def generate_qos_parameters() -> Dict[str, Any]:
        """Generate advanced QoS parameters."""
        return {
            "qos_flow_identifier": random_choice(QOS_FLOW_IDENTIFIERS),
            "guaranteed_bit_rate": f"{random_int(1, 1000)}Mbps",
            "maximum_bit_rate": f"{random_int(100, 10000)}Mbps",
            "packet_delay_budget": f"{random_int(1, 300)}ms",
            "packet_error_rate": f"{random_float(0.0001, 0.01, 6)}",
            "priority_level": random_int(1, 127),
            "preemption_capability": random_choice(['MAY_PREEMPT', 'SHALL_NOT_PREEMPT']),
            "preemption_vulnerability": random_choice(['PREEMPTABLE', 'NOT_PREEMPTABLE']),
            "reflective_qos": random_choice(['ENABLED', 'DISABLED']),
            "notification_control": random_choice(['REQUESTED', 'NOT_REQUESTED']),
            "maximum_data_burst_volume": f"{random_int(1, 1000)}KB",
            "averaging_window": f"{random_int(1000, 10000)}ms"
        }
    
    @staticmethod
    def generate_security_parameters() -> Dict[str, Any]:
        """Generate advanced security parameters."""
        return {
            "authentication_method": random_choice(['5G_AKA', 'EAP_AKA_Prime', 'EAP_TLS', 'Certificate_Based']),
            "encryption_algorithm": random_choice(['128_NEA1', '128_NEA2', '128_NEA3', '256_NEA1', '256_NEA2']),
            "integrity_protection": random_choice(['128_NIA1', '128_NIA2', '128_NIA3', '256_NIA1', '256_NIA2']),
            "key_management": {
                "kdf": random_choice(['HMAC_SHA256', 'HMAC_SHA384', 'HMAC_SHA512']),
                "key_length": random_choice(['128_bit', '256_bit', '384_bit']),
                "key_rotation_interval": f"{random_int(1, 24)}hours",
                "key_derivation_counter": random_int(1, 65535)
            },
            "security_context": {
                "kamf": f"0x{uuid.uuid4().hex[:64]}",
                "kausf": f"0x{uuid.uuid4().hex[:64]}",
                "kseaf": f"0x{uuid.uuid4().hex[:64]}",
                "supi": f"imsi-{random_int(100000000000000, 999999999999999)}",
                "suci": f"suci-0-001-01-{uuid.uuid4().hex[:16]}"
            },
            "privacy_protection": {
                "supi_concealment": random_choice(['ENABLED', 'DISABLED']),
                "temporary_identifiers": random_choice(['5G_GUTI', '5G_TMSI', 'Random_TMSI']),
                "location_privacy": random_choice(['FULL_PROTECTION', 'PARTIAL_PROTECTION', 'NO_PROTECTION'])
            },
            "zero_trust_architecture": {
                "identity_verification": 'continuous_behavioral_authentication',
                "device_trust": 'hardware_based_attestation',
                "network_segmentation": 'micro_segmentation_with_dynamic_policies',
                "data_protection": 'end_to_end_encryption_with_quantum_resistance'
            }
        }
    
    @staticmethod
    def generate_resource_allocation() -> Dict[str, Any]:
        """Generate advanced resource allocation parameters."""
        return {
            "compute_resources": {
                "cpu_architecture": random_choice(['x86_64', 'ARM64', 'RISC_V']),
                "cpu_cores": random_int(2, 128),
                "cpu_frequency": f"{random_float(1.5, 4.0)}GHz",
                "memory_size": f"{random_int(4, 512)}GB",
                "memory_type": random_choice(['DDR4', 'DDR5', 'HBM2', 'LPDDR5']),
                "storage_capacity": f"{random_int(100, 10000)}GB",
                "storage_type": random_choice(['NVMe_SSD', 'SATA_SSD', 'NVMe_PCIe4', 'Optane'])
            },
            "network_resources": {
                "bandwidth_allocation": f"{random_int(10, 10000)}Mbps",
                "latency_requirement": f"{random_float(0.1, 100)}ms",
                "jitter_tolerance": f"{random_float(0.1, 10)}ms",
                "packet_loss_threshold": f"{random_float(0.001, 1)}%",
                "connection_density": f"{random_int(1000, 1000000)}_devices_per_km2"
            },
            "virtualization_parameters": {
                "hypervisor": random_choice(['KVM', 'Xen', 'VMware_vSphere', 'Hyper_V']),
                "container_runtime": random_choice(['Docker', 'Containerd', 'CRI_O', 'Podman']),
                "orchestration_platform": random_choice(['Kubernetes', 'OpenShift', 'Docker_Swarm', 'Nomad']),
                "resource_isolation": random_choice(['CPU_Pinning', 'NUMA_Affinity', 'SR_IOV', 'DPDK'])
            },
            "ai_driven_resource_allocation": {
                "prediction_model": 'lstm_with_attention_mechanism',
                "optimization_algorithm": 'multi_objective_genetic_algorithm',
                "adaptation_speed": f"{random_int(100, 1000)}ms",
                "accuracy_level": f"{random_float(85, 99)}%"
            }
        }
    
    @staticmethod
    def generate_monitoring_parameters() -> Dict[str, Any]:
        """Generate advanced monitoring parameters."""
        radio_metrics = {param: {
            "current_value": random_float(-120, 0),
            "threshold": random_float(-110, -70),
            "unit": "ms" if "Time" in param else "dBm"
        } for param in RADIO_PARAMETERS}
        
        protocol_metrics = {param: {
            "current_value": random_float(1, 1000),
            "threshold": random_float(10, 500),
            "unit": "ms"
        } for param in PROTOCOL_PARAMETERS}
        
        performance_metrics = {param: {
            "current_value": random_float(0.1, 100),
            "threshold": random_float(1, 50),
            "unit": "%" if any(x in param for x in ["Rate", "Loss"]) else 
                   "ms" if any(x in param for x in ["Latency", "Jitter"]) else
                   "Mbps" if "Throughput" in param else "units"
        } for param in PERFORMANCE_METRICS}
        
        return {
            "kpi_metrics": {
                "radio_metrics": radio_metrics,
                "protocol_metrics": protocol_metrics,
                "performance_metrics": performance_metrics
            },
            "alerting_configuration": {
                "severity_levels": ['CRITICAL', 'MAJOR', 'MINOR', 'WARNING', 'INFO'],
                "escalation_policy": {
                    "level1": f"{random_int(1, 5)}minutes",
                    "level2": f"{random_int(5, 15)}minutes",
                    "level3": f"{random_int(15, 60)}minutes"
                },
                "notification_channels": random_choice(['SNMP', 'REST_API', 'Kafka', 'WebSocket', 'gRPC']),
                "correlation_rules": [
                    'Radio_Performance_Degradation',
                    'Network_Congestion_Detection',
                    'Service_Quality_Impact',
                    'Resource_Exhaustion_Prediction'
                ]
            },
            "analytics_configuration": {
                "data_collection": {
                    "sampling_rate": f"{random_int(1, 100)}%",
                    "aggregation_interval": f"{random_int(1, 60)}seconds",
                    "retention_period": f"{random_int(7, 365)}days",
                    "compression_ratio": f"{random_int(2, 10)}:1"
                },
                "ml_models": {
                    "anomaly_detection": random_choice(['Isolation_Forest', 'One_Class_SVM', 'LSTM_Autoencoder']),
                    "predictive_analytics": random_choice(['ARIMA', 'Prophet', 'Neural_Network', 'Random_Forest']),
                    "optimization_algorithm": random_choice(['Genetic_Algorithm', 'Particle_Swarm', 'Simulated_Annealing'])
                }
            }
        }