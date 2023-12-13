import webbrowser
import os
import sys
from threading import Timer

from flask import Flask, render_template, request, jsonify
import subprocess

# Get the path to the core module (core directory)
core_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core')
sys.path.append(core_dir_path)
import core

HOST_ADDRESS = "127.0.0.1"
PORT = 5000

# Replace with local instance of jquery if name/path is different
REL_LOCAL_JQUERY_SOURCE = "js/jquery-3.7.0.min.js"
LOCAL_JQUERY_SOURCE = f"static/{REL_LOCAL_JQUERY_SOURCE}"

WEB_JQUERY_SOURCE = "https://code.jquery.com/jquery-3.7.0.min.js"
WEB_JQUERY_SOURCE_CHECKSUM = "sha384-NXgwF8Kv9SSAr+jemKKcbvQsz+teULH/a5UNJvZc6kP47hZgl62M1vGnw6gHQhb1"
WEB_JQUERY_SOURCE_CROSSORIGIN = "anonymous"

MODELS_PATH = core.MODELS_DIR

TMP_SOURCE_FILE_SAVE_DIR = f"{core.SOURCE_FILE_SAVE_DIR}/_tmp"

app = Flask(__name__)

@app.before_request
def load_existing_models():
    # create parallel list here
    # user will choose a string entry from the list, and the same id will be used for it
    # e.g. choosing entry #2 will get the 2nd entry from the existing_models array
    app.existing_models = core.get_existing_models()

@app.route('/')
def index():
    
    # Determine if a local or remote JQuery script will be used
    # Assuming the directory structure has not been changed
    local_source = os.path.join(os.getcwd(), LOCAL_JQUERY_SOURCE)
    if os.path.exists(local_source):
        jquery_source = url_for('static', filename=REL_LOCAL_JQUERY_SOURCE)
        integrity = None
        crossorigin = None
    else:
        jquery_source = "https://code.jquery.com/jquery-3.7.0.min.js"
        integrity = "sha384-NXgwF8Kv9SSAr+jemKKcbvQsz+teULH/a5UNJvZc6kP47hZgl62M1vGnw6gHQhb1"
        crossorigin = "anonymous"
    
    return render_template("index.html", \
        models = app.existing_models, \
        jquery_source = jquery_source, \
        integrity = integrity, \
        crossorigin = crossorigin, \
    )

# def open_browser():
    # webbrowser.open_new(f"http://localhost:{PORT}")

@app.route('/generate_sentence', methods=['POST'])
def generate_sentence():
    if request.method == 'POST':
        chosen_model = app.existing_models[int(request.form.get("chosen_model_id"))]
        word_generate_num = int(request.form.get("word_generate_num")) 
        token_count_per_entry = int(request.form.get("token_count_per_entry"))

        core.check_create_model(chosen_model)
        generated_sentence = core.generate_sentence(chosen_model, word_generate_num, token_count_per_entry)
        return generated_sentence

@app.route('/create_model', methods=['POST'])
def create_model():
    if request.method == 'POST':
        tmp_source_file_path = __save_user_file_contents(request.files['user_source_file'])
        token_length = int(request.form.get("token_length"))

        model_name, model_path, source_file_path, create_new_list_item = core.check_add_model(tmp_source_file_path, token_length)

        if create_new_list_item:
            new_model = core.generate_model(model_name, model_path, source_file_path, token_length)
            app.existing_models.append(new_model)

            # TODO: return checksum as value?
            return jsonify(model_name = new_model.get_name(), model_unique_value = os.path.basename(source_file_path)[0])

# private funcs

def __save_user_file_contents(user_source_file):
    tmp_source_file_path = os.path.join(TMP_SOURCE_FILE_SAVE_DIR, user_source_file.filename)
    core.try_create_folder(TMP_SOURCE_FILE_SAVE_DIR)
    user_source_file.save(tmp_source_file_path)

    return tmp_source_file_path

if __name__ == "__main__":
    # Timer(1, open_browser).start()
    app.run(host=HOST_ADDRESS, port=PORT, debug=True)