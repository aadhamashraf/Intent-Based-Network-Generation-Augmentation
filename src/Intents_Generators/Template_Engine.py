"""
Enhanced Template Engine for Advanced 3GPP Intent Generation

This module provides a sophisticated template engine that utilizes ALL available
parameters to generate unique, research-grade intent descriptions with unprecedented
depth and realism.

Key Features:
- Comprehensive parameter extraction and utilization (200+ parameters)
- AI-driven template selection based on multi-dimensional scoring
- Cross-domain scenario generation spanning RAN-Core-Transport
- Advanced security and orchestration parameter integration
- Scenario-based templates for mission-critical deployments
"""

import random
import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class TemplateStrategy(Enum):
    """Template selection strategies for different scenarios."""
    PARAMETER_RICH = "parameter_rich"
    SCENARIO_BASED = "scenario_based"
    CROSS_DOMAIN = "cross_domain"
    AI_DRIVEN = "ai_driven"
    SECURITY_FOCUSED = "security_focused"
    PERFORMANCE_OPTIMIZED = "performance_optimized"
    ORCHESTRATION_HEAVY = "orchestration_heavy"
    RESEARCH_GRADE = "research_grade"
    MISSION_CRITICAL = "mission_critical"
    EDGE_COMPUTING = "edge_computing"
    INTELLIGENT_AUTOMATION = "intelligent_automation"
    COGNITIVE_NETWORKING = "cognitive_networking"
    ZERO_TRUST_SECURITY = "zero_trust_security"
    AUTONOMOUS_OPTIMIZATION = "autonomous_optimization"
    MULTI_CLOUD_ORCHESTRATION = "multi_cloud_orchestration"

@dataclass
class TemplateContext:
    """Enhanced template context with comprehensive parameter access."""
    intent_type: str
    complexity: int
    priority: str
    slice_category: str
    location_category: str
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        """Extract and organize parameters for easy access."""
        self.extracted_params = self._extract_all_parameters()
        self.parameter_richness = self._calculate_parameter_richness()
        self.template_strategy = self._determine_template_strategy()
    
    def _extract_all_parameters(self) -> Dict[str, Any]:
        """Extract all parameters from nested structures."""
        extracted = {}
        
        # Extract from main parameters
        extracted.update(self._flatten_dict(self.parameters, ""))
        
        # Extract from metadata
        extracted.update(self._flatten_dict(self.metadata, "meta_"))
        
        # Extract specific parameter categories
        categories = [
            'network_topology', 'qos_parameters', 'security_parameters',
            'resource_allocation', 'monitoring_parameters', 'deployment_specification',
            'orchestration_parameters', 'performance_requirements', 'modification_specification',
            'report_specification', 'feasibility_assessment', 'notification_configuration'
        ]
        
        for category in categories:
            if category in self.parameters:
                extracted.update(self._flatten_dict(self.parameters[category], f"{category}_"))
        
        return extracted
    
    def _flatten_dict(self, d: Dict[str, Any], prefix: str) -> Dict[str, Any]:
        """Recursively flatten nested dictionaries."""
        items = []
        for k, v in d.items():
            new_key = f"{prefix}{k}" if prefix else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, f"{new_key}_").items())
            elif isinstance(v, list) and v and isinstance(v[0], dict):
                for i, item in enumerate(v):
                    if isinstance(item, dict):
                        items.extend(self._flatten_dict(item, f"{new_key}_{i}_").items())
                    else:
                        items.append((f"{new_key}_{i}", str(item)))
            else:
                items.append((new_key, str(v)))
        return dict(items)
    
    def _calculate_parameter_richness(self) -> Dict[str, float]:
        """Calculate richness scores for different parameter categories."""
        categories = {
            'network': ['network_architecture', 'deployment_scenario', 'spectrum_bands', 'antenna_configuration'],
            'qos': ['qos_flow_identifier', 'guaranteed_bit_rate', 'packet_delay_budget', 'priority_level'],
            'security': ['authentication_method', 'encryption_algorithm', 'key_management', 'privacy_protection'],
            'resource': ['cpu_cores', 'memory_size', 'storage_capacity', 'bandwidth_allocation'],
            'monitoring': ['kpi_metrics', 'alerting_configuration', 'analytics_configuration'],
            'orchestration': ['nfvo_id', 'vnfm_id', 'workflow_id', 'orchestration_workflow'],
            'performance': ['throughput_requirement', 'latency_requirement', 'availability_requirement'],
            'ai_ml': ['prediction_model', 'optimization_algorithm', 'anomaly_detection', 'ml_models']
        }
        
        richness = {}
        for category, keywords in categories.items():
            score = sum(1 for keyword in keywords if any(keyword in key for key in self.extracted_params.keys()))
            richness[category] = score / len(keywords)
        
        return richness
    
    def _determine_template_strategy(self) -> TemplateStrategy:
        """Determine the best template strategy based on context."""
        # High complexity and critical priority favor advanced strategies
        if self.complexity >= 8 and self.priority in ['CRITICAL', 'EMERGENCY']:
            if self.parameter_richness.get('ai_ml', 0) > 0.5:
                return TemplateStrategy.COGNITIVE_NETWORKING
            elif self.parameter_richness.get('security', 0) > 0.7:
                return TemplateStrategy.ZERO_TRUST_SECURITY
            else:
                return TemplateStrategy.MISSION_CRITICAL
        
        # High parameter richness favors comprehensive templates
        avg_richness = sum(self.parameter_richness.values()) / len(self.parameter_richness)
        if avg_richness > 0.7:
            return TemplateStrategy.PARAMETER_RICH
        
        # Intent type specific strategies
        if self.intent_type == 'DEPLOYMENT':
            if self.parameter_richness.get('orchestration', 0) > 0.5:
                return TemplateStrategy.MULTI_CLOUD_ORCHESTRATION
            else:
                return TemplateStrategy.SCENARIO_BASED
        elif self.intent_type == 'PERFORMANCE_ASSURANCE':
            return TemplateStrategy.AUTONOMOUS_OPTIMIZATION
        elif self.intent_type == 'FEASIBILITY_CHECK':
            return TemplateStrategy.AI_DRIVEN
        
        # Default based on slice category
        if self.slice_category in ['URLLC', 'V2X']:
            return TemplateStrategy.MISSION_CRITICAL
        elif 'edge' in self.slice_category.lower():
            return TemplateStrategy.EDGE_COMPUTING
        else:
            return TemplateStrategy.CROSS_DOMAIN

