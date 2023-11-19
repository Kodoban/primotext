import sys
import os
import sqlite3
import hashlib

from pathlib import Path
from model_generator import Model
from text_generator import TextGenerator

PROGRAM_ROOT_DIR = str(Path(__file__).resolve().parent.resolve().parent)
MODELS_DIR = PROGRAM_ROOT_DIR + '/_models'
SOURCE_FILE_SAVE_DIR = PROGRAM_ROOT_DIR + '/_source_files'

def get_existing_models():
    # Create database (or get database if it already exists)
    con, cur = __check_create_database()

    cur.execute("SELECT model_name, model_path, source_file_path, token_length FROM models")
    queried_models = dbCur.fetchall()
    existing_models = []
    for model_info in queried_models:
        model_name, model_path, source_file, token_length = model_info
        models.append(generate_model(model_name, model_path, source_file, token_length))

    return con, cur, existing_models

def __check_create_database():
    __try_create_folder(MODELS_DIR)
    con = sqlite3.connect(f"{MODELS_DIR}/text_models.db")
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS models (
                    "model_name"	    TEXT NOT NULL,
                    "model_path"	    TEXT NOT NULL,
                    "source_file_path"	TEXT NOT NULL,
                    "token_length"	    INT NOT NULL,
                    "sha256checksum"	TEXT NOT NULL UNIQUE,
                    PRIMARY KEY("token_length","sha256checksum")
                    );
    """)
    con.commit()

    return con, cur

def __try_create_folder(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print(f'Created directory {dir_name}\n')
        return True
    else:
        print(f'{dir_name} already exists')
        return False

def generate_model(model_name, model_path, file_path, token_length):
    return Model(model_name, model_path, file_path, token_length)

##########

def check_add_model(con, cur, source_file_path, token_length):
    model_name, model_path, checksum = __check_model_already_exists(cur, source_file_path, token_length)

    # Model for file has not been generated yet
    if model_name is None:
        model_name = os.path.splitext(os.path.basename(source_file_path))[0] 
        model_path = MODELS_DIR + '/' + model_name + '.csv'

        cur.execute("INSERT INTO models VALUES (?,?,?,?,?)", (model_name, model_path, source_file_path, token_length, checksum,))
        con.commit()

        return model_name, model_path, True
    else:
        print(f"Model {model_name} already exists (Token length: {token_length})")
        return model_name, model_path, False

def __check_model_already_exists(dbCur, file, token_length):
    checksum = __calc_file_sha256_checksum(file)
    dbCur.execute("SELECT model_name, model_path FROM models WHERE token_length = ? AND sha256checksum = ?", (token_length, checksum,))
    entry = dbCur.fetchone()

    # Case 1: Model exists in DB
    if entry:
        model_name, model_path = entry
        # Case 1.1: Model exists in DB and the transition matrix (in .csv form) is present in the model_path directory
        #   Action: Return model_name and model_path
        if __try_create_folder(model_path):
            return model_name, model_path, checksum

        # Case 1.2: Model exists in DB and so does the model_path directory, but the transition matrix (in .csv) is not present in the directory
        #   Action: Treat like model does not exist and create it from scratch (INSERT INTO command will be ignored by the DB)
        else:
            return None, None, checksum

    # Case 2: Model does not exist in DB and neither does the folder
    #   Action: Create the folder and the model afterwards
    # self.try_create_folder(model_path)
    return None, None, checksum

def __calc_file_sha256_checksum(file):
    with open(file, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")
        f.close()
        return digest.hexdigest()

##########

def check_create_model(model):
    model_path = model.get_path()
    source_path = model.get_source_path()

    # Model .csv does not exist, create it (provided the source file exists)
    if not os.path.exists(model_path) and os.path.exists(source_path):
        model.create_transition_matrix()
    # Model .csv exists, import the matrix
    elif model_path:
        model.import_transition_matrix()

#######

def generate_sentence(model, word_generate_num, token_count_per_entry):
    tgen = TextGenerator(model.get_transition_matrix(), \
                model.get_sorted_tokens(), word_generate_num, token_count_per_entry)

    return tgen.get_sentence()