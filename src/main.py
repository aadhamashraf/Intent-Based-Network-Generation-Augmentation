"""Main execution function."""
print("Advanced 3GPP Intent-Based Networking Data Generator")
print("=" * 60)

# Initialize generator
generator = Advanced3GPPIntentGenerator(use_llm_synthesis=True)

# Generate dataset
print("Generating 5000 sophisticated intent records...")

def progress_callback(current, total):
    progress = (current / total) * 100
    print(f"Progress: {progress:.1f}% ({current}/{total})")

intents = generator.generate_batch(5000, progress_callback)

print(f"Generated {len(intents)} intent records")

# Evaluate dataset
print("\nEvaluating dataset quality...")
evaluation_results = generator.evaluate_dataset(intents)

print("Dataset Quality Metrics:")
metrics = evaluation_results['overall_metrics']
print(f"  - Overall Quality: {metrics.overall_quality:.2f}/10")
print(f"  - Technical Accuracy: {metrics.technical_accuracy:.2f}/10")
print(f"  - 3GPP Compliance: {metrics.compliance_level:.2f}/10")
print(f"  - Research Value: {metrics.research_value:.2f}/10")

# Export data
print("\nExporting datasets...")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Export JSON
json_filename = f"3gpp_intents_{timestamp}.json"
generator.export_to_json(intents, json_filename)
print(f"  - JSON: {json_filename}")

# Export CSV
csv_filename = f"3gpp_intents_{timestamp}.csv"
generator.export_to_csv(intents, csv_filename)
print(f"  - CSV: {csv_filename}")

# Export research dataset
research_filename = f"3gpp_research_dataset_{timestamp}.json"
generator.export_research_dataset(intents, research_filename, evaluation_results)
print(f"  - Research Dataset: {research_filename}")

print("\nGeneration complete!")
print("\nDataset Statistics:")
print(f"  - Total Records: {len(intents)}")

# Intent type distribution
intent_stats = {}
for intent_type in IntentType:
    count = len([i for i in intents if i.intent_type == intent_type.value])
    intent_stats[intent_type.value] = count
    print(f"  - {intent_type.value}: {count}")

# Complexity distribution
complexity_stats = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0}
for intent in intents:
    complexity = intent.metadata.get('technical_complexity', 5)
    if complexity <= 3:
        complexity_stats['LOW'] += 1
    elif complexity <= 7:
        complexity_stats['MEDIUM'] += 1
    else:
        complexity_stats['HIGH'] += 1

print("\nComplexity Distribution:")
for level, count in complexity_stats.items():
    print(f"  - {level}: {count}")

print("\nKey Insights:")
for insight in evaluation_results['batch_insights']:
    print(f"  - {insight}")
