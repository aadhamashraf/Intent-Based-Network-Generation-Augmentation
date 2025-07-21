#!/usr/bin/env python3
"""
Test suite for evaluation components.
"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from Evaluation.evaluation_metric import DataEvaluator, EvaluationMetrics


class TestEvaluation(unittest.TestCase):
    """Test cases for evaluation components."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.evaluator = DataEvaluator()
        self.sample_intents = [
            "Deploy AMF network function with high availability requirements",
            "Configure network slice for eMBB service with enhanced performance",
            "Establish performance monitoring for URLLC applications"
        ]
    
    def test_evaluator_initialization(self):
        """Test evaluator initialization."""
        self.assertIsNotNone(self.evaluator)
        self.assertIsInstance(self.evaluator.quality_thresholds, dict)
        self.assertIn('technical_accuracy', self.evaluator.quality_thresholds)
    
    def test_evaluation_metrics_structure(self):
        """Test evaluation metrics structure."""
        metrics = EvaluationMetrics(
            technical_accuracy=8.5,
            realism_score=7.8,
            compliance_level=9.0,
            research_value=7.5,
            implementability=8.0,
            overall_quality=8.2
        )
        
        self.assertEqual(metrics.technical_accuracy, 8.5)
        self.assertEqual(metrics.realism_score, 7.8)
        self.assertEqual(metrics.compliance_level, 9.0)
        self.assertEqual(metrics.research_value, 7.5)
        self.assertEqual(metrics.implementability, 8.0)
        self.assertEqual(metrics.overall_quality, 8.2)
    
    def test_batch_evaluation_structure(self):
        """Test batch evaluation structure."""
        # Note: This test may not work without Ollama/LLM setup
        # We'll test the structure instead
        try:
            result = self.evaluator.evaluate_batch(self.sample_intents)
            
            # Check result structure
            self.assertIn('overall_metrics', result)
            self.assertIn('detailed_evaluations', result)
            self.assertIn('batch_insights', result)
            
            # Check metrics type
            self.assertIsInstance(result['overall_metrics'], EvaluationMetrics)
            
        except Exception as e:
            # If LLM is not available, that's expected
            self.assertIn('ollama', str(e).lower())
    
    def test_quality_thresholds(self):
        """Test quality thresholds."""
        thresholds = self.evaluator.quality_thresholds
        
        required_thresholds = [
            'technical_accuracy', 'realism_score', 'compliance_level',
            'research_value', 'implementability', 'overall_quality'
        ]
        
        for threshold in required_thresholds:
            self.assertIn(threshold, thresholds)
            self.assertIsInstance(thresholds[threshold], (int, float))
            self.assertGreaterEqual(thresholds[threshold], 0)
            self.assertLessEqual(thresholds[threshold], 10)


if __name__ == '__main__':
    unittest.main()