# Import Libraries

from flask import Flask, render_template, redirect, request, jsonify, session
import pandas as pd
import numpy as np
from bintocsv import convert_bin_to_csv
from separate_files import get_unique_values_from_files
import plotly.graph_objects as go
from datetime import datetime
import uuid
import os

app = Flask(__name__)  # Initializing flask app
app.secret_key = 'your_secret_key_here'
uid=uuid.uuid4()


@app.route('/clear_session')
def clear_session():
    session.pop('col_name1')
    session.pop('col_name2')
    session.pop('col_name3')
    session.pop('col_name4')
    session.pop('file_name1')
    session.pop('file_name2')
    session.pop('file_name3')
    session.pop('file_name4')

@app.route('/update_stats', methods=['POST'])
def update_stats():
    data = request.get_json()
    zoom_range = data.get('range')
    graph_index = data.get('graph_index')
    
    uid = session.get('user_id')
    
    # List of file names and column names associated with each graph
    file_names = [
        session.get('file_name1'),
        session.get('file_name2'),
        session.get('file_name3'),
        session.get('file_name4')
    ]
    
    col_names = [
        session.get('col_name1'),
        session.get('col_name2'),
        session.get('col_name3'),
        session.get('col_name4')
    ]
    
    # Ensure the graph index is valid
    if graph_index < 0 or graph_index >= len(file_names):
        return jsonify({"error": "Invalid graph index"}), 400
    
    file_name = file_names[graph_index]
    col_name = col_names[graph_index]
    
    if not file_name or not col_name:
        return jsonify({"error": "File or column not specified"}), 400
    
    # Read the appropriate CSV file
    df = pd.read_csv(f'output/{uid}/csv/{file_name}.csv')
    df['TimeUS'] = pd.to_datetime(df['TimeUS'])
    
    start = None
    end = None

    # Filter the data based on zoom range if provided
    if zoom_range:
        x_min = zoom_range.get('x_min')
        x_max = zoom_range.get('x_max')

        if x_min and x_max:
            start = pd.to_datetime(x_min)
            end = pd.to_datetime(x_max)
            zoomed_data = df[(df['TimeUS'] >= start) & (df['TimeUS'] <= end)]
        else:
            zoomed_data = df
    else:
        zoomed_data = df

    # Calculate statistics for the zoomed data
    if not zoomed_data.empty:
        stats = {
            "graph_id": f"graph{graph_index+1}",
            "mean": round(zoomed_data[col_name].mean(),2),
            "median": round(zoomed_data[col_name].median(),2),
            "starting_value": round(zoomed_data[col_name].iloc[0],2),
            "last_value": round(zoomed_data[col_name].iloc[-1],2),
            "std_dev": round(zoomed_data[col_name].std(),2),
            "variance": round(zoomed_data[col_name].var(),2),
        }
    else:
        stats = {
            "mean": None,
            "median": None,
            "starting_value": None,
            "last_value": None,
            "std_dev": None,
            "variance": None,
        }
    
    return jsonify(stats)


# Defining Routes
@app.route("/")  # Landing page
def home():
    return render_template('index.html')

@app.route("/upload", methods=['POST']) # uploading the file
def upload_file():
    if request.method == 'POST':  # To check whether request is of type post
        # Create a unique session directory for the user
        user_id = session.get('user_id')
        
        if not user_id:
            user_id = str(uid)
            session['user_id'] = user_id

        user_output_dir = os.path.join('output', user_id)
        os.makedirs(user_output_dir, exist_ok=True)
        print(user_id)

        # Save the uploaded file
        f = request.files['fupload']
        user_output_dir=str(user_output_dir)
        filename=str(f.filename)
        file_path = os.path.join(user_output_dir, filename)
        session['file_path'] = file_path
        session.permanent = True  # Make the session permanent to respect the expiration time
        f.save(file_path)   
        
        # Convert file to CSV
        convert_bin_to_csv(file_path, os.path.join(user_output_dir, 'csv'))

        # return redirect('/view')  # Redirect to the view page after uploading
        
        return jsonify({'message': 'File successfully uploaded'}), 200
    return redirect('/')

# @app.route('/home', defaults={'filename': None})
@app.route('/view', methods=['GET','POST']) # log viewer and analysis page
@app.route('/view<filename>', methods=['GET'])
def view1(filename=None):
    is_single_row=0
    vals={}
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/')  # Redirect to home if no session

    file_dir = os.path.join('output', user_id)
    csv_dir = os.path.join(file_dir, 'csv')

    # Ensure the directory exists
    if not os.path.exists(csv_dir):
        return "No files available"

    file_names = [os.path.splitext(name)[0] for name in os.listdir(csv_dir) if name.endswith('.csv')]  # Get CSV filenames
    csv_columns = {}
    selected_file_columns = []
    html_table = None

    if filename:
        filename = str(filename)
        file_path = os.path.join(csv_dir, f'{filename}.csv')
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)  # Read the selected file
            
            is_single_row = len(df) == 1
            html_table = df.to_html(index=False, classes='table table-bordered mt-2')  # Convert dataframe to HTML table

    uv = get_unique_values_from_files(user_id)  # Get the unique values from column (used when there are multiple sensors)

    # Generate the dictionary of files and their columns
    for file in file_names:
        file_path = os.path.join(csv_dir, f'{file}.csv')
        df = pd.read_csv(file_path)
        csv_columns[file] = list(df.columns)


