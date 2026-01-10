"""
Unit tests for Advanced3GPPIntentGenerator.
"""
import pytest
from src.Intents_Generators.Advanced3GPPIntentGenerator import Advanced3GPPIntentGenerator


class TestAdvanced3GPPIntentGenerator:
    """Test suite for Advanced3GPPIntentGenerator."""
    
    @pytest.fixture
    def generator(self):
        """Create a generator instance for testing."""
        return Advanced3GPPIntentGenerator()
    
    def test_initialization(self, generator):
        """Test that generator initializes correctly."""
        assert generator is not None
        assert hasattr(generator, 'constraint_engine')
        assert hasattr(generator, 'template_engine')
    
    def test_generate_single_intent(self, generator):
        """Test generating a single intent."""
        intent = generator.generate_intent()
        
        # Verify basic structure
        assert intent is not None
        assert 'id' in intent
        assert 'intent_type' in intent
        assert 'description' in intent
        assert 'timestamp' in intent
        assert 'priority' in intent
        assert 'parameters' in intent
    
    def test_intent_id_uniqueness(self, generator):
        """Test that generated intents have unique IDs."""
        intent1 = generator.generate_intent()
        intent2 = generator.generate_intent()
        
        assert intent1['id'] != intent2['id']
    
    def test_intent_type_validity(self, generator):
        """Test that intent type is valid."""
        valid_types = [
            'Deployment Intent',
            'Modification Intent',
            'Performance Assurance Intent',
            'Intent Report Request',
            'Intent Feasibility Check',
            'Regular Notification Request'
        ]
        
        intent = generator.generate_intent()
        assert intent['intent_type'] in valid_types
    
    def test_priority_validity(self, generator):
        """Test that priority is valid."""
        valid_priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'EMERGENCY']
        
        intent = generator.generate_intent()
        assert intent['priority'] in valid_priorities
    
    def test_description_not_empty(self, generator):
        """Test that description is not empty."""
        intent = generator.generate_intent()
        assert len(intent['description']) > 0
    
    def test_parameters_structure(self, generator):
        """Test that parameters have expected structure."""
        intent = generator.generate_intent()
        params = intent['parameters']
        
        # Check for key parameter categories
        assert isinstance(params, dict)
        # Should have at least some parameters
        assert len(params) > 0
    
    def test_batch_generation(self, generator):
        """Test generating multiple intents."""
        batch_size = 5
        intents = generator.generate_batch(batch_size)
        
        assert len(intents) == batch_size
        
        # Verify all IDs are unique
        ids = [intent['id'] for intent in intents]
        assert len(ids) == len(set(ids))
    
    def test_quality_score_range(self, generator):
        """Test that quality score is in valid range."""
        intent = generator.generate_intent()
        
        if 'metadata' in intent and 'quality_score' in intent['metadata']:
            score = intent['metadata']['quality_score']
            assert 0 <= score <= 10
    
    def test_complexity_range(self, generator):
        """Test that complexity is in valid range."""
        intent = generator.generate_intent()
        
        if 'metadata' in intent and 'complexity' in intent['metadata']:
            complexity = intent['metadata']['complexity']
            assert 1 <= complexity <= 10
