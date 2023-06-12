
# cd 'folder that houses this script'
# ./recurring_task.ps1
# Specify the path to your file here
$file_path = "D:\Development\powershell\reminders.txt"
$stop_file = "stop.txt"

# Read lines from file
$lines = Get-Content $file_path

# Use a counter to track the current line
$count = 0

# Load Windows Forms for notifications
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;

public class Windows {
    [DllImport("user32.dll", CharSet = CharSet.Auto)]
    public static extern int MessageBox(IntPtr hWnd, String text, String caption, int options);
}
"@

# Loop infinitely
while($true)
{
    # If the stop file exists, exit the script
    if (Test-Path $stop_file) {
        Remove-Item $stop_file -ErrorAction SilentlyContinue
        exit
    }

    # Get the current line and show it as a notification
    $current_line = $lines[$count]
    [Windows]::MessageBox(0, $current_line, "Notification", 1) 

    # Wait for a while before showing the next notification
    Start-Sleep -Seconds (2*60) # adjust this for the interval you want

    # Move to the next line
    $count++

    # If we've reached the end of the lines, start over
    if ($count -ge $lines.Count) {
        $count = 0
    }
}

