import sys
import os
import sqlite3
import hashlib
import shutil

from pathlib import Path
from model_generator import Model
from text_generator import TextGenerator

PROGRAM_ROOT_DIR = str(Path(__file__).resolve().parent.resolve().parent)
MODELS_DIR = PROGRAM_ROOT_DIR + '/_models'
SOURCE_FILE_SAVE_DIR = PROGRAM_ROOT_DIR + '/_source_files'

MODELS_DB_PATH = PROGRAM_ROOT_DIR + "/text_models.db"

def get_existing_models():
    # TODO: Warn about models in DB that are missing their .csv transition matrices (Action: Delete model from DB)
    #       or are missing their source file (Action: Show warning sign or place in different category? E.g. allow only importing the model 
    #       (Maybe for models that have just the .csv, also grey out tokens per entry etc?)
    #       (Extra feature: Add option to add source file manually if checksum matches with database? Other fields too later on)

    # Try to create models and source file folders
    try_create_folder(MODELS_DIR)
    try_create_folder(SOURCE_FILE_SAVE_DIR)

    # Connect to database 
    con, cur = __connect_to_database()

    # Create model table if it does not already exist
    cur.execute("""CREATE TABLE IF NOT EXISTS models (
                    "model_name"	    TEXT NOT NULL,
                    "model_path"	    TEXT NOT NULL UNIQUE,
                    "source_file_path"	TEXT NOT NULL,
                    "token_length"	    INT NOT NULL,
                    "sha256checksum"	TEXT NOT NULL UNIQUE,
                    PRIMARY KEY("token_length","sha256checksum")
                    );
    """)
    con.commit()

    # Get key info from existing models in the table
    cur.execute("SELECT model_name, model_path, source_file_path, token_length FROM models")
    queried_models = cur.fetchall()
    con.close()

    existing_models = []
    for model_info in queried_models:
        model_name, model_path, source_file_path, token_length = model_info
        existing_models.append(generate_model(model_name, model_path, source_file_path, token_length))

    return existing_models

def try_create_folder(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
        print(f'Created directory {dir_name}\n')
        return True
    else:
        print(f'{dir_name} already exists')
        return False

def __connect_to_database():
    con = sqlite3.connect(f"{MODELS_DB_PATH}")
    cur = con.cursor()

    return con, cur

def generate_model(model_name, model_path, source_file_path, token_length):
    return Model(model_name, model_path, source_file_path, token_length)

##########
def check_add_model(source_file_tmp_path, token_length):

# def check_add_model(con, cur, source_file_tmp_path, token_length):
    model_name, model_path, source_file_path, checksum = __check_model_already_exists(source_file_tmp_path, token_length)

    # Model for source file has not been generated yet (or the .csv file containing the transition matrix for the model does not exist anymore)
    if model_name is None:
        
        # If source file's name is "test.txt", model_name = "test", user_source_file_ext = ".txt"
        model_name, user_source_file_ext = os.path.splitext(os.path.basename(source_file_tmp_path))
        
        # model_path follows the following template: {model name}__{first 8 digits of checksum}_t{token length}.csv
        # So a model with the name "test" and token_length = 2, will become "test_abc12345_t2.csv"
        # The checksum is used to differentiate models in case they share the same base name AND have the same token length (e.g. test.txt and test.py)
        # When using the same file as the base, the token length must be different for the models to be considered different
        model_path = f"{MODELS_DIR}/{model_name}__{checksum[:8]}_t{token_length}.csv"

        # source_file_path follows the following template: {model name}__{first 8 digits of checksum}{source file extension}
        # So a model with the filename "test.txt" will be saved in that directory as "test_abc12345.txt"
        source_file_path = f"{SOURCE_FILE_SAVE_DIR}/{model_name}__{checksum[:8]}{user_source_file_ext}"

        # Try to copy the source file from the temporary directory it has been saved in by the script/program that imported this module
        # TODO: Handle exceptions properly
        try:
            shutil.copy(source_file_tmp_path, source_file_path)
            print("Source file copied successfully.")

        # Throw exception if there are permission issues
        # TODO: Manually save the file contents to source_file_path if copying is not possible?
        except PermissionError:
            print("Permission denied.")
        
        # Other errors
        except:
            print("Error while copying source file.")

        con, cur = __connect_to_database()
        cur.execute("INSERT OR REPLACE INTO models VALUES (?,?,?,?,?)", (model_name, model_path, source_file_path, token_length, checksum,))
        con.commit()
        con.close()

        return model_name, model_path, source_file_path, True
    else:
        print(f"Model {model_name} already exists (Token length: {token_length})")
        return model_name, model_path, False

def __check_model_already_exists(file, token_length):
    # Declare the returned value so that there is only one return statement
    model_name = None
    model_path = None
    source_file_path = None
    checksum = None

    con, cur = __connect_to_database()
    checksum = __calc_file_sha256_checksum(file)
    cur.execute("SELECT model_name, model_path, source_file_path FROM models WHERE token_length = ? AND sha256checksum = ?", (token_length, checksum,))
    entry = cur.fetchone()

    # Case 1: Model exists in DB (at least in name)
    # TODO: Check for rare cases (e.g. models folder gets deleted while program is running?)
    if entry:
        model_name, model_path, source_file_path = entry
        # Case 1.1: The transition matrix (in .csv form) is present in the model_path directory
        #   Action: Return model_name and model_path (checksum is irrelevant in this case?)

        # Case 1.2: The transition matrix (in .csv) is not present in the directory
        #   Action: Treat like model does not exist and create it from scratch 
        #   NOTE for this case: The INSERT INTO query will update the DB entry. This is the intended behavior, 
        #       as the source file's name may have changed but not the contents (which would affect the checksum),
        #       so the DB should register the new name  
        if not os.path.exists(model_path):
            model_name = None
            model_path = None
            source_file_path = None

    con.close()
    # Case 1.1: return "test.txt", "test__abc12345_t2.csv", "test__abc12345.txt","abc123454rwef...."
    # Case 1.2: return None, None, "abc123454rwef...."
    return model_name, model_path, source_file_path, checksum

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