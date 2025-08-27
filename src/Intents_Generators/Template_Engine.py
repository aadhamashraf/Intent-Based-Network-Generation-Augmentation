"""
Advanced Template Engine for Intent-Based Network Generation

This module provides sophisticated template generation that heavily leverages
all generated parameters to create realistic, interconnected network intent
descriptions with concrete values and cross-referenced components.
"""

import random
import re
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class TemplateContext:
    """Context for template generation with comprehensive parameter integration."""
    intent_type: str
    complexity: int
    priority: str
    slice_category: str
    location_category: str
    parameters: Dict[str, Any]
    metadata: Dict[str, Any]

class AdvancedTemplateEngine:
    """Advanced template engine with deep parameter integration."""
    
    def __init__(self):
        self.deployment_templates = self._initialize_deployment_templates()
        self.modification_templates = self._initialize_modification_templates()
        self.performance_templates = self._initialize_performance_templates()
        self.report_templates = self._initialize_report_templates()
        self.feasibility_templates = self._initialize_feasibility_templates()
        self.notification_templates = self._initialize_notification_templates()
        
        self.template_registry = {
            'Deployment Intent': self.deployment_templates,
            'Modification Intent': self.modification_templates,
            'Performance Assurance Intent': self.performance_templates,
            'Intent Report Request': self.report_templates,
            'Intent Feasibility Check': self.feasibility_templates,
            'Regular Notification Request': self.notification_templates
        }
    
    def generate_description(self, context: TemplateContext) -> str:
        """Generate sophisticated description using context and parameters."""
        templates = self.template_registry.get(context.intent_type, self.deployment_templates)
        
        # Select template based on complexity and priority
        template_category = self._select_template_category(context)
        selected_templates = templates.get(template_category, templates['deployment_focused'])
        
        template = random.choice(selected_templates)
        
        # Replace placeholders with actual parameter values
        description = self._populate_template(template, context)
        
        return description
    
    def _select_template_category(self, context: TemplateContext) -> str:
        """Select appropriate template category based on context."""
        if context.complexity >= 8:
            categories = ['orchestration_focused', 'security_focused', 'performance_focused']
        elif context.complexity >= 6:
            categories = ['deployment_focused', 'performance_focused', 'orchestration_focused']
        else:
            categories = ['deployment_focused', 'qos_focused']
        
        if context.priority in ['CRITICAL', 'EMERGENCY']:
            categories = ['security_focused', 'performance_focused'] + categories
        
        return random.choice(categories)
    
    def _populate_template(self, template: str, context: TemplateContext) -> str:
        """Populate template with actual parameter values."""
        description = template
        params = context.parameters
        substitutions = {
            '{location}': self._get_location_description(context),
            '{slice_type}': self._get_slice_description(context),
            '{priority_level}': context.priority.lower(),
            '{complexity_level}': self._get_complexity_description(context.complexity),
        }

        # --- Add all parameter substitutions (deployment, qos, resources, etc.) ---
        # (your substitution code remains as-is, unchanged for brevity)

        # Apply all substitutions
        for placeholder, value in substitutions.items():
            description = description.replace(placeholder, str(value))
        
        # Clean up any remaining placeholders
        description = re.sub(r'\{[^}]+\}', 'advanced', description)
        
        return description
    
    def _get_location_description(self, context: TemplateContext) -> str:
        location_map = {
            'urban': 'high-density metropolitan deployment zone',
            'rural': 'extended coverage rural service area',
            'highway': 'high-mobility corridor infrastructure',
            'industrial': 'mission-critical industrial automation facility'
        }
        return location_map.get(context.location_category, 'advanced network deployment location')
    
    def _get_slice_description(self, context: TemplateContext) -> str:
        slice_map = {
            'eMBB': 'enhanced mobile broadband service tier',
            'URLLC': 'ultra-reliable low-latency communication framework',
            'mMTC': 'massive machine-type communication infrastructure',
            'V2X': 'vehicle-to-everything connectivity ecosystem'
        }
        return slice_map.get(context.slice_category, 'advanced network slice configuration')
    
    def _get_complexity_description(self, complexity: int) -> str:
        if complexity >= 9:
            return 'research-grade sophisticated'
        elif complexity >= 7:
            return 'enterprise-class advanced'
        elif complexity >= 5:
            return 'production-ready comprehensive'
        else:
            return 'standard optimized'

    # --------------------------
    # Template Initializers
    # --------------------------

    def _initialize_deployment_templates(self) -> Dict[str, List[str]]:
        return {
            "deployment_focused": [
                "Ensure {reliability_requirement} reliability with {horizontal_scaling}, {vertical_scaling}, and {auto_scaling_policy} adjustments.",
                "Assess {backhaul_type} at {backhaul_capacity} and {backhaul_latency}, sustaining {slice_type} traffic demands in {location}.",
                "Confirm {auth_method} and {encryption_algorithm} performance impact on {slice_type} service.",
                "Validate {ml_anomaly_model} anomaly detection, {optimization_algorithm} optimization, and {sampling_rate} data monitoring.",
                "Audit {storage_type} I/O performance, {packet_error_rate}, and {latency_requirement_perf} adherence.",
                "Check {antenna_type}, {beamforming_capability}, and {mid_band_spectrum}-{high_band_spectrum} utilization for {slice_type} optimization.",
                "Report {availability_requirement} uptime, {reliability_requirement} stability, and {integrity_protection} effectiveness under {priority_level} operations."
            ]
        }

    def _initialize_modification_templates(self) -> Dict[str, List[str]]:
        return {
            "orchestration_focused": [
                "Modify {network_function} deployment to {deployment_flavor} at {location} ensuring {availability_requirement}.",
                "Reconfigure {vnf_provider} {vnf_version} to support {slice_type} with {cpu_cores} cores and {memory_size}.",
                "Adjust orchestration flow {workflow_version} with {execution_timeout} timeout and {rollback_strategy} fallback.",
            ]
        }

    def _initialize_performance_templates(self) -> Dict[str, List[str]]:
        return {
            "performance_focused": [
                "Optimize throughput to {throughput_requirement} while maintaining {latency_requirement_perf} latency and {availability_requirement} uptime.",
                "Recalibrate SLA thresholds: {guaranteed_bitrate}, {packet_delay_budget}, {packet_error_rate}.",
                "Enforce {auto_scaling_policy} scaling policy to maintain {cpu_frequency}, {memory_size}, and {bandwidth_allocation}.",
            ]
        }

    def _initialize_report_templates(self) -> Dict[str, List[str]]:
        return {
            "report_focused": [
                "Generate {network_function} report: {cpu_cores} usage, {memory_size}, {storage_capacity}, {bandwidth_allocation}, and {availability_requirement} uptime.",
                "Compile orchestration analytics via {nfvo_id}, {vnfm_id}, {workflow_version}, and {execution_timeout} for {priority_level} {slice_type}.",
                "Summarize SLA performance: {guaranteed_bitrate}, {latency_requirement_perf}, and {reliability_requirement}.",
                "Provide {deployment_flavor} efficiency metrics, {instantiation_level}, and {auto_scaling_policy} results.",
                "Report security stats on {auth_method}, {encryption_algorithm}, {key_length}, and {key_rotation_interval}.",
                "Generate KPI trends with {sampling_rate}, {aggregation_interval}, {retention_period}, and {ml_anomaly_model}.",
                "Assess {qos_flow_id}, {packet_delay_budget}, {priority_level_num}, and {jitter_tolerance} handling.",
                "Compile connectivity analytics for {backhaul_type}, {backhaul_capacity}, and {backhaul_latency}.",
                "Summarize radio performance with {antenna_type}, {beamforming_capability}, and {mid_band_spectrum}-{high_band_spectrum} spectrum.",
                "Generate holistic report: {optimization_algorithm} tuning, {auto_scaling_policy}, and {availability_requirement} guarantees."
            ]
        }

    def _initialize_feasibility_templates(self) -> Dict[str, List[str]]:
        return {
            "feasibility_focused": [
                "Assess feasibility of {network_function} handling {guaranteed_bitrate} with {latency_requirement} and {cpu_cores}-core {cpu_frequency} at {location}.",
                "Check if {deployment_flavor} with {memory_size}, {storage_capacity}, and {availability_requirement} is viable.",
                "Evaluate {auth_method}, {encryption_algorithm}, {key_rotation_interval}, and {integrity_protection} feasibility for {slice_type}.",
                "Test if {qos_flow_id} can meet {packet_delay_budget}, {priority_level_num}, and {jitter_tolerance} requirements.",
                "Analyze {backhaul_type} with {backhaul_capacity}, {backhaul_latency}, and {connection_density} support.",
                "Review {antenna_type} with {beamforming_capability}, {mid_band_spectrum}, and {high_band_spectrum} spectrum feasibility.",
                "Determine whether {horizontal_scaling}, {vertical_scaling}, and {auto_scaling_policy} meet {priority_level} demands.",
                "Validate if {ml_anomaly_model} and {optimization_algorithm} ensure SLA feasibility.",
                "Examine {storage_type} resilience under {packet_error_rate} and {latency_requirement_perf} constraints.",
                "Confirm viability of {instantiation_level} and {workflow_version} orchestration for {slice_type} at {location}."
            ]
        }

    def _initialize_notification_templates(self) -> Dict[str, List[str]]:
        return {
            "notification_focused": [
                "Notify if {throughput_requirement} drops below SLA or {latency_requirement_perf} exceeds {priority_level} threshold.",
                "Send alert on {cpu_cores} overload, {memory_size} saturation, or {storage_capacity} nearing limit.",
                "Trigger notification for {auth_method} failures, {encryption_algorithm} breaches, or {key_rotation_interval} expiry.",
                "Alert when {packet_error_rate} exceeds tolerance or {guaranteed_bitrate} falls short.",
                "Send notification if {availability_requirement} uptime or {reliability_requirement} reliability degrades.",
                "Generate QoS alert for {qos_flow_id} flow failure or {priority_level_num} mismatch.",
                "Raise warning on {backhaul_latency} exceeding SLA or {backhaul_capacity} saturation.",
                "Notify about {antenna_type} misconfiguration, {beamforming_capability} issues, or {mid_band_spectrum}-{high_band_spectrum} interference.",
                "Alert if {horizontal_scaling} or {vertical_scaling} fails to trigger under {auto_scaling_policy}.",
                "Send monitoring notification for {ml_anomaly_model} anomalies or {optimization_algorithm} inefficiency."
            ]
        }
