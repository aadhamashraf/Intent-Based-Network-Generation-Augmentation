"""
Intent-Based Network Generation Augmentation Toolkit

This package provides comprehensive tools for generating, augmenting, analyzing, 
and evaluating advanced intent-based networking (IBN) datasets tailored for 
5G/3GPP research.

Main Components:
- Data Generation: Advanced 3GPP intent generators
- Augmentation: Multiple text augmentation techniques
- Evaluation: LLM-based and statistical evaluation tools
- Analysis: Comprehensive dataset analytics

Author: Adham Ashraf Eltholth
License: MIT
"""

__version__ = "2.0.0"
__author__ = "Adham Ashraf Eltholth"

# Import main classes for easy access
from .Intents_Generators.Advanced3GPPIntentGenerator import Advanced3GPPIntentGenerator
from .Intents_Generators.Data_Structures import NetworkIntent, EvaluationMetrics
from .augmentation_utils import *
from .config import parse_args

__all__ = [
    'Advanced3GPPIntentGenerator',
    'NetworkIntent', 
    'EvaluationMetrics',
    'parse_args'
]