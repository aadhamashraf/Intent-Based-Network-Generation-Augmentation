class ModificationIntentGenerator:
    """Generator for modification intent records."""
    
    @staticmethod
    def generate_parameters() -> Dict[str, Any]:
        """Generate modification-specific parameters."""
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
