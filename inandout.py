import requests
import time
import re

# Discord webhook URL
WEBHOOK_URL = 'your-web-hook-url'

# Dictionary to store the events that have already been sent to Discord
sent_events = {}

# Function that sends a message to the Discord channel
def send_message(player, log_status, time_of_event):
    message = f'{player} {log_status} the Minecraft server at {time_of_event}.'
    data = {'content': message}
    requests.post(WEBHOOK_URL, json=data)

# Function that reads the Minecraft server logs
def read_logs():
    with open('/path/to/your/logs', 'r') as log_file:
        for line in log_file:
            if 'logged in' in line:
                try:
                    player = line.split(" ")[5].split("[")[0]
                    time_of_event = line.split('[')[1].split(']')[0].split(' ')[1]
                except IndexError:
                    print("Error: Could not parse player information from line")
                    print(line)
                    continue
                event = f'{player} logged in at {time_of_event}'
                if event not in sent_events:
                    sent_events[event] = True
                    send_message(player, "logged in to", time_of_event)
            elif 'left the game' in line:
                try:
                    player = line.split(" ")[5].split("[")[0]
                    time_of_event = line.split('[')[1].split(']')[0].split(' ')[1]
                except IndexError:
                    print("Error: Could not parse player information from line")
                    print(line)
                    continue
                event = f'{player} lost connection at {time_of_event}'
                if event not in sent_events:
                    sent_events[event] = True
                    send_message(player, "lost connection from", time_of_event)

while True:
    read_logs()
        time.sleep(10)
