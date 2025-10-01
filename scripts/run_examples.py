#!/usr/bin/env python3
"""
Example scripts for Intent-Based Network Generation Augmentation toolkit.
"""
import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Intents_Generators.Advanced3GPPIntentGenerator import Advanced3GPPIntentGenerator
from Evaluation.evaluation_metric import DataEvaluator
from augmentation_utils import paraphrase, back_translate, synonym_augment, typo_augment, entity_shuffle


def example_basic_generation():
    """Example: Basic intent generation."""
    print("Example 1: Basic Intent Generation")
    print("-" * 40)
    
    generator = Advanced3GPPIntentGenerator(use_llm_synthesis=False)
    
    intents = generator.generate_batch(5)
    
    print(f"Generated {len(intents)} intents:")
    for i, intent in enumerate(intents, 1):
        print(f"\n{i}. {intent.intent_type}")
        print(f"   Description: {intent.description[:100]}...")
        print(f"   Priority: {intent.priority}")
        print(f"   Location: {intent.location}")
    
    return intents


def example_augmentation():
    """Example: Text augmentation."""
    print("\nExample 2: Text Augmentation")
    print("-" * 40)
    
    original_text = "Deploy AMF network function with high availability requirements for eMBB service"
    
    print(f"Original: {original_text}")

    augmentations = [
        ("Synonym", synonym_augment),
        ("Paraphrasing", paraphrase),
        ("Backtranslation", back_translate),
        ("Typo Simulation", typo_augment),
        ("Entity Shuffling", entity_shuffle)
    ] 

    for name, func in augmentations:
        try:
            result = func(original_text)
            print(f"{name}: {result}")
        except Exception as e:
            print(f"{name}: Error - {e}")


def example_evaluation():
    """Example: Dataset evaluation."""
    print("\nExample 3: Dataset Evaluation")
    print("-" * 40)
    
    sample_intents = [
        "Deploy AMF network function with high availability requirements",
        "Configure network slice for eMBB service with enhanced performance",
        "Establish performance monitoring for URLLC applications"
    ]
    
    print("Sample intents for evaluation:")
    for i, intent in enumerate(sample_intents, 1):
        print(f"{i}. {intent}")
    
    try:
        evaluator = DataEvaluator()
        result = evaluator.evaluate_batch(sample_intents)
        
        print(f"\nEvaluation Results:")
        print(f"Overall Quality: {result['overall_metrics'].overall_quality:.2f}")
        print(f"Technical Accuracy: {result['overall_metrics'].technical_accuracy:.2f}")
        
    except Exception as e:
        print(f"\nEvaluation failed (expected without LLM setup): {e}")


def example_export_formats():
    """Example: Different export formats."""
    print("\nExample 4: Export Formats")
    print("-" * 40)
    
    generator = Advanced3GPPIntentGenerator(use_llm_synthesis=False)
    intents = generator.generate_batch(3)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    csv_file = f"example_output_{timestamp}.csv"
    generator.export_to_csv(intents, csv_file)
    print(f"✓ Exported to CSV: {csv_file}")
    
    json_file = f"example_output_{timestamp}.json"
    generator.export_to_json(intents, json_file)
    print(f"✓ Exported to JSON: {json_file}")
    
    research_file = f"example_research_{timestamp}.json"
    generator.export_research_dataset(intents, research_file)
    print(f"✓ Exported research dataset: {research_file}")
    
    return csv_file, json_file, research_file


def example_custom_configuration():
    """Example: Custom configuration."""
    print("\nExample 5: Custom Configuration")
    print("-" * 40)
    
    generator = Advanced3GPPIntentGenerator(use_llm_synthesis=False)
    
    def progress_callback(current, total):
        if current % 2 == 0:  # Print every 2nd update
            print(f"Progress: {current}/{total} ({current/total*100:.1f}%)")
    
    print("Generating 10 intents with progress tracking:")
    intents = generator.generate_batch(10, progress_callback)
    
    intent_types = {}
    priorities = {}
    
    for intent in intents:
        intent_types[intent.intent_type] = intent_types.get(intent.intent_type, 0) + 1
        priorities[intent.priority] = priorities.get(intent.priority, 0) + 1
    
    print(f"\nGenerated {len(intents)} intents")
    print("Intent Type Distribution:")
    for intent_type, count in intent_types.items():
        print(f"  {intent_type}: {count}")
    
    print("Priority Distribution:")
    for priority, count in priorities.items():
        print(f"  {priority}: {count}")


def main():
    """Run all examples."""
    print("Intent-Based Network Generation Augmentation Toolkit")
    print("Example Scripts")
    print("=" * 60)
    
    try:
        intents = example_basic_generation()
        example_augmentation()
        example_evaluation()
        files = example_export_formats()
        example_custom_configuration()
        
        print("\n" + "=" * 60)
        print("✓ All examples completed successfully!")
        print(f"\nGenerated files:")
        for file in files:
            if os.path.exists(file):
                print(f"  - {file}")
        
        print(f"\nTo clean up generated files, run:")
        print(f"  rm example_output_* example_research_*")
        
    except Exception as e:
        print(f"\n✗ Example failed: {e}")
        print("This may be due to missing dependencies or models.")
        print("Run: python scripts/setup_environment.py")


if __name__ == "__main__":
    main()