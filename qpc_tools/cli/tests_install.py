#
# Copyright (c) 2019 Red Hat, Inc.
#
# This software is licensed to you under the GNU General Public License,
# version 3 (GPLv3). There is NO WARRANTY for this software, express or
# implied, including the implied warranties of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. You should have received a copy of GPLv3
# along with this software; if not, see
# https://www.gnu.org/licenses/gpl-3.0.txt.
#
"""Test the Install CLI module."""

import io
import sys
import unittest
from unittest.mock import patch
from argparse import ArgumentParser, Namespace  # noqa: I100

from qpc_tools import messages
from qpc_tools.cli.install import InstallCLICommand
from qpc_tools.tests_utilities import HushUpStderr, redirect_stdout
from qpc_tools.translation import _


PARSER = ArgumentParser()
SUBPARSER = PARSER.add_subparsers(dest='subcommand')


class InstallCLICommandTests(unittest.TestCase):
    """Class for testing the install CLI commands."""

    def setUp(self):
        """Create test setup."""
        # Temporarily disable stderr for these tests, CLI errors clutter up
        # nosetests command.
        self.orig_stderr = sys.stderr
        sys.stderr = HushUpStderr()
        # pylint:disable=line-too-long
        self.effect = [(b'', b" [WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'\n [WARNING]: Consider using the yum, dnf or zypper module rather than running 'rpm'.  If you need to use command because yum, dnf or zypper is insufficient you can add 'warn: false' to this command task or set 'command_warnings=False' in\nansible.cfg to get rid of this message.\n")]  # noqa: E501

    def tearDown(self):
        """Remove test setup."""
        # Restore stderr
        sys.stderr = self.orig_stderr

    @patch('qpc_tools.cli.install.subprocess.Popen')
    def test_install_cli_success(self, subprocess):
        """Testing the installation of CLI command was successful."""
        subprocess.return_value.returncode = 0
        subprocess.return_value.communicate.side_effect = self.effect
        mock_ansible_logs = 'test0\ntest1\n'
        byte_ansible_logs = bytes(mock_ansible_logs, 'utf-8')
        subprocess.return_value.stdout = io.BytesIO(byte_ansible_logs)
        cred_out = io.StringIO()
        cac = InstallCLICommand(SUBPARSER)
        args = Namespace()
        with redirect_stdout(cred_out):
            cac.main(args)
            expected = mock_ansible_logs + _(messages.CLI_INSTALLATION_SUCCESSFUL)
            self.assertEqual(cred_out.getvalue().strip(), expected)

    @patch('qpc_tools.cli.install.subprocess.Popen')
    def test_install_cli_failure(self, subprocess):
        """Testing a failed CLI installlation."""
        subprocess.return_value.returncode = 1
        subprocess.return_value.communicate.side_effect = self.effect
        mock_ansible_logs = 'test0\ntest1\n'
        byte_ansible_logs = bytes(mock_ansible_logs, 'utf-8')
        subprocess.return_value.stdout = io.BytesIO(byte_ansible_logs)
        cred_out = io.StringIO()
        cac = InstallCLICommand(SUBPARSER)
        args = Namespace()
        with redirect_stdout(cred_out):
            cac.main(args)
            expected = mock_ansible_logs + _(messages.CLI_INSTALLATION_FAILED)
            self.assertEqual(cred_out.getvalue().strip(), expected)

    @patch('qpc_tools.cli.install.subprocess.Popen')
    def test_value_error(self, subprocess):
        """Testing a failed CLI installlation."""
        subprocess.return_value.returncode = 1
        subprocess.return_value.communicate.side_effect = ValueError()
        mock_ansible_logs = 'test0\ntest1\n'
        byte_ansible_logs = bytes(mock_ansible_logs, 'utf-8')
        subprocess.return_value.stdout = io.BytesIO(byte_ansible_logs)
        cred_out = io.StringIO()
        cac = InstallCLICommand(SUBPARSER)
        args = Namespace()
        with redirect_stdout(cred_out):
            cac.main(args)
            expected = mock_ansible_logs + _(messages.CLI_INSTALLATION_FAILED)
            self.assertEqual(cred_out.getvalue().strip(), expected)