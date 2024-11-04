import pandas as pd
from flask import session
import os
# Function to get unique values from files
files = []
def getuv(user_id):
    fi=os.listdir(f'output/{user_id}/csv')
    for i in fi:
        fp=f'output/{user_id}/csv/{i}'
        files.append(fp)
    return files

def get_unique_values_from_files(user_id):
    unique_values = {}
    files=getuv(user_id)
    for f in files:
        if f.endswith(".csv"):
            df = pd.read_csv(f)
            for column in df.columns:
                if column == 'I' or column == 'IMU':
                    unique_vals = df[column].unique().tolist()
                    if 1 < len(unique_vals) < 5:
                        if f not in unique_values:
                            f=f.split('/')[-1]
                            f=f.replace('.csv', '')
                            unique_values[f] = unique_vals
    # print(f'uv{unique_values}')             
    return unique_values
