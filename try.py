from pprint import pprint
from src.Intents_Generators.Report_Request_Intent_Generator import ReportRequestIntentGenerator

rr_generator = ReportRequestIntentGenerator()

print("=== GENERATED PARAMETERS ===")
generated_params = rr_generator.generate_parameters()
pprint(generated_params)

print("\n=== CONSTRAINED PARAMETERS ===")
constrained_params = rr_generator.generate_constrained_parameters(
    slice_type="URLLC",    # Example slice type
    priority="HIGH",       # Example priority
    location="Cairo",      # Example location
    complexity=3           # Example complexity level
)
pprint(constrained_params)

print("\n=== DESCRIPTION ===")
description = rr_generator.generate_description(constrained_params, "Cairo", "URLLC")
print(description)
