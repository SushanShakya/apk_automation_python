import json
import requests
import termcolor
from halo import Halo

THREAD_ID = "1171697957775609937"
TOKEN_FILE = 'discord_token.json'

spinner_config = {
    "interval": 80,
		"frames": [
			"⠋",
			"⠙",
			"⠹",
			"⠸",
			"⠼",
			"⠴",
			"⠦",
			"⠧",
			"⠇",
			"⠏"
		]
}

def authenticate():
    with open(TOKEN_FILE, 'r') as f:
            token_data = json.load(f)
    return token_data.get('access_token')

@Halo(text="Updating Message", spinner=spinner_config)
def send_message(thread_id, message_content):
    access_token = authenticate()
    headers = {
        'Authorization': f'{access_token}',
        'Content-Type': 'application/json'
    }
    send_message_url = f'https://discord.com/api/v9/channels/{thread_id}/messages'
    message_payload = {
        'content': message_content,
        'thread_id': thread_id
    }
    response = requests.post(send_message_url, headers=headers, json=message_payload)
    return response
    

def main():
    access_token = authenticate()
    if access_token:
        message_content = "TEST MESSAGE"
        response = send_message(access_token, THREAD_ID, message_content)
        if response.status_code == 200:
            termcolor.cprint('\u2713 Message sent successfully','green')
        else:
            termcolor.cprint(f'Failed to send message. Status code: {response.status_code}, Error: {response.text}','red')


if __name__ == "__main__":
    main()
