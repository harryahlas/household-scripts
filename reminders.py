import random
from plyer import notification

def random_line(file_path):
    lines = open(file_path).read().splitlines()
    return random.choice(lines)

file_path = "D:\\github\\household-scripts\\harry_reminders.txt"
reminder = random_line(file_path)
print(reminder)

notification.notify(
    title="Reminder",
    message=reminder,
    app_name="Python Script",
    timeout=10
)




import random

def random_line(file_path):
    lines = open(file_path).read().splitlines()
    return random.choice(lines)

file_path = "D:\\github\\household-scripts\\harry_reminders.txt"
reminder = random_line(file_path)
print(reminder)
from plyer import notification
import sys 
print(sys.executable)
