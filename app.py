# Import Libraries

from flask import Flask, render_template, redirect, request, jsonify
import pandas as pd
from bintocsv import convert_bin_to_csv
from separate_files import get_unique_values_from_files
import plotly.graph_objects as go
import os

app = Flask(__name__)  # Initializing flask app

# Defining Routes
@app.route("/")  # Landing page
def home():
    return render_template('index.html')

@app.route("/upload", methods=['POST']) # uploading the file
def upload_file():
    if request.method == 'POST':  # To check whether request is of type post
        f = request.files['fupload'] # Get the file from the user
        print("file upload: ", f.filename)
        convert_bin_to_csv(f.filename, 'output') # convert .bin log file to .csv
        return redirect('/view')  # Redirect to the view page after uploading
    return redirect('/')

# @app.route('/home', defaults={'filename': None})
@app.route('/view', methods=['GET','POST']) # log viewer and analysis page
@app.route('/view<filename>', methods=['GET'])
def view1(filename=None):
    file_dir = 'output'
    file_names = [os.path.splitext(name)[0] for name in os.listdir(file_dir)] # getting the filename
    csv_columns = {}
    selected_file_columns = []
    html_table=None

    if filename:  # Check if the is uploaded or not
        filename=str(filename)
        fp=f'output/{filename}.csv'
        fp=str(fp)
        df=pd.read_csv(fp) # read the selected file
        html_table = df.to_html(index=False, classes='table table-bordered mt-2') # Convert the dataframe to html table to be displayed on page
    
    uv = get_unique_values_from_files()  # Get the unique values from column (used when there multiple sensors)
    print(f"{uv}")

    # Generate the dictionary of files and their columns
    for file in file_names:
        file_path = os.path.join(file_dir, file + ".csv")
        df = pd.read_csv(file_path)
        csv_columns[file] = list(df.columns)


