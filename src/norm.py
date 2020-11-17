import argparse
import sys, io
from main import Normalizer


input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')


Normalizer.stream(input_stream)
