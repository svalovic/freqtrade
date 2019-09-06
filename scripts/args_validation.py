import argparse
from argparse import Namespace, SUPPRESS, ArgumentError, _SubParsersAction, _UNRECOGNIZED_ARGS_ATTR


class ExtendAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        print(f"{id(self)} {id(namespace)} call {namespace} values: {values}")
        items = getattr(namespace, self.dest) or []
        items.append(values)
        setattr(namespace, self.dest, items)


class SubParsersAction(_SubParsersAction):

    def __call__(self, parser, namespace, values, option_string=None):
        parser_name = values[0]
        arg_strings = values[1:]

        # set the parser name if requested
        if self.dest is not SUPPRESS:
            setattr(namespace, self.dest, parser_name)

        # select the parser
        try:
            parser = self._name_parser_map[parser_name]
        except KeyError:
            args = {'parser_name': parser_name,
                    'choices': ', '.join(self._name_parser_map)}
            msg = _('unknown parser %(parser_name)r (choices: %(choices)s)') % args
            raise ArgumentError(self, msg)

        # parse all the remaining options into the namespace
        # store any unrecognized options on the object, so that the top
        # level parser can decide what to do with them

        # In case this subparser defines new defaults, we parse them
        # in a new namespace object and then update the original
        # namespace for the relevant parts.
        subnamespace, arg_strings = parser.parse_known_args(arg_strings, None)
        for key, value in vars(subnamespace).items():
            if hasattr(namespace, key) and isinstance(value, list):
                getattr(namespace, key).extend(value)
            else:
                setattr(namespace, key, value)

        if arg_strings:
            vars(namespace).setdefault(_UNRECOGNIZED_ARGS_ATTR, [])
            getattr(namespace, _UNRECOGNIZED_ARGS_ATTR).extend(arg_strings)


parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.register('action', 'extend', ExtendAction)

parent_parser.add_argument('-c', '--config',
                           help=f'Specify configuration file (default:). ',
                           action='extend',
                           metavar='PATH',)

parent_parser.add_argument('-d', '--datadir',
                           help='Path to directory with historical backtesting data.',
                           metavar='PATH',
                           required=False, dest='datadir'
                           )

parser = argparse.ArgumentParser("helping hand", parents=[parent_parser])
parser.register('action', 'parsers', SubParsersAction)

subparsers = parser.add_subparsers(dest="subparser", )

subparsers.add_parser("test", parents=[parent_parser], )

ns = Namespace()
print(vars(parser.parse_args(namespace=ns)))
