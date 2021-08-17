""" Main script which will start the web server after, if needed, the setup wizard."""

import os
import sys
import argparse

parser = argparse.ArgumentParser(description='The mc-server-tools website node.')
parser.add_argument('-s', '--setup', action="store_true")
args = parser.parse_args()


def install_dependencies():
    print("Installing dependencies...")
    if os.system(sys.executable + " -m pip install pip -U > /dev/null") or \
            os.system(sys.executable + " -m pip install dash getmac wakeonlan > /dev/null"):
        print("\033[91mERROR: Pip failed, is it installed?")
        exit(1)

if not os.path.isfile("config.json") or args.setup:
    install_dependencies()
    os.system(sys.executable + " setup_wizard.py")

os.system(sys.executable + " start_dash.py")
