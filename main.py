import configparser
from colorama import init, Fore
import os
import subprocess
import sys
import re

config = configparser.ConfigParser()
config.read('config.ini')

startDir = config['Directory']['startDir']
username = config['Emulator']['username']

init()

exp = re.compile("cd .")

colorCodes = {'BLACK':'\u001b[30m', 'RED':'\u001b[31m', 'GREEN':'\u001b[32m', 'YELLOW':'\u001b[33m', 'BLUE':'\u001b[34m', 'MAGENTA':'\u001b[35m', 'CYAN':'\u001b[36m', 'WHITE':'\u001b[37m'}

def terminal(name, startDir):
    try:
        os.chdir(startDir)
        color = colorCodes.get(config['Emulator']['foreColor'])
        errorColor = colorCodes.get(config['Emulator']['errorColor'])
        if color != None and errorColor != None:
            print(color + config['Emulator']['startLine'])
            while True:
                currentDir = os.getcwd()
                inputText = f"{name} - {currentDir} $ "
                inp = input(inputText)
                match = bool(re.match(exp, inp))
                if inp.lower() == 'exit':
                    sys.exit()
                elif match == True:
                    splitInp = inp.split(" ")
                    finalInp = " ".join(splitInp[1:])
                    try:
                        os.chdir(finalInp)
                    except FileNotFoundError:
                        err = "emuthon: cd: {}: No such file or directory".format(finalInp)
                        print(errorColor + err)
                        print(errorColor + color)
                else:
                    subprocess.run(inp, shell=True)
        else:
            print(Fore.RED + 'Invalid color code. Quitting.')
            sys.exit()
    except KeyboardInterrupt:
        print(Fore.RED + 'Quitting.')
        sys.exit()

terminal(username, startDir)
