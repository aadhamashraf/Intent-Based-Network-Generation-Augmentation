"""
Health check module for verifying system dependencies.

This module provides centralized dependency checking for all external
dependencies including Ollama, PyTorch, NLTK, and other ML libraries.
"""
import logging
import subprocess
import sys
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class DependencyStatus:
    """Status of a single dependency."""
    name: str
    available: bool
    version: Optional[str] = None
    error_message: Optional[str] = None


class HealthCheck:
    """
    Centralized health check system for all dependencies.
    
    This class provides methods to check availability of external
    dependencies and report their status in a structured way.
    """
    
    def __init__(self):
        """Initialize the health check system."""
        self.dependency_status: Dict[str, DependencyStatus] = {}
    
    def check_python_package(self, package_name: str, import_name: Optional[str] = None) -> DependencyStatus:
        """
        Check if a Python package is available.
        
        Args:
            package_name: Name of the package (e.g., 'torch')
            import_name: Optional different import name (e.g., 'cv2' for 'opencv-python')
            
        Returns:
            DependencyStatus object
        """
        import_name = import_name or package_name
        
        try:
            module = __import__(import_name)
            version = getattr(module, '__version__', 'unknown')
            
            status = DependencyStatus(
                name=package_name,
                available=True,
                version=version
            )
            logger.info(f"✓ {package_name} available (version: {version})")
            
        except ImportError as e:
            status = DependencyStatus(
                name=package_name,
                available=False,
                error_message=str(e)
            )
            logger.warning(f"✗ {package_name} not available: {str(e)}")
        
        self.dependency_status[package_name] = status
        return status
    
    def check_ollama(self) -> DependencyStatus:
        """
        Check if Ollama service is available and running.
        
        Returns:
            DependencyStatus object
        """
        try:
            # Try to run ollama list command
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                status = DependencyStatus(
                    name='ollama',
                    available=True,
                    version='service_running'
                )
                logger.info("✓ Ollama service is running")
            else:
                status = DependencyStatus(
                    name='ollama',
                    available=False,
                    error_message=f"Ollama command failed: {result.stderr}"
                )
                logger.warning(f"✗ Ollama service check failed: {result.stderr}")
                
        except FileNotFoundError:
            status = DependencyStatus(
                name='ollama',
                available=False,
                error_message="Ollama command not found in PATH"
            )
            logger.warning("✗ Ollama not found in PATH")
            
        except subprocess.TimeoutExpired:
            status = DependencyStatus(
                name='ollama',
                available=False,
                error_message="Ollama command timed out"
            )
            logger.warning("✗ Ollama command timed out")
            
        except Exception as e:
            status = DependencyStatus(
                name='ollama',
                available=False,
                error_message=str(e)
            )
            logger.warning(f"✗ Ollama check failed: {str(e)}")
        
        self.dependency_status['ollama'] = status
        return status
    
    def check_ollama_model(self, model_name: str = 'mistral') -> DependencyStatus:
        """
        Check if a specific Ollama model is available.
        
        Args:
            model_name: Name of the model to check
            
        Returns:
            DependencyStatus object
        """
        try:
            result = subprocess.run(
                ['ollama', 'list'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0 and model_name in result.stdout:
                status = DependencyStatus(
                    name=f'ollama_model_{model_name}',
                    available=True,
                    version='installed'
                )
                logger.info(f"✓ Ollama model '{model_name}' is available")
            else:
                status = DependencyStatus(
                    name=f'ollama_model_{model_name}',
                    available=False,
                    error_message=f"Model '{model_name}' not found in ollama list"
                )
                logger.warning(f"✗ Ollama model '{model_name}' not found")
                
        except Exception as e:
            status = DependencyStatus(
                name=f'ollama_model_{model_name}',
                available=False,
                error_message=str(e)
            )
            logger.warning(f"✗ Ollama model check failed: {str(e)}")
        
        self.dependency_status[f'ollama_model_{model_name}'] = status
        return status
    
    def check_cuda(self) -> DependencyStatus:
        """
        Check if CUDA is available for PyTorch.
        
        Returns:
            DependencyStatus object
        """
        try:
            import torch
            
            if torch.cuda.is_available():
                cuda_version = torch.version.cuda
                device_count = torch.cuda.device_count()
                device_name = torch.cuda.get_device_name(0) if device_count > 0 else 'unknown'
                
                status = DependencyStatus(
                    name='cuda',
                    available=True,
                    version=f"{cuda_version} ({device_count} device(s), {device_name})"
                )
                logger.info(f"✓ CUDA available: {status.version}")
            else:
                status = DependencyStatus(
                    name='cuda',
                    available=False,
                    error_message="PyTorch installed but CUDA not available"
                )
                logger.info("✗ CUDA not available (CPU mode)")
                
        except ImportError:
            status = DependencyStatus(
                name='cuda',
                available=False,
                error_message="PyTorch not installed"
            )
            logger.warning("✗ Cannot check CUDA: PyTorch not installed")
        
        self.dependency_status['cuda'] = status
        return status
    
    def check_all_augmentation_dependencies(self) -> Dict[str, DependencyStatus]:
        """
        Check all dependencies required for text augmentation.
        
        Returns:
            Dictionary of dependency statuses
        """
        logger.info("Checking augmentation dependencies...")
        
        dependencies = [
            'torch',
            'spacy',
            'nltk',
            'transformers',
            'deep_translator',
            'Faker'
        ]
        
        results = {}
        for dep in dependencies:
            results[dep] = self.check_python_package(dep)
        
        # Also check CUDA
        results['cuda'] = self.check_cuda()
        
        return results
    
    def check_all_evaluation_dependencies(self) -> Dict[str, DependencyStatus]:
        """
        Check all dependencies required for evaluation.
        
        Returns:
            Dictionary of dependency statuses
        """
        logger.info("Checking evaluation dependencies...")
        
        results = {}
        results['ollama'] = self.check_ollama()
        
        if results['ollama'].available:
            results['ollama_mistral'] = self.check_ollama_model('mistral')
        
        return results
    
    def run_full_health_check(self) -> Tuple[bool, Dict[str, DependencyStatus]]:
        """
        Run a complete health check of all dependencies.
        
        Returns:
            Tuple of (all_critical_available, all_statuses)
        """
        logger.info("=" * 60)
        logger.info("Running Full System Health Check")
        logger.info("=" * 60)
        
        # Check core dependencies
        core_deps = ['numpy', 'pandas']
        for dep in core_deps:
            self.check_python_package(dep)
        
        # Check augmentation dependencies
        self.check_all_augmentation_dependencies()
        
        # Check evaluation dependencies
        self.check_all_evaluation_dependencies()
        
        # Determine if all critical dependencies are available
        critical_deps = ['numpy', 'pandas']
        all_critical_available = all(
            self.dependency_status.get(dep, DependencyStatus(dep, False)).available
            for dep in critical_deps
        )
        
        logger.info("=" * 60)
        logger.info(f"Health Check Complete: {'✓ PASS' if all_critical_available else '✗ FAIL'}")
        logger.info("=" * 60)
        
        return all_critical_available, self.dependency_status
    
    def get_summary(self) -> str:
        """
        Get a human-readable summary of dependency status.
        
        Returns:
            Formatted summary string
        """
        lines = ["Dependency Status Summary:", "=" * 60]
        
        for name, status in self.dependency_status.items():
            symbol = "✓" if status.available else "✗"
            version_info = f" ({status.version})" if status.version else ""
            error_info = f" - {status.error_message}" if status.error_message else ""
            
            lines.append(f"{symbol} {name}{version_info}{error_info}")
        
        lines.append("=" * 60)
        
        available_count = sum(1 for s in self.dependency_status.values() if s.available)
        total_count = len(self.dependency_status)
        lines.append(f"Available: {available_count}/{total_count}")
        
        return "\n".join(lines)


# Global health check instance
_global_health_check = HealthCheck()


def get_health_check() -> HealthCheck:
    """Get the global health check instance."""
    return _global_health_check
