from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga_dummy.utils import EventLog, assert_action_performed, attribute_value


@pytest.fixture
def button():
    return toga.Button("Test Button")


@pytest.fixture
def sample_icon(app):
    return toga.Icon("resources/sample")


def test_button_created(button):
    """A button can be created."""
    # Round trip the impl/interface
    assert button._impl.interface == button

    assert_action_performed(button, "create Button")
    assert button.text == "Test Button"
    assert button.icon is None


def test_icon_button_created(button, sample_icon):
    """A button can be created."""
    button = toga.Button(icon=sample_icon)

    # Round trip the impl/interface
    assert button._impl.interface == button
    assert_action_performed(button, "create Button")
    assert button.text == ""
    assert button.icon == sample_icon


def test_button_no_content():
    """A button must have text or an icon."""
    with pytest.raises(ValueError, match=r"Must specify either text or an icon"):
        toga.Button()


def test_button_both_content(sample_icon):
    """A button cannot have both text and an icon."""
    with pytest.raises(ValueError, match=r"Cannot specify both text and an icon"):
        toga.Button(text="Bad text", icon=sample_icon)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("New Text", "New Text"),
        ("", ""),
        (None, ""),
        ("\u200B", ""),
        (12345, "12345"),
        ("Contains\nnewline", "Contains"),
    ],
)
def test_button_text(button, sample_icon, value, expected):
    """The button label can be modified."""
    assert button.text == "Test Button"
    assert button.icon is None

    # Clear the event log
    EventLog.reset()

    button.text = value
    assert button.text == expected
    assert button.icon is None

    # test backend has the right values
    assert attribute_value(button, "text") == expected
    assert attribute_value(button, "icon") is None

    # A refresh was performed
    assert_action_performed(button, "refresh")

    # Change to an icon
    button.icon = sample_icon
    assert button.icon == sample_icon

    # test backend has the right values
    assert attribute_value(button, "text") == ""
    assert attribute_value(button, "icon") == sample_icon

    # A refresh was performed
    assert_action_performed(button, "refresh")


@pytest.mark.parametrize("construct", [True, False])
def test_button_icon(button, construct):
    """The button icon can be modified."""
    assert button.text == "Test Button"
    assert button.icon is None

    if construct:
        icon = toga.Icon("path/to/icon")
    else:
        icon = "path/to/icon"

    # Set the icon
    button.icon = icon
    assert isinstance(button.icon, toga.Icon)
    assert button.icon.path == Path("path/to/icon")

    # test backend has the right values
    assert attribute_value(button, "text") == ""
    assert attribute_value(button, "icon").path == Path("path/to/icon")

    # A refresh was performed
    assert_action_performed(button, "refresh")

    # Change back to text
    button.text = "New value"
    assert button.text == "New value"
    assert button.icon is None

    # test backend has the right values
    assert attribute_value(button, "text") == "New value"
    assert attribute_value(button, "icon") is None

    # A refresh was performed
    assert_action_performed(button, "refresh")


def test_button_on_press(button):
    """The on_press handler can be invoked."""
    # No handler initially
    assert button._on_press._raw is None

    # Define and set a new callback
    handler = Mock()

    button.on_press = handler

    assert button.on_press._raw == handler

    # Invoke the callback
    button._impl.simulate_press()

    # Callback was invoked
    handler.assert_called_once_with(button)
