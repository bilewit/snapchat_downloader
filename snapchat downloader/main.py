from snap_data import *
from google_drive_uploader import *



def main():
    login_google()
    parent_status()
    folder_list = refresh_folder_list()
    file = 'memories_history.json'
    offline_trio = compress_json_info(file)
    status = -1
    total_snaps = len(offline_trio)
    print('There are a total of '+str(total_snaps)+' snaps')
    #item = link, type, date
    for item in offline_trio:
        #run the post to get the amazon, type, name
        online_snap = online_final_trio(item)
        url = online_snap[0]
        # this will return .jpg or .mp4
        file_type = file_type_end(online_snap[1])
        # this saves a temp file of snap chat
        file_name = save_file(item, file_type)
        #this will download temp file
        temp_save_file(file_type,url)
        # this will upload the file
        upload_file(file_name,file_type)
        status += 1
        f = open("status.txt", "w")
        f.write('You have downloaded '+str(status)+' of '+str(total_snaps)+' snaps')
        f.close()
        print("currently: " + str(status) + " of " + str(total_snaps))


main()