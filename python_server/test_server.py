import os
import sys

sys.path.append('../python_server')
os.environ["test"] = "True"
from server import *