# Getting the user input and plotting
    if request.method == 'POST':
        selected_columns1 = request.form.getlist('selected_col1')
        print(f's1cols: {len(selected_columns1)}')
        selected_columns2 = request.form.getlist('selected_col2')
        # print(f'{selected_columns2}')
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

        # print(f'{selected_columns2} {plt_type2}')

        colors = ['blue', 'red', 'green', 'purple']  # List of colors
        response_data = {}

        # ---------------------------Plot 1------------------------------------------------------------------------------
        
        if selected_columns1 and plt_type1:
            fig1 = go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
            scols=[]
            res_stats=None
            for i, item in enumerate(selected_columns1):
                file_name, col_name = item.split('[')
                col_name = col_name.strip(']')
                scols.append(col_name)
                session['col_name1']=col_name
                session['file_name1']=file_name
                
                df = pd.read_csv(os.path.join(csv_dir, file_name + ".csv"))
                df.set_index('TimeUS', inplace=True)
                color = colors[i % len(colors)] 
                vals={'mean_value' : round(df[col_name].mean(),2),
                'median_value' : round(df[col_name].median(),2),
                'starting_value' : round(df[col_name].iloc[0],2),
                'last_value' : round(df[col_name].iloc[-1],2),
                'std_dev' : round(df[col_name].std(),2),
                'variance' : round(df[col_name].var(),2)}
                
                if plt_type1 == 'Scatter':
                    fig1.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color,size=2))
                elif plt_type1 == 'Histogram':
                    fig1.add_histogram(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                elif plt_type1 == 'line':
                    fig1.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color,width=1.2))
            scol=" and ".join(scols)
            # dt=(df.index[0].split(' ')[0])
            fig1.update_layout(
                xaxis=dict(title=f'Time\n(Date:)',
                                        tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                yaxis=dict(title=f'{scol}',
                                            showgrid=True,
                                            zeroline=True,),
                                        title=f'Time vs {scol}',
                                        template='plotly_dark'
            )
            fig1=fig1.to_html(full_html=False, config={'scrollZoom': True})
            response_data={'fig1':fig1, 'selected_columns1':selected_columns1,'unival1':unival1, 'stats':vals}
            if response_data:
                return jsonify(response_data)
            
        elif unival1 and plt_type1:
            # Iterate through the list
            fig1 = go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
            scols=[]
            file_name=None
            col_name=None
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
                session['col_name1']=col
                session['file_name1']=fname
                print(f'{scols}')
                f1=session.get('file_name1')
                c1=session.get('col_name1')
                print(f'{f1}------------------{c1}')
                print(f'{fname}+{colval}+{col}')
                
                # Load DataFrame
                df = pd.read_csv(f'output/{user_id}/csv/{fname}.csv')
                
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
                vals={'mean_value' : round(df[col_name].mean(),2),
                'median_value' : round(df[col_name].median(),2),
                'starting_value' : round(df[col_name].iloc[0],2),
                'last_value' : round(df[col_name].iloc[-1],2),
                'std_dev' : round(df[col_name].std(),2),
                'variance' : round(df[col_name].var(),2)}
                
                if not flt_df.empty and col in flt_df.columns:
                    color = colors[i % len(colors)]
                    if plt_type1 == 'Scatter':
                        fig1.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='markers', marker=dict(color=color, size=2))
                    elif plt_type1 == 'Histogram':
                        fig1.add_histogram(x=df.index, y=flt_df[col].to_numpy(), name=f'{col} Histogram', marker_color=color)
                    elif plt_type1 == 'line':
                        fig1.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='lines', line=dict(color=color,width=1.2))
                else:
                    print(f"Data for {col} not available or empty.")
            print(scols)
            if len(scols) > 1:
                scol=' and '.join(scols)
            else:
                scol=''.join(scols)
            dt=(df.index[0].split(' ')[0])
            fig1.update_layout(
                    xaxis=dict(title=f'Time\n(Date:{dt})',
                                        tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                yaxis=dict(title=f'{scol}',
                                            showgrid=True,
                                            zeroline=True,),
                                        title=f'Time vs {scol}',
                                        template='plotly_dark'
                )
            fig1=fig1.to_html(full_html=False, config={'scrollZoom': True})
            response_data={'fig1':fig1, 'selected_columns1':selected_columns1,'unival1':unival1,'stats':vals}
            if response_data:
                return jsonify(response_data)
        
        
        # ---------------------------Plot2------------------------------------------------------------------------------
        if selected_columns2 and plt_type2:
            fig2 = go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
            scols=[]
            for i, item in enumerate(selected_columns2):
                file_name, col_name = item.split('[')
                col_name = col_name.strip(']')
                scols.append(col_name)
                session['col_name2']=col_name
                session['file_name2']=file_name
                df = pd.read_csv(os.path.join(csv_dir, file_name + ".csv"))
                df.set_index('TimeUS', inplace=True)
                color = colors[i % len(colors)]
                vals={'mean_value' : round(df[col_name].mean(),2),
                'median_value' : round(df[col_name].median(),2),
                'starting_value' : round(df[col_name].iloc[0],2),
                'last_value' : round(df[col_name].iloc[-1],2),
                'std_dev' : round(df[col_name].std(),2),
                'variance' : round(df[col_name].var(),2)}
                
                if plt_type2 == 'Scatter':
                    fig2.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color,size=2))
                elif plt_type2 == 'Histogram':
                    fig2.add_histogram(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                elif plt_type2 == 'line':
                    fig2.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color,width=1.2))
            scol=" and ".join(scols)
            # dt=(df.index[0].split(' ')[0])
            fig2.update_layout(
                xaxis=dict(title=f'Time\n(Date:)',
                                        tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                yaxis=dict(title=f'{scol}',
                                            showgrid=True,
                                            zeroline=True,),
                                        title=f'Time vs {scol}',
                                        template='plotly_dark'
            )
            fig2=fig2.to_html(full_html=False, config={'scrollZoom': True})
            response_data={'fig2':fig2, 'selected_columns2':selected_columns2, 'unival2':unival2, 'stats':vals}
            if response_data:
                return jsonify(response_data)

        elif unival2 and plt_type2:
            # Iterate through the list
            fig2 = go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
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
                df = pd.read_csv(f'output/{user_id}/csv/{fname}.csv')
                
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
                vals={'mean_value' : round(df[col_name].mean(),2),
                'median_value' : round(df[col_name].median(),2),
                'starting_value' : round(df[col_name].iloc[0],2),
                'last_value' : round(df[col_name].iloc[-1],2),
                'std_dev' : round(df[col_name].std(),2),
                'variance' : round(df[col_name].var(),2)}
                
                if not flt_df.empty and col in flt_df.columns:
                    color = colors[i % len(colors)]
                    if plt_type2 == 'Scatter':
                        fig2.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='markers', marker=dict(color=color, size=2))
                    elif plt_type2 == 'Histogram':
                        fig2.add_histogram(x=df.index, y=flt_df[col].to_numpy(), name=f'{col} Histogram', marker_color=color)
                    elif plt_type2 == 'line':
                        fig2.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='lines', line=dict(color=color,width=1.2))
                else:
                    print(f"Data for {col} not available or empty.")
            print(scols)
            scol=' and '.join(scols)
            dt=(df.index[0].split(' ')[0])
            fig2.update_layout(
                    xaxis=dict(title=f'Time\n(Date:{dt})',
                                        tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                yaxis=dict(title=f'{scol}',
                                            showgrid=True,
                                            zeroline=True,),
                                        title=f'Time vs {scol}',
                                        template='plotly_dark'
                )
            fig2=fig2.to_html(full_html=False, config={'scrollZoom': True})
            response_data={'fig2':fig2, 'selected_columns2':selected_columns2, 'unival2':unival2, 'stats':vals}
            if response_data:
                return jsonify(response_data)

# -------------------------------------plot3---------------------------------       
        if selected_columns3 and plt_type3:
            fig3 = go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
            scols=[]
            for i, item in enumerate(selected_columns3):
                file_name, col_name = item.split('[')
                col_name = col_name.strip(']')
                session['col_name3']=col_name
                session['file_name3']=file_name
                scols.append(col_name)
                df = pd.read_csv(os.path.join(csv_dir, file_name + ".csv"))
                df.set_index('TimeUS', inplace=True)
                color = colors[i % len(colors)]
                vals={'mean_value' : round(df[col_name].mean(),2),
                'median_value' : round(df[col_name].median(),2),
                'starting_value' : round(df[col_name].iloc[0],2),
                'last_value' : round(df[col_name].iloc[-1],2),
                'std_dev' : round(df[col_name].std(),2),
                'variance' : round(df[col_name].var(),2)}

                if plt_type3 == 'Scatter':
                    fig3.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color, size=2))
                elif plt_type3 == 'Histogram':
                    fig3.add_histogram(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                elif plt_type3 == 'line':
                    fig3.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color, width=1.2))
            scol=" and ".join(scols)
            dt=(df.index[0].split(' ')[0])
            fig3.update_layout(
                xaxis=dict(title=f'Time\n(Date:{dt})',
                                        tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                yaxis=dict(title=f'{scol}',
                                            showgrid=True,
                                            zeroline=True,),
                                        title=f'Time vs {scol}',
                                        template='plotly_dark'
            )
            fig3=fig3.to_html(full_html=False, config={'scrollZoom': True})
            response_data={'fig3':fig3, 'selected_columns3':selected_columns3, 'unival3':unival3, 'stats':vals}
            if response_data:
                return jsonify(response_data)

        elif unival3 and plt_type3:
            # Iterate through the list
            fig3 = go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
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
                df = pd.read_csv(f'output/{user_id}/csv/{fname}.csv')
                
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
                vals={'mean_value' : round(df[col_name].mean(),2),
                'median_value' : round(df[col_name].median(),2),
                'starting_value' : round(df[col_name].iloc[0],2),
                'last_value' : round(df[col_name].iloc[-1],2),
                'std_dev' : round(df[col_name].std(),2),
                'variance' : round(df[col_name].var(),2)}
                
                if not flt_df.empty and col in flt_df.columns:
                    color = colors[i % len(colors)]
                    if plt_type3 == 'Scatter':
                        fig3.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='markers', marker=dict(color=color, size=2))
                    elif plt_type3 == 'Histogram':
                        fig3.add_histogram(x=df.index, y=flt_df[col].to_numpy(), name=f'{col} Histogram', marker_color=color)
                    elif plt_type3 == 'line':
                        fig3.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='lines', line=dict(color=color, width=1.2))
                else:
                    print(f"Data for {col} not available or empty.")
            print(scols)
            scol=' and '.join(scols)
            dt=(df.index[0].split(' ')[0])
            fig3.update_layout(
                    xaxis=dict(title=f'Time\n(Date:{dt})',
                                        tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                yaxis=dict(title=f'{scol}',
                                            showgrid=True,
                                            zeroline=True,),
                                        title=f'Time vs {scol}',
                                        template='plotly_dark'
                )
            fig3=fig3.to_html(full_html=False, config={'scrollZoom': True})
            response_data={'fig3':fig3, 'selected_columns3':selected_columns3, 'unival3':unival3,'stats':vals}
            if response_data:
                return jsonify(response_data)
            
# -------------------------------------plot4---------------------------------       
        if selected_columns4 and plt_type4:
            fig4 = go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
            scols=[]
            for i, item in enumerate(selected_columns4):
                file_name, col_name = item.split('[')
                col_name = col_name.strip(']')
                session['col_name4']=col_name
                session['file_name4']=file_name
                scols.append(col_name)
                df = pd.read_csv(os.path.join(csv_dir, file_name + ".csv"))
                df.set_index('TimeUS', inplace=True)
                color = colors[i % len(colors)]
                vals={'mean_value' : round(df[col_name].mean(),2),
                'median_value' : round(df[col_name].median(),2),
                'starting_value' : round(df[col_name].iloc[0],2),
                'last_value' : round(df[col_name].iloc[-1],2),
                'std_dev' : round(df[col_name].std(),2),
                'variance' : round(df[col_name].var(),2)}
                
                if plt_type4 == 'Scatter':
                    fig4.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color, size=2))
                elif plt_type4 == 'Histogram':
                    fig4.add_histogram(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                elif plt_type4 == 'line':
                    fig4.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color, width=1.2))
            scol=" and ".join(scols)
            dt=(df.index[0].split(' ')[0])
            fig4.update_layout(
                xaxis=dict(title=f'Time\n(Date:{dt})',
                                        tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                yaxis=dict(title=f'{scol}',
                                            showgrid=True,
                                            zeroline=True,),
                                        title=f'Time vs {scol}',
                                        template='plotly_dark'
            )
            fig4=fig4.to_html(full_html=False, config={'scrollZoom': True})
            response_data={'fig4':fig4, 'selected_columns4':selected_columns4, 'unival4':unival4, 'stats':vals}
            if response_data:
                return jsonify(response_data)

        elif unival4 and plt_type4:
            # Iterate through the list
            fig4 = go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
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
                df = pd.read_csv(f'output/{user_id}/csv/{fname}.csv')
                
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
                vals={'mean_value' : round(df[col_name].mean(),2),
                'median_value' : round(df[col_name].median(),2),
                'starting_value' : round(df[col_name].iloc[0],2),
                'last_value' : round(df[col_name].iloc[-1],2),
                'std_dev' : round(df[col_name].std(),2),
                'variance' : round(df[col_name].var(),2)}
                
                if not flt_df.empty and col in flt_df.columns:
                    color = colors[i % len(colors)]
                    if plt_type4 == 'Scatter':
                        fig4.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='markers', marker=dict(color=color, size=2))
                    elif plt_type4 == 'Histogram':
                        fig4.add_histogram(x=df.index, y=flt_df[col].to_numpy(), name=f'{col} Histogram', marker_color=color)
                    elif plt_type4 == 'line':
                        fig4.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='lines', line=dict(color=color, width=1.2))
                else:
                    print(f"Data for {col} not available or empty.")
            print(scols)
            scol=' and '.join(scols)
            dt=(df.index[0].split(' ')[0])
            fig4.update_layout(
                    xaxis=dict(title=f'Time\n(Date:{dt})',
                                        tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                yaxis=dict(title=f'{scol}',
                                            showgrid=True,
                                            zeroline=True,),
                                        title=f'Time vs {scol}',
                                        template='plotly_dark'
                )
            fig4=fig4.to_html(full_html=False, config={'scrollZoom': True})
            response_data={'fig4':fig4, 'selected_columns4':selected_columns4, 'unival4':unival4,'stats':vals   }
            if response_data:
                return jsonify(response_data)

    # For GET requests or if no POST data is provided
    selected_file_columns = csv_columns.get(filename, []) if filename else []
    # print(f'{vals}')
    return render_template('graph.html', files=file_names,tbl=html_table, uv=uv,is_single_row=is_single_row, cl=csv_columns, selected_file_columns=selected_file_columns, vals=vals)


@app.route('/droneatt')
def droneatt():
    # user_id=session.get("user_id")
    # return jsonify(user_id)
    user_id=session.get("user_id")
    df=pd.read_csv(f'output/{user_id}/csv/ATT.csv')
    roll = df['Roll'].tolist()
    pitch = df['Pitch'].tolist()
    yaw = df['Yaw'].tolist()
    time = df['TimeUS'].tolist()  # Time is for the x-axis
    return render_template('droneatt.html', roll=roll, pitch=pitch, yaw=yaw, time=time)

# --------------------------------residual------------------------------------------------------------------------------------------------------------
@app.route('/residual', methods=['GET','POST']) # log viewer and analysis page
def residual():
    vals={}
    user_id = session.get('user_id')
    file_dir = os.path.join('output', user_id)
    csv_dir = os.path.join(file_dir, 'csv')
    file_names = [os.path.splitext(name)[0] for name in os.listdir(csv_dir) if name.endswith('.csv')]  # Get CSV filenames
    csv_columns = {}
    selected_file_columns = []
    uv = get_unique_values_from_files(user_id)  # Get the unique values from column (used when there are multiple sensors)

    # Generate the dictionary of files and their columns
    for file in file_names:
        file_path = os.path.join(csv_dir, f'{file}.csv')
        df = pd.read_csv(file_path)
        csv_columns[file] = list(df.columns)


# Getting the user input and plotting
    if request.method == 'POST':
        selected_columns1 = request.form.getlist('selected_col1')
        print(f's1cols: {len(selected_columns1)}')
        unival1 = request.form.getlist('unv1')
        plt_type1 = request.form.get('plt_type1')
        # res_fig, resi_fig=None
        colors = ['blue', 'red', 'green', 'purple']  # List of colors
        response_data = {}

        # ---------------------------Plot 1------------------------------------------------------------------------------
        
        if selected_columns1 and plt_type1:
            if len(selected_columns1)==2:
                res_fig = go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
                resi_fig=go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
                mod_fig=go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
                scols=[]
                res_stats=None
                
                for i, item in enumerate(selected_columns1):
                    file_name, col_name = item.split('[')
                    col_name = col_name.strip(']')
                    scols.append(col_name)
                    # session['col_name1']=col_name
                    # session['file_name1']=file_name
                    df = pd.read_csv(os.path.join(csv_dir, file_name + ".csv"))
                    df.set_index('TimeUS', inplace=True)
                    color = colors[i % len(colors)] 
                    ogvals={'mean_value' : round(df[col_name].mean(),2),
                'median_value' : round(df[col_name].median(),2),
                'starting_value' : round(df[col_name].iloc[0],2),
                'last_value' : round(df[col_name].iloc[-1],2),
                'std_dev' : round(df[col_name].std(),2),
                'variance' : round(df[col_name].var(),2)}
                    
                    
                    if plt_type1 == 'Scatter':
                        res_fig.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color,size=2))
                    elif plt_type1 == 'Histogram':
                        res_fig.add_histogram(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                    elif plt_type1 == 'line':
                        res_fig.add_scatter(x=df.index, y=df[col_name].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color,width=1.2))
                        
                scol=" and ".join(scols)
                dt=(df.index[0].split(' ')[0])
                res_fig.update_layout(
                    xaxis=dict(title=f'Time\n(Date:{dt})',
                                            tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                            showgrid=True,
                                            zeroline=True,
                                            ),
                                    yaxis=dict(title=f'{scol}',
                                                showgrid=True,
                                                zeroline=True,),
                                            title=f'Time vs {scol}',
                                            template='plotly_dark'
                )
                df['res']=(df[scols[0]]-df[scols[1]])
                resvals={'mean_value' : round(df['res'].mean(),2),
                    'median_value' : round(df['res'].median(),2),
                    'starting_value' : round(df['res'].iloc[0],2),
                    'last_value' : round(df['res'].iloc[-1],2),
                    'std_dev' : round(df['res'].std(),2),
                    'variance' : round(df['res'].var(),2)}
                
                df['mod_df']=df['res'].abs()
                mod_dfvals={'mean_value' : round(df['mod_df'].mean(),2),
                    'median_value' : round(df['mod_df'].median(),2),
                    'starting_value' : round(df['mod_df'].iloc[0],2),
                    'last_value' : round(df['mod_df'].iloc[-1],2),
                    'std_dev' : round(df['mod_df'].std(),2),
                    'variance' : round(df['mod_df'].var(),2)}
                # print(f'{vals}')

                if plt_type1 == 'Scatter':
                    resi_fig.add_scatter(x=df.index, y=df['res'].to_numpy(), name=f'{col_name}', mode='markers', marker=dict(color=color,size=2))
                    mod_fig.add_scatter(x=df.index, y=df['mod_df'].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color='blue',width=1.2))
                elif plt_type1 == 'Histogram':
                    resi_fig.add_histogram(x=df.index, y=df['res'].to_numpy(), name=f'{col_name} Histogram', marker_color=color)
                    mod_fig.add_histogram(x=df.index, y=df['mod_df'].to_numpy(), name=f'{col_name} Histogram', marker_color='blue')
                elif plt_type1 == 'line':
                    resi_fig.add_scatter(x=df.index, y=df['res'].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color=color,width=1.2))
                    mod_fig.add_scatter(x=df.index, y=df['mod_df'].to_numpy(), name=f'{col_name}', mode='lines', line=dict(color='blue',width=1.2))
                
                mod_fig.update_layout(
                    xaxis=dict(title=f'Time\n(Date:{dt})',
                                            # tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                            showgrid=True,
                                            zeroline=True,
                                            ),
                                    yaxis=dict(title=f'Residual of {scol}',
                                                showgrid=True,
                                                zeroline=True,),    
                                            title=f'Time vs Mod_Residual of {scol}',
                                            template='plotly_dark'
                )
                resi_fig.update_layout(
                    xaxis=dict(title=f'Time\n(Date:{dt})',
                                            # tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                            showgrid=True,
                                            zeroline=True,
                                            ),
                                    yaxis=dict(title=f'Residual of {scol}',
                                                showgrid=True,
                                                zeroline=True,),
                                            title=f'Time vs Residual of {scol}',
                                            template='plotly_dark'
                )
                
                res_fig=res_fig.to_html(full_html=False, config={'scrollZoom': True})
                mod_fig=mod_fig.to_html(full_html=False, config={'scrollZoom': True})
                resi_fig=resi_fig.to_html(full_html=False, config={'scrollZoom': True})
                
                response_data={'res_fig':res_fig,'resi_fig':resi_fig,'mod_fig':mod_fig, 'selected_columns1':selected_columns1,'unival1':unival1, 'ogstats':ogvals, 'resstats':resvals, 'mod_dfstats':mod_dfvals}
                if response_data:
                    return jsonify(response_data)  
        


        elif unival1 and plt_type1:
            # Iterate through the list
            res_fig = go.Figure(layout=go.Layout(margin=dict(l=40, r=20, t=40, b=20)))
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
                df = pd.read_csv(f'output/{user_id}/csv/{fname}.csv')
                
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
                vals={'mean_value' : round(df[col_name].mean(),2),
                'median_value' : round(df[col_name].median(),2),
                'starting_value' : round(df[col_name].iloc[0],2),
                'last_value' : round(df[col_name].iloc[-1],2),
                'std_dev' : round(df[col_name].std(),2),
                'variance' : round(df[col_name].var(),2)}
                
                if not flt_df.empty and col in flt_df.columns:
                    color = colors[i % len(colors)]
                    if plt_type1 == 'Scatter':
                        res_fig.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='markers', marker=dict(color=color, size=2))
                    elif plt_type1 == 'Histogram':
                        res_fig.add_histogram(x=df.index, y=flt_df[col].to_numpy(), name=f'{col} Histogram', marker_color=color)
                    elif plt_type1 == 'line':
                        res_fig.add_scatter(x=df.index, y=flt_df[col].to_numpy(), name=f'{col}', mode='lines', line=dict(color=color,width=1.2))
                else:
                    print(f"Data for {col} not available or empty.")
            print(scols)
            if len(scols) > 1:
                scol=' and '.join(scols)
            else:
                scol=''.join(scols)
            dt=(df.index[0].split(' ')[0])
            res_fig.update_layout(
                    xaxis=dict(title=f'Time\n(Date:{dt})',
                                        tickformat='%H:%M:%S',  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                yaxis=dict(title=f'{scol}',
                                            showgrid=True,
                                            zeroline=True,),
                                        title=f'Time vs {scol}',
                                        template='plotly_dark'
                )
            res_fig=res_fig.to_html(full_html=False, config={'scrollZoom': True})
            response_data={'res_fig':res_fig, 'selected_columns1':selected_columns1,'unival1':unival1,'stats':vals}
            if response_data:
                return jsonify(response_data)

    # For GET requests or if no POST data is provided
    # selected_file_columns = csv_columns.get(filename, []) if filename else []
    # print(f'{vals}')
    return render_template('residual.html', files=file_names,selected_file_columns=selected_file_columns, uv=uv, cl=csv_columns, vals=vals)   #selected_file_columns=selected_file_columns

@app.route('/dronepath')
def fp():
    user_id=session.get('user_id')
    df = pd.read_csv(f'output/{user_id}/csv/GPS.csv')
    # df.set_index('TimeUS', inplace=True)
    df_curr = pd.read_csv(f'output/{user_id}/csv/BAT.csv')
    df_rpy = pd.read_csv(f'output/{user_id}/csv/ATT.csv')
    df_baro=pd.read_csv(f'output/{user_id}/csv/BARO.csv')
    df_baro0 = df_baro[df_baro['I'] == 0]['Alt'].reset_index(drop=True)
    df_baro1 = df_baro[df_baro['I'] == 1]['Alt'].reset_index(drop=True)
    df_baro0t=df_baro[df_baro['I'] == 0]['TimeUS'].reset_index(drop=True)
    df_baro1t=df_baro[df_baro['I'] == 1]['TimeUS'].reset_index(drop=True)
    telemetry_data = pd.read_csv(f'output/{user_id}/csv/MODE.csv')


    # ---------------------------------------------------------------------------flightmodes--------------------------------------------------------------------------

    last_gps_timestamp=df['TimeUS'].iloc[-1]
    durations=[]

    for i in range(len(telemetry_data)-1):
        start_time=telemetry_data['TimeUS'].iloc[i]
        end_time=telemetry_data['TimeUS'].iloc[i+1]
        durations.append(end_time-start_time)
    
    last_mode_start_time=telemetry_data['TimeUS'].iloc[-1]
    last_mode_duration = last_gps_timestamp - last_mode_start_time
    durations.append(last_mode_duration)
    telemetry_data['Duration'] = durations
    telemetry_data['DurationSec'] = telemetry_data['Duration']

    mode_mapping = {
        0: "STABILIZE",
        2: "ALT_HOLD",  
        4: "AUTO",
        5: "LOITER",
        6: "RTL"
    }
    telemetry_data['ModeName'] = telemetry_data['Mode'].map(mode_mapping)

    # Convert TimeUS from microseconds to seconds for easier interpretation
    # telemetry_data['TimeSec'] = telemetry_data['TimeUS'] / 1_000_000

    # Define unique colors for each mode
    color_map = {
        "STABILIZE": "rgba(255, 99, 71, 0.6)",   # Red
        "AUTO": "rgba(255, 215, 0, 0.6)",        # Gold
        "LOITER": "rgba(255, 165, 0, 0.6)",    # Sky Blue
        "RTL": "rgba(50, 205, 50, 0.6)",
        "ALT_HOLD": "rgba(255, 255, 0, 0.6)"          # Green
    }

            
            

    # ---------------------------------------------att_fig------------------------------------------------------------------

    att_fig = go.Figure(layout=go.Layout(margin=dict(l=60, t=20), height=200))
    att_fig.add_scatter(x=df['TimeUS'], y=df['Alt'].to_numpy(), name='Alt', mode='lines', line=dict(color='red', width=1.2))

    start_time = 0

    for index, row in telemetry_data.iterrows():
        mode_name=row['ModeName']
        duration=row['DurationSec']
        end_time=start_time+duration

        if mode_name in color_map:
            att_fig.add_shape(
            type="rect",
            x0=start_time, x1=end_time,
            y0=df['Alt'].min(), y1=df['Alt'].max(),  # Adjust y-range as needed for your data
            fillcolor=color_map[mode_name],
            opacity=0.7,  # Increase opacity for better visibility
            line=dict(width=0),
            layer="below"
        )

            # att_fig.add_annotation(
            # x=(start_time + end_time)+5,  # Place text in the center of the rectangle
            # y=10,  # Vertical position (adjust as needed)
            # text=mode_name,
            # showarrow=False,
            # font=dict(size=10, color=color_map[mode], weight="bold"),
            # textangle=90
        # )
        start_time = end_time

    # Add invisible traces for each mode to include in the legend
    for mode, color in color_map.items():
        att_fig.add_trace(
            go.Scatter(
                x=[None], y=[None],
                mode='markers',
                marker=dict(size=10, color=color),
                name=mode
            )
        )

    att_fig.update_layout(
        xaxis=dict(title="Time (s)", showgrid=True, zeroline=True),
        yaxis=dict(title="Altitude (m)", showgrid=True, zeroline=True),
        template='simple_white'
    )

    att_fig = att_fig.to_json()


    # ---------------------------------------------agl_fig------------------------------------------------------------------

    agl_fig=go.Figure(layout=go.Layout(margin=dict(l=60,t=20), height=220))
    agl_fig.add_scatter(x=df_baro0t.to_numpy(), y=df_baro0.to_numpy(), name='Baro0', mode='lines', line=dict(color='red',width=1.2))
    agl_fig.add_scatter(x=df_baro1t.to_numpy(), y=df_baro1.to_numpy(), name='Baro1', mode='lines', line=dict(color='orange',width=1.2))
    
    agl_fig.update_layout(xaxis=dict(title="Time (s)",  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,range=[0, df['TimeUS'].max()]
                                        ),
                                        yaxis=dict(title="Agl (m)",showgrid=True,
                                      ),showlegend=True,
                                        template='simple_white')

    agl_fig=agl_fig.to_json()

     # ---------------------------------------------curr_fig------------------------------------------------------------------

    curr_fig=go.Figure(layout=go.Layout(margin=dict(l=60,t=20), height=220))
    curr_fig.add_scatter(x=df_curr['TimeUS'], y=df_curr['Curr'], name='Current', mode='lines', line=dict(color='red',width=1.2))
    curr_fig.update_layout(xaxis=dict(title="Time (s)",  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                        yaxis=dict(title="Current (A)",showgrid=True,
                                      ),
                                        template='simple_white')

    curr_fig=curr_fig.to_json()

     # ---------------------------------------------rpy_fig------------------------------------------------------------------

    rpy_fig=go.Figure(layout=go.Layout(margin=dict(l=60,t=20), height=220))
    rpy_fig.add_scatter(x=df_rpy['TimeUS'], y=df_rpy['Roll'], name='Roll', mode='lines', line=dict(color='red',width=1.2))
    rpy_fig.add_scatter(x=df_rpy['TimeUS'], y=df_rpy['Pitch'], name='Pitch', mode='lines', line=dict(color='blue',width=1.2))
    rpy_fig.add_scatter(x=df_rpy['TimeUS'], y=df_rpy['Yaw'], name='Yaw', mode='lines', line=dict(color='orange',width=1.2))
    rpy_fig.update_layout(xaxis=dict(title="Time (s)",  # Display time in HH:mm:ss format
                                        showgrid=True,
                                        zeroline=True,
                                        ),
                                        yaxis=dict(title="Roll,Pitch and Yaw (Degree)",showgrid=True,
                                      ),showlegend=True,
                                        template='simple_white')

    rpy_fig=rpy_fig.to_json()
    return render_template('flightpath.html', att_fig=att_fig, agl_fig=agl_fig, curr_fig=curr_fig, rpy_fig=rpy_fig)


@app.route('/get_flight_data')
def get_flight_data():
    user_id=session.get('user_id')
    df = pd.read_csv(f'output/{user_id}/csv/GPS.csv')
    selected_columns = df[['Lat', 'Lng', 'Alt','TimeUS']]
    flight_data = selected_columns.to_dict(orient='records')
    df_curr = pd.read_csv(f'output/{user_id}/csv/BAT.csv')
    df_rpy = pd.read_csv(f'output/{user_id}/csv/ATT.csv')
    df_baro=pd.read_csv(f'output/{user_id}/csv/BARO.csv')

    # Select only the columns for latitude, longitude, and altitude
    # selected_columns['Curr']=df_curr['Curr']
    # selected_columns['Roll']=df_rpy['Roll']
    # selected_columns['Pitch']=df_rpy['Pitch']
    # selected_columns['Yaw']=df_rpy['Yaw']

    # Filter barometer data by sensor index (0 and 1)
    # df_baro0 = df_baro[df_baro['I'] == 0]['Alt'].reset_index(drop=True)
    # df_baro1 = df_baro[df_baro['I'] == 1]['Alt'].reset_index(drop=True)

    # Add baro0 and baro1 as new columns to selected_columns
    # selected_columns['baro0'] = df_baro0
    # selected_columns['baro1'] = df_baro1

    # Convert the data to a list of dictionaries (latitude, longitude, altitude)

    # Return the flight data as JSON
    return jsonify(flight_data)

@app.route("/logout")
def logout():
    user_id=session.get("user_id")
    if user_id:
        upop=session.pop('user_id', None)
        spop=session.pop('file_path', None)
        # print(f'{upop}-{spop}')
        return redirect('/')
    return "error"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(3000), debug=True)