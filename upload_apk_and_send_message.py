import argparse
import termcolor

from apk_automation import upload_and_get_drive_path
from daily_update_automation import send_message
from read_commit_messages import get_last_n_commit_messages
import inquirer

def select_item(items):
    questions = [
        inquirer.List('item',
                      message="Select an item:",
                      choices=items,
                  ),
    ]
    answers = inquirer.prompt(questions)
    return answers['item']


def obtain_args():
    parser = argparse.ArgumentParser(description="Upload APKs to Drive and Send Message to Discord");
    parser.add_argument("-n", "--name", type=str, help="Name of the Apk file to upload", default="app-release", required=False)
    parser.add_argument("-c", "--commits", type=int, help="Number of commits to consider for update message",default=5, required=False)
    parser.add_argument("-u", "--update-only",action="store_true", help="Only Send Update Message", default=False, required=False)
    return parser.parse_args()

def main():
    args = obtain_args()

    apps = {
        "Customer App": "1177608860685582446",
        "Store Manager App": "1171697957775609937",
        "Owners App": "1198975249383952414"
    }

    selected_app = select_item(list(apps.keys()))

    if args.update_only:
        link = upload_and_get_drive_path(args.name)

    commits = get_last_n_commit_messages(args.commits)

    ordered_commits = "\n".join(map(lambda i, s: f"{i}. {s}", range(1, len(commits)+1), commits))

    link_message = "APK Link:\n{link}" if link is not None else ""

    message = f'''
{link_message}

Updates :
{ordered_commits}
'''
    response = send_message(apps[selected_app], message)
    if response.status_code == 200:
        termcolor.cprint('\u2713 Message sent successfully','green')
    else:
        termcolor.cprint(f'Failed to send message. Status code: {response.status_code}, Error: {response.text}','red')


if __name__ == '__main__':
    main()