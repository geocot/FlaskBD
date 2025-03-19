# Python program to solve JSONDecodeError: Expecting value: line 1 column 1 (char 0)
import json

file_path = "donnees/normales.json"

with open(file_path, 'r') as j:
     contents = json.loads(j.read())
     print(contents)