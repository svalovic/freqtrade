import argparse
from argparse import Namespace

parent_parser = argparse.ArgumentParser(add_help=False)

parent_parser.add_argument('-c', '--config',
                           help=f'Specify configuration file (default:). ',
                           action='append',
                           metavar='PATH',)

parent_parser.add_argument('-d', '--datadir',
                           help='Path to directory with historical backtesting data.',
                           metavar='PATH',
                           required=False, dest='datadir'
                           )

parser = argparse.ArgumentParser("helping hand", parents=[parent_parser])

subparsers = parser.add_subparsers(dest="subparser", )

subparsers.add_parser("test", parents=[parent_parser], )

ns = Namespace()
print(vars(parser.parse_args(namespace=ns)))
