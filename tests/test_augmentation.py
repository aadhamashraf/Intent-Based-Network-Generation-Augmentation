#!/usr/bin/env python3
"""
Test suite for augmentation utilities.
"""
import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from augmentation_utils import (synonym_augment, typo_augment, entity_shuffle, adversarial_noise)


class TestAugmentationUtils(unittest.TestCase):
    """Test cases for augmentation utilities."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_text = "Deploy AMF network function with high availability"
    
    def test_synonym_augment(self):
        """Test synonym augmentation."""
        result = synonym_augment(self.test_text)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertAlmostEqual(len(result.split()), len(self.test_text.split()), delta=2)
    
    def test_typo_augment(self):
        """Test typo augmentation."""
        result = typo_augment(self.test_text)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertAlmostEqual(len(result), len(self.test_text), delta=2)
    
    def test_entity_shuffle(self):
        """Test entity shuffling."""
        result = entity_shuffle(self.test_text)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        result_words = set(result.split())
        original_words = set(self.test_text.split())
        self.assertEqual(result_words, original_words)
    
    def test_adversarial_noise(self):
        """Test adversarial noise."""
        result = adversarial_noise(self.test_text)
        
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
        self.assertAlmostEqual(len(result), len(self.test_text), delta=3)
    
    def test_empty_text_handling(self):
        """Test handling of empty text."""
        empty_text = ""
        
        self.assertEqual(synonym_augment(empty_text), empty_text)
        self.assertEqual(entity_shuffle(empty_text), empty_text)
    
    def test_short_text_handling(self):
        """Test handling of very short text."""
        short_text = "Hi" 
        
        self.assertIsInstance(synonym_augment(short_text), str)
        self.assertIsInstance(entity_shuffle(short_text), str)


if __name__ == '__main__':
    unittest.main()