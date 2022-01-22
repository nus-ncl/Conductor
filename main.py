import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
from bin import specification_parser
from config import default
import argparse
import subprocess


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--specification_file', required=True)
    args = parser.parse_args()

    # print(f'Hello {args.specification_file}')
    # specification_parser.parser(f"{default.SPECIFICATION_PATH}/log4shell/deter_vm_baremetal_flavor.yml")
    specification_parser.parser(f"{args.specification_file}")
    vagrant_cmd = "cd output/Conductor/output/conductor/log4shell/n1;vagrant status"
    subprocess.Popen(vagrant_cmd.split())
