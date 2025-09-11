import subprocess
import sys
from importlib.metadata import version, PackageNotFoundError
from packaging.version import parse

def test_dependencies():
    """
    Tests that the dependencies are installed correctly and that the version of
    PyJWT is compatible with flask-jwt-extended.
    """
    try:
        # Check if pyjwt is installed and at the correct version
        pyjwt_version = version("pyjwt")
        if parse(pyjwt_version) < parse("2.10.0"):
            # If not, install the dependencies
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "openthairag/requirements.txt"])
            pyjwt_version = version("pyjwt")
        assert parse(pyjwt_version) >= parse("2.10.0")
    except PackageNotFoundError:
        # If not installed, install the dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "openthairag/requirements.txt"])
        try:
            pyjwt_version = version("pyjwt")
            assert parse(pyjwt_version) >= parse("2.10.0")
        except PackageNotFoundError:
            assert False, "PyJWT is not installed after attempting to install dependencies."
