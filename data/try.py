import json
data = {}
with open("user_1.json", "r") as read_file:
    data = json.load(read_file)
    print(data['room1']['current_temperature_setting'])

with open("user_1.json", "w") as write_file:
    data['room1']['current_temprature_setting'] = 26
    json.dump(data, write_file)
