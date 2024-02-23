# loads a jsonl file and gets a random 1000 lines from it
import random
import sys

# Get the filename from the command line argument
filename = sys.argv[1]
output_filename = sys.argv[2]
# Load the file using open

with open(filename) as f:
    data = f.readlines()

# Get 1000 random lines
random_lines = random.sample(data, 1000)

# output the random lines to a new file
with open(output_filename, 'w') as f:
    f.writelines(random_lines)
