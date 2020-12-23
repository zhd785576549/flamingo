from argparse import ArgumentParser


class BaseCommand:

    def create_parser(self):
        parser = ArgumentParser()
        self.add_argument(parser=parser)
        return parser

    def add_argument(self, parser: ArgumentParser):
        pass

    def run_from_argv(self, prog_name, sub_command, argv):
        parser = self.create_parser()
        options = parser.parse_args(argv)
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        self.execute(*args, **cmd_options)

    def execute(self, *args, **kwargs):
        self.handle(*args, **kwargs)

    def handle(self, *args, **options):
        """
        The actual logic of the command. Subclasses must implement
        this method.
        """
        raise NotImplementedError('subclasses of BaseCommand must provide a handle() method')
