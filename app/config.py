import yaml
import os

from deepmerge import always_merger

from app.parse import parse_row


def load(f):
    with open(f, "r") as stream:
        from_file = yaml.safe_load(stream)
        from_environ = {k.removeprefix('config.'): v for k, v in os.environ.items() if k.startswith('config.')}
        from_environ = parse_row(from_environ)
        return always_merger.merge(from_file, from_environ)
