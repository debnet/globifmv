# coding: utf-8
from django.core.management import BaseCommand
from django.utils.translation import gettext as _

from fmv.utils import import_harlowe


class Command(BaseCommand):
    help = _("Importe un fichier Twine au format Harlowe")
    leave_locale_alone = True

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help=_("Chemin du fichier"))

    def handle(self, filename=None, *args, **options):
        import_harlowe(filename)
