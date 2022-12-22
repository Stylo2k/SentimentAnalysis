'''
Script used to beautify json files. It takes the path to the json file as a command line argument
or asks for it if not specified. It then asks for the path to the output file and writes the json
data to it with indentation of 4 spaces.
'''

import json
import sys

# ask for the path to the json file relative to the current directory if not specified
# using the command line arguments 

path = sys.argv[1] if len(sys.argv) > 1 else input('Enter the path to the json file: ')

# read the file containing the json data
with open(path) as f:
    data = json.load(f)

# ask for the path to the output file relative to the current directory
output_path = input('Enter the path to the output file: ')

# write the json data to the output file
with open(output_path, 'w') as f:
    json.dump(data, f, indent=4)