# Getting the user input and plotting
    if request.method == 'POST':
        selected_columns1 = request.form.getlist('selected_col1')
        selected_columns2 = request.form.getlist('selected_col2')
        selected_columns3 = request.form.getlist('selected_col3')
        selected_columns4 = request.form.getlist('selected_col4')
        unival1 = request.form.getlist('unv1')
        plt_type1 = request.form.get('plt_type1')
        unival2 = request.form.getlist('unv2')
        plt_type2 = request.form.get('plt_type2')
        unival3 = request.form.getlist('unv3')
        plt_type3 = request.form.get('plt_type3')
        unival4 = request.form.getlist('unv4')
        plt_type4 = request.form.get('plt_type4')

        colors = ['blue', 'red', 'green', 'purple']  # List of colors
        response_data = {}

        # ---------------------------Plot1------------------------------------------------------------------------------
        
        if selected_columns1 and plt_type1:
            fig1 = go.Figure()
            cols=[]
            for i, item in enumerate(selected_columns1):
                file_name, col_name = item.split('[')
                col_name = col_name.strip(']')
                cols.append(col_name)
                df = pd.read_csv(os.path.join(file_dir, file_name + ".csv"))
                df.set_index('TimeUS', inplace=True)
                color = colors[i % len(colors)]
                if plt_type1 == 'Scatter':
                    fig1.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color))
                elif plt_type1 == 'Histogram':
                    fig1.add_histogram(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                elif plt_type1 == 'line':
                    fig1.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color))
            
            scol=' and '.join(cols)
            fig1.update_layout(
                title=f"Time vs {scol}",
                xaxis_title='Time',
                template='plotly_dark'
            )
            response_data['fig1'] = fig1.to_html(full_html=False, config={'scrollZoom': True})
        elif unival1 and plt_type1:
            # Iterate through the list
            fig1 = go.Figure()
            scols=[]
            for i, item in enumerate(unival1):
                # Split at the first '[' to get 'BARO1' and 'Press]'
                prefix, column = item.split('[')
                
                # Extract the last character (which is the number) and the rest of the prefix
                number = prefix[-1]  # '1'
                prefix = prefix[:-1]  # 'BARO'
                
                # Remove the closing bracket from the column name
                column = column.rstrip(']')  # 'Press'
                
                # Store them in variables
                fname = prefix
                colval = number
                col = column
                scols.append(col)
                print(f'{fname}+{colval}+{col}')
                
                # Load DataFrame
                df = pd.read_csv(f'output/{fname}.csv')
                
                # Determine filtering based on column existence and value
                if 'I' in df.columns and 'IMU' in df.columns:
                    if colval == '1':
                        flt_df = df[(df['I'] == 1) | (df['IMU'] == 1)]
                    elif colval == '0':
                        flt_df = df[(df['I'] == 0) | (df['IMU'] == 0)]
                    elif colval == '2':
                        flt_df = df[(df['I'] == 2) | (df['IMU'] == 2)]
                elif 'I' in df.columns:
                    if colval == '1':
                        flt_df = df[df['I'] == 1]
                    elif colval == '0':
                        flt_df = df[df['I'] == 0]
                    elif colval == '2':
                        flt_df = df[df['I'] == 2]
                elif 'IMU' in df.columns:
                    if colval == '1':
                        flt_df = df[df['IMU'] == 1]
                    elif colval == '0':
                        flt_df = df[df['IMU'] == 0]
                    elif colval == '2':
                        flt_df = df[df['IMU'] == 2]
                else:
                    flt_df = pd.DataFrame()  # Default to empty DataFrame if neither column exists

                df.set_index('TimeUS', inplace=True)
                
                if not flt_df.empty and col in flt_df.columns:
                    color = colors[i % len(colors)]
                    if plt_type1 == 'Scatter':
                        fig1.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='markers', marker=dict(color=color))
                    elif plt_type1 == 'Histogram':
                        fig1.add_histogram(x=df.index, y=flt_df[col].to_numpy(), name=f'{col} Histogram', marker_color=color)
                    elif plt_type1 == 'line':
                        fig1.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='lines', line=dict(color=color))
                else:
                    print(f"Data for {col} not available or empty.")
            print(scols)
            if len(scols) > 1:
                scol=' and '.join(scols)
            else:
                scol=''.join(scols)
            fig1.update_layout(
                    title=f'Time vs {scol}',
                    xaxis_title='Time',
                    yaxis_title='Value',
                    template='plotly_dark'
                )
            response_data['fig1'] = fig1.to_html(full_html=False, config={'scrollZoom': True}) # to convert graph to html and add to dict
        
        
        # ---------------------------Plot2------------------------------------------------------------------------------
        if selected_columns2 and plt_type2:
            fig2 = go.Figure()
            scols=[]
            for i, item in enumerate(selected_columns2):
                file_name, col_name = item.split('[')
                col_name = col_name.strip(']')
                scols.append(col_name)
                df = pd.read_csv(os.path.join(file_dir, file_name + ".csv"))
                df.set_index('TimeUS', inplace=True)
                color = colors[i % len(colors)]
                if plt_type2 == 'Scatter':
                    fig2.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color))
                elif plt_type2 == 'Histogram':
                    fig2.add_histogram(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                elif plt_type2 == 'line':
                    fig2.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color))
            scol=" and ".join(scols)
            fig2.update_layout(
                title=f'Time vs {scol}',
                xaxis_title='Time',
                template='plotly_dark'
            )
            response_data['fig2'] = fig2.to_html(full_html=False, config={'scrollZoom': True})
        elif unival2 and plt_type2:
            # Iterate through the list
            fig2 = go.Figure()
            scols=[]
            for i, item in enumerate(unival2):
                # Split at the first '[' to get 'BARO1' and 'Press]'
                prefix, column = item.split('[')
                
                # Extract the last character (which is the number) and the rest of the prefix
                number = prefix[-1]  # '1'
                prefix = prefix[:-1]  # 'BARO'
                
                # Remove the closing bracket from the column name
                column = column.rstrip(']')  # 'Press'
                
                # Store them in variables
                fname = prefix
                colval = number
                col = column
                scols.append(col)
                print(f'{fname}+{colval}+{col}')
                
                # Load DataFrame
                df = pd.read_csv(f'output/{fname}.csv')
                
                # Determine filtering based on column existence and value
                if 'I' in df.columns and 'IMU' in df.columns:
                    if colval == '1':
                        flt_df = df[(df['I'] == 1) | (df['IMU'] == 1)]
                    elif colval == '0':
                        flt_df = df[(df['I'] == 0) | (df['IMU'] == 0)]
                    elif colval == '2':
                        flt_df = df[(df['I'] == 2) | (df['IMU'] == 2)]
                elif 'I' in df.columns:
                    if colval == '1':
                        flt_df = df[df['I'] == 1]
                    elif colval == '0':
                        flt_df = df[df['I'] == 0]
                    elif colval == '2':
                        flt_df = df[df['I'] == 2]
                elif 'IMU' in df.columns:
                    if colval == '1':
                        flt_df = df[df['IMU'] == 1]
                    elif colval == '0':
                        flt_df = df[df['IMU'] == 0]
                    elif colval == '2':
                        flt_df = df[df['IMU'] == 2]
                else:
                    flt_df = pd.DataFrame()  # Default to empty DataFrame if neither column exists

                df.set_index('TimeUS', inplace=True)
                
                if not flt_df.empty and col in flt_df.columns:
                    color = colors[i % len(colors)]
                    if plt_type2 == 'Scatter':
                        fig2.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='markers', marker=dict(color=color))
                    elif plt_type2 == 'Histogram':
                        fig2.add_histogram(x=df.index, y=flt_df[col].to_numpy(), name=f'{col} Histogram', marker_color=color)
                    elif plt_type2 == 'line':
                        fig2.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='lines', line=dict(color=color))
                else:
                    print(f"Data for {col} not available or empty.")
            print(scols)
            scol=' and '.join(scols)
            fig2.update_layout(
                    title=f'Time vs {scol}',
                    xaxis_title='Time',
                    yaxis_title='Value',
                    template='plotly_dark'
                )
            response_data['fig2'] = fig2.to_html(full_html=False, config={'scrollZoom': True})
        if response_data:
            return jsonify(response_data)

