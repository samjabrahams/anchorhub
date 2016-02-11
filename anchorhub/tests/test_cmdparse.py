"""
cmdparse.py unit tests

cmdparse.py:
http://www.github.com/samjabrahams/anchorhub/compatibility.py
"""

import anchorhub.cmdparse as cmd
import anchorhub.settings.default_settings as ds


def test_parse_args():
    """
    cmdparse.py: Test parse_args()

    The first three sets of assertions check for all the various flag names,
    both the long versions (--flag) and the short versions (-f)

    The final set of assertions check the default values
    """
    args = ['.', 'output', '-e', '.md', '.rst']
    pargs = cmd.parse_args(args)
    assert pargs.input == '.'
    assert pargs.output == 'output'
    assert pargs.extensions == ['.md', '.rst']

    args2 = ['../bears', '-w', '[--> <--]', '-X']
    pargs2 = cmd.parse_args(args2)
    assert pargs2.input == '../bears'
    assert pargs2.wrapper == '[--> <--]'
    assert pargs2.overwrite == True

    args3 = ['.', '--overwrite', '--wrapper', '$$$$ $$$$', '--extension',
             '.txt', '.fbi', '.wat', '.hub']
    pargs3 = cmd.parse_args(args3)
    assert pargs3.input == '.'
    assert pargs3.overwrite == True
    assert pargs3.wrapper == '$$$$ $$$$'
    assert pargs3.extensions == ['.txt', '.fbi', '.wat', '.hub']

    args4 = ['.']
    pargs4 = cmd.parse_args(args4)
    assert pargs4.input == ds.INPUT
    assert pargs4.output == ds.OUTPUT
    assert pargs4.wrapper == ds.WRAPPER
    assert pargs4.overwrite == False
    assert pargs4.extensions == ds.ARGPARSE_EXTENSION['default']


def test_parse_args_dict():
    """
    cmdparse.py: Test parse_args_dict()

    The first three sets of assertions check for all the various flag names,
    both the long versions (--flag) and the short versions (-f)

    The final set of assertions check the default values
    """
    args = ['.', 'output', '-e', '.md', '.rst']
    pargs = cmd.parse_args_dict(args)
    assert pargs['input'] == '.'
    assert pargs['output'] == 'output'
    assert pargs['extensions'] == ['.md', '.rst']

    args2 = ['../bears', '-w', '[--> <--]', '-X']
    pargs2 = cmd.parse_args_dict(args2)
    assert pargs2['input'] == '../bears'
    assert pargs2['wrapper'] == '[--> <--]'
    assert pargs2['overwrite'] == True

    args3 = ['.', '--overwrite', '--wrapper', '$$$$ $$$$', '--extension',
             '.txt', '.fbi', '.wat', '.hub']
    pargs3 = cmd.parse_args_dict(args3)
    assert pargs3['input'] == '.'
    assert pargs3['overwrite'] == True
    assert pargs3['wrapper'] == '$$$$ $$$$'
    assert pargs3['extensions'] == ['.txt', '.fbi', '.wat', '.hub']

    args4 = ['.']
    pargs4 = cmd.parse_args_dict(args4)
    assert pargs4['input'] == ds.INPUT
    assert pargs4['output'] == ds.OUTPUT
    assert pargs4['wrapper'] == ds.WRAPPER
    assert pargs4['overwrite'] == False
    assert pargs4['extensions'] == ds.ARGPARSE_EXTENSION['default']
