import os
import termcolor 
from pydrive.auth import GoogleAuth 
from pydrive.drive import GoogleDrive
from halo import Halo
import time
import argparse

dirId = "15GRbTHZbeAyN3YGpW8V5Q4Gy_Jcz31Lf"
new_file_name = time.strftime("%Y%m%d-%H%M%S")
new_file_title = f"{new_file_name}.apk"
dirpath = os.getcwd()

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

def obtain_args():
    parser = argparse.ArgumentParser(description="Upload APKs to Drive");
    parser.add_argument("-n", "--name", type=str, help="Name of the Apk file to upload", default="app-release", required=False)
    parser.add_argument("-D", "--delete-all",action="store_true", help="Delete all uploaded APKs", default=False, required=False)
    parser.add_argument("-d", "--delete-retain-last", action="store_true", help="Delete uploaded APKs except the last uploaded", default=False, required=False)
    return parser.parse_args()


@Halo(text="Deleting From Drive", spinner=spinner_config)
def delete_all_from_drive(drive: GoogleDrive):
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(dirId)}).GetList() 
    for file in file_list:
        file.Delete()

@Halo(text="Deleting From Drive Except Last Uploaded", spinner=spinner_config)
def delete_all_from_drive_except_last(drive: GoogleDrive):
    file_listx = drive.ListFile({'q': "'{}' in parents and trashed=false".format(dirId)}).GetList() 
    file_listx.sort(key=lambda x: x['createdDate'])
    file_list = file_listx[:-1]
    for file in file_list:
        file.Delete()

@Halo(text="Uploading APK to Drive", spinner=spinner_config)
def upload_to_drive(drive: GoogleDrive, path_to_apk: str):
    gfile = drive.CreateFile({'parents': [{'id': dirId}]})
    gfile['title'] = new_file_title 
    gfile.SetContentFile(path_to_apk)
    gfile.Upload()
    return gfile

@Halo(text="Fetching Drive Link", spinner=spinner_config)
def get_uploaded_file_id(drive):
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(dirId)}).GetList() 
    file_id = ""
    for file in file_list:
        if(file['title'] == new_file_title): 
            file_id = file['id']
    return file_id

def get_apk_path(apk_name: str):
    return f"{dirpath}\\build\\app\\outputs\\flutter-apk\\{apk_name}.apk"

def main():
    args = obtain_args()

    # Google Authorization
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile()

    # Creation of Drive Object
    drive = GoogleDrive(gauth)

    if args.delete_all:
        delete_all_from_drive(drive)
        termcolor.cprint(f"\u2713 Deletion Complete !",'red')
        return
    
    if args.delete_retain_last:
        delete_all_from_drive_except_last(drive)
        termcolor.cprint(f"\u2713 Deletion Complete !",'red')
        return

    path_to_apk = get_apk_path(args.name)
    # Upload the File to Google Drive
    upload_to_drive(drive, path_to_apk)
    termcolor.cprint(f"\u2713 Upload Complete !",'green')

    # Load the Link to Share
    file_id = get_uploaded_file_id(drive)
    print('\nLink : ');
    termcolor.cprint(f"https://drive.google.com/file/d/{file_id}/view?usp=sharing", 'green')

if __name__ == '__main__':
    main()