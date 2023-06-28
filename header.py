'''
This file contains the header of the program. It is used to import all the necessary modules and to define the functions that can be executed.
It also limits the scope of the functions that can be executed to the ones that are defined in the func_list dictionary.
'''

import sys
sys.dont_write_bytecode = True
from src.config import logger

def help():
    help_contents = "Usage(s):\n"
    help_contents += "===================================================================================\n"
    help_contents += "'python .\main.py install'\n"
    help_contents += "This will install all dependancies reuired for the bot.\n"
    help_contents += "\n"
    help_contents += "'python .\main.py uninstall'\n"
    help_contents += "This will uninstall all dependancies that were reuired for the bot.\n"
    help_contents += "\n"
    help_contents += "'python .\main.py clean'\n"
    help_contents += "This will delete all training data.\n"
    help_contents += "\n"
    help_contents += "'python .\main.py version'\n"
    help_contents += "This will print out the versions of karas, cuda, cuDNN and other important versions.\n"
    help_contents += "===================================================================================\n"
    print(help_contents)

# Hold a reference to all the functions that can be executed within a dictionary.
func_list = {
    "help": help,
}

try:
    # Only imports the modules if they are installed.
    from src.app import app

    # Append new references to all the functions that can be executed within a dictionary.
    func_list["api"] = app
except ImportError as e:
    logger.error("Import error: ", e)
    logger.error("On header.py")