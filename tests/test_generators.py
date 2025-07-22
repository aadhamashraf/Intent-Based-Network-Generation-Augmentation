#!/usr/bin/env python3
"""
Test suite for intent generators.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Intents_Generators.Advanced3GPPIntentGenerator import Advanced3GPPIntentGenerator
from Intents_Generators.Constants_Enums import IntentType, Priority
from Intents_Generators.Data_Structures import NetworkIntent


class TestIntentGenerators(unittest.TestCase):
    """Test cases for intent generators."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = Advanced3GPPIntentGenerator(use_llm_synthesis=False)
    
    def test_generator_initialization(self):
        """Test generator initialization."""
        self.assertIsNotNone(self.generator)
        self.assertFalse(self.generator.use_llm_synthesis)
        self.assertEqual(len(self.generator.generators), len(IntentType))
    
    def test_single_intent_generation(self):
        """Test single intent generation."""
        intent = self.generator.generate_intent()
        
        self.assertIsInstance(intent, NetworkIntent)
        self.assertIsNotNone(intent.id)
        self.assertIsNotNone(intent.intent_type)
        self.assertIsNotNone(intent.description)
        self.assertIsNotNone(intent.timestamp)
        self.assertIsNotNone(intent.priority)
        self.assertIsInstance(intent.parameters, dict)
        self.assertIsInstance(intent.metadata, dict)
    
    def test_batch_generation(self):
        """Test batch intent generation."""
        batch_size = 5
        intents = self.generator.generate_batch(batch_size)
        
        self.assertEqual(len(intents), batch_size)
        
        # Check all intents are valid
        for intent in intents:
            self.assertIsInstance(intent, NetworkIntent)
            self.assertIsNotNone(intent.id)
            self.assertIsNotNone(intent.description)
    
    def test_intent_types_coverage(self):
        """Test that all intent types can be generated."""
        intents = self.generator.generate_batch(50)
        
        # Get all generated intent types
        generated_types = set(intent.intent_type for intent in intents)
        
        # Should have multiple types (though not necessarily all)
        self.assertGreater(len(generated_types), 1)
    
    def test_priority_levels(self):
        """Test priority level generation."""
        intents = self.generator.generate_batch(20)
        
        generated_priorities = set(intent.priority for intent in intents)
        
        self.assertGreater(len(generated_priorities), 1)
        
        valid_priorities = {p.value for p in Priority}
        for priority in generated_priorities:
            self.assertIn(priority, valid_priorities)
    
    def test_metadata_structure(self):
        """Test metadata structure."""
        intent = self.generator.generate_intent()
        
        required_metadata_fields = ['version', 'standard', 'compliance', 'research_context','technical_complexity', 'generation_timestamp']
        
        for field in required_metadata_fields:
            self.assertIn(field, intent.metadata)
    
    def test_parameters_structure(self):
        """Test parameters structure."""
        intent = self.generator.generate_intent()
        
        self.assertIsInstance(intent.parameters, dict)
        self.assertGreater(len(intent.parameters), 0)
        
        self.assertIn('timestamp', intent.parameters)
        self.assertIn('request_id', intent.parameters)


class TestSpecificGenerators(unittest.TestCase):
    """Test specific intent generators."""
    
    def test_deployment_generator(self):
        """Test deployment intent generator."""
        from Intents_Generators.Deployment_Intent_Generator import DeploymentIntentGenerator
        
        generator = DeploymentIntentGenerator()
        params = generator.generate_parameters()
        
        self.assertIsInstance(params, dict)
        self.assertIn('deployment_specification', params)
        self.assertIn('orchestration_parameters', params)
    
    def test_modification_generator(self):
        """Test modification intent generator."""
        from Intents_Generators.Modification_Intent_Generator import ModificationIntentGenerator
        
        generator = ModificationIntentGenerator()
        params = generator.generate_parameters()
        
        self.assertIsInstance(params, dict)
        self.assertIn('modification_specification', params)
    
    def test_performance_generator(self):
        """Test performance assurance intent generator."""
        from Intents_Generators.Performance_Assurance_Intent_Generator import PerformanceAssuranceIntentGenerator
        
        generator = PerformanceAssuranceIntentGenerator()
        params = generator.generate_parameters()
        
        self.assertIsInstance(params, dict)
        self.assertIn('performance_objectives', params)


if __name__ == '__main__':
    unittest.main()