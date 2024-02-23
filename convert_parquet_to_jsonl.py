import sys
import pandas as pd

# Get the filename from the command line argument
filename = sys.argv[1]

# Load the file using pandas
data = pd.read_parquet(filename)

# Replace the extension with jsonl
new_filename = filename.rsplit('.', 1)[0] + '.jsonl'

data.to_json(new_filename, orient='records', lines=True)
