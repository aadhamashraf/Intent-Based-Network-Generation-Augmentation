"""
Unit tests for Enhanced_Constraint_Engine.
"""
import pytest
from src.Intents_Generators.Enhanced_Constraint_Engine import EnhancedConstraintEngine


class TestEnhancedConstraintEngine:
    """Test suite for EnhancedConstraintEngine."""
    
    @pytest.fixture
    def engine(self):
        """Create an engine instance for testing."""
        return EnhancedConstraintEngine()
    
    def test_initialization(self, engine):
        """Test that engine initializes correctly."""
        assert engine is not None
        assert hasattr(engine, 'domain_profiles')
        assert hasattr(engine, 'slice_constraints')
    
    def test_categorize_slice_type(self, engine):
        """Test slice type categorization."""
        # Test known slice types
        assert engine.categorize_slice_type('eMBB_Gaming') == 'eMBB'
        assert engine.categorize_slice_type('URLLC_Autonomous_Driving') == 'URLLC'
        assert engine.categorize_slice_type('mMTC_Smart_City') == 'mMTC'
        assert engine.categorize_slice_type('V2X_Highway') == 'V2X'
    
    def test_categorize_location(self, engine):
        """Test location categorization."""
        # Test known locations
        assert engine.categorize_location('Urban_Dense_City_Center') == 'urban'
        assert engine.categorize_location('Rural_Agricultural_Area') == 'rural'
        assert engine.categorize_location('Highway_Interstate') == 'highway'
    
    def test_generate_constrained_priority(self, engine):
        """Test priority generation with constraints."""
        priority = engine.generate_constrained_priority('eMBB', 'urban', 5)
        
        valid_priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'EMERGENCY']
        assert priority in valid_priorities
    
    def test_generate_constrained_complexity(self, engine):
        """Test complexity generation."""
        complexity = engine.generate_constrained_complexity('URLLC', 'CRITICAL')
        
        assert isinstance(complexity, int)
        assert 1 <= complexity <= 10
    
    def test_generate_qos_parameters(self, engine):
        """Test QoS parameter generation."""
        qos = engine.generate_constrained_qos_parameters('eMBB', 8)
        
        assert isinstance(qos, dict)
        assert 'qos_flow_identifier' in qos
        assert 'guaranteed_bit_rate' in qos
        assert 'packet_delay_budget' in qos
    
    def test_generate_resource_allocation(self, engine):
        """Test resource allocation generation."""
        resources = engine.generate_constrained_resource_allocation('URLLC', 9, 'CRITICAL')
        
        assert isinstance(resources, dict)
        assert 'compute_resources' in resources
        assert 'network_resources' in resources
    
    def test_urllc_latency_constraints(self, engine):
        """Test that URLLC generates low latency requirements."""
        qos = engine.generate_constrained_qos_parameters('URLLC', 9)
        
        # URLLC should have very low latency
        delay = qos.get('packet_delay_budget', '100ms')
        # Extract numeric value
        if 'ms' in delay:
            delay_value = float(delay.replace('ms', ''))
            assert delay_value <= 10  # URLLC typically < 10ms
    
    def test_embb_throughput_constraints(self, engine):
        """Test that eMBB generates high throughput requirements."""
        qos = engine.generate_constrained_qos_parameters('eMBB', 8)
        
        # eMBB should have high bitrate
        assert 'guaranteed_bit_rate' in qos
        assert 'maximum_bit_rate' in qos
    
    def test_compliance_standards(self, engine):
        """Test compliance standards generation."""
        compliance = engine.generate_constrained_compliance_standards('urban', 'CRITICAL')
        
        assert isinstance(compliance, list)
        assert len(compliance) > 0
    
    def test_research_context(self, engine):
        """Test research context generation."""
        context = engine.generate_constrained_research_context(9, 'eMBB')
        
        assert isinstance(context, list)
        # High complexity should generate research contexts
        if 9 >= 8:
            assert len(context) > 0
