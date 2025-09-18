
import re
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from Intents_Generators.Parameter_Generator import ParameterGenerator
from Intents_Generators.Constants_Enums import NETWORK_FUNCTIONS, ADVANCED_SLICE_TYPES, QOS_FLOW_IDENTIFIERS, RADIO_PARAMETERS, PROTOCOL_PARAMETERS, PERFORMANCE_METRICS
from Intents_Generators.Template_Engine import AdvancedTemplateEngine

# 1. Collect all available parameter names from ParameterGenerator and constants
all_param_names = set()

def collect_keys(d, prefix=""):
    for k, v in d.items():
        if isinstance(v, dict):
            collect_keys(v, prefix + k + ".")
        else:
            all_param_names.add(prefix + k if prefix == "" else prefix + k)

# Network topology
collect_keys(ParameterGenerator.generate_network_topology())
# QoS
collect_keys(ParameterGenerator.generate_qos_parameters())
# Security
collect_keys(ParameterGenerator.generate_security_parameters())
# Resource allocation
collect_keys(ParameterGenerator.generate_resource_allocation())
# Monitoring
collect_keys(ParameterGenerator.generate_monitoring_parameters())

# Add constants (flat lists)
all_param_names.update([
    "network_function", "slice_type", "location", "qos_flow_identifier"
])

# 2. Extract all unique placeholders from all templates
engine = AdvancedTemplateEngine()
placeholder_pattern = re.compile(r"{([a-zA-Z0-9_]+)}")
used_placeholders = set()
for intent_type, levels in engine.templates.items():
    for level, templates in levels.items():
        for template in templates:
            used_placeholders.update(placeholder_pattern.findall(template))

# 3. Calculate intersection and percentage
used_params = all_param_names & used_placeholders

print(f"Total available parameters: {len(all_param_names)}")
print(f"Total placeholders in templates: {len(used_placeholders)}")
print(f"Parameters used in templates: {len(used_params)}")
print(f"Used parameter names: {sorted(used_params)}")
print(f"Percentage of used parameters: {len(used_params) / len(all_param_names) * 100:.2f}%")
