""" Main script which will start the discord bot after, if needed, the setup wizard."""

import setup_wizard
import os
import subprocess
import sys


def install_dependencies():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pip", "-U"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "dash"])


if not os.path.isfile("config.json"):
    install_dependencies()
    setup_wizard.Wizard()

import start_dash
