import json
import os


def _get_fixture_filepath(filepath):
    return os.path.abspath(
        os.path.join(
            os.path.join(
                os.path.dirname(__file__),
                "",
                "",
                filepath,
            )
        )
    )


def load_fixture(filepath, **kwargs):
    """
    Return the contents of a fixture file.

    If the file is a JSON file, we return the Python payload (not the JSON
    string).
    """
    root = kwargs.pop("root", None)
    with open(_get_fixture_filepath(filepath), **kwargs) as f:
        if filepath.endswith(".json"):
            data = json.load(f)
            if root is not None:
                return data[root]
            return data
        return f.read()
