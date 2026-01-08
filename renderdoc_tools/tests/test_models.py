"""Unit tests for models"""
import pytest
from renderdoc_tools.core.models import CaptureData, CaptureInfo, Action


def test_capture_data_default_lists():
    """Test that default lists are not shared between instances"""
    # Create two instances
    data1 = CaptureData(capture_info=CaptureInfo(api=2))
    data2 = CaptureData(capture_info=CaptureInfo(api=2))
    
    # Modify one instance
    test_action = Action(
        event_id=1,
        action_id=1,
        name="DrawIndexed",
        flags="Drawcall"
    )
    data1.actions.append(test_action)
    
    # Verify the other instance is not affected
    assert len(data1.actions) == 1
    assert len(data2.actions) == 0, "Mutable default bug: lists are shared!"


def test_capture_info_creation():
    """Test basic CaptureInfo creation"""
    info = CaptureInfo(api=2)
    assert info.api == 2


def test_action_with_aliases():
    """Test Action model with camelCase aliases"""
    action = Action(
        eventId=100,
        actionId=50,
        name="DrawIndexed",
        flags="Drawcall",
        numIndices=36
    )
    assert action.event_id == 100
    assert action.num_indices == 36
