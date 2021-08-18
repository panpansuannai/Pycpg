import argparse
from decorator import singleton

class Config(object):
    prog_name = 'Pycpg'
    usage = '''Convert C-like code to procedural graph'''
    def __init__(self, input_file: str,
                 output_file: str, output_type: str):
        self._input_file = input_file
        self._output_file = output_file
        self._output_type = output_type

    @property
    def input_file(self) -> str:
        return self._input_file
    @property
    def output_file(self) -> str:
        return self._output_file
    @property
    def output_type(self) -> str:
        return self._output_type
    
parser = argparse.ArgumentParser(prog=Config.prog_name,
                                 usage=Config.usage,
                                 add_help=True,
                                 allow_abbrev=True,
                                 exit_on_error=True)
parser.add_argument('--from', '-f')
parser.add_argument('--out', '-o')
parser.add_argument('--type', '-t')
namespace = parser.parse_args(None)
print(namespace)