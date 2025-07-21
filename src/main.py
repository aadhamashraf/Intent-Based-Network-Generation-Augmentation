#!/usr/bin/env python3
"""
Main execution script for the Intent-Based Network Generation Augmentation toolkit.

This script demonstrates the complete workflow:
1. Generate sophisticated 3GPP intent records
2. Apply various augmentation techniques
3. Evaluate dataset quality
4. Export in multiple formats

Usage:
    python main.py [options]
    
For command-line options, see config.py
"""

import sys
import os
import json
import random
from datetime import datetime
from dataclasses import asdict

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from Intents_Generators.Advanced3GPPIntentGenerator import Advanced3GPPIntentGenerator
from Intents_Generators.Constants_Enums import IntentType
from Intents_Generators.utilis_generator import generate_unique_id
from Evaluation.evaluation_metric import DataEvaluator
from config import parse_args
from augmentation_utils import *

def main():
    """Main execution function with command-line argument support."""
    args = parse_args()
    
    print("Advanced 3GPP Intent-Based Networking Data Generator")
    print("=" * 60)
    print(f"Configuration:")
    print(f"  - Records to generate: {args.num_records}")
    print(f"  - Random seed: {args.random_seed}")
    print(f"  - Output CSV: {args.output_file}")
    print(f"  - Output JSONL: {args.jsonl_file}")
    
    # Set random seed for reproducibility
    random.seed(args.random_seed)
    
    # Initialize generator
    generator = Advanced3GPPIntentGenerator(use_llm_synthesis=True)
    
    # Generate dataset
    print(f"\nGenerating {args.num_records} sophisticated intent records...")
    
    def progress_callback(current, total):
        progress = (current / total) * 100
        print(f"Progress: {progress:.1f}% ({current}/{total})")
    
    intents = generator.generate_batch(args.num_records, progress_callback)
    print(f"Generated {len(intents)} intent records")
    
    # Apply augmentations if requested
    augmented_intents = []
    if any([args.use_paraphrasing, args.use_backtranslation, args.use_synonym_aug, 
            args.use_gpt2_aug, args.use_contextual_synonym_aug, args.use_bert_fill_aug, 
            args.use_adversarial_aug]):
        
        print("\nApplying augmentation techniques...")
        
        for intent in intents:
            # Original intent
            augmented_intents.append(intent)
            
            # Apply augmentations based on ratios
            if args.use_paraphrasing and random.random() < args.paraphrase_ratio:
                augmented_intent = intent.__class__(**intent.__dict__)
                augmented_intent.description = paraphrase(intent.description)
                augmented_intent.id = generate_unique_id("AUG_PARA")
                augmented_intents.append(augmented_intent)
            
            if args.use_backtranslation and random.random() < args.backtranslate_ratio:
                augmented_intent = intent.__class__(**intent.__dict__)
                augmented_intent.description = back_translate(intent.description)
                augmented_intent.id = generate_unique_id("AUG_BT")
                augmented_intents.append(augmented_intent)
            
            if args.use_synonym_aug and random.random() < args.synonym_ratio:
                augmented_intent = intent.__class__(**intent.__dict__)
                augmented_intent.description = synonym_augment(intent.description)
                augmented_intent.id = generate_unique_id("AUG_SYN")
                augmented_intents.append(augmented_intent)
            
            
        print(f"Augmented dataset size: {len(augmented_intents)} records")
        intents = augmented_intents
    
    # Evaluate dataset
    print("\nEvaluating dataset quality...")
    evaluator = DataEvaluator()
    evaluation_results = evaluator.evaluate_batch([intent.description for intent in intents[:5]])  # Sample for demo
    
    print("Dataset Quality Metrics:")
    metrics = evaluation_results['overall_metrics']
    print(f"  - Overall Quality: {metrics.overall_quality:.2f}/10")
    print(f"  - Technical Accuracy: {metrics.technical_accuracy:.2f}/10")
    print(f"  - 3GPP Compliance: {metrics.compliance_level:.2f}/10")
    print(f"  - Research Value: {metrics.research_value:.2f}/10")
    
    # Export data
    print("\nExporting datasets...")
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Export CSV
    csv_filename = args.output_file.replace('.csv', f'_{timestamp}.csv')
    generator.export_to_csv(intents, csv_filename)
    print(f"  - CSV: {csv_filename}")
    
    # Export JSONL
    jsonl_filename = args.jsonl_file.replace('.jsonl', f'_{timestamp}.jsonl')
    with open(jsonl_filename, 'w', encoding='utf-8') as f:
        for intent in intents:
            f.write(json.dumps(asdict(intent), ensure_ascii=False) + '\n')
    print(f"  - JSONL: {jsonl_filename}")
    
    # Export research dataset
    research_filename = f"3gpp_research_dataset_{timestamp}.json"
    generator.export_research_dataset(intents, research_filename, evaluation_results)
    print(f"  - Research Dataset: {research_filename}")
    
    # Export metadata
    metadata = {
        "generation_timestamp": datetime.now().isoformat(),
        "total_records": len(intents),
        "configuration": vars(args),
        "evaluation_summary": {
            "overall_quality": metrics.overall_quality,
            "technical_accuracy": metrics.technical_accuracy,
            "compliance_level": metrics.compliance_level,
            "research_value": metrics.research_value
        }
    }
    
    with open(args.metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"  - Metadata: {args.metadata_file}")
    
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

if __name__ == "__main__":
    main()
