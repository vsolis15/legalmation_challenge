from db import create_tables
from db_methods import insert_file, get_file_by_id, get_files, get_file_by_name
from flask import Flask, request, jsonify, redirect, url_for, flash, render_template, Blueprint
import os
import xml.etree.ElementTree as ET
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'xml'}
vs_list = ['vs', 'vs.', 'v.']

# For Testing Purposes
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    create_tables()
    app.config.from_mapping(
        SECRET_KEY='super secret key',
        DATABASE=os.path.join(app.instance_path, 'web_app.sqlite'),
    )
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    return app

app = Flask(__name__)
app.config["DEBUG"] = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'

# Check to see if the uploaded file has the right extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Collects Plaintiff info
def find_plaintiffs(text_arr):
    plaintiffs_list = []
    add_plain = False
    start = len(text_arr) - 1
    #curr_line = text_arr[start]
    while ('COUNTY OF' not in text_arr[start] and start >= 0):
        curr_line = text_arr[start]
        if (add_plain):
            plaintiffs_list.insert(0, curr_line)
        if ('Plaintiff' in curr_line):
            add_plain = True
        start -= 1
    return plaintiffs_list

#Collects Defendant info
def find_defendants(text_arr):
    defendants_list = []
    start = len(text_arr) - 1
    while (not is_vs(text_arr[start]) and start >= 0):
        curr_line = text_arr[start]
        defendants_list.insert(0, curr_line)
        start -= 1
    return defendants_list

# Checks to see if we find some form of vs in the xml file
def is_vs(text):
    if text in vs_list:
        return True
    for vs in vs_list:
        if vs in text:
            return True
    return False 

# Put together Plaintiff or Defendant info into a string
def assemble_string(text_arr):
    my_string = ''
    for text in text_arr:
        my_string += text
    return my_string


# Renders file.html to upload a file and store relevant info
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file detected')
            return redirect(request.url)
        file = request.files['file']
        # check if it is an xml file
        allowed = allowed_file(file.filename)
        # check if the file is there
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        elif file and allowed:
            # secure the filename and check if the file is in the DB
            filename = secure_filename(file.filename)
            exist_file = get_file_by_name(filename)
            
            if (exist_file is not None):
                flash('File already exists')
                return redirect(request.url)
            
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Create an XML parser and iterate through the XML tree
            tree = ET.parse(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            root = tree.getroot()

            text_list = []
            plain_list = []
            def_list = []
            
            add_def = False
            for child in root.iter():
                desc = child.text
                if (desc is not None) and (desc != ''):
                    # Once a version of vs is hit double back and collect the plaintiff info
                    if (is_vs(desc)):
                        plain_list = find_plaintiffs(text_list)
                        add_def = True
                    # Once we find the plaintiff look for defendant info and collect it 
                    if (add_def and ('Defendant' in desc)):
                        def_list = find_defendants(text_list)
                        add_def = False
                    # Collect possibly relevant info
                    if (len(desc) > 2):
                        text_list.append(desc)
            
            # put together info and insert it into a table
            plaintiffs = assemble_string(plain_list)
            defendants = assemble_string(def_list)

            insert_file(filename, plaintiffs, defendants)

            # Redirect to view files in a table
            return redirect(url_for('files'))
        else:

            flash('Incorrect File Format')
            return redirect(request.url)

    return render_template('index.html')

# You can view files in a simple table format
@app.route('/files')
def files():
    files = get_files()
    #print(files)
    return render_template("files.html", rows = files)

# this api route can be hit to receive all files in a JSON format
@app.route('/api/files')
def return_files():
    files = get_files()
    return jsonify(files)

# this api route can be hit to receive a specific file in a JSON format by id
# you can look for ids by either going to /files or looking through all files @ /api/files
@app.route('/api/get_file/<id>')
def return_by_id(id):
    file = get_file_by_id(id)
    return jsonify(file)
 
if __name__ == "__main__":
    create_tables()
    app.run()
