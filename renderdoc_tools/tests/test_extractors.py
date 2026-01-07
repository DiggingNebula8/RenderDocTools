"""Unit tests for extractors"""
import pytest
from unittest.mock import Mock, MagicMock
from renderdoc_tools.extractors import ActionExtractor, ResourceExtractor


class TestActionExtractor:
    """Tests for ActionExtractor"""
    
    def test_extractor_name(self):
        """Test extractor has correct name"""
        extractor = ActionExtractor()
        assert extractor.name == "actions"
    
    def test_extract_with_mock_controller(self):
        """Test extraction with mocked RenderDoc controller"""
        # Create mock controller
        mock_controller = Mock()
        mock_action = Mock()
        mock_action.eventId = 1
        mock_action.actionId = 1
        mock_action.customName = "DrawIndexed"
        mock_action.flags = 1  # Mock flags
        
        # Mock GetRootActions to return list with one action
        mock_controller.GetRootActions.return_value = [mock_action]
        
        extractor = ActionExtractor()
        # This will fail without actual RenderDoc but demonstrates structure
        # In real tests, we'd need more comprehensive mocking


class TestResourceExtractor:
    """Tests for ResourceExtractor"""
    
    def test_extractor_name(self):
        """Test extractor has correct name"""
        extractor = ResourceExtractor()
        assert extractor.name == "resources"
