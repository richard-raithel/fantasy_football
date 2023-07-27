import pandas as pd
import os

import os
import pandas as pd

# Get the directory of the current script
script_directory = os.path.dirname(os.path.realpath(__file__))

# Define the data directory
data_directory = os.path.join(script_directory, 'input')

# List all files in the data directory
files = os.listdir(data_directory)

# Filter the list for csv files
csv_files = [f for f in files if f.endswith('.csv')]

# If there are any csv files
if csv_files:
    # Get the first csv file
    file_name = csv_files[0]
    print(f"File Name: {file_name}")

    # Define the full file path
    file_path = os.path.join(data_directory, file_name)

    # Read the CSV file
    df = pd.read_csv(file_path, delimiter='$', header=None)

    # Print the first few rows of the DataFrame
    print(df.head())
else:
    print("No CSV files found in directory.")

df = df.T.stack().reset_index(drop=True)
df2 = df.apply(lambda st: st[st.find("(")+1:st.find(")")])
frames = [df, df2]
result = pd.concat(frames, axis=1)
result[0] = result[0].apply(lambda x: "".join(x.split(" ", 2)[2:4]))
result[0] = result[0].apply(lambda x: "".join(x.split(",", 2)[:1]))
result.columns = ['Player', 'PosRank']
for i in range(80, 250):
    result.at[i, 'Player'] = "".join(str(result.at[i, 'Player']).split(" ", 2)[2:4])
result.drop(result.index[250:380], inplace=True)
result.reset_index(drop=True)
print(result.to_string())
result.to_csv('output/sorted_players.csv', index=False)
