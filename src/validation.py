"""
Parameter validation module for Intent-Based Network Generation.

This module provides validation utilities to ensure data quality and
prevent silent failures when parameters are missing or invalid.
"""
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ValidationIssue:
    """Represents a validation issue found during parameter checking."""
    parameter_path: str
    severity: str  # 'WARNING', 'ERROR', 'INFO'
    message: str
    default_used: Optional[Any] = None


class ParameterValidator:
    """
    Validates parameters and logs quality issues.
    
    This class tracks when default values are used instead of actual
    generated parameters, helping identify data quality problems.
    """
    
    def __init__(self, strict_mode: bool = False):
        """
        Initialize the validator.
        
        Args:
            strict_mode: If True, raise exceptions on validation failures.
                        If False, log warnings and continue.
        """
        self.strict_mode = strict_mode
        self.issues: List[ValidationIssue] = []
        self._setup_quality_logger()
    
    def _setup_quality_logger(self):
        """Set up dedicated logger for data quality issues."""
        self.quality_logger = logging.getLogger('data_quality')
        if not self.quality_logger.handlers:
            handler = logging.FileHandler('data_quality.log')
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.quality_logger.addHandler(handler)
            self.quality_logger.setLevel(logging.WARNING)
    
    def validate_parameter(
        self,
        value: Any,
        path: str,
        expected_type: Optional[type] = None,
        required: bool = True
    ) -> bool:
        """
        Validate a single parameter.
        
        Args:
            value: The parameter value to validate
            path: Dot-separated path to the parameter
            expected_type: Expected Python type
            required: Whether the parameter is required
            
        Returns:
            True if validation passed, False otherwise
        """
        # Check if value is None
        if value is None:
            if required:
                issue = ValidationIssue(
                    parameter_path=path,
                    severity='ERROR',
                    message=f'Required parameter {path} is None'
                )
                self.issues.append(issue)
                self.quality_logger.error(issue.message)
                
                if self.strict_mode:
                    raise ValueError(issue.message)
                return False
            else:
                return True
        
        # Check type if specified
        if expected_type is not None and not isinstance(value, expected_type):
            issue = ValidationIssue(
                parameter_path=path,
                severity='WARNING',
                message=f'Parameter {path} has type {type(value).__name__}, expected {expected_type.__name__}'
            )
            self.issues.append(issue)
            self.quality_logger.warning(issue.message)
            
            if self.strict_mode:
                raise TypeError(issue.message)
            return False
        
        return True
    
    def log_default_usage(self, path: str, default_value: Any, reason: str = ""):
        """
        Log when a default value is used instead of a generated parameter.
        
        Args:
            path: Dot-separated path to the parameter
            default_value: The default value being used
            reason: Optional reason why default was used
        """
        message = f'Using default value for {path}: {default_value}'
        if reason:
            message += f' (Reason: {reason})'
        
        issue = ValidationIssue(
            parameter_path=path,
            severity='WARNING',
            message=message,
            default_used=default_value
        )
        self.issues.append(issue)
        self.quality_logger.warning(message)
    
    def validate_parameter_dict(
        self,
        params: Dict[str, Any],
        required_keys: List[str],
        path_prefix: str = ""
    ) -> bool:
        """
        Validate a dictionary of parameters.
        
        Args:
            params: Dictionary of parameters to validate
            required_keys: List of required keys
            path_prefix: Prefix for parameter paths (for nested dicts)
            
        Returns:
            True if all required keys present, False otherwise
        """
        all_valid = True
        
        for key in required_keys:
            full_path = f"{path_prefix}.{key}" if path_prefix else key
            
            if key not in params:
                issue = ValidationIssue(
                    parameter_path=full_path,
                    severity='ERROR',
                    message=f'Required key {full_path} missing from parameters'
                )
                self.issues.append(issue)
                self.quality_logger.error(issue.message)
                all_valid = False
                
                if self.strict_mode:
                    raise KeyError(issue.message)
        
        return all_valid
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of validation issues.
        
        Returns:
            Dictionary with issue counts and details
        """
        return {
            'total_issues': len(self.issues),
            'errors': len([i for i in self.issues if i.severity == 'ERROR']),
            'warnings': len([i for i in self.issues if i.severity == 'WARNING']),
            'defaults_used': len([i for i in self.issues if i.default_used is not None]),
            'issues': self.issues
        }
    
    def clear_issues(self):
        """Clear the list of accumulated issues."""
        self.issues = []


# Global validator instance
_global_validator = ParameterValidator(strict_mode=False)


def get_validator() -> ParameterValidator:
    """Get the global validator instance."""
    return _global_validator


def set_strict_mode(enabled: bool):
    """Enable or disable strict validation mode globally."""
    _global_validator.strict_mode = enabled
