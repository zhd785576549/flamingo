from flamingo.command import base


class Command(base.TemplateCommand):

    def handle(self, *args, **options):
        super().handle("project", **options)
