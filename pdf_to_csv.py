import PyPDF2
import pandas as pd
import os


year = '2022'

# Get the directory of the current script
script_directory = os.path.dirname(os.path.realpath(__file__))

# Define the data directory
data_directory = os.path.join(script_directory, 'input/' + year)

# List all files in the data directory
files = os.listdir(data_directory)

# Filter the list for pdf files
pdf_files = [f for f in files if f.endswith('.pdf')]

# If there are any pdf files
if pdf_files:
    # Get the first pdf file
    file_name = pdf_files[0]
    print(f"File Name: {file_name}")

    # Define the full file path
    file_path = os.path.join(data_directory, file_name)

else:
    print("No PDF files found in directory.")

# Read the PDF and extract the data
data = []
if file_path:
    with open(file_path, 'rb') as f:
        pdf = PyPDF2.PdfReader(f)
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            content = page.extract_text()
            # Split the content of each page into lines (rows)
            rows = content.split('\n')
            # Split each row into columns and add to the data list
            for row in rows:
                columns = row.split(',')  # replace ',' with your column separator
                data.append(columns)

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Save the data to a CSV file
df.to_csv(data_directory + "/output.csv", index=False, header=False)

# Read the CSV file
df = pd.read_csv(data_directory + "/output.csv", header=None)

# Only include the first 80 rows
df = df.iloc[:80]

# Save the updated DataFrame to the CSV file
df.to_csv(data_directory + "/output.csv", index=False, header=False)

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