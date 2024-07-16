import json

# File path
file_path = './data/forumData.json'

# Data to be added
new_entry = {
    "name": "sathiyajith",
    "rollno": 56,
    "cgpa": 8.6,
    "phonenumber": "9976770500"
}

# Open and read the existing JSON file
with open(file_path, 'r') as openfile:
    json_array = json.load(openfile)

# Append the new entry to the list
json_array.append(new_entry)

# Write the updated list back to the JSON file
with open(file_path, 'w') as openfile:
    json.dump(json_array, openfile, indent=4)