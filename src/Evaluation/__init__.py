"""
Evaluation Module

This module provides comprehensive evaluation tools for intent-based
networking datasets including LLM-based evaluation, statistical analysis,
and automated summarization.

Components:
- LLM_evaluation: Expert-level LLM evaluation using local models
- base_evaluation: Statistical and linguistic analysis
- evaluation_metric: Structured evaluation metrics and scoring
- evaluation_summarizer: Automated report generation and insights
"""

from .evaluation_metric import EvaluationMetrics, DataEvaluator

__all__ = [
    'EvaluationMetrics',
    'DataEvaluator'
]