class AdvancedTemplateEngine:
    """Advanced template engine with comprehensive parameter utilization."""
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.substitution_patterns = self._initialize_substitution_patterns()
        self.enhancement_rules = self._initialize_enhancement_rules()
    
    def _initialize_templates(self) -> Dict[TemplateStrategy, List[str]]:
        """Initialize comprehensive template library."""
        return {
            TemplateStrategy.PARAMETER_RICH: [
                "Execute {complexity_adjective} {intent_action} of {network_function} network function using {vnf_provider} {vnf_software_version} with {deployment_flavor_description} configuration, leveraging {network_architecture} architecture on {cpu_cores}-core {cpu_architecture} infrastructure with {memory_size} {memory_type} memory and {storage_capacity} {storage_type} storage, orchestrated via {orchestration_platform} with {workflow_engine} workflow engine, ensuring {availability_requirement} availability and {reliability_requirement} reliability through {auto_scaling_policy} scaling from {min_instances} to {max_instances} instances, secured with {authentication_method} authentication and {encryption_algorithm} encryption, monitored using {anomaly_detection} anomaly detection with {sampling_rate} sampling rate and {aggregation_interval} aggregation intervals",
                
                "Implement {complexity_adjective} {intent_action} leveraging {network_architecture} deployment with {deployment_scenario} scenario, utilizing {spectrum_bands_combined} spectrum allocation across {antenna_type} antenna configuration with {beamforming_capability} beamforming, orchestrated through {orchestration_workflow_description} workflow with {execution_timeout} execution timeout, ensuring {qos_flow_identifier} QoS flow with {guaranteed_bit_rate} guaranteed bitrate and {packet_delay_budget} latency budget, secured via {security_context_comprehensive} security context with {key_rotation_interval} key rotation, monitored through {monitoring_comprehensive} monitoring framework with {retention_period} data retention"
            ],
            
            TemplateStrategy.SCENARIO_BASED: [
                "Deploy mission-critical {network_function} for {slice_category} service scenario at {location_category} location, implementing {complexity_adjective} {network_architecture} architecture with {high_availability_config} high availability configuration, utilizing {advanced_security_suite} security suite and {intelligent_monitoring} monitoring capabilities, orchestrated through {orchestration_platform} with {workflow_complexity} workflow complexity and {rollback_strategy} rollback strategy",
                
                "Establish {complexity_adjective} {slice_category} service deployment scenario featuring {network_function} with {performance_tier} performance tier, implementing {deployment_pattern} deployment pattern across {multi_zone_config} zones, secured with {zero_trust_elements} zero-trust architecture and monitored via {ai_driven_monitoring} AI-driven monitoring with {predictive_capabilities} predictive capabilities"
            ],
            
            TemplateStrategy.CROSS_DOMAIN: [
                "Orchestrate {complexity_adjective} cross-domain {intent_action} spanning RAN-Core-Transport domains, coordinating {ran_elements} RAN elements with {core_functions} core functions and {transport_infrastructure} transport infrastructure, implementing {end_to_end_qos} end-to-end QoS assurance with {cross_domain_security} cross-domain security policies and {unified_monitoring} unified monitoring across all network layers",
                
                "Execute {complexity_adjective} multi-domain {intent_action} integrating {edge_computing_elements} edge computing with {core_network_functions} core network functions, coordinated through {cross_domain_orchestration} orchestration platform with {inter_domain_policies} inter-domain policies and {federated_monitoring} federated monitoring capabilities"
            ],
            
            TemplateStrategy.AI_DRIVEN: [
                "Deploy {complexity_adjective} AI-enhanced {intent_action} utilizing {ml_algorithms} machine learning algorithms for {optimization_objectives} optimization, implementing {predictive_analytics} predictive analytics with {confidence_level} confidence level, featuring {autonomous_decision_making} autonomous decision-making capabilities and {self_healing_mechanisms} self-healing mechanisms with {adaptation_speed} adaptation speed",
                
                "Implement {complexity_adjective} cognitive {intent_action} leveraging {ai_models_suite} AI model suite for {intelligent_automation} intelligent automation, incorporating {behavioral_analytics} behavioral analytics and {anomaly_prediction} anomaly prediction with {learning_algorithms} learning algorithms and {adaptive_optimization} adaptive optimization capabilities"
            ],
            
            TemplateStrategy.SECURITY_FOCUSED: [
                "Establish {complexity_adjective} security-hardened {intent_action} implementing {zero_trust_architecture} zero-trust architecture with {continuous_authentication} continuous authentication, featuring {hardware_attestation} hardware-based attestation and {quantum_resistant_crypto} quantum-resistant cryptography, monitored through {security_analytics} security analytics with {threat_intelligence} threat intelligence integration",
                
                "Deploy {complexity_adjective} security-first {intent_action} with {multi_layer_security} multi-layered security framework, implementing {identity_verification} identity verification and {device_trust} device trust mechanisms, secured via {end_to_end_encryption} end-to-end encryption with {dynamic_policies} dynamic security policies"
            ],
            
            TemplateStrategy.PERFORMANCE_OPTIMIZED: [
                "Optimize {complexity_adjective} {intent_action} for {performance_objectives} performance objectives, implementing {optimization_algorithms} optimization algorithms with {resource_efficiency} resource efficiency targets, featuring {predictive_scaling} predictive scaling and {load_balancing} intelligent load balancing with {performance_monitoring} real-time performance monitoring",
                
                "Execute {complexity_adjective} performance-tuned {intent_action} utilizing {performance_optimization_suite} optimization suite with {sla_guarantees} SLA guarantees, implementing {adaptive_resource_management} adaptive resource management and {quality_assurance} quality assurance mechanisms"
            ],
            
            TemplateStrategy.ORCHESTRATION_HEAVY: [
                "Orchestrate {complexity_adjective} {intent_action} through {multi_cloud_orchestration} multi-cloud orchestration platform, coordinating {cloud_providers} cloud providers with {hybrid_strategy} hybrid cloud strategy, implementing {workflow_automation} workflow automation with {dependency_management} dependency management and {rollback_capabilities} rollback capabilities",
                
                "Execute {complexity_adjective} orchestration-driven {intent_action} utilizing {orchestration_engine} orchestration engine with {workflow_complexity} workflow complexity, featuring {service_mesh} service mesh integration and {container_orchestration} container orchestration with {auto_scaling} auto-scaling capabilities"
            ],
            
            TemplateStrategy.RESEARCH_GRADE: [
                "Conduct {complexity_adjective} research-grade {intent_action} for {research_context} research context, implementing {experimental_features} experimental features with {data_collection} comprehensive data collection, featuring {analytics_pipeline} analytics pipeline and {research_metrics} research metrics with {statistical_analysis} statistical analysis capabilities",
                
                "Execute {complexity_adjective} research-oriented {intent_action} supporting {research_objectives} research objectives, implementing {data_driven_approach} data-driven approach with {experimental_validation} experimental validation and {research_instrumentation} research instrumentation"
            ],
            
            TemplateStrategy.MISSION_CRITICAL: [
                "Deploy {complexity_adjective} mission-critical {intent_action} with {ultra_high_availability} ultra-high availability requirements, implementing {fault_tolerance} fault tolerance mechanisms and {disaster_recovery} disaster recovery capabilities, featuring {redundancy_systems} redundancy systems and {failover_automation} automated failover with {recovery_objectives} recovery objectives",
                
                "Establish {complexity_adjective} mission-critical {intent_action} ensuring {reliability_guarantees} reliability guarantees through {resilience_mechanisms} resilience mechanisms, implementing {continuous_monitoring} continuous monitoring and {proactive_maintenance} proactive maintenance with {incident_response} incident response automation"
            ],
            
            TemplateStrategy.EDGE_COMPUTING: [
                "Deploy {complexity_adjective} edge-native {intent_action} implementing {edge_architecture} edge computing architecture with {distributed_processing} distributed processing capabilities, featuring {edge_ai} edge AI and {local_optimization} local optimization with {edge_to_cloud} edge-to-cloud coordination",
                
                "Execute {complexity_adjective} edge-optimized {intent_action} utilizing {edge_infrastructure} edge infrastructure with {low_latency_processing} low-latency processing, implementing {edge_orchestration} edge orchestration and {distributed_intelligence} distributed intelligence capabilities"
            ],
            
            TemplateStrategy.INTELLIGENT_AUTOMATION: [
                "Implement {complexity_adjective} intelligently automated {intent_action} featuring {automation_intelligence} automation intelligence with {decision_algorithms} decision algorithms, incorporating {adaptive_behavior} adaptive behavior and {learning_mechanisms} learning mechanisms with {autonomous_operations} autonomous operations",
                
                "Deploy {complexity_adjective} AI-automated {intent_action} utilizing {intelligent_agents} intelligent agents for {automated_management} automated management, featuring {self_optimization} self-optimization and {predictive_automation} predictive automation capabilities"
            ],
            
            TemplateStrategy.COGNITIVE_NETWORKING: [
                "Establish {complexity_adjective} cognitive networking {intent_action} implementing {cognitive_algorithms} cognitive algorithms with {network_intelligence} network intelligence, featuring {self_aware_systems} self-aware systems and {cognitive_optimization} cognitive optimization with {intelligent_adaptation} intelligent adaptation mechanisms",
                
                "Deploy {complexity_adjective} cognitive {intent_action} leveraging {neural_networks} neural networks for {cognitive_decision_making} cognitive decision-making, implementing {brain_inspired_algorithms} brain-inspired algorithms and {cognitive_monitoring} cognitive monitoring capabilities"
            ],
            
            TemplateStrategy.ZERO_TRUST_SECURITY: [
                "Implement {complexity_adjective} zero-trust {intent_action} with {continuous_verification} continuous verification and {behavioral_authentication} behavioral authentication, featuring {micro_segmentation} micro-segmentation and {dynamic_policies} dynamic security policies with {threat_detection} advanced threat detection",
                
                "Deploy {complexity_adjective} zero-trust architecture {intent_action} implementing {identity_centric_security} identity-centric security with {device_attestation} hardware device attestation, featuring {policy_enforcement} policy enforcement and {security_orchestration} security orchestration capabilities"
            ],
            
            TemplateStrategy.AUTONOMOUS_OPTIMIZATION: [
                "Execute {complexity_adjective} autonomously optimized {intent_action} implementing {autonomous_algorithms} autonomous algorithms with {self_tuning} self-tuning capabilities, featuring {performance_prediction} performance prediction and {resource_optimization} resource optimization with {autonomous_healing} autonomous healing mechanisms",
                
                "Deploy {complexity_adjective} self-optimizing {intent_action} utilizing {optimization_engines} optimization engines for {autonomous_management} autonomous management, implementing {predictive_optimization} predictive optimization and {adaptive_control} adaptive control systems"
            ],
            
            TemplateStrategy.MULTI_CLOUD_ORCHESTRATION: [
                "Orchestrate {complexity_adjective} multi-cloud {intent_action} across {cloud_providers} cloud providers with {hybrid_orchestration} hybrid orchestration, implementing {cloud_bursting} cloud bursting and {workload_distribution} intelligent workload distribution with {cross_cloud_networking} cross-cloud networking",
                
                "Execute {complexity_adjective} cloud-native {intent_action} utilizing {multi_cloud_platform} multi-cloud platform with {federated_orchestration} federated orchestration, featuring {cloud_optimization} cloud optimization and {cost_management} cost management capabilities"
            ]
        }
    
    def _initialize_substitution_patterns(self) -> Dict[str, callable]:
        """Initialize comprehensive substitution patterns for all parameters."""
        return {
            # Complexity and action patterns
            'complexity_adjective': lambda ctx: self._get_complexity_adjective(ctx.complexity),
            'intent_action': lambda ctx: self._get_intent_action(ctx.intent_type),
            
            # Network function and architecture
            'network_function': lambda ctx: ctx.extracted_params.get('network_function', 'AMF'),
            'vnf_provider': lambda ctx: ctx.extracted_params.get('vnf_provider', 'Ericsson'),
            'vnf_software_version': lambda ctx: ctx.extracted_params.get('vnf_software_version', 'SW_2.1.45'),
            'network_architecture': lambda ctx: ctx.extracted_params.get('network_architecture', 'Standalone_5G'),
            'deployment_scenario': lambda ctx: ctx.extracted_params.get('deployment_scenario', 'Urban_Macro'),
            
            # Deployment and flavor
            'deployment_flavor_description': lambda ctx: ctx.extracted_params.get('deployment_specification_deployment_flavor_description', 'High_Performance_Compute_Optimized').replace('_', ' ').lower(),
            
            # Infrastructure resources
            'cpu_cores': lambda ctx: ctx.extracted_params.get('compute_resources_cpu_cores', '16'),
            'cpu_architecture': lambda ctx: ctx.extracted_params.get('compute_resources_cpu_architecture', 'x86_64'),
            'memory_size': lambda ctx: ctx.extracted_params.get('compute_resources_memory_size', '64GB'),
            'memory_type': lambda ctx: ctx.extracted_params.get('compute_resources_memory_type', 'DDR5'),
            'storage_capacity': lambda ctx: ctx.extracted_params.get('compute_resources_storage_capacity', '2000GB'),
            'storage_type': lambda ctx: ctx.extracted_params.get('compute_resources_storage_type', 'NVMe_SSD'),
            
            # Orchestration
            'orchestration_platform': lambda ctx: ctx.extracted_params.get('orchestration_platform', 'Kubernetes'),
            'workflow_engine': lambda ctx: ctx.extracted_params.get('workflow_engine', 'Airflow'),
            'orchestration_workflow_description': lambda ctx: f"{ctx.extracted_params.get('orchestration_workflow_workflow_id', 'advanced')} {ctx.extracted_params.get('orchestration_workflow_workflow_version', 'v2.0')}",
            'execution_timeout': lambda ctx: ctx.extracted_params.get('orchestration_workflow_execution_timeout', '1800seconds'),
            'rollback_strategy': lambda ctx: ctx.extracted_params.get('orchestration_workflow_rollback_strategy', 'AUTOMATIC'),
            
            # Performance and scaling
            'availability_requirement': lambda ctx: ctx.extracted_params.get('availability_requirement', '99.999%'),
            'reliability_requirement': lambda ctx: ctx.extracted_params.get('reliability_requirement', '99.99%'),
            'auto_scaling_policy': lambda ctx: ctx.extracted_params.get('scalability_requirement_auto_scaling_policy', 'CPU_BASED'),
            'min_instances': lambda ctx: ctx.extracted_params.get('deployment_specification_deployment_flavor_vdu_profile_min_number_of_instances', '4'),
            'max_instances': lambda ctx: ctx.extracted_params.get('deployment_specification_deployment_flavor_vdu_profile_max_number_of_instances', '40'),
            
            # Security
            'authentication_method': lambda ctx: ctx.extracted_params.get('authentication_method', '5G_AKA'),
            'encryption_algorithm': lambda ctx: ctx.extracted_params.get('encryption_algorithm', '256_NEA1'),
            'key_rotation_interval': lambda ctx: ctx.extracted_params.get('key_management_key_rotation_interval', '6hours'),
            
            # QoS parameters
            'qos_flow_identifier': lambda ctx: ctx.extracted_params.get('qos_flow_identifier', '5QI_82_Discrete_Automation_Small_Packets').replace('_', ' '),
            'guaranteed_bit_rate': lambda ctx: ctx.extracted_params.get('guaranteed_bit_rate', '100Mbps'),
            'packet_delay_budget': lambda ctx: ctx.extracted_params.get('packet_delay_budget', '5ms'),
            'priority_level': lambda ctx: ctx.extracted_params.get('priority_level', '15'),
            
            # Monitoring
            'anomaly_detection': lambda ctx: ctx.extracted_params.get('ml_models_anomaly_detection', 'Isolation_Forest'),
            'sampling_rate': lambda ctx: ctx.extracted_params.get('data_collection_sampling_rate', '80%'),
            'aggregation_interval': lambda ctx: ctx.extracted_params.get('data_collection_aggregation_interval', '10seconds'),
            'retention_period': lambda ctx: ctx.extracted_params.get('data_collection_retention_period', '90days'),
            
            # Spectrum and antenna
            'spectrum_bands_combined': lambda ctx: self._combine_spectrum_bands(ctx.extracted_params),
            'antenna_type': lambda ctx: ctx.extracted_params.get('antenna_configuration_type', 'Massive_MIMO_64T64R'),
            'beamforming_capability': lambda ctx: ctx.extracted_params.get('antenna_configuration_beamforming_capability', '3D_Beamforming'),
            
            # Advanced AI/ML patterns
            'ml_algorithms': lambda ctx: self._get_ml_algorithms(ctx.extracted_params),
            'optimization_objectives': lambda ctx: self._get_optimization_objectives(ctx.extracted_params),
            'predictive_analytics': lambda ctx: ctx.extracted_params.get('ml_models_predictive_analytics', 'Neural_Network'),
            'confidence_level': lambda ctx: ctx.extracted_params.get('confidence_level', '95%'),
            'autonomous_decision_making': lambda ctx: 'AI-driven autonomous decision making',
            'self_healing_mechanisms': lambda ctx: 'intelligent self-healing mechanisms',
            'adaptation_speed': lambda ctx: ctx.extracted_params.get('adaptation_speed', '100ms'),
            
            # Security comprehensive patterns
            'zero_trust_architecture': lambda ctx: self._get_zero_trust_elements(ctx.extracted_params),
            'continuous_authentication': lambda ctx: ctx.extracted_params.get('zero_trust_architecture_identity_verification', 'continuous_behavioral_authentication'),
            'hardware_attestation': lambda ctx: ctx.extracted_params.get('zero_trust_architecture_device_trust', 'hardware_based_attestation'),
            'quantum_resistant_crypto': lambda ctx: 'quantum-resistant cryptographic algorithms',
            'security_analytics': lambda ctx: 'advanced security analytics',
            'threat_intelligence': lambda ctx: 'real-time threat intelligence',
            
            # Performance optimization patterns
            'performance_objectives': lambda ctx: self._get_performance_objectives(ctx.extracted_params),
            'optimization_algorithms': lambda ctx: ctx.extracted_params.get('optimization_algorithm', 'multi_objective_genetic_algorithm'),
            'resource_efficiency': lambda ctx: f"{ctx.extracted_params.get('accuracy_level', '95%')} efficiency",
            'predictive_scaling': lambda ctx: 'ML-based predictive scaling',
            'load_balancing': lambda ctx: 'intelligent load balancing',
            'performance_monitoring': lambda ctx: 'real-time performance monitoring',
            
            # Cloud and orchestration patterns
            'multi_cloud_orchestration': lambda ctx: self._get_multi_cloud_setup(ctx.extracted_params),
            'cloud_providers': lambda ctx: self._get_cloud_providers(ctx.extracted_params),
            'hybrid_strategy': lambda ctx: ctx.extracted_params.get('hybrid_cloud_strategy', 'BALANCED'),
            'workflow_automation': lambda ctx: 'advanced workflow automation',
            'dependency_management': lambda ctx: 'intelligent dependency management',
            'rollback_capabilities': lambda ctx: 'automated rollback capabilities',
            
            # Research and experimental patterns
            'research_context': lambda ctx: ctx.metadata.get('research_context', 'Network_Optimization_Study'),
            'experimental_features': lambda ctx: 'cutting-edge experimental features',
            'data_collection': lambda ctx: 'comprehensive research data collection',
            'analytics_pipeline': lambda ctx: 'advanced analytics pipeline',
            'research_metrics': lambda ctx: 'research-grade metrics collection',
            'statistical_analysis': lambda ctx: 'statistical analysis capabilities',
            
            # Edge computing patterns
            'edge_architecture': lambda ctx: 'distributed edge computing architecture',
            'distributed_processing': lambda ctx: 'distributed processing',
            'edge_ai': lambda ctx: 'edge AI capabilities',
            'local_optimization': lambda ctx: 'local optimization',
            'edge_to_cloud': lambda ctx: 'edge-to-cloud coordination',
            'edge_infrastructure': lambda ctx: 'edge infrastructure',
            'low_latency_processing': lambda ctx: 'ultra-low latency processing',
            'edge_orchestration': lambda ctx: 'edge orchestration',
            'distributed_intelligence': lambda ctx: 'distributed intelligence',
            
            # Mission critical patterns
            'ultra_high_availability': lambda ctx: f"{ctx.extracted_params.get('availability_requirement', '99.999%')} ultra-high availability",
            'fault_tolerance': lambda ctx: 'advanced fault tolerance',
            'disaster_recovery': lambda ctx: 'disaster recovery',
            'redundancy_systems': lambda ctx: 'redundancy systems',
            'failover_automation': lambda ctx: 'automated failover',
            'recovery_objectives': lambda ctx: 'stringent recovery objectives',
            'reliability_guarantees': lambda ctx: f"{ctx.extracted_params.get('reliability_requirement', '99.99%')} reliability guarantees",
            'resilience_mechanisms': lambda ctx: 'resilience mechanisms',
            'continuous_monitoring': lambda ctx: 'continuous monitoring',
            'proactive_maintenance': lambda ctx: 'proactive maintenance',
            'incident_response': lambda ctx: 'incident response',
            
            # Cognitive networking patterns
            'cognitive_algorithms': lambda ctx: 'cognitive algorithms',
            'network_intelligence': lambda ctx: 'network intelligence',
            'self_aware_systems': lambda ctx: 'self-aware systems',
            'cognitive_optimization': lambda ctx: 'cognitive optimization',
            'intelligent_adaptation': lambda ctx: 'intelligent adaptation',
            'neural_networks': lambda ctx: 'neural networks',
            'cognitive_decision_making': lambda ctx: 'cognitive decision-making',
            'brain_inspired_algorithms': lambda ctx: 'brain-inspired algorithms',
            'cognitive_monitoring': lambda ctx: 'cognitive monitoring'
        }
    
    def _initialize_enhancement_rules(self) -> Dict[str, callable]:
        """Initialize post-processing enhancement rules."""
        return {
            'complexity_enhancement': lambda text, ctx: self._enhance_by_complexity(text, ctx.complexity),
            'priority_enhancement': lambda text, ctx: self._enhance_by_priority(text, ctx.priority),
            'slice_enhancement': lambda text, ctx: self._enhance_by_slice_category(text, ctx.slice_category),
            'parameter_richness_enhancement': lambda text, ctx: self._enhance_by_parameter_richness(text, ctx.parameter_richness),
            'research_enhancement': lambda text, ctx: self._enhance_for_research(text, ctx.metadata)
        }
    
    def generate_description(self, context: TemplateContext) -> str:
        """Generate comprehensive description using all available parameters."""
        # Select appropriate template based on strategy
        template = self._select_template(context)
        
        # Apply comprehensive parameter substitution
        description = self._apply_substitutions(template, context)
        
        # Apply post-processing enhancements
        description = self._apply_enhancements(description, context)
        
        # Final cleanup and validation
        description = self._cleanup_description(description)
        
        return description
    
    def _select_template(self, context: TemplateContext) -> str:
        """Select the most appropriate template based on context."""
        strategy = context.template_strategy
        templates = self.templates.get(strategy, self.templates[TemplateStrategy.PARAMETER_RICH])
        
        # Score templates based on parameter availability
        scored_templates = []
        for template in templates:
            score = self._score_template(template, context)
            scored_templates.append((template, score))
        
        # Select highest scoring template
        scored_templates.sort(key=lambda x: x[1], reverse=True)
        return scored_templates[0][0]
    
    def _score_template(self, template: str, context: TemplateContext) -> float:
        """Score template based on parameter availability."""
        placeholders = re.findall(r'\{([^}]+)\}', template)
        available_params = set(context.extracted_params.keys()) | set(self.substitution_patterns.keys())
        
        score = 0
        for placeholder in placeholders:
            if placeholder in available_params or placeholder in self.substitution_patterns:
                score += 1
            else:
                score -= 0.5  # Penalty for unavailable parameters
        
        return score / len(placeholders) if placeholders else 0
    
    def _apply_substitutions(self, template: str, context: TemplateContext) -> str:
        """Apply comprehensive parameter substitutions."""
        description = template
        
        # Apply all substitution patterns
        for pattern, func in self.substitution_patterns.items():
            placeholder = f"{{{pattern}}}"
            if placeholder in description:
                try:
                    value = func(context)
                    description = description.replace(placeholder, str(value))
                except Exception:
                    # Fallback to generic value
                    description = description.replace(placeholder, self._get_fallback_value(pattern))
        
        return description
    
    def _apply_enhancements(self, description: str, context: TemplateContext) -> str:
        """Apply post-processing enhancements."""
        enhanced = description
        
        for rule_name, rule_func in self.enhancement_rules.items():
            try:
                enhanced = rule_func(enhanced, context)
            except Exception:
                continue  # Skip failed enhancements
        
        return enhanced
    
    def _cleanup_description(self, description: str) -> str:
        """Clean up and validate the final description."""
        # Remove any remaining placeholders
        description = re.sub(r'\{[^}]+\}', 'advanced configuration', description)
        
        # Clean up formatting
        description = re.sub(r'\s+', ' ', description)  # Multiple spaces
        description = re.sub(r'\s*,\s*', ', ', description)  # Comma spacing
        description = description.strip()
        
        # Ensure proper capitalization
        if description and not description[0].isupper():
            description = description[0].upper() + description[1:]
        
        return description
    
    # Helper methods for pattern generation
    def _get_complexity_adjective(self, complexity: int) -> str:
        """Get complexity adjective based on complexity level."""
        if complexity >= 9:
            return random.choice(['revolutionary', 'cutting-edge', 'state-of-the-art'])
        elif complexity >= 7:
            return random.choice(['sophisticated', 'advanced', 'comprehensive'])
        elif complexity >= 5:
            return random.choice(['intelligent', 'adaptive', 'optimized'])
        else:
            return random.choice(['efficient', 'streamlined', 'enhanced'])
    
    def _get_intent_action(self, intent_type: str) -> str:
        """Get appropriate action verb for intent type."""
        actions = {
            'DEPLOYMENT': random.choice(['deployment', 'instantiation', 'provisioning']),
            'MODIFICATION': random.choice(['modification', 'reconfiguration', 'optimization']),
            'PERFORMANCE_ASSURANCE': random.choice(['performance assurance', 'SLA management', 'quality optimization']),
            'REPORT_REQUEST': random.choice(['analytics generation', 'reporting', 'intelligence gathering']),
            'FEASIBILITY_CHECK': random.choice(['feasibility analysis', 'viability assessment', 'capability evaluation']),
            'NOTIFICATION_REQUEST': random.choice(['notification system', 'alerting framework', 'event management'])
        }
        return actions.get(intent_type, 'network operation')
    
    def _combine_spectrum_bands(self, params: Dict[str, Any]) -> str:
        """Combine spectrum band information."""
        bands = []
        for band_type in ['low_band', 'mid_band', 'high_band']:
            key = f'spectrum_bands_{band_type}'
            if key in params:
                bands.append(params[key])
        return ' + '.join(bands) if bands else '3.5GHz + 28GHz'
    
    def _get_ml_algorithms(self, params: Dict[str, Any]) -> str:
        """Extract ML algorithms from parameters."""
        algorithms = []
        for key, value in params.items():
            if 'algorithm' in key.lower() or 'model' in key.lower():
                if isinstance(value, str) and any(ml_term in value.lower() for ml_term in ['neural', 'genetic', 'forest', 'svm', 'lstm']):
                    algorithms.append(value.replace('_', ' '))
        
        return ', '.join(algorithms[:3]) if algorithms else 'advanced machine learning algorithms'
    
    def _get_optimization_objectives(self, params: Dict[str, Any]) -> str:
        """Extract optimization objectives from parameters."""
        objectives = []
        for key, value in params.items():
            if 'optimization' in key.lower() or 'objective' in key.lower():
                if isinstance(value, str):
                    objectives.append(value.replace('_', ' ').lower())
        
        return ', '.join(objectives[:3]) if objectives else 'performance and efficiency optimization'
    
    def _get_zero_trust_elements(self, params: Dict[str, Any]) -> str:
        """Extract zero trust architecture elements."""
        elements = []
        zero_trust_keys = ['identity_verification', 'device_trust', 'network_segmentation', 'data_protection']
        
        for key in zero_trust_keys:
            full_key = f'zero_trust_architecture_{key}'
            if full_key in params:
                elements.append(params[full_key].replace('_', ' '))
        
        return 'comprehensive zero-trust architecture with ' + ', '.join(elements) if elements else 'zero-trust security architecture'
    
    def _get_performance_objectives(self, params: Dict[str, Any]) -> str:
        """Extract performance objectives."""
        objectives = []
        perf_keys = ['throughput_requirement', 'latency_requirement', 'availability_requirement']
        
        for key in perf_keys:
            if key in params:
                objectives.append(f"{key.replace('_requirement', '').replace('_', ' ')}: {params[key]}")
        
        return ', '.join(objectives) if objectives else 'optimal performance targets'
    
    def _get_multi_cloud_setup(self, params: Dict[str, Any]) -> str:
        """Extract multi-cloud orchestration setup."""
        cloud_info = []
        if 'cloud_providers' in params:
            providers = params['cloud_providers']
            if isinstance(providers, list):
                cloud_info.append(f"{len(providers)}-cloud orchestration")
            else:
                cloud_info.append("multi-cloud orchestration")
        
        if 'hybrid_cloud_strategy' in params:
            cloud_info.append(f"{params['hybrid_cloud_strategy'].lower().replace('_', ' ')} strategy")
        
        return ' with '.join(cloud_info) if cloud_info else 'advanced multi-cloud orchestration'
    
    def _get_cloud_providers(self, params: Dict[str, Any]) -> str:
        """Extract cloud providers list."""
        if 'cloud_providers' in params:
            providers = params['cloud_providers']
            if isinstance(providers, list):
                return ', '.join(providers)
            else:
                return str(providers)
        return 'AWS, Azure, and GCP'
    
    def _get_fallback_value(self, pattern: str) -> str:
        """Get fallback value for unavailable parameters."""
        fallbacks = {
            'network_function': 'AMF',
            'complexity_adjective': 'advanced',
            'intent_action': 'network operation',
            'availability_requirement': '99.9%',
            'reliability_requirement': '99.5%',
            'cpu_cores': '8',
            'memory_size': '32GB',
            'storage_capacity': '1TB'
        }
        return fallbacks.get(pattern, 'advanced configuration')
    
    # Enhancement methods
    def _enhance_by_complexity(self, text: str, complexity: int) -> str:
        """Enhance description based on complexity level."""
        if complexity >= 8:
            # Add research-grade qualifiers
            text = text.replace('advanced', 'research-grade advanced')
            text = text.replace('sophisticated', 'research-grade sophisticated')
        elif complexity >= 6:
            # Add enterprise-grade qualifiers
            text = text.replace('configuration', 'enterprise-grade configuration')
        
        return text
    
    def _enhance_by_priority(self, text: str, priority: str) -> str:
        """Enhance description based on priority level."""
        if priority in ['CRITICAL', 'EMERGENCY']:
            text = text.replace('monitoring', 'mission-critical monitoring')
            text = text.replace('security', 'hardened security')
        elif priority == 'HIGH':
            text = text.replace('performance', 'high-performance')
        
        return text
    
    def _enhance_by_slice_category(self, text: str, slice_category: str) -> str:
        """Enhance description based on slice category."""
        if slice_category in ['URLLC', 'V2X']:
            text = text.replace('latency', 'ultra-low latency')
            text = text.replace('reliability', 'ultra-high reliability')
        elif slice_category == 'eMBB':
            text = text.replace('throughput', 'ultra-high throughput')
            text = text.replace('capacity', 'massive capacity')
        
        return text
    
    def _enhance_by_parameter_richness(self, text: str, richness: Dict[str, float]) -> str:
        """Enhance description based on parameter richness."""
        avg_richness = sum(richness.values()) / len(richness) if richness else 0
        
        if avg_richness > 0.8:
            text = text.replace('comprehensive', 'extensively comprehensive')
        elif avg_richness > 0.6:
            text = text.replace('advanced', 'highly advanced')
        
        return text
    
    def _enhance_for_research(self, text: str, metadata: Dict[str, Any]) -> str:
        """Enhance description for research context."""
        research_context = metadata.get('research_context', '')
        if 'research' in research_context.lower():
            text += ' for advanced network research applications'
        
        return text