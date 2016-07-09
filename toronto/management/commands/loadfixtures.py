from django.core.management.commands import loaddata

class Command(loaddata.Command):

    def handle(self, *args, **kwargs):
        kwargs['settings'] = kwargs.get('settings', 'councilmatic.settings')
        super(Command, self).handle(*args, **kwargs)
