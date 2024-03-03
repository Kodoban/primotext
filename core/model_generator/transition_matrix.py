from string import punctuation

SPECIAL_END_TOKEN = "~~}EOF"

class TransitionMatrix:
    def __init__(self, text=None, csv_reader=None):
        # Either text or csv_reader is None
        
        # List of tokens passed -> Create the transition matrix after going through the text file
        if csv_reader is None:

            # Step 1. Create a dictionary of all words in the text file
            stats = {} # { token str : { token_after str : count int } }

            previous_token = None
            main_token = None
            for token in text:
                # The token contains an alphanumeric token and optionally punctuation marks at the beginning or the end of the token
                # The function checks whether the token starts or ends with punctuation marks. 
                # If so, it splits the string so that the alphanumeric token and the punctuation marks (if they exist)
                ## punc_left, main_token, punc_right = self.__add_new_token(stats, token, previous_token)

                # for token="@!hello?>" => punc_left = ["@", "!"], main_token = "hello", punc_right = ["?", ">"]
                punc_left, main_token, punc_right = self.__check_for_edge_punctuation([], token, [])
                
                # left punctuation marks
                for left_punc_mark in punc_left:
                    previous_token = self.__add_token_to_stats(stats, left_punc_mark, previous_token)

                # main token
                previous_token = self.__add_token_to_stats(stats, main_token, previous_token)

                # right punctuation marks
                for right_punc_mark in punc_right:
                    previous_token = self.__add_token_to_stats(stats, right_punc_mark, previous_token)

                # Set the right-most token (last punctuation mark if it exists, else the token itself) as the last token checked
                previous_token = main_token if not punc_right else punc_right[-1]

            """ 
            Check if last token examined (aka previous_token) can be succeeded
            Assuming a Markov chain with 1-word tokens of the sentence "a text of text M", the 'M' token does not point to any other tokens.
            Practically, if 'M' is selected to be printed, the generated sentence will have to end after it.
            However, the probability of the tokens (and their sum as well) that can succeed 'M' is 0.
            To avoid raising an error (this would defeat the purpose and ease of simply dropping a text file and generating sentences from it)
                or pointing to the first token (Source: https://www.cs.princeton.edu/courses/archive/fall14/cos126/assignments/markov.html, would create inaccuracies though),
                the solution will be to add a special end token just for this case, which will stop the text generation if it is selected. 
            """
            if not stats[previous_token]:
                stats[previous_token][SPECIAL_END_TOKEN] = 1
                """
                Add the special end token to the matrix so it becomes Markovian. 
                Since the sum of its probabilities must equal 1, even if the text generation will stop after it is selected,
                    the "hack" is to arbitrarily have it pointing to any token with a probability of 1,
                    therefore it points to itself in a closed loop to not "interfere" with the actual tokens. 
                """
                stats[SPECIAL_END_TOKEN] = {SPECIAL_END_TOKEN : 1}

            # Sort tokens alphabetically 
            self.sorted_tokens = sorted(stats.keys())

            # Step 2. Create the transition matrix
            print("Creating the transition matrix (this might take some time)...")
            # Calculate probabilities
            self.matrix = {}
            # all_sums_one = True

            for token in self.sorted_tokens:
                self.matrix[token] = {} # { token str : { next_token str : probability float } }

                # Calculate the amount of times the token appears in the text. 
                # This will be used to calculate the probability of each succeeding token to come after it
                token_total_count = sum(stats[token].values())

                for candidate_next_token in self.sorted_tokens:

                    # If candidate_next_token appears in the succeeding dictionary of token,
                    #   calculate the probability of the latter succeeding token (candidate_next_token count / token_total_count)  
                    # If candidate_next_token does not appear in that dictionary, return 0 to designate that there is no probability it will succeed token
                    # stats[token].get(candidate_next_token, 0) returns the value in the dictionary if candidate_next_token exists, otherwise 0
                    self.matrix[token][candidate_next_token] = \
                        stats[token].get(candidate_next_token, 0) / token_total_count

        # csv_reader passed -> Import the tokens and probabilities from the csv file
        elif text is None:
            
            # Ignore header, sorted_tokens can also be generated from the first column
            next(csv_reader, None)

            self.sorted_tokens = []
            self.array_matrix = []
            for row in csv_reader:
                # First element is the token itself
                self.sorted_tokens.append(row.pop(0))
                # The rest of the row is the probabilities as strings, so they are converted to floats before being inserted
                self.array_matrix.append([float(x) for x in row])

    def get_sorted_tokens(self):
        # array_tokens = []
        # for token in self.sorted_tokens:
        #     array_tokens.append(token.get_token())

        return self.sorted_tokens

    def get_matrix(self):

        if hasattr(self, 'array_matrix'): # transition matrix was imported -> array matrix exists
            pass
        else: # transition matrix was created as a dict -> convert to 2D array for easier printing
            self.array_matrix = [[0 for col in range(len(self.sorted_tokens))] for row in range(len(self.sorted_tokens))]

            for j, main_token in enumerate(self.matrix.keys()):
                for i, candidate_next_token in enumerate(self.matrix.keys()):
                    self.array_matrix[i][j] = self.matrix[main_token][candidate_next_token]

        return self.array_matrix

    #private

    def __check_for_edge_punctuation(self, punc_left, token, punc_right):

        """
        The original token as passed
        E.g. for token="@!hello?>", raw_token = "@!hello?>" on first pass
        On following recursions, raw_token will have the following values:
            "!hello?>" => punc_left = ["@"]
            "hello?>" => punc_left = ["@", "!"]
            "hello?" => punc_right = [">"]
            "hello" => punc_right = ["?", ">"]
        At the end of the last recursion, neither if statement is true, so raw_token contains just a token without punctuation marks (e.g. "hello")
        The return values for the initial call will be:
            punc_left = ["@", "!"]
            raw_token = "hello"
            punc_right = ["?", ">"]
        """
        raw_token = token

        # Checks if there are punctuation marks to the left of the main token
        # For token="@!hello?>", punc_left = ["@", "!"]
        if token and token[0] in punctuation:
            punc_left.append(token[0])
            punc_left, raw_token, punc_right = self.__check_for_edge_punctuation(punc_left, token[1:], punc_right)

        # Checks if there are punctuation marks to the right of the main token
        # The punctation marks are checked in reverse order, but are placed in the list in the order they appear in
        # For token="@!hello?>", punc_right = ["?", ">"] (> was checked first, then ?)
        elif token and token[-1] in punctuation:
            punc_right.insert(0, token[-1])
            punc_left, raw_token, punc_right = self.__check_for_edge_punctuation(punc_left, token[:-1], punc_right)

        return punc_left, raw_token, punc_right

    def __add_token_to_stats(self, stats, new_token, previous_token):

        # Adds new_token to the stats dictionary if it doesn't exist already. Afterwards, the dictionary of succeeding words is created.
        # If new_token already exists, this command has no effect on the stats dictionary
        stats[new_token] = stats.setdefault(new_token, {})

        # Sets new_token as a succeeding token in previous_token's dictionary
        # If new_token does not exist in that dictionary, it is added to it and its count is initialized to 0. 
        # Afterwards, its count is incremented by 1
        # Only the latter takes place if new_token exists in that dictionary
        #
        # Note: previous_token is None only when checking the first token of the file, so this block cannot be executed
        if not previous_token is None:
            stats[previous_token][new_token] = stats[previous_token].get(new_token, 0) + 1

        return new_token