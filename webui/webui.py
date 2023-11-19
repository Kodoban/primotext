import webbrowser
import os
import sys
from threading import Timer

from flask import Flask, render_template, request
import subprocess

# Get the path to the core module (core directory)
core_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core')
sys.path.append(core_dir_path)
import core

HOST_ADDRESS = "127.0.0.1"
PORT = 5000

# Replace with local instance of jquery if name/path is different
REL_LOCAL_JQUERY_SOURCE = "js/jquery-3.7.0.min.js"
LOCAL_JQUERY_SOURCE = "static/" + REL_LOCAL_JQUERY_SOURCE

WEB_JQUERY_SOURCE = "https://code.jquery.com/jquery-3.7.0.min.js"
WEB_JQUERY_SOURCE_CHECKSUM = "sha384-NXgwF8Kv9SSAr+jemKKcbvQsz+teULH/a5UNJvZc6kP47hZgl62M1vGnw6gHQhb1"
WEB_JQUERY_SOURCE_CROSSORIGIN = "anonymous"

MODELS_PATH = core.MODELS_DIR

app = Flask(__name__)

@app.before_request
def load_existing_models():
    # create parallel list here
    # user will choose a string entry from the list, and the same id will be used for it
    # e.g. choosing entry #2 will get the 2nd entry from the existing_models array
    app.dbCon, app.dbCur, app.existing_models = core.get_existing_models()

@app.route('/')
def index():
    #return "Hello World"

    jquery_source, integrity, crossorigin = __determine_jquery_source()
    
    return render_template("index.html", \
        models=[model.get_name() for model in app.existing_models], \
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
    if request_method == 'POST':
        file_path = request.form.get("file_path")
        token_length = request.form.get("token_length")

        model_name, model_path, create_new_list_item = core.check_add_model(app.dbCon, app.dbCur, file_path, token_length)

        if create_new_list_item:
            new_model = core.generate_model(model_name, model_path, file_path, token_length)
            app.existing_models.append(new_model)
            app.existing_models_string.append(new_model.get_name())

            # TODO: return checksum as value?
            return new_model.get_name()

# private funcs

def __determine_jquery_source():
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

    return jquery_source, integrity, crossorigin

if __name__ == "__main__":
    # Timer(1, open_browser).start()
    app.run(host=HOST_ADDRESS, port=PORT, debug=True)