
from datetime import datetime
import requests
import os
from ç import load_dotenv

""" 
 Remember to set KB_ID, KB_URL, API_KEY and GLOBAL_AUTH_TOKEN keys in your .env file
 Also you'll need to install dotenv

 To get the GLOBAL_AUTH_TOKEN do the following on the CLI:
 - To install the CLI, run: 

        pip install nuclia


 - After is intalled you need to authenticate and get the token with:

        nuclia auth login


 - This will take you to a browswer where you can copy the token 

 More documentation about the CLI here:
 https://docs.nuclia.dev/docs/guides/sdk/python-sdk/README

"""
def load_keys():
    print("Loading enviorment keys...")
    load_dotenv()

load_keys()

NUCLIA_MANAGEMENT_API = "https://nuclia.cloud/api/v1"
NUCLIA_KB_API = f'https://{os.getenv("KB_ZONE")}.nuclia.cloud/api/v1'

show_log = True
def logger(logger = True):
    global show_log
    show_log = logger

def print_time(line):
    if show_log is True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(f'.{current_time} | {line}')

class API:
    def get_model():
        url = f'{NUCLIA_KB_API}/kb/{os.getenv("KB_ID")}/configuration'
        response = requests.get(
            url,headers={"Authorization": f"Bearer {os.getenv('GLOBAL_AUTH_TOKEN')}"}
        )
        assert response.status_code == 200
        return response.json()['generative_model']


    def set_model(model):
        current_model= API.get_model()
        url = f'{NUCLIA_KB_API}/kb/{os.getenv("KB_ID")}/configuration'
        response = requests.patch(
            url, 
            json={
                "generative_model": model
            },
            headers={"Authorization": f"Bearer {os.getenv('GLOBAL_AUTH_TOKEN')}"}
        )
        print_time(f'| | | | | | | | | | Generative model PATCHed from {current_model} ---> {model}')
        assert response.status_code == 204


    def search(query, prompt = ""):
        print_time(f'answering in...')
        url = f'{NUCLIA_KB_API}/kb/{os.getenv("KB_ID")}/chat'
        response = requests.post(
            url, 
            json={
                "query": query, 
                "prompt": prompt
            },
            headers={
                "Authorization": f'Bearer {os.getenv("GLOBAL_AUTH_TOKEN")}',
                "x-synchronous": "true"
                }
        )

        print_time(f'answering out......')
        assert response.status_code == 200
        return response.json()["answer"]




