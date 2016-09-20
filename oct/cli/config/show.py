import click
import config

_short_help = 'View all or some serialized configuration options.'


@click.command(
    short_help=_short_help,
    help=_short_help + '''

View the entirety of the serialized configuration options
used by default for Ansible interactions by not passing any
specific options to view. View a specific option or options
by passing option names as arguments.

\b
Examples:
  View all of the configuration options
  $ oct config show
\b
  View the 'verbosity' configuration option
  $ oct config show 'verbosity'
\b
  View the 'check', 'become', and 'verbosity' configuration options
  $ oct config show 'check' 'become' 'verbosity'
'''
)
@click.option(
    '--all', '-a',
    help='Print all configuration options.',
    is_flag=True
)
@click.argument(
    'options',
    nargs=-1
)
def show(options, all):
    """
    Print a nice representation of the configuration option
    as found in the serialized configuration. If no options
    are specified or if all are requested, print all options.

    :param options: which options to show the value for
    """
    to_print = {}

    if options and not all:
        for option in options:
            if option not in config._config:
                raise click.UsageError(message='Option ' + option + ' not found in configuration.')
            else:
                to_print[option] = config._config[option]

        print_options(to_print)
    else:
        print_options(config._config)


def print_options(options):
    """
    Print a nice representation of key-value pairs.

    :param options: the key-value pairs to print
    """
    max_length = max([len(repr(key)) for key in options])
    for key in options:
        click.echo('%*r: %r' % (max_length, str(key), str(options[key])))
