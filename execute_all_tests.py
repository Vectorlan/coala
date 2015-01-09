#! /bin/python3

"""
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
import os
import sys
import argparse

from coalib.tests.TestHelper import TestHelper


def show_help():
    print("Usage: {name} [OPTIONS]".format(name=sys.argv[0]))
    print()
    print("--help  : Show this help text")
    print("--cover : Use coverage to get statement and branch coverage of tests")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cover", help="measure code coverage", action="store_true")
    args = parser.parse_args()

    files = TestHelper.get_test_files(os.path.abspath("coalib/tests"))
    exit(TestHelper.execute_python3_files(files, args.cover))
