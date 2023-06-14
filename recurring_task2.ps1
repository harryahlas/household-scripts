# Read the text file
$filePath = "D:\github\household-scripts\harry_reminders.txt"
$content = Get-Content -Path $filePath

# Select a random line from the file
$randomLine = Get-Random -InputObject $content | ForEach-Object { $_.Split('`n')[-1] }

# Display the random line as a reminder in Windows
$toast = [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
$toast.CreateToastNotifier("Reminder", 5).Show($randomLine)
