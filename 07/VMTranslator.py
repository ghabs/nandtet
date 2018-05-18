from parser import Parser, Command
from writer import Writer
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse and output assembler')
    parser.add_argument('input', metavar='input', type=str,
                   help='location of input text')
    parser.add_argument('output', metavar='output', type=str,
                   help='location of output text')
    args = parser.parse_args()
    p = Parser(args.input)
    w = Writer(args.output)
    ci = p.parse()
    res = w.write(ci)
