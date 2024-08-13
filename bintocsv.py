from pymavlink import mavutil
import csv
import os
import pandas as pd
import datetime


def convert_bin_to_csv(bin_file, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    # Get the creation time of the file in seconds since the epoch
    creation_time = os.path.getctime(bin_file)
    # Convert the creation time to a datetime object
    creation_date = datetime.datetime.fromtimestamp(creation_time)
    # log_date = datetime.datetime.fromtimestamp(os.path.getctime(bin_file)).date()
    # Open the binary log file
    mlog = mavutil.mavlink_connection(bin_file)
    
    # Define a dictionary to store the messages
    data = {}
    
    # Read the messages from the binary log file
    while True:
        msg = mlog.recv_msg()
        if msg is None:
            break
        if msg.get_type() not in data:
            data[msg.get_type()] = []
        # Convert the message to a dictionary and append it
        data[msg.get_type()].append(msg.to_dict())

    # Write each message type to a separate CSV file
    for msg_type, msgs in data.items():
        csv_file = os.path.join(output_dir, f"{msg_type}.csv")
        
        # Check if there are messages to write
        if msgs:
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(msgs)
            # Convert milliseconds to HH:MM:SS in 'Timestamp' column if it exists
            if 'TimeUS' in df.columns:
                df['TimeUS'] = pd.to_timedelta(df['TimeUS'], unit='ms')
                # df['TimeUS'] = df['TimeUS'].apply(lambda x: x.replace(year=log_date.year, month=log_date.month))
                df['TimeUS'] = creation_date + df['TimeUS']
                df['TimeUS'] = df['TimeUS'].dt.strftime('%Y-%m-%d %H:%M:%S')
            # Write the DataFrame to a CSV file
            df.to_csv(csv_file, index=False)
        else:
            print(f"No messages of type {msg_type} to write to CSV.")

    print(f"Converted {bin_file} to CSV files in {output_dir}")