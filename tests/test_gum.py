import unittest
from unittest.mock import patch, call, Mock # Added Mock for type hinting
from pygum._gum import ginput, choose, write, confirm, filter
from pygum._command_wrapper import CmdOutput

class TestGumCommands(unittest.TestCase):

    @patch('pygum._gum.command_wrapper')
    def test_ginput_basic(self, mock_command_wrapper: Mock):
        # Configure the mock
        expected_cmd_output = CmdOutput(msg="Test Name", status=0, cmd=['gum', 'input', '--prompt', 'Name:', '--placeholder', 'Your name'])
        mock_command_wrapper.return_value = expected_cmd_output

        # Call the function
        result = ginput(prompt="Name:", placeholder="Your name")

        # Assertions
        mock_command_wrapper.assert_called_once_with(['gum', 'input', '--prompt', 'Name:', '--placeholder', 'Your name'])
        self.assertEqual(result, "Test Name")

    @patch('pygum._gum.command_wrapper')
    def test_ginput_detailed_output(self, mock_command_wrapper: Mock):
        # Configure the mock
        mock_cmd_output = CmdOutput(msg="Test Name", status=0, cmd=['gum', 'input', '--prompt', 'Name:'])
        mock_command_wrapper.return_value = mock_cmd_output

        # Call the function
        result = ginput(prompt="Name:", detailed=True)

        # Assertions
        mock_command_wrapper.assert_called_once_with(['gum', 'input', '--prompt', 'Name:'])
        self.assertEqual(result, mock_cmd_output)

    @patch('pygum._gum.command_wrapper')
    def test_choose_basic(self, mock_command_wrapper: Mock):
        expected_cmd_output = CmdOutput(msg="apple", status=0, cmd=['gum', 'choose', '--limit', '1', '--cursor', '>', '"apple" "banana"'])
        mock_command_wrapper.return_value = expected_cmd_output

        result = choose(["apple", "banana"], limit=1, cursor=">")

        mock_command_wrapper.assert_called_once_with(['gum', 'choose', '--limit', '1', '--cursor', '>', '"apple" "banana"'])
        self.assertEqual(result, "apple")

    @patch('pygum._gum.command_wrapper')
    def test_write_basic(self, mock_command_wrapper: Mock):
        expected_cmd_output = CmdOutput(msg="Hello World", status=0, cmd=['gum', 'write', '--value', 'Hello', '--placeholder', 'Type...'])
        mock_command_wrapper.return_value = expected_cmd_output

        result = write(value="Hello", placeholder="Type...")

        mock_command_wrapper.assert_called_once_with(['gum', 'write', '--value', 'Hello', '--placeholder', 'Type...'])
        self.assertEqual(result, "Hello World")

    @patch('pygum._gum.command_wrapper')
    def test_confirm_basic_yes(self, mock_command_wrapper: Mock):
        # Simulating a 'yes' response (status 0)
        expected_cmd_output = CmdOutput(msg="", status=0, cmd=['gum', 'confirm', '--prompt', 'Proceed?', '--affirmative', 'Yes', '--negative', 'No'])
        mock_command_wrapper.return_value = expected_cmd_output

        result = confirm(prompt="Proceed?", affirmative="Yes", negative="No")
        
        # _gum_runner returns result.msg or None. If msg is empty, it's None.
        # For confirm, a status of 0 usually means success (affirmative).
        # The task description says "confirm often returns status 0 for yes, 1 for no, message might be empty".
        # "Assert confirm returns None (as msg is empty) or handle based on typical success."
        # Let's assume for this basic test, if the command_wrapper returns status 0,
        # the confirm function (via _gum_runner) should return None (because msg is "").
        # A more advanced test might check the CmdOutput object if detailed=True to infer success.
        mock_command_wrapper.assert_called_once_with(['gum', 'confirm', '--prompt', 'Proceed?', '--affirmative', 'Yes', '--negative', 'No'])
        self.assertIsNone(result) # As per current _gum_runner logic: result.msg or None

    @patch('pygum._gum.command_wrapper')
    def test_confirm_basic_no(self, mock_command_wrapper: Mock):
        # Simulating a 'no' response (status 1)
        expected_cmd_output = CmdOutput(msg="User cancelled.", status=1, cmd=['gum', 'confirm', '--prompt', 'Proceed?'])
        mock_command_wrapper.return_value = expected_cmd_output

        result = confirm(prompt="Proceed?") # Not specifying affirmative/negative for this variant

        # If status is non-zero, and msg is "User cancelled.", _gum_runner returns "User cancelled."
        mock_command_wrapper.assert_called_once_with(['gum', 'confirm', '--prompt', 'Proceed?'])
        self.assertEqual(result, "User cancelled.")

    # It would be good to also test the 'filter' command as it has special handling for stdin
    @patch('pygum._gum.command_wrapper')
    def test_filter_basic(self, mock_command_wrapper: Mock):
        expected_cmd_output = CmdOutput(msg="selected_choice", status=0, cmd=['gum', 'filter', '--prompt', 'Select:'])
        mock_command_wrapper.return_value = expected_cmd_output

        choices_list = ["choice1", "choice2", "selected_choice"]
        choices_str_for_stdin = "\n".join(choices_list)

        result = filter(choices_list, prompt="Select:")

        # Assert that command_wrapper was called with cmd_args and stdin_data
        mock_command_wrapper.assert_called_once_with(
            ['gum', 'filter', '--prompt', 'Select:'],
            stdin_data=choices_str_for_stdin
        )
        self.assertEqual(result, "selected_choice")

    @patch('pygum._gum.command_wrapper')
    def test_ginput_with_style_attributes(self, mock_command_wrapper: Mock):
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
        self.assertEqual(result, "Styled Input")


if __name__ == '__main__':
    unittest.main()
