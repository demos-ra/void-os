"""the command: the relational model, data bank, tools, hooks, view and system generation wired into the void-os command, each handed what it needs"""
__all__ = ['void_os']
import os
import sys
from datetime import datetime, timedelta
from void_os.data_bank import _data_bank
from void_os.hooks import _hooks
from void_os.relational_model import _relational_model
from void_os.system_generation import _system_generation
from void_os.tools import _tools
from void_os.view import _view

def void_os() -> int | float:
    void_os_5_arguments = sys.argv[1:]
    try:
        values = _system_generation.values(_relational_model)
    except _system_generation.NotMTSVError as error:
        void_os_11_utf_8_encode = bytes(str(error) + '\n', 'utf-8')
        sys.stderr.buffer.write(void_os_11_utf_8_encode)
        sys.exit(1)
    given = dict(values['records'])
    if len(void_os_5_arguments) == 0:
        _tools.serve(values, _relational_model, _data_bank)
        return 0
    if void_os_5_arguments[0] == given['view operand']:
        void_os_10_is_a_terminal = os.isatty(1)
        void_os_10_local_offset = datetime.now().astimezone().utcoffset() // timedelta(minutes=1)
        try:
            _view.view(values, void_os_5_arguments[1:], void_os_10_is_a_terminal, void_os_10_local_offset, _relational_model, _data_bank)
        except _view.RefusedError as error:
            void_os_11_utf_8_encode = bytes(str(error) + '\n', 'utf-8')
            sys.stderr.buffer.write(void_os_11_utf_8_encode)
            sys.exit(1)
        except _view.KeepingFailedError as error:
            void_os_11_utf_8_encode = bytes(str(error) + '\n', 'utf-8')
            sys.stderr.buffer.write(void_os_11_utf_8_encode)
            sys.exit(1)
        return 0
    if len(void_os_5_arguments) == 1 and void_os_5_arguments[0] in ['SessionStart', 'SubagentStart', 'UserPromptSubmit', 'PostToolUse', 'SubagentStop', 'Stop', 'sessionStart', 'subagentStart', 'beforeSubmitPrompt', 'postToolUse', 'subagentStop', 'stop']:
        void_os_7_working_directory = os.getcwd()
        try:
            _hooks.hook(values, void_os_5_arguments[0], void_os_7_working_directory, _relational_model, _data_bank)
        except _hooks.KeepingFailedError as error:
            void_os_11_utf_8_encode = bytes(str(error) + '\n', 'utf-8')
            sys.stderr.buffer.write(void_os_11_utf_8_encode)
            sys.exit(1)
        except _hooks.NonConformingError as error:
            void_os_11_utf_8_encode = bytes(str(error) + '\n', 'utf-8')
            sys.stderr.buffer.write(void_os_11_utf_8_encode)
            sys.exit(1)
        sys.exit(0)
    void_os_8_utf_8_encode = bytes(given['usage message'] + '\n', 'utf-8')
    sys.stderr.buffer.write(void_os_8_utf_8_encode)
    sys.exit(1)
