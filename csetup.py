import os
import logging
import json

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)

logo = """
█▀▄▀█ █ ▀▄▀ █▀▄▀█ ▄▀█ ▀█▀ █▀▀ █░█
█░▀░█ █ █░█ █░▀░█ █▀█ ░█░ █▄▄ █▀█
"""
print(logo)

client_id = str(input("Enter the Client ID: "))
client_secret = str(input("Enter the Client Secret: "))
command_prefix = str(input("Enter your preferred command prefix (the prefix which you will use to call the CLI (example: /mx), don't write the /, just the prefix (Make sure the prefix doesn't already exist in the C Folder): "))

logging.info("Creating creds.env")
with open("creds.env", "a") as file:
    logging.info("Entering Client ID, Client Secret to creds.env")
    file.write(f'CLIENT_ID="{client_id}"\nCLIENT_SECRET="{client_secret}"\nCOMMAND_PREFIX="\{command_prefix}"')
    logging.info("Client ID, Client Secret successfully written into creds.env")

logging.info("Creating tokens.json")
with open("tokens.json", "a") as file:
    logging.info("Initializing JSON values for tokens.json")
    json_data = {
        "access_token": '',
        "refresh_token": ''
    }
    json.dump(json_data, file, indent=2)
    logging.info("Values initialized.")

logging.info(f"Creating {command_prefix}.cmd")
with open(f"{command_prefix}.cmd", "a") as file:
    logging.info(f"Creating / command with prefix {command_prefix}")
    mixmatch_path = os.path.abspath("mixmatch.py")
    file.write(f'@echo off\npython "{mixmatch_path}" %*')
    logging.info("Command successfully created.")
logging.info(f"Congratulations, you now have a usable command! The command file ({command_prefix}.cmd) is located in this directory, please move the C Drive (C:\) to use it everywhere.")
print("WARNING: DO NOT RUN THIS FILE AGAIN, IT MAY CORRUPT CRUTICAL CREDENTIAL FILES, IT IS ADVISED YOU DELETE THIS FILE OFF YOUR SYSTEM.")
