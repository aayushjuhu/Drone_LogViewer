# importing the libraries
from flask import Flask, render_template,redirect,request
import pandas as pd
from bintocsv import convert_bin_to_csv
import plotly.graph_objects as go
import plotly.express as px
import random
import os

app = Flask(__name__) # Initializing flask app


# Defining Routes
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['fupload']
        print("file upload: ",f.filename)
        convert_bin_to_csv(f.filename, 'output')
        return redirect('/home')
    return redirect('/')

@app.route('/home', defaults={'filename': None})
@app.route('/view',methods=['GET','POST'])
@app.route('/view<filename>')
def view1(filename=None):
    file_dir = 'output'
    file_name = os.listdir(file_dir)
    file_name = [os.path.splitext(name)[0] for name in file_name]
    csv_columns = {}
    
    # Generate the dictionary of files and their columns
    for file in file_name:
        file_path = os.path.join(file_dir, file+".csv")
        df = pd.read_csv(file_path)
        csv_columns[file] = list(df.columns)
    
    graph_html=None
    c=0
  
    if request.method=="POST": 
        selected_columns = request.form.getlist('selected_col')
        cols=[]
        fig=go.Figure()
        # fig=px.scatter()
        colors = ['blue', 'red', 'green', 'purple']  # List of colors
        
        for i, item in enumerate (selected_columns):
            # Split the item into filename and column name
            file_name, col_name = item.split('[')
            col_name = col_name.strip(']')  # Remove the trailing ']'
            cols.append(col_name)
            df=pd.read_csv(file_dir+"/"+file_name+".csv")
            df.set_index('TimeUS',inplace=True)
            c = colors[i % len(colors)]
            # fig=px.scatter(df,x=df.index,y=df[col_name], color_discrete_sequence=[c])
            # df['SmoothedRoll'] = df['Roll'].rolling(window=10).mean()
            fig.add_scatter(x=df.index,y=df[col_name].to_numpy(), name=f'{col_name}',mode='lines', line=dict(color=c))

            # fig.add_trace(go.Scatter(x=df.index, y=df[col_name], name=f'{col_name}', line=dict(dash='dash', color=c)))

        #     # Update the layout
        fig.update_layout(
            # title="Time vs "+cols[0],
            # xaxis_title=cols[0],
            # yaxis_title=cols[1],
            template='plotly_dark'
        )
        graph_html = fig.to_html(full_html=False)
    if filename:
        # If a filename is provided, generate the HTML table for that file
        data = pd.read_csv(os.path.join(file_dir, filename+".csv"))
        tbl = data.to_html(index=False, classes='table table-striped table-bordered table-hover text-center')
        return render_template('view.html', files=file_name, table=tbl, cl=csv_columns,fig=graph_html)
    
    # If no filename is provided, just display the file list
    return render_template('view.html', files=file_name, cl=csv_columns,fig=graph_html)


if __name__=="__main__":
    app.run(debug=True)