# -------------------------------------plot3---------------------------------       
        if selected_columns3 and plt_type3:
            fig3 = go.Figure()
            scols=[]
            for i, item in enumerate(selected_columns3):
                file_name, col_name = item.split('[')
                col_name = col_name.strip(']')
                scols.append(col_name)
                df = pd.read_csv(os.path.join(file_dir, file_name + ".csv"))
                df.set_index('TimeUS', inplace=True)
                color = colors[i % len(colors)]
                if plt_type3 == 'Scatter':
                    fig3.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color))
                elif plt_type3 == 'Histogram':
                    fig3.add_histogram(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                elif plt_type3 == 'line':
                    fig3.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color))
            scol=" and ".join(scols)
            fig3.update_layout(
                title=f'Time vs {scol}',
                xaxis_title='Time',
                template='plotly_dark'
            )
            response_data['fig3'] = fig3.to_html(full_html=False, config={'scrollZoom': True})
        elif unival3 and plt_type3:
            # Iterate through the list
            fig3 = go.Figure()
            scols=[]
            for i, item in enumerate(unival3):
                # Split at the first '[' to get 'BARO1' and 'Press]'
                prefix, column = item.split('[')
                
                # Extract the last character (which is the number) and the rest of the prefix
                number = prefix[-1]  # '1'
                prefix = prefix[:-1]  # 'BARO'
                
                # Remove the closing bracket from the column name
                column = column.rstrip(']')  # 'Press'
                
                # Store them in variables
                fname = prefix
                colval = number
                col = column
                scols.append(col)
                print(f'{fname}+{colval}+{col}')
                
                # Load DataFrame
                df = pd.read_csv(f'output/{fname}.csv')
                
                # Determine filtering based on column existence and value
                if 'I' in df.columns and 'IMU' in df.columns:
                    if colval == '1':
                        flt_df = df[(df['I'] == 1) | (df['IMU'] == 1)]
                    elif colval == '0':
                        flt_df = df[(df['I'] == 0) | (df['IMU'] == 0)]
                    elif colval == '2':
                        flt_df = df[(df['I'] == 2) | (df['IMU'] == 2)]
                elif 'I' in df.columns:
                    if colval == '1':
                        flt_df = df[df['I'] == 1]
                    elif colval == '0':
                        flt_df = df[df['I'] == 0]
                    elif colval == '2':
                        flt_df = df[df['I'] == 2]
                elif 'IMU' in df.columns:
                    if colval == '1':
                        flt_df = df[df['IMU'] == 1]
                    elif colval == '0':
                        flt_df = df[df['IMU'] == 0]
                    elif colval == '2':
                        flt_df = df[df['IMU'] == 2]
                else:
                    flt_df = pd.DataFrame()  # Default to empty DataFrame if neither column exists

                df.set_index('TimeUS', inplace=True)
                
                if not flt_df.empty and col in flt_df.columns:
                    color = colors[i % len(colors)]
                    if plt_type3 == 'Scatter':
                        fig3.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='markers', marker=dict(color=color))
                    elif plt_type3 == 'Histogram':
                        fig3.add_histogram(x=df.index, y=flt_df[col].to_numpy(), name=f'{col} Histogram', marker_color=color)
                    elif plt_type3 == 'line':
                        fig3.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='lines', line=dict(color=color))
                else:
                    print(f"Data for {col} not available or empty.")
            print(scols)
            scol=' and '.join(scols)
            fig3.update_layout(
                    title=f'Time vs {scol}',
                    xaxis_title='Time',
                    yaxis_title='Value',
                    template='plotly_dark'
                )
            response_data['fig3'] = fig3.to_html(full_html=False, config={'scrollZoom': True})
        if response_data:
            return jsonify(response_data)

