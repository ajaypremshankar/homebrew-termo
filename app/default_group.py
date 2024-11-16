import click

class DefaultGroup(click.Group):

    def __init__(self, *args, **kwargs):
        # To resolve as the default command.
        if not kwargs.get('ignore_unknown_options', True):
            raise ValueError('Default group accepts unknown options')
        self.ignore_unknown_options = True
        self.default_cmd_name = kwargs.pop('default', None)
        self.default_if_no_args = kwargs.pop('default_if_no_args', False)
        super(DefaultGroup, self).__init__(*args, **kwargs)

    def set_default_command(self, command):
        """Sets a command function as the default command."""
        cmd_name = command.name
        self.add_command(command)
        self.default_cmd_name = cmd_name

    def parse_args(self, ctx, args):
        if not args and self.default_if_no_args:
            args.insert(0, self.default_cmd_name)
        return super(DefaultGroup, self).parse_args(ctx, args)

    def get_command(self, ctx, cmd_name):
        if cmd_name not in self.commands:
            # No command name matched.
            ctx.arg0 = cmd_name
            cmd_name = self.default_cmd_name
        return super(DefaultGroup, self).get_command(ctx, cmd_name)

    def resolve_command(self, ctx, args):
        base = super(DefaultGroup, self)
        cmd_name, cmd, args = base.resolve_command(ctx, args)

        if hasattr(ctx, 'arg0'):
            print(f"{ctx.arg0}")
            args.insert(0, ctx.arg0)
            cmd_name = cmd.name
        return cmd_name, cmd, args
