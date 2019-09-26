#!/usr/bin/env python
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
"""QPC Command Line utilities."""

from __future__ import print_function

import logging
import os


QPC_PATH = 'qpc_tools'
CONFIG_HOME_PATH = '~/.config/'
DATA_HOME_PATH = '~/.local/share/'
CONFIG_HOME = os.path.expanduser(CONFIG_HOME_PATH)
DATA_HOME = os.path.expanduser(DATA_HOME_PATH)
CONFIG_DIR = os.path.join(CONFIG_HOME, QPC_PATH)
DATA_DIR = os.path.join(DATA_HOME, QPC_PATH)
QPC_LOG = os.path.join(DATA_DIR, 'qpc-tools.log')

LOG_LEVEL_INFO = 0

# pylint: disable=invalid-name
logging.captureWarnings(True)
log = logging.getLogger('qpc_tools')


def setup_logging(verbosity):
    """Set up Python logging for qpc.

    Must be run after ensure_data_dir_exists().

    :param verbosity: verbosity level, as measured in -v's on the command line.
        Can be None for default.
    """
    if verbosity == LOG_LEVEL_INFO:
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    # Using basicConfig here means that all log messages, even
    # those not coming from qpc, will go to the log file
    logging.basicConfig(filename=QPC_LOG, format='%(asctime)s - %(name)s - '
                                                 '%(levelname)s - %(message)s')
    # but we only adjust the log level for the 'qpc' logger.
    log.setLevel(log_level)
    # the StreamHandler sends warnings and above to stdout, but
    # only for messages going to the 'qpc' logger, i.e. QPC
    # output.
    stderr_handler = logging.StreamHandler()
    stderr_handler.setLevel(logging.ERROR)
    log.addHandler(stderr_handler)


def log_args(args):
    """Log the arguments for each qpc command.

    :param args: the arguments provided to the qpc command
    """
    message = 'Args: "%s"'
    log.info(message, args)
