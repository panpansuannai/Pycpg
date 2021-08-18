from io import TextIOWrapper
from sys import stdin
from args_parser import parse as args_parse, Config
from lexer import lexer
from parser import parser

def read_code_text(io_in: TextIOWrapper) -> str:
    return io_in.read()

def exit_with_str(status, msg: str):
    print(msg)
    exit(status)

def main():
    config = args_parse()

    if config.input_file is None:
        '''Get input from standard input'''
        struts = parser.parse(read_code_text(stdin), lexer=lexer)
    else :
        try:
            with open(config.input_file, 'rt') as file:
                ''' Read with `t` mode, 
                file must be instance of TextIOWrapper'''
                assert isinstance(file, TextIOWrapper)

                structs = parser.parse(read_code_text(file), lexer=lexer)
        except FileNotFoundError:
            exit_with_str(0, "{}: File Not Found.".format(config.input_file))
            return
        except :
            exit_with_str(0, "{}: Open file error.".format(config.input_file))
            return
    
if __name__ == '__main__':
    main()