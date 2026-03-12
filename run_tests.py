import sys
import os

# Set PYTHONPATH
sys.path.insert(0, os.path.abspath(os.curdir))

import pytest

if __name__ == "__main__":
    retcode = pytest.main(["-v", "tests/test_core.py"])
    sys.exit(retcode)
