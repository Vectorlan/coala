import os
import tempfile
from coalib.results.Diff import Diff
from coalib.results.result_actions.ResultAction import ResultAction


class OpenEditorAction(ResultAction):
    def apply(self, result, original_file_dict, file_diff_dict, editor: str):
        """
        Opens the file in an editor.

        :param editor: The editor to open the file with.
        """
        filename = result.file
        file = original_file_dict[filename]
        new_file = file_diff_dict.get(filename, Diff()).apply(file)
        tempfile_handle, tempfile_name = tempfile.mkstemp(pefix=filename)
        os.write(tempfile_handle, "".join(new_file))
        os.close(tempfile_handle)

        os.system(editor + " " + tempfile_name)

        return file_diff_dict
