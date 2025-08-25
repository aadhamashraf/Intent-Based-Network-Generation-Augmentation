"""
Advanced Template Engine for Intent Description Generation

This module provides sophisticated template-based generation of natural language
descriptions for network intents, ensuring consistency, realism, and technical accuracy.
"""
import random
from typing import Dict, Any, List
from dataclasses import dataclass

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
    """Advanced template engine for generating sophisticated intent descriptions."""
    
    def __init__(self):
        self.templates = self._initialize_templates()
        self.modifiers = self._initialize_modifiers()
        self.technical_terms = self._initialize_technical_terms()
        
    def _initialize_templates(self) -> Dict[str, List[str]]:
        """Initialize intent description templates."""
        return {
            'DEPLOYMENT': [
                "Deploy {complexity_modifier} {network_function} network function with {feature_set} at {location} supporting {slice_description} {technical_details}",
                "Establish {complexity_modifier} {network_function} deployment featuring {feature_set} for {slice_description} at {location} {technical_details}",
                "Implement {complexity_modifier} {network_function} instance with {feature_set} configuration at {location} enabling {slice_description} {technical_details}",
                "Execute {complexity_modifier} deployment of {network_function} incorporating {feature_set} at {location} for {slice_description} {technical_details}",
                "Provision {complexity_modifier} {network_function} service with {feature_set} at {location} supporting {slice_description} {technical_details}"
            ],
            'MODIFICATION': [
                "Modify {complexity_modifier} {target_resource} configuration with {modification_type} at {location} for {slice_description} {technical_details}",
                "Update {complexity_modifier} {target_resource} parameters through {modification_type} at {location} supporting {slice_description} {technical_details}",
                "Reconfigure {complexity_modifier} {target_resource} using {modification_type} approach at {location} for {slice_description} {technical_details}",
                "Adjust {complexity_modifier} {target_resource} settings via {modification_type} at {location} enabling {slice_description} {technical_details}",
                "Transform {complexity_modifier} {target_resource} through {modification_type} at {location} optimizing {slice_description} {technical_details}"
            ],
            'PERFORMANCE_ASSURANCE': [
                "Establish {complexity_modifier} performance assurance framework for {slice_description} at {location} with {sla_level} {technical_details}",
                "Implement {complexity_modifier} SLA monitoring system for {slice_description} at {location} ensuring {sla_level} {technical_details}",
                "Deploy {complexity_modifier} performance management solution for {slice_description} at {location} guaranteeing {sla_level} {technical_details}",
                "Configure {complexity_modifier} assurance mechanisms for {slice_description} at {location} maintaining {sla_level} {technical_details}",
                "Activate {complexity_modifier} performance oversight for {slice_description} at {location} delivering {sla_level} {technical_details}"
            ],
            'REPORT_REQUEST': [
                "Generate {complexity_modifier} {report_type} report for {slice_description} at {location} covering {report_scope} {technical_details}",
                "Produce {complexity_modifier} {report_type} analysis of {slice_description} at {location} including {report_scope} {technical_details}",
                "Create {complexity_modifier} {report_type} assessment for {slice_description} at {location} encompassing {report_scope} {technical_details}",
                "Compile {complexity_modifier} {report_type} evaluation of {slice_description} at {location} featuring {report_scope} {technical_details}",
                "Deliver {complexity_modifier} {report_type} summary for {slice_description} at {location} with {report_scope} {technical_details}"
            ],
            'FEASIBILITY_CHECK': [
                "Conduct {complexity_modifier} feasibility analysis for {slice_description} at {location} evaluating {assessment_scope} {technical_details}",
                "Perform {complexity_modifier} viability assessment of {slice_description} at {location} examining {assessment_scope} {technical_details}",
                "Execute {complexity_modifier} feasibility study for {slice_description} at {location} analyzing {assessment_scope} {technical_details}",
                "Undertake {complexity_modifier} capability evaluation of {slice_description} at {location} reviewing {assessment_scope} {technical_details}",
                "Complete {complexity_modifier} readiness assessment for {slice_description} at {location} investigating {assessment_scope} {technical_details}"
            ],
            'NOTIFICATION_REQUEST': [
                "Configure {complexity_modifier} notification system for {slice_description} at {location} with {notification_type} {technical_details}",
                "Establish {complexity_modifier} alerting mechanism for {slice_description} at {location} using {notification_type} {technical_details}",
                "Setup {complexity_modifier} event notification for {slice_description} at {location} via {notification_type} {technical_details}",
                "Deploy {complexity_modifier} monitoring alerts for {slice_description} at {location} through {notification_type} {technical_details}",
                "Activate {complexity_modifier} notification service for {slice_description} at {location} employing {notification_type} {technical_details}"
            ]
        }
    
    def _initialize_modifiers(self) -> Dict[str, List[str]]:
        """Initialize complexity and quality modifiers."""
        return {
            'complexity_low': ['basic', 'standard', 'conventional', 'straightforward', 'simple'],
            'complexity_medium': ['advanced', 'enhanced', 'sophisticated', 'comprehensive', 'robust'],
            'complexity_high': ['cutting-edge', 'state-of-the-art', 'revolutionary', 'next-generation', 'ultra-advanced'],
            'technical_quality': ['research-grade', 'enterprise-class', 'carrier-grade', 'mission-critical', 'production-ready'],
            'performance_focus': ['high-performance', 'optimized', 'efficient', 'scalable', 'resilient'],
            'innovation_level': ['innovative', 'pioneering', 'breakthrough', 'transformative', 'disruptive']
        }
    
    def _initialize_technical_terms(self) -> Dict[str, List[str]]:
        """Initialize technical terminology for different contexts."""
        return {
            'orchestration': ['orchestration', 'automation', 'coordination', 'management', 'control'],
            'optimization': ['optimization', 'enhancement', 'improvement', 'refinement', 'tuning'],
            'analytics': ['analytics', 'intelligence', 'insights', 'analysis', 'assessment'],
            'security': ['security', 'protection', 'hardening', 'safeguarding', 'defense'],
            'performance': ['performance', 'efficiency', 'throughput', 'responsiveness', 'capability'],
            'reliability': ['reliability', 'availability', 'resilience', 'robustness', 'stability'],
            'scalability': ['scalability', 'elasticity', 'adaptability', 'flexibility', 'extensibility']
        }
    
    def generate_description(self, context: TemplateContext) -> str:
        """Generate sophisticated intent description using templates."""
        # Select appropriate template
        templates = self.templates.get(context.intent_type, self.templates['DEPLOYMENT'])
        template = random.choice(templates)
        
        # Generate template variables
        variables = self._generate_template_variables(context)
        
        # Fill template with variables
        try:
            description = template.format(**variables)
        except KeyError as e:
            # Fallback if template variable is missing
            description = self._generate_fallback_description(context)
        
        return description
    
    def _generate_template_variables(self, context: TemplateContext) -> Dict[str, str]:
        """Generate variables for template filling."""
        variables = {
            'complexity_modifier': self._get_complexity_modifier(context.complexity),
            'location': self._format_location(context.location_category),
            'slice_description': self._format_slice_description(context.slice_category),
            'technical_details': self._generate_technical_details(context),
            'network_function': self._select_network_function(context),
            'feature_set': self._generate_feature_set(context),
            'target_resource': self._select_target_resource(context),
            'modification_type': self._select_modification_type(context),
            'sla_level': self._generate_sla_level(context),
            'report_type': self._select_report_type(context),
            'report_scope': self._generate_report_scope(context),
            'assessment_scope': self._generate_assessment_scope(context),
            'notification_type': self._select_notification_type(context)
        }
        
        return variables
    
    def _get_complexity_modifier(self, complexity: int) -> str:
        """Get complexity modifier based on complexity level."""
        if complexity <= 3:
            return random.choice(self.modifiers['complexity_low'])
        elif complexity <= 7:
            return random.choice(self.modifiers['complexity_medium'])
        else:
            return random.choice(self.modifiers['complexity_high'])
    
    def _format_location(self, location_category: str) -> str:
        """Format location for description."""
        location_descriptions = {
            'urban': 'urban deployment zone',
            'rural': 'rural coverage area',
            'industrial': 'industrial facility',
            'highway': 'highway corridor'
        }
        return location_descriptions.get(location_category, 'network location')
    
    def _format_slice_description(self, slice_category: str) -> str:
        """Format slice description."""
        slice_descriptions = {
            'eMBB': 'enhanced mobile broadband services',
            'URLLC': 'ultra-reliable low-latency communications',
            'mMTC': 'massive machine-type communications',
            'V2X': 'vehicle-to-everything connectivity'
        }
        return slice_descriptions.get(slice_category, 'network slice services')
    
    def _generate_technical_details(self, context: TemplateContext) -> str:
        """Generate technical details based on context."""
        details = []
        
        # Add complexity-based details
        if context.complexity >= 7:
            details.append(f"featuring {random.choice(self.modifiers['technical_quality'])} architecture")
        
        if context.complexity >= 8:
            details.append(f"with {random.choice(self.modifiers['innovation_level'])} capabilities")
        
        # Add priority-based details
        if context.priority in ['CRITICAL', 'EMERGENCY']:
            details.append(f"ensuring {random.choice(self.technical_terms['reliability'])} requirements")
        
        # Add slice-specific details
        if context.slice_category in ['URLLC', 'V2X']:
            details.append(f"with {random.choice(self.technical_terms['performance'])} guarantees")
        
        # Add research context
        if context.metadata.get('research_relevance') == 'HIGH':
            details.append("for advanced network research applications")
        
        return ' '.join(details) if details else "with comprehensive feature set"
    
    def _select_network_function(self, context: TemplateContext) -> str:
        """Select appropriate network function."""
        slice_nf_mapping = {
            'eMBB': ['UPF', 'SMF', 'AMF'],
            'URLLC': ['UPF', 'SMF', 'PCF', 'NWDAF'],
            'mMTC': ['UPF', 'SMF', 'UDM'],
            'V2X': ['UPF', 'AMF', 'PCF', 'NWDAF']
        }
        
        nfs = slice_nf_mapping.get(context.slice_category, ['UPF', 'SMF', 'AMF'])
        return random.choice(nfs)
    
    def _generate_feature_set(self, context: TemplateContext) -> str:
        """Generate feature set description."""
        features = []
        
        if context.complexity >= 6:
            features.append(f"{random.choice(self.technical_terms['orchestration'])} capabilities")
        
        if context.complexity >= 7:
            features.append(f"{random.choice(self.technical_terms['analytics'])} integration")
        
        if context.complexity >= 8:
            features.append(f"{random.choice(self.technical_terms['optimization'])} algorithms")
        
        if context.priority in ['CRITICAL', 'EMERGENCY']:
            features.append(f"{random.choice(self.technical_terms['security'])} hardening")
        
        return ', '.join(features) if features else "advanced configuration"
    
    def _select_target_resource(self, context: TemplateContext) -> str:
        """Select target resource for modification."""
        resources = ['VNF instance', 'network slice', 'QoS flow', 'PDU session', 'service configuration']
        return random.choice(resources)
    
    def _select_modification_type(self, context: TemplateContext) -> str:
        """Select modification type."""
        modifications = ['parameter optimization', 'configuration update', 'resource scaling', 'policy adjustment']
        return random.choice(modifications)
    
    def _generate_sla_level(self, context: TemplateContext) -> str:
        """Generate SLA level description."""
        if context.priority in ['CRITICAL', 'EMERGENCY']:
            return "99.999% availability with sub-millisecond response times"
        elif context.priority == 'HIGH':
            return "99.99% availability with optimized performance metrics"
        else:
            return "99.9% availability with standard service levels"
    
    def _select_report_type(self, context: TemplateContext) -> str:
        """Select report type."""
        reports = ['performance analytics', 'compliance assessment', 'resource utilization', 'security audit']
        return random.choice(reports)
    
    def _generate_report_scope(self, context: TemplateContext) -> str:
        """Generate report scope."""
        scopes = [
            'multi-dimensional KPI analysis',
            'comprehensive performance metrics',
            'detailed resource consumption patterns',
            'advanced correlation analytics'
        ]
        return random.choice(scopes)
    
    def _generate_assessment_scope(self, context: TemplateContext) -> str:
        """Generate assessment scope."""
        scopes = [
            'technical and economic viability',
            'operational readiness and resource availability',
            'compliance and risk assessment',
            'implementation feasibility and timeline analysis'
        ]
        return random.choice(scopes)
    
    def _select_notification_type(self, context: TemplateContext) -> str:
        """Select notification type."""
        types = [
            'real-time event streaming',
            'intelligent alerting mechanisms',
            'adaptive notification policies',
            'multi-channel delivery systems'
        ]
        return random.choice(types)
    
    def _generate_fallback_description(self, context: TemplateContext) -> str:
        """Generate fallback description if template fails."""
        complexity_mod = self._get_complexity_modifier(context.complexity)
        slice_desc = self._format_slice_description(context.slice_category)
        location = self._format_location(context.location_category)
        
        return (f"Execute {complexity_mod} {context.intent_type.lower().replace('_', ' ')} "
                f"for {slice_desc} at {location} with advanced network management capabilities "
                f"and comprehensive research-grade analytics")