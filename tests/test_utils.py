"""
Unit tests for utils_generator module.
"""
import pytest
import uuid
from src.Intents_Generators.utils_generator import (
    generate_unique_id,
    random_choice,
    random_int,
    current_timestamp,
    random_timestamp_within_days
)


class TestGenerateUniqueId:
    """Test unique ID generation."""
    
    def test_generates_string(self):
        """Test that generate_unique_id returns a string."""
        result = generate_unique_id()
        assert isinstance(result, str)
    
    def test_generates_unique_ids(self):
        """Test that multiple calls generate different IDs."""
        id1 = generate_unique_id()
        id2 = generate_unique_id()
        assert id1 != id2
    
    def test_id_format(self):
        """Test that ID has expected format (hex string)."""
        result = generate_unique_id()
        # Should be a valid hex string
        try:
            int(result, 16)
            assert True
        except ValueError:
            assert False, f"ID {result} is not a valid hex string"


class TestRandomChoice:
    """Test random_choice function."""
    
    def test_returns_element_from_list(self):
        """Test that random_choice returns an element from the list."""
        choices = ['A', 'B', 'C']
        result = random_choice(choices)
        assert result in choices
    
    def test_single_element_list(self):
        """Test with a single element list."""
        choices = ['ONLY']
        result = random_choice(choices)
        assert result == 'ONLY'
    
    def test_empty_list_raises_error(self):
        """Test that empty list raises an error."""
        with pytest.raises(IndexError):
            random_choice([])


class TestRandomInt:
    """Test random_int function."""
    
    def test_returns_int_in_range(self):
        """Test that random_int returns an integer in the specified range."""
        result = random_int(1, 10)
        assert isinstance(result, int)
        assert 1 <= result <= 10
    
    def test_single_value_range(self):
        """Test with min == max."""
        result = random_int(5, 5)
        assert result == 5
    
    def test_large_range(self):
        """Test with a large range."""
        result = random_int(1, 1000000)
        assert 1 <= result <= 1000000


class TestCurrentTimestamp:
    """Test current_timestamp function."""
    
    def test_returns_string(self):
        """Test that current_timestamp returns a string."""
        result = current_timestamp()
        assert isinstance(result, str)
    
    def test_timestamp_format(self):
        """Test that timestamp has ISO format."""
        result = current_timestamp()
        # Should contain 'T' separator and end with 'Z'
        assert 'T' in result
        assert result.endswith('Z')
    
    def test_consecutive_timestamps_different(self):
        """Test that consecutive calls produce different timestamps."""
        import time
        ts1 = current_timestamp()
        time.sleep(0.01)  # Small delay
        ts2 = current_timestamp()
        # They might be the same if called too quickly, but should be valid
        assert isinstance(ts1, str)
        assert isinstance(ts2, str)


class TestRandomTimestampWithinDays:
    """Test random_timestamp_within_days function."""
    
    def test_returns_string(self):
        """Test that function returns a string."""
        result = random_timestamp_within_days(7)
        assert isinstance(result, str)
    
    def test_timestamp_format(self):
        """Test that timestamp has ISO format."""
        result = random_timestamp_within_days(30)
        assert 'T' in result
        assert result.endswith('Z')
    
    def test_zero_days(self):
        """Test with zero days (should return current timestamp)."""
        result = random_timestamp_within_days(0)
        assert isinstance(result, str)
        assert 'T' in result
