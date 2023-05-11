import os
import pywintypes
import win32file
import win32con
import time

def change_file_time(path, newtime):
    # Convert the timestamp to Windows FILETIME
    newtime = int(time.mktime(newtime.timetuple()))
    newfiletime = pywintypes.Time(newtime).timetuple()
    newfiletime = win32file.SystemTimeToDateTime(newfiletime)

    # Get the current file times
    handle = win32file.CreateFile(
        path, win32con.FILE_WRITE_ATTRIBUTES, 0, None, win32con.OPEN_EXISTING,
        win32con.FILE_ATTRIBUTE_NORMAL, None)

    # Change the last modified time
    win32file.SetFileTime(handle, newfiletime, newfiletime, newfiletime)
    handle.Close()

def change_files_in_folder(folder_path, new_time):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            change_file_time(file_path, new_time)

if __name__ == "__main__":
    import datetime
    folder_path = 'your folder path here'  # replace with your folder path
    new_time = datetime.datetime.now()  # replace with your desired time
    change_files_in_folder(folder_path, new_time)
