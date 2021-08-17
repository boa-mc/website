"""The setup wizard for both the Discord bot."""
import json
import os
from threading import Thread
import socket
from time import sleep
from getmac import get_mac_address


class Wizard:
    """The main class."""
    def __init__(self):
        os.system("clear")
        print("Welcome to the website setup.\n"
              "This tool will guide you to get your web server running.")
        print("If you have not already set up the Minecraft server, please do it now. On start, it should show an IP.")
        while True:
            server_address = input("What's that IP? ")
            if server_address == socket.getfqdn():
                server_address = "localhost"
            print("Trying to connect to the server...")
            t = Thread(target=self.ping_server, args=(server_address,))
            self.pingOk = False
            t.start()
            sleep(1)
            if self.pingOk:
                break
            else:
                print("The ping to the server failed! Please verify it is running and the IP is correct.")
        os.system("clear")
        if server_address == "localhost":
            macaddress = None
        else:
            macaddress = get_mac_address()
            print("Apparently, you have chosen to run the webserver on another computer than the Minecraft server.\nYou will be able to remotely turn on the server using Wake on Lan (WoL) if this is enabled in its BIOS.\nIf you want to disable this, set mac_address to null in config.json.")
        while True:
            port = int(input("On which port do you want your web server to be running? "))
            if self.is_port_in_use(port):
                print("This port is already in use.")
            elif port < 1024:
                print("Normal system users are not allowed to use ports below 1024.\n"
                      "You will have to run the server as root.")
                answer = input("Do you want to continue? [Y/n]")
                if answer.lower() == "y" or answer == "":
                    break
            else:
                break
        os.system("clear")
        print("The setup is now done. Starting the web server...")
        config = {
            "server_address": server_address,
            "port": port,
            "macaddress": macaddress
        }
        json.dump(config, open("config.json", "w"))

    def ping_server(self, ip):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, 25556))
                s.sendall(b"ping")
                response = s.recv(1024)
            if response == b"pong":
                self.pingOk = True
        except ConnectionRefusedError:
            pass

    def is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0


Wizard()