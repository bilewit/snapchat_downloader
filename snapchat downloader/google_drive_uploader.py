from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from PIL import Image
import urllib.request
import requests
import time

#login to google n fun
global folder_list
folder_list = []

# returns a updated list of tuples of folder_name, folder_id


def login_google():
    global drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
    drive = GoogleDrive(gauth)

def refresh_folder_list():
    folders = drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in folders:
        folder_list.append((folder['title'], folder['id']))
    return folder_list

def parent_status():
    status = False
    folder_list = refresh_folder_list()
    #print(folder_list)
    for folder in folder_list:
        for item in folder:
            if 'snap_backup' == item:
                status = True
            if status == True:
                return folder[1]
    else:
        init_parent()


def init_parent():
    g_main_dir = 'snap_backup'
    folder = drive.CreateFile({'title': g_main_dir, 'mimeType': 'application/vnd.google-apps.folder'})
    folder.Upload()
    parent_status()




#looks for folder that has a year and creates a year folder
#if not there because the parent folder is always constant


def find_year_folder(name):
    status = False
    folder_list = refresh_folder_list()
    for folder in folder_list:
        for item in folder:
            if name == item:
                print('i mean we made it to the end ?')
                status = True
            if status == True:
                parent_id = folder[1]
                return parent_id
    else:
        parent_id = parent_status()
        create_folder(parent_id,name)
        return find_year_folder(name)

def find_month_folder(name):
    status = False
    folder_list = refresh_folder_list()
    for folder in folder_list:
        for item in folder:
            if name == item:
                status = True
            if status == True:
                return folder[1]
    else:
        year = name[:4]
        parent_id = find_year_folder(year)
        create_folder(parent_id,name)
        return find_month_folder(name)

#creates a folder given parent id, and a name for folder
def create_folder(parent_id,name):
    g_file = drive.CreateFile({'title': name,'mimeType' : 'application/vnd.google-apps.folder','parents': [{'id': parent_id}]})
    g_file.Upload()

def temp_save_file(file_type, url):
    #save the file correctly as temp.ext
    r = requests.get(url, allow_redirects=True, stream=True)
    open('temp'+file_type, 'wb').write(r.content)




def save_file(item, file_type):
    url = item[0]
    response = requests.get(url)
    # gets the file type xxx/yyy and then splits and takes yyy
    # file_type = response.headers['Content-Type'].split('/')[1]
    # get the file name
    file_name = item[2]
    # get the date of the file
    file_month = file_name[:7]
    file_year = file_name[:4]
    #temp_save_file(file_type, url)
    return file_name

def upload_file(filename,file_type):
    path = 'temp'+file_type
    parent_id = find_month_folder(str(filename[:7]))
    g_file = drive.CreateFile({'parents': [{'id': parent_id}]})
    g_file.SetContentFile(path)
    g_file['title'] = filename
    g_file.Upload()
    print('uploaded file')
















