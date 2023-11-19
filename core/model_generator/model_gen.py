from .transition_matrix import TransitionMatrix

import re
import csv 

import time #remove 

class ModelGenerator:

    def __init__(self, model, csv_path=None):
        if csv_path is None:
            # Create transition matrix from source file
            contents = self.__read_file(model.get_source_path())
            clean_text = self.__clean_up_text(contents, model.get_token_length())

            transition_matrix = TransitionMatrix(text=clean_text)
            model.set_transition_matrix(transition_matrix)

            self.__print_to_csv(transition_matrix.get_matrix(), transition_matrix.get_sorted_tokens(), model.get_path(), model.get_token_length())

        else:
            # Import transition matrix
            with open(csv_path) as csv_model:
                csv_reader = csv.reader(csv_model, delimiter=',')
                model.set_transition_matrix(TransitionMatrix(csv_reader=csv_reader))


    # private functions

    def __read_file(self, file):
        with open(file, "r") as f:
            contents = f.read()

        return contents

    def __clean_up_text(self, contents, token_length):  # Check for variable token length:
        match token_length:
            case 1:
                contents = re.sub(r'\s+', ' ', contents) # remove all "large" whitespaces
                contents = contents.lower()  # convert all text to lowercase
                contents = re.sub(r'(\S)--(\S)', r'\1 -- \2', contents) # add space before and after of double dashes, e.g. "and--oh" becomes "and -- oh"
                split_contents = contents.split(" ")  # split text into words
                return [s for s in split_contents if s != ''] # remove any remaining whitespace characters

    # def print_words_to_file(stats_matrix, sorted_words, dir_name, word_count_per_entry):
        
    #     try_create_folder(dir_name)

    #     # DEBUG: Create a file with all detected words in the order they appear in
    #     print("\rSaving all detected words (first instance only) in order of appearance...", end="")
    #     with open(os.path.join(dir_name, "serialized_reading_order_" + str(word_count_per_entry) + "_word_states_DEBUG.txt"), "w") as f:
    #         # Write each element of the list to a new line in the file
    #         for word in stats_matrix._matrix.keys():
    #             f.write(word + "\n")
    #     time.sleep(0.8)
    #     print("\rSaving all detected words (first instance only) in order of appearance... Saved to file", \
    #         os.path.join(dir_name, "serialized_reading_order_" + str(word_count_per_entry) + "_word_states_DEBUG.txt"),'\n')

    #     # Create a file with all detected words in alphabetical order
    #     print("\rSaving all detected words in alphabetical order...", end="")
    #     with open(os.path.join(dir_name, "serialized_alphabetical_order_ " + str(word_count_per_entry) + "_word_states.txt"), "w") as f:
    #         # Write each element of the list to a new line in the file
    #         for word in sorted_words:
    #             f.write(word + "\n")
    #     time.sleep(0.8)
    #     print("\rSaving all detected words in alphabetical order... Saved to file", \
    #         os.path.join(dir_name,"serialized_alphabetical_order_" + str(word_count_per_entry) + "_word_states.txt"),'\n')

    def __print_to_csv(self, array_matrix, sorted_tokens, csv_path, token_count_per_entry):

        # try_create_folder(filename)

        # Add the word to the first column (for CSV)
        csv_ready_matrix = [[sorted_tokens[i]] + array_matrix[i] for i in range(len(sorted_tokens))]

        #  csv_ready_matrix = []
        # st_tokens = []
        # for i in range(len(sorted_tokens)):
        #     sorted_tokens[i].get_token()]

        # Print the matrix to a .csv file
        print("\rSaving the transition matrix...", end="")
        time.sleep(0.5)

        #change path name to reflect words per token
        with open(csv_path, "w", newline="") as csvtable:
        #with open(os.path.join(dir_name, "transition_matrix_" + str(word_count_per_entry) + "_word_states.csv"), "w", newline="") as csvtable:
            csvwriter = csv.writer(csvtable)
            # Header
            csvwriter.writerow([' '] + [sorted_tokens[i] for i in range(len(sorted_tokens))])
            
            # Write the data row by row
            for row in csv_ready_matrix:
                csvwriter.writerow(row)

            time.sleep(0.8)
            print('\rSaving the transition matrix... Saved to file', \
                #os.path.join(dir_name,"transition_matrix_"+ str(word_count_per_entry) + "_word_states.csv"),'\n')
                #("transition_matrix_"+ str(token_count_per_entry) + "_word_states.csv"),'\n')
                csv_path, '\n')

            # Sum up the probabilities for each word (column), and print whether they all add up to 1
            # To avoid round-off errors, the sums are rounded to 8 decimal digits
            print("Calculating probabilities... ", end="")
            probabilities = [round(sum(col),8) for col in zip(*(array_matrix))]
            prob_not_1 = [i for i in range(len(probabilities)) if probabilities[i] != 1]
            tokens_prob_not_1 = [sorted_tokens[prob_not_1[i]] for i in range(len(prob_not_1))]

            # If the sum of each column is equal to 1, then a set containing all sums must be {1}, with only one element
            # If there are more elements, there is a sum that does not equal 1, and therefore the matrix is not Markovian
            if len(set(probabilities))==1:
                print("All probabilities (columns) individually equal 1\n") 
            else: 
                print("Not all probabilities equal 1\n")
                print(tokens_prob_not_1)