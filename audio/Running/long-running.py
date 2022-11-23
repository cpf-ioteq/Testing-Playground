#!/usr/bin/env python3
#!/usr/bin/env python3

import subprocess as sp
import argparse

parser = argparse.ArgumentParser(add_help=False)
sp.run(
    'python3 base_stream.py 100 40 25'
    '& python3 base_stream.py 25 2 14'
    '& python3 base_stream.py 100 0 25'
    , shell=True)
