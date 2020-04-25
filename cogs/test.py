import csv
import os

with open(f'{os.getcwd()}/cogs/cmd_poll_channels/guild_settings.csv', 'r', newline='') as settings:
    reader = csv.reader(settings)
    header = next(reader)
    settings = {}
    for row in reader:
        settings[row[0]] = row[1]
print(header, settings)
