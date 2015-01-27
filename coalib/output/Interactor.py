from coalib.bearlib.abstractions.SectionCreatable import SectionCreatable
from coalib.results.Result import Result
from coalib.output.printers.ConsolePrinter import ConsolePrinter
from coalib.misc.i18n import _
from coalib.settings.FunctionMetadata import FunctionMetadata


class Interactor(SectionCreatable):
    def __init__(self, log_printer=ConsolePrinter()):
        SectionCreatable.__init__(self)
        self.log_printer = log_printer

    def _print_result(self, result):
        """
        Prints the result.
        """
        raise NotImplementedError

    def _print_actions(self, actions):
        """
        Prints the given actions and lets the user choose.

        :param actions: A list of FunctionMetadata objects.
        :return: A touple with the name member of the FunctionMetadata object chosen by the user and a Section
        containing at least all needed values for the action.
        """
        raise NotImplementedError

    def print_result(self, result, file_dict, file_diff_dict):
        """
        Prints the result appropriate to the output medium.

        :param result: A derivative of Result.
        :param file_dict: Dictionary containing filename: file_contents
        """
        if not isinstance(result, Result):
            self.log_printer.warn(_("One of the results can not be printed since it is not a valid derivative of the "
                                    "coala result class."))
            return

        self._print_result(result)

        actions = result.get_actions()
        if actions == []:
            return

        action_dict = {}
        metadata_list = []
        for action in actions:
            metadata = action.get_metadata()
            action_dict[metadata.name] = action
            metadata_list.append(metadata)

        chosen_action, section = action_dict[self._print_actions(metadata_list)]
        chosen_action.apply_from_section(result, file_dict, file_diff_dict, section)

    def print_results(self, result_list, file_dict, file_diff_dict):
        """
        Prints all given results. They will be sorted.

        :param result_list: List of the results
        :param file_dict: Dictionary containing filename: file_contents
        """
        if not isinstance(result_list, list):
            raise TypeError("result_list should be of type list")
        if not isinstance(file_dict, dict):
            raise TypeError("file_dict should be of type dict")

        sorted_results = sorted(result_list)
        for result in sorted_results:
            self.print_result(result, file_dict, file_diff_dict)

    def acquire_settings(self, settings):
        """
        This method prompts the user for the given settings.

        :param settings: a dictionary with the settings name as key and a list containing a description in [0] and the
                         name of the bears who need this setting in [1] and following. Example:
        {"UseTabs": ["describes whether tabs should be used instead of spaces",
                     "SpaceConsistencyBear",
                     "SomeOtherBear"]}

        :return: a dictionary with the settings name as key and the given value as value.
        """
        raise NotImplementedError

    @classmethod
    def get_metadata(cls):
        return FunctionMetadata.from_function(cls.__init__, ["self", "log_printer"])
