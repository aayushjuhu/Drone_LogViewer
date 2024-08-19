# Importing the libraries

from flask import Flask, render_template, redirect, request
import pandas as pd
from bintocsv import convert_bin_to_csv
from separate_files import get_unique_values_from_files
import plotly.graph_objects as go
import os

app = Flask(__name__)  # Initializing flask app



# Defining Routes
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['fupload']
        print("file upload: ",f.filename)
        convert_bin_to_csv(f.filename, 'output')
        return redirect('/view')  # Redirect to the view page after uploading
    return redirect('/')

@app.route('/home', defaults={'filename': None})
@app.route('/view', methods=['GET', 'POST'])
@app.route('/view/<filename>', methods=['GET'])
def view1(filename=None):
    file_dir = 'output'
    file_names = [os.path.splitext(name)[0] for name in os.listdir(file_dir)]
    csv_columns = {}
    selected_file_columns=[]
    uv = get_unique_values_from_files()
    print(f"{uv}")

    
    # Generate the dictionary of files and their columns
    for file in file_names:
        file_path = os.path.join(file_dir, file + ".csv")
        df = pd.read_csv(file_path)
        csv_columns[file] = list(df.columns)

    graph_html = None
    
    if request.method == 'POST': 
        selected_columns1 = request.form.getlist('selected_col')
        unival1=request.form.getlist('selected_col1')
        plt_type1 = request.form.get('plt_type')
        selected_columns2 = request.form.getlist('selected_col')
        unival2=request.form.getlist('selected_col1')
        plt_type2 = request.form.get('plt_type')
        selected_columns3 = request.form.getlist('selected_col')
        unival3=request.form.getlist('selected_col1')
        plt_type3 = request.form.get('plt_type')
        selected_columns4 = request.form.getlist('selected_col')
        unival4=request.form.getlist('selected_col1')
        plt_type4 = request.form.get('plt_type')
        cols = []

        print(f'{selected_columns}')
        print(f'{unival}')
        
        colors = ['blue', 'red', 'green', 'purple']  # List of colors
        
        if selected_columns:
            fig = go.Figure()
            for i, item in enumerate(selected_columns):
                file_name, col_name = item.split('[')
                col_name = col_name.strip(']')
                cols.append(col_name)
                df = pd.read_csv(os.path.join(file_dir, file_name + ".csv"))
                df.set_index('TimeUS', inplace=True)
                color = colors[i % len(colors)]
                if plt_type == 'Scatter':
                    fig.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color))
                elif plt_type == 'Histogram':
                    fig.add_histogram(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                elif plt_type == 'line':
                    fig.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color))
            
            fig.update_layout(
                xaxis_title='Time',
                template='plotly_dark'
            )
            graph_html = fig.to_html(full_html=False,config = {'scrollZoom': True})
        
            # Handle data for the selected filename
            selected_file_columns = csv_columns.get(filename, []) if filename else []
            return render_template('graph.html', files=file_names, uv=uv, cl=csv_columns, selected_file_columns=selected_file_columns, fig=graph_html)
        elif unival:
            # Iterate through the list
            fig = go.Figure()
            scols=[]
            for i, item in enumerate(unival):
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
                    if plt_type == 'Scatter':
                        fig.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='markers', marker=dict(color=color))
                    elif plt_type == 'Histogram':
                        fig.add_histogram(x=df.index, y=flt_df[col].to_numpy(), name=f'{col} Histogram', marker_color=color)
                    elif plt_type == 'line':
                        fig.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='lines', line=dict(color=color))
                else:
                    print(f"Data for {col} not available or empty.")
            print(scols)
            scol=''.join(scols)
            fig.update_layout(
                    title=f'Time vs {scol}',
                    xaxis_title='Time',
                    yaxis_title='Value',
                    template='plotly_dark'
                )
            graph_html = fig.to_html(full_html=False, config = {'scrollZoom': True})
            return render_template('graph.html', files=file_names, uv=uv, cl=csv_columns, fig=graph_html,selected_file_columns=selected_file_columns)
  
    return render_template('graph.html', files=file_names, uv=uv, cl=csv_columns,fig=graph_html,selected_file_columns=selected_file_columns)


if __name__=="__main__":
    app.run(debug=True)