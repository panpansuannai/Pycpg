import argparse
from decorator import singleton

class Config(object):
    '''
    The configure parsed from the command-line.
    '''
    def __init__(self, input_file: str,
                 output_file: str, output_type: str):
        '''
        Args:
            input_file(str|None) : input file to read the source code, 
                read from standard input if empty
            output_file(str) : file name to output the graph
            output_type(str) : graph type to output
        '''
        self._input_file = input_file
        self._output_file = output_file
        self._output_type = output_type
    
    @classmethod
    def prog_name(cls) -> str:
        return 'Pycpg'

    @classmethod
    def description(cls) -> str:
        return '''Convert C-like code to procedural graph'''

    @property
    def input_file(self) -> str:
        return self._input_file
    @property
    def output_file(self) -> str:
        return self._output_file
    @property
    def output_type(self) -> str:
        return self._output_type

def first_of_list_or_default(lst: list, default):
    if lst is not None and len(lst) > 0:
        return lst[0]
    else:
        return default

def parse() -> Config :
    parser = argparse.ArgumentParser(prog=Config.prog_name(),
                                    description=Config.description(),
                                    add_help=True,
                                    allow_abbrev=True,
                                    exit_on_error=True)
    parser.add_argument('--from', '-f', nargs=1, required=False)
    parser.add_argument('--out', '-o', nargs=1, required=True)
    parser.add_argument('--type', '-t', choices=['svg','png'],
                         nargs=1, required=False)
    namespace = vars(parser.parse_args())

    ''' If input file in None, read from standard input'''
    input_file = first_of_list_or_default(namespace['from'], None)

    output_file = first_of_list_or_default(namespace['out'], None)
    ''' Output file is required by the argument parser '''
    assert output_file is not None

    output_type = first_of_list_or_default(namespace['type'], 'svg')

    return Config(input_file, output_file, output_type)