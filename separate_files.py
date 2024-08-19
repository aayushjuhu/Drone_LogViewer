import pandas as pd
import os
# Function to get unique values from files
files = []
fi=os.listdir('output')
for i in fi:
    fp='output/'+i
    files.append(fp)


def get_unique_values_from_files():
    unique_values = {}
    for f in files:
        df = pd.read_csv(f)
        for column in df.columns:
            if column == 'I' or column == 'IMU':
                unique_vals = df[column].unique().tolist()
                if 1 < len(unique_vals) < 5:
                    if f not in unique_values:
                        f=f.split('/')[-1]
                        f=f.replace('.csv', '')
                        unique_values[f] = unique_vals
                        
    return unique_values