"""
Advanced Template Engine for Intent Description Generation

This module provides sophisticated template-based generation of natural language
descriptions for network intents, ensuring consistency between descriptions and
underlying parameters.
"""

import random
from dataclasses import dataclass
from typing import Dict, Any, List, Tuple
from .Constants_Enums import NETWORK_FUNCTIONS, ADVANCED_SLICE_TYPES
from .utilis_generator import random_choice, random_int


@dataclass
class TemplateContext:
    """Context information for template generation."""
    intent_type: str
    complexity: int
    priority: str
    slice_category: str
    location_category: str
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]


class AdvancedTemplateEngine:
    """Advanced template engine for generating contextually appropriate descriptions."""
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.modifiers = self._initialize_modifiers()
        self.technical_terms = self._initialize_technical_terms()
    
    def _initialize_templates(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize template patterns by intent type and complexity."""
        return {
            "Deployment Intent": {
                "basic": [
                    "Deploy {network_function} network function at {location} for {slice_type}",
                    "Establish {network_function} deployment supporting {slice_type} requirements",
                    "Provision {network_function} instance for {slice_type} service delivery"
                ],
                "advanced": [
                    "Execute {complexity_modifier} deployment of {network_function} network function with {performance_modifier} configuration at {location} supporting {slice_type} service requirements",
                    "Implement {complexity_modifier} {network_function} deployment featuring {technical_feature} capabilities for {slice_type} optimization at {location}",
                    "Orchestrate {complexity_modifier} {network_function} instantiation with {orchestration_feature} and {performance_modifier} resource allocation for {slice_type}"
                ],
                "research": [
                    "Execute {complexity_modifier} deployment of {network_function} network function with {performance_modifier} configuration at {location} supporting {slice_type} service requirements with advanced orchestration capabilities, comprehensive security hardening, and intelligent resource optimization algorithms for research-grade network performance analysis",
                    "Implement {complexity_modifier} {network_function} deployment featuring {technical_feature} capabilities, {orchestration_feature}, and {ai_feature} for {slice_type} optimization at {location} with comprehensive telemetry collection and advanced analytics integration",
                    "Orchestrate {complexity_modifier} multi-vendor {network_function} deployment with {performance_modifier} resource allocation, {security_feature}, and {monitoring_feature} for {slice_type} research applications at {location}"
                ]
            },
            "Modification Intent": {
                "basic": [
                    "Modify {target_resource} configuration for {slice_type} optimization",
                    "Update {target_resource} parameters to enhance {performance_aspect}",
                    "Reconfigure {target_resource} to support {new_requirement}"
                ],
                "advanced": [
                    "Implement {complexity_modifier} modification of {target_resource} through {operation_type} operation at {location} for {slice_type}",
                    "Execute {complexity_modifier} {target_resource} reconfiguration with {change_pattern} deployment strategy and {rollback_feature}",
                    "Apply {complexity_modifier} parameter updates to {target_resource} with {validation_feature} and comprehensive impact analysis"
                ],
                "research": [
                    "Implement {complexity_modifier} modification of {target_resource} through {operation_type} operation at {location} for {slice_type} with advanced impact analysis, intelligent rollback mechanisms, and comprehensive validation procedures for research-oriented network optimization studies",
                    "Execute {complexity_modifier} {target_resource} reconfiguration featuring {change_pattern} deployment strategy, {ai_feature}, and {monitoring_feature} with detailed performance correlation analysis",
                    "Orchestrate {complexity_modifier} multi-dimensional parameter optimization for {target_resource} with {validation_feature}, predictive impact modeling, and automated quality assurance for advanced network research"
                ]
            },
            "Performance Assurance Intent": {
                "basic": [
                    "Establish performance monitoring for {slice_type} at {location}",
                    "Configure SLA enforcement for {service_level} service tier",
                    "Implement performance assurance policies for {target_kpi}"
                ],
                "advanced": [
                    "Establish {complexity_modifier} performance assurance framework for {slice_type} at {location} with {sla_tier} service level",
                    "Configure {complexity_modifier} SLA enforcement with {assurance_action} and {monitoring_feature}",
                    "Implement {complexity_modifier} performance optimization with {prediction_feature} and automated remediation"
                ],
                "research": [
                    "Establish {complexity_modifier} performance assurance framework for {slice_type} at {location} with {sla_tier} service level guaranteeing {availability_target} availability through predictive analytics, machine learning-based optimization, and autonomous remediation capabilities for advanced network research applications",
                    "Configure {complexity_modifier} multi-dimensional SLA enforcement featuring {assurance_action}, {ai_feature}, and {monitoring_feature} with comprehensive KPI correlation analysis and intelligent threshold adaptation",
                    "Implement {complexity_modifier} closed-loop performance optimization with {prediction_feature}, automated root cause analysis, and self-healing capabilities for research-grade network assurance"
                ]
            },
            "Intent Report Request": {
                "basic": [
                    "Generate {report_type} report for {slice_type} operations",
                    "Create performance analytics covering {time_period}",
                    "Produce compliance assessment for {domain} domain"
                ],
                "advanced": [
                    "Generate {complexity_modifier} {report_type} report covering {domain} domain operations at {location} for {slice_type}",
                    "Create {complexity_modifier} analytics report with {aggregation_method} analysis and {delivery_method} delivery",
                    "Produce {complexity_modifier} multi-dimensional assessment with {validation_feature} and automated insights generation"
                ],
                "research": [
                    "Generate {complexity_modifier} {report_type} report covering {domain} domain operations at {location} for {slice_type} with advanced data analytics, multi-dimensional correlation analysis, and research-grade statistical modeling for comprehensive network intelligence gathering",
                    "Create {complexity_modifier} analytics framework featuring {aggregation_method} analysis, {ai_feature}, and {visualization_feature} with automated pattern recognition and predictive insights generation",
                    "Produce {complexity_modifier} comprehensive assessment with {validation_feature}, cross-domain correlation analysis, and machine learning-enhanced anomaly detection for advanced network research"
                ]
            },
            "Intent Feasibility Check": {
                "basic": [
                    "Assess feasibility of {target_deployment} implementation",
                    "Evaluate technical viability for {slice_type} deployment",
                    "Analyze resource requirements for {proposed_change}"
                ],
                "advanced": [
                    "Conduct {complexity_modifier} feasibility analysis for {target_deployment} implementation at {location}",
                    "Evaluate {complexity_modifier} technical and economic viability with {assessment_scope} assessment",
                    "Analyze {complexity_modifier} multi-dimensional feasibility with {risk_analysis} and recommendation engine"
                ],
                "research": [
                    "Conduct {complexity_modifier} {assessment_scope} feasibility analysis for {target_deployment} implementation at {location} with advanced risk modeling, economic impact assessment, and AI-driven recommendation engine providing {recommendation_outcome} guidance for research-informed decision making",
                    "Evaluate {complexity_modifier} comprehensive viability assessment featuring {risk_analysis}, {economic_analysis}, and {technical_analysis} with predictive modeling and scenario simulation capabilities",
                    "Analyze {complexity_modifier} multi-dimensional feasibility with {validation_feature}, Monte Carlo risk simulation, and machine learning-enhanced decision support for advanced network planning research"
                ]
            },
            "Regular Notification Request": {
                "basic": [
                    "Configure notification system for {event_type} events",
                    "Establish alerting for {slice_type} monitoring",
                    "Setup event delivery via {delivery_channel}"
                ],
                "advanced": [
                    "Configure {complexity_modifier} notification system for {event_type} monitoring at {location} for {slice_type}",
                    "Establish {complexity_modifier} event management with {subscription_type} subscription and {delivery_mechanism} delivery",
                    "Setup {complexity_modifier} intelligent alerting with {filtering_feature} and {qos_guarantee} delivery guarantee"
                ],
                "research": [
                    "Configure {complexity_modifier} {subscription_type} notification system for {event_type} monitoring at {location} for {slice_type} with {delivery_mechanism} delivery mechanism, advanced message transformation, and intelligent filtering capabilities for research-grade network event management",
                    "Establish {complexity_modifier} event orchestration framework featuring {filtering_feature}, {ai_feature}, and {monitoring_feature} with semantic event correlation and automated escalation procedures",
                    "Setup {complexity_modifier} intelligent notification ecosystem with {qos_guarantee} delivery guarantee, predictive alerting, and machine learning-enhanced event classification for advanced network operations research"
                ]
            }
        }
    
    def _initialize_modifiers(self) -> Dict[str, List[str]]:
        """Initialize modifier terms for template enhancement."""
        return {
            "complexity_modifier": [
                "sophisticated", "advanced", "comprehensive", "intelligent", "adaptive",
                "multi-layered", "enterprise-grade", "research-oriented", "cutting-edge",
                "next-generation", "AI-enhanced", "cloud-native", "microservices-based"
            ],
            "performance_modifier": [
                "high-performance", "ultra-reliable", "low-latency", "high-throughput",
                "deterministic", "real-time", "mission-critical", "carrier-grade",
                "enterprise-class", "production-ready", "scalable", "resilient"
            ],
            "technical_feature": [
                "zero-trust security", "edge computing integration", "AI-driven optimization",
                "blockchain-secured", "quantum-resistant encryption", "self-healing capabilities",
                "predictive analytics", "autonomous operation", "multi-cloud orchestration",
                "intent-driven automation", "cognitive networking", "digital twin integration"
            ],
            "orchestration_feature": [
                "cloud-native orchestration", "multi-vendor coordination", "automated lifecycle management",
                "intent-based automation", "policy-driven deployment", "service mesh integration",
                "GitOps-enabled deployment", "infrastructure-as-code", "continuous deployment",
                "blue-green deployment", "canary release management", "A/B testing framework"
            ],
            "ai_feature": [
                "machine learning optimization", "predictive analytics", "anomaly detection",
                "intelligent automation", "cognitive decision making", "neural network processing",
                "deep learning insights", "reinforcement learning", "natural language processing",
                "computer vision analysis", "federated learning", "explainable AI"
            ],
            "security_feature": [
                "zero-trust architecture", "end-to-end encryption", "quantum-safe cryptography",
                "behavioral analytics", "threat intelligence integration", "automated incident response",
                "continuous security monitoring", "identity-based access control", "micro-segmentation",
                "security orchestration", "compliance automation", "privacy-preserving analytics"
            ],
            "monitoring_feature": [
                "comprehensive telemetry", "real-time observability", "distributed tracing",
                "performance analytics", "predictive monitoring", "intelligent alerting",
                "automated root cause analysis", "service topology mapping", "business impact analysis",
                "SLA compliance tracking", "capacity planning", "trend analysis"
            ]
        }
    
    def _initialize_technical_terms(self) -> Dict[str, List[str]]:
        """Initialize technical terminology mappings."""
        return {
            "slice_categories": {
                "URLLC": ["ultra-reliable low-latency", "mission-critical", "industrial automation", "tactile internet"],
                "eMBB": ["enhanced mobile broadband", "high-throughput", "multimedia streaming", "immersive experience"],
                "mMTC": ["massive machine-type communication", "IoT connectivity", "sensor networks", "smart city"],
                "V2X": ["vehicle-to-everything", "autonomous driving", "intelligent transportation", "connected mobility"]
            },
            "location_categories": {
                "urban": ["metropolitan area", "dense urban environment", "city center", "commercial district"],
                "rural": ["remote area", "countryside", "agricultural region", "sparse coverage zone"],
                "highway": ["transportation corridor", "mobility network", "vehicular pathway", "transit route"],
                "industrial": ["manufacturing facility", "industrial complex", "production environment", "factory floor"]
            }
        }
    
    def generate_description(self, context: TemplateContext) -> Tuple[str, str]:
        """Generate a contextually appropriate description and return the base template used."""
        # Determine template complexity level
        complexity_level = self._determine_complexity_level(context.complexity)
        
        # Select appropriate template
        intent_templates = self.templates.get(context.intent_type, self.templates["Deployment Intent"])
        template_list = intent_templates.get(complexity_level, intent_templates["basic"])
        base_template = random_choice(template_list)
        
        # Generate context-specific replacements
        replacements = self._generate_replacements(context)
        
        # Apply replacements to template
        description = self._apply_replacements(base_template, replacements)
        
        return description, base_template
    
    def _determine_complexity_level(self, complexity: int) -> str:
        """Determine template complexity level based on complexity score."""
        if complexity >= 8:
            return "research"
        elif complexity >= 5:
            return "advanced"
        else:
            return "basic"
    
    def _generate_replacements(self, context: TemplateContext) -> Dict[str, str]:
        """Generate context-specific replacement values."""
        replacements = {
            "network_function": random_choice(NETWORK_FUNCTIONS),
            "slice_type": context.parameters.get('slice_type', random_choice(ADVANCED_SLICE_TYPES)).replace('_', ' '),
            "location": context.parameters.get('location', 'network location'),
            "complexity_modifier": random_choice(self.modifiers["complexity_modifier"]),
            "performance_modifier": random_choice(self.modifiers["performance_modifier"]),
            "technical_feature": random_choice(self.modifiers["technical_feature"]),
            "orchestration_feature": random_choice(self.modifiers["orchestration_feature"]),
            "ai_feature": random_choice(self.modifiers["ai_feature"]),
            "security_feature": random_choice(self.modifiers["security_feature"]),
            "monitoring_feature": random_choice(self.modifiers["monitoring_feature"])
        }
        
        # Add intent-specific replacements
        if context.intent_type == "Modification Intent":
            replacements.update({
                "target_resource": random_choice(["VNF instance", "network slice", "QoS flow", "PDU session"]),
                "operation_type": random_choice(["modify info", "change flavour", "change connectivity", "operate"]),
                "change_pattern": random_choice(["rolling update", "blue-green", "canary", "immediate"]),
                "rollback_feature": "intelligent rollback mechanisms",
                "validation_feature": "comprehensive validation procedures"
            })
        
        elif context.intent_type == "Performance Assurance Intent":
            replacements.update({
                "sla_tier": random_choice(["platinum", "gold", "silver", "bronze"]) + " tier",
                "assurance_action": random_choice(["predictive scaling", "traffic rerouting", "resource optimization"]),
                "prediction_feature": random_choice(["predictive analytics", "machine learning forecasting", "AI-driven prediction"]),
                "availability_target": f"{random_int(99, 99)}." + "9" * random_int(2, 4) + "%"
            })
        
        elif context.intent_type == "Intent Report Request":
            replacements.update({
                "report_type": random_choice(["performance analytics", "security audit", "compliance assessment", "resource utilization"]),
                "domain": random_choice(["RAN", "core", "transport", "management", "security"]),
                "time_period": random_choice(["last 24 hours", "past week", "monthly", "quarterly"]),
                "aggregation_method": random_choice(["statistical", "trend", "correlation", "predictive"]),
                "delivery_method": random_choice(["real-time", "scheduled", "on-demand", "event-driven"]),
                "validation_feature": "comprehensive data validation",
                "visualization_feature": "interactive visualization"
            })
        
        elif context.intent_type == "Intent Feasibility Check":
            replacements.update({
                "target_deployment": random_choice(["network slice", "VNF deployment", "service instantiation", "infrastructure upgrade"]),
                "assessment_scope": random_choice(["comprehensive", "technical", "economic", "operational"]),
                "risk_analysis": "advanced risk modeling",
                "economic_analysis": "economic impact assessment",
                "technical_analysis": "technical viability analysis",
                "recommendation_outcome": random_choice(["proceed", "proceed with conditions", "defer", "reject"])
            })
        
        elif context.intent_type == "Regular Notification Request":
            replacements.update({
                "event_type": random_choice(["performance", "security", "fault", "configuration", "lifecycle"]),
                "subscription_type": random_choice(["event-based", "periodic", "threshold-based", "hybrid"]),
                "delivery_mechanism": random_choice(["webhook", "Kafka", "WebSocket", "gRPC"]),
                "delivery_channel": random_choice(["webhook", "email", "SMS", "Slack"]),
                "filtering_feature": "intelligent filtering capabilities",
                "qos_guarantee": random_choice(["exactly-once", "at-least-once", "at-most-once"])
            })
        
        return replacements
    
    def _apply_replacements(self, template: str, replacements: Dict[str, str]) -> str:
        """Apply replacements to template string."""
        description = template
        
        for placeholder, value in replacements.items():
            description = description.replace(f"{{{placeholder}}}", value)
        
        # Clean up any remaining placeholders
        import re
        description = re.sub(r'\{[^}]+\}', 'network component', description)
        
        return description