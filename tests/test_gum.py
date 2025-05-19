from unittest.mock import patch, call, Mock # call might not be used, Mock for type hinting
from pygum._gum import ginput, choose, write, confirm, filter
from pygum._command_wrapper import CmdOutput

@patch('pygum._gum.command_wrapper')
def test_ginput_basic(mock_command_wrapper: Mock):
    # Configure the mock
    expected_cmd_output = CmdOutput(msg="Test Name", status=0, cmd=['gum', 'input', '--prompt', 'Name:', '--placeholder', 'Your name'])
    mock_command_wrapper.return_value = expected_cmd_output

    # Call the function
    result = ginput(prompt="Name:", placeholder="Your name")

    # Assertions
    mock_command_wrapper.assert_called_once_with(['gum', 'input', '--prompt', 'Name:', '--placeholder', 'Your name'])
    assert result == "Test Name"

@patch('pygum._gum.command_wrapper')
def test_ginput_detailed_output(mock_command_wrapper: Mock):
    # Configure the mock
    mock_cmd_output = CmdOutput(msg="Test Name", status=0, cmd=['gum', 'input', '--prompt', 'Name:'])
    mock_command_wrapper.return_value = mock_cmd_output

    # Call the function
    result = ginput(prompt="Name:", detailed=True)

    # Assertions
    mock_command_wrapper.assert_called_once_with(['gum', 'input', '--prompt', 'Name:'])
    assert result == mock_cmd_output

@patch('pygum._gum.command_wrapper')
def test_choose_basic(mock_command_wrapper: Mock):
    expected_cmd_output = CmdOutput(msg="apple", status=0, cmd=['gum', 'choose', '--limit', '1', '--cursor', '>', '"apple" "banana"'])
    mock_command_wrapper.return_value = expected_cmd_output

    result = choose(["apple", "banana"], limit=1, cursor=">")

    mock_command_wrapper.assert_called_once_with(['gum', 'choose', '--limit', '1', '--cursor', '>', '"apple" "banana"'])
    assert result == "apple"

@patch('pygum._gum.command_wrapper')
def test_write_basic(mock_command_wrapper: Mock):
    expected_cmd_output = CmdOutput(msg="Hello World", status=0, cmd=['gum', 'write', '--value', 'Hello', '--placeholder', 'Type...'])
    mock_command_wrapper.return_value = expected_cmd_output

    result = write(value="Hello", placeholder="Type...")

    mock_command_wrapper.assert_called_once_with(['gum', 'write', '--value', 'Hello', '--placeholder', 'Type...'])
    assert result == "Hello World"

@patch('pygum._gum.command_wrapper')
def test_confirm_basic_yes(mock_command_wrapper: Mock):
    # Simulating a 'yes' response (status 0)
    expected_cmd_output = CmdOutput(msg="", status=0, cmd=['gum', 'confirm', '--prompt', 'Proceed?', '--affirmative', 'Yes', '--negative', 'No'])
    mock_command_wrapper.return_value = expected_cmd_output

    result = confirm(prompt="Proceed?", affirmative="Yes", negative="No")
    
    mock_command_wrapper.assert_called_once_with(['gum', 'confirm', '--prompt', 'Proceed?', '--affirmative', 'Yes', '--negative', 'No'])
    assert result is None # As per current _gum_runner logic: result.msg or None

@patch('pygum._gum.command_wrapper')
def test_confirm_basic_no(mock_command_wrapper: Mock):
    # Simulating a 'no' response (status 1)
    expected_cmd_output = CmdOutput(msg="User cancelled.", status=1, cmd=['gum', 'confirm', '--prompt', 'Proceed?'])
    mock_command_wrapper.return_value = expected_cmd_output

    result = confirm(prompt="Proceed?") # Not specifying affirmative/negative for this variant

    mock_command_wrapper.assert_called_once_with(['gum', 'confirm', '--prompt', 'Proceed?'])
    assert result == "User cancelled."

@patch('pygum._gum.command_wrapper')
def test_filter_basic(mock_command_wrapper: Mock):
    expected_cmd_output = CmdOutput(msg="selected_choice", status=0, cmd=['gum', 'filter', '--prompt', 'Select:'])
    mock_command_wrapper.return_value = expected_cmd_output

    choices_list = ["choice1", "choice2", "selected_choice"]
    choices_str_for_stdin = "\n".join(choices_list)

    result = filter(choices_list, prompt="Select:")

    mock_command_wrapper.assert_called_once_with(
        ['gum', 'filter', '--prompt', 'Select:'],
        stdin_data=choices_str_for_stdin
    )
    assert result == "selected_choice"

@patch('pygum._gum.command_wrapper')
def test_ginput_with_style_attributes(mock_command_wrapper: Mock):
    # Configure the mock
    expected_cmd_output = CmdOutput(msg="Styled Input", status=0, cmd=[
        'gum', 'input', '--prompt', 'Enter:', 
        '--cursor.foreground', '#FF0000', 
        '--prompt.border', 'double',
        '--prompt-align', 'center' # Test mixed single and double underscores
    ])
    mock_command_wrapper.return_value = expected_cmd_output

    # Call the function with style attributes
    result = ginput(
        prompt="Enter:",
        cursor__foreground="#FF0000", 
        prompt__border="double",
        prompt_align="center" # Example of standard underscore conversion
    )

    # Assertions
    mock_command_wrapper.assert_called_once_with([
        'gum', 'input', '--prompt', 'Enter:', 
        '--cursor.foreground', '#FF0000', 
        '--prompt.border', 'double',
        '--prompt-align', 'center'
    ])
    assert result == "Styled Input"