# -------------------------------------plot4---------------------------------       
        if selected_columns4 and plt_type4:
            fig4 = go.Figure()
            scols=[]
            for i, item in enumerate(selected_columns4):
                file_name, col_name = item.split('[')
                col_name = col_name.strip(']')
                scols.append(col_name)
                df = pd.read_csv(os.path.join(file_dir, file_name + ".csv"))
                df.set_index('TimeUS', inplace=True)
                color = colors[i % len(colors)]
                if plt_type4 == 'Scatter':
                    fig4.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color))
                elif plt_type4 == 'Histogram':
                    fig4.add_histogram(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                elif plt_type4 == 'line':
                    fig4.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color))
            scol=" and ".join(scols)
            fig4.update_layout(
                title=f'Time vs {scol}',
                xaxis_title='Time',
                template='plotly_dark'
            )
            response_data['fig4'] = fig4.to_html(full_html=False, config={'scrollZoom': True})
        elif unival4 and plt_type4:
            # Iterate through the list
            fig4 = go.Figure()
            scols=[]
            for i, item in enumerate(unival4):
                # Split at the first '[' to get 'BARO1' and 'Press]'
                prefix, column = item.split('[')
                
                # Extract the last character (which is the number) and the rest of the prefix
                number = prefix[-1]  # '1'
                prefix = prefix[:-1]  # 'BARO'
                
                # Remove the closing bracket from the column name
                column = column.rstrip(']')  # 'Press'
                
                # Store them in variables
                fname = prefix
                colval = number
                col = column
                scols.append(col)
                print(f'{fname}+{colval}+{col}')
                
                # Load DataFrame
                df = pd.read_csv(f'output/{fname}.csv')
                
                # Determine filtering based on column existence and value
                if 'I' in df.columns and 'IMU' in df.columns:
                    if colval == '1':
                        flt_df = df[(df['I'] == 1) | (df['IMU'] == 1)]
                    elif colval == '0':
                        flt_df = df[(df['I'] == 0) | (df['IMU'] == 0)]
                    elif colval == '2':
                        flt_df = df[(df['I'] == 2) | (df['IMU'] == 2)]
                elif 'I' in df.columns:
                    if colval == '1':
                        flt_df = df[df['I'] == 1]
                    elif colval == '0':
                        flt_df = df[df['I'] == 0]
                    elif colval == '2':
                        flt_df = df[df['I'] == 2]
                elif 'IMU' in df.columns:
                    if colval == '1':
                        flt_df = df[df['IMU'] == 1]
                    elif colval == '0':
                        flt_df = df[df['IMU'] == 0]
                    elif colval == '2':
                        flt_df = df[df['IMU'] == 2]
                else:
                    flt_df = pd.DataFrame()  # Default to empty DataFrame if neither column exists

                df.set_index('TimeUS', inplace=True)
                
                if not flt_df.empty and col in flt_df.columns:
                    color = colors[i % len(colors)]
                    if plt_type4 == 'Scatter':
                        fig4.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='markers', marker=dict(color=color))
                    elif plt_type4 == 'Histogram':
                        fig4.add_histogram(x=df.index, y=flt_df[col].to_numpy(), name=f'{col} Histogram', marker_color=color)
                    elif plt_type4 == 'line':
                        fig4.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='lines', line=dict(color=color))
                else:
                    print(f"Data for {col} not available or empty.")
            print(scols)
            scol=' and '.join(scols)
            fig4.update_layout(
                    title=f'Time vs {scol}',
                    xaxis_title='Time',
                    yaxis_title='Value',
                    template='plotly_dark'
                )
            response_data['fig4'] = fig4.to_html(full_html=False, config={'scrollZoom': True})
        if response_data:
            return jsonify(response_data)

    # For GET requests or if no POST data is provided
    selected_file_columns = csv_columns.get(filename, []) if filename else []
    return render_template('graph.html', files=file_names,tbl=html_table, uv=uv, cl=csv_columns, selected_file_columns=selected_file_columns)

if __name__ == "__main__":
    app.run(debug=True)
