import os 
import json
import argparse
import termcolor

from apk_automation import upload_and_get_drive_path
from daily_update_automation import send_message
from read_commit_messages import get_last_n_commit_messages
import inquirer

script_path = os.path.dirname(os.path.realpath(__file__))

def obtain_args():
    parser = argparse.ArgumentParser(description="Upload APKs to Drive and Send Message to Discord");
    parser.add_argument("-n", "--name", type=str, help="Name of the Apk file to upload", default="app-release", required=False)
    parser.add_argument("-c", "--commits", type=int, help="Number of commits to consider for update message",default=5, required=False)
    parser.add_argument("-a", "--app", type=str, help="App for which the APK is to be uploaded",default=None, required=False)
    parser.add_argument("-u", "--update-only",action="store_true", help="Only Send Update Message", default=False, required=False)
    parser.add_argument("-p", "--print-only",action="store_true", help="Print the message to send", default=False, required=False)
    parser.add_argument("-nu", "--no-update",action="store_true", help="Do not update the message to discord", default=False, required=False)
    return parser.parse_args()

def get_supported_apps():
    file_path = os.path.join(script_path, "upload_apps.json") 
    with open(file_path, 'r') as f:
        return json.load(f)

def save_to_file(data):
    file_path = "drive.rc"
    with open(file_path, 'w') as file:
        file.write(data)

def retrieve_from_file():
    file_path = "drive.rc"
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as file:
        return file.read().strip()

def select_item(items):
    questions = [
        inquirer.List('item',
                      message="Select an item:",
                      choices=items,
                  ),
    ]
    answers = inquirer.prompt(questions)
    return answers['item']

def get_message(link, commits):
    commits = get_last_n_commit_messages(commits)

    ordered_commits = "\n".join(map(lambda i, s: f"{i}. {s}", range(1, len(commits)+1), commits))

    link_message = f"APK Link:\n{link}" if link is not None else ""

    return f'''

From Sushan's Task Bot :

{link_message}

Updates :
```
{ordered_commits}
```
'''

def main():
    args = obtain_args()

    link = retrieve_from_file()

    if args.print_only:
        print(get_message(link, args.commits)) 
        return

    selected_app = None

    apps_meta = {
        'customer': "Customer App",
        'employee': "Store Manager App",
        'owner': "Owners App",
    }

    tags = {
         "Customer App":'customer',
         "Store Manager App":'employee',
         "Owners App": 'employee',
    }

    if args.app is not None:
        selected_app = apps_meta[args.app]

    apps = get_supported_apps() 

    if not args.no_update and selected_app is None :
        selected_app = select_item(list(apps.keys()))

    if not args.update_only:
        link = upload_and_get_drive_path(args.name, tags[selected_app])
        save_to_file(link)

    message = get_message(link, args.commits)

    if args.no_update:
        print(message)
        return;

    response = send_message(apps[selected_app], message)
    if response.status_code == 200:
        termcolor.cprint('\u2713 Message sent successfully','green')
    else:
        termcolor.cprint(f'Failed to send message. Status code: {response.status_code}, Error: {response.text}','red')


if __name__ == '__main__':
    main()