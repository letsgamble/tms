import os
from dotenv import load_dotenv
from os.path import exists

ENV_FILE_EXISTS = exists('.env')


if ENV_FILE_EXISTS:
    load_dotenv()
else:
    with open(".env", "w") as f:
        f.write(f'smtp_server=\n')
        f.write(f'port=\n')
        f.write(f'sender_email=\n')
        f.write(f'password=\n')
        f.write(f'receiver_email=\n')
    load_dotenv()

smtp_server = os.getenv('smtp_server')
print(smtp_server)
