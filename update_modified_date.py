import os
import time
import win32file
import win32con
import datetime
import pywintypes

def change_file_time(path, new_time):
    # Get the current file times
    handle = win32file.CreateFile(
        path, win32con.GENERIC_WRITE, 0, None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)

    # Change the last modified time
    win32file.SetFileTime(handle, None, None, pywintypes.Time(new_time))

    handle.Close()

def change_files_in_folder(folder_path, new_time):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            change_file_time(file_path, new_time)

if __name__ == "__main__":
    folder_path = 'your folder path here'  # replace with your folder path
    new_time = datetime.datetime(2023, 5, 1, 10, 30)  # replace with your desired time
    change_files_in_folder(folder_path, new_time)
