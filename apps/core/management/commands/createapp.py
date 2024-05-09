import os

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create nested app"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        try:
            self.app_dir = settings.APP_DIRS
        except:
            self.app_dir = None
        if self.app_dir:
            self.check_app_dir(self.app_dir)

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)
        if self.app_dir:
            parser.add_argument(
                "dir",
                nargs="?",
                default=self.app_dir,
                type=str,
                help="Optional directory",
            )
        else:
            parser.add_argument("dir", type=str)

    def replace_name():
        lines = open(file_name, "r").readlines()
        lines[line_num] = text
        out = open(file_name, "w")
        out.writelines(lines)
        out.close()

    def update_app_config(self, name, app_dir):
        app_path = os.path.join(settings.BASE_DIR, app_dir)
        config_path = os.path.join(app_path, name, "apps.py")
        lines = open(config_path, "r").readlines()
        for i, line in enumerate(lines):
            if f"name = '{name}'" in line:
                lines[i] = line.replace(
                    f"name = '{name}'", f"name = '{app_dir}.{name}'"
                )
        out = open(config_path, "w")
        out.writelines(lines)
        out.close()

    def handle(self, *args, **kwargs):
        name = kwargs.get("name")
        app_dir = kwargs.get("dir")
        self.check_app_dir(app_dir)
        self.make_dir(name, app_dir)
        formated_name = app_dir + "/" + name
        management.call_command("startapp", name, formated_name)
        self.update_app_config(name, app_dir)

    def check_app_dir(self, name):
        if not os.path.exists(os.path.join(os.path.join(settings.BASE_DIR, name))):
            raise ValueError(f"{name} is not exists")

    def make_dir(self, folder_name, app_dir):
        path = os.path.join(os.path.join(settings.BASE_DIR, app_dir), folder_name)
        if not os.path.exists(path):
            os.makedirs(path)
            return
        raise CommandError(
            f'App or folder already exists with name "{folder_name}" into "{app_dir}"'
        )
