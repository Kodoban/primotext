from string import punctuation

class TransitionMatrix:
    def __init__(self, text=None, csv_reader=None):
        if csv_reader is None:
            # List of tokens passed
            self.__create_transition_matrix(text)
        elif text is None:
            # csv_reader passed
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

    def __create_transition_matrix(self, text):

        stats = self.__create_stats_dict(text) # { token str : { token_after str : count int } }

        print("Creating the transition matrix (this might take some time)...")
        # Calculate probabilities
        self.matrix = {}
        all_sums_one = True

        for token in self.sorted_tokens:
            self.matrix[token] = {} # { token str : { next_token str : probability float } }

            # Calculate the amount of times the token appears in the text. 
            # This will be used to calculate the probability of each succeeding token to come after it
            token_total_count = sum(stats[token].values())

            for candidate_next_token in self.sorted_tokens:

                # BUG: If last token in text only appear at the end of the text, token_total_count will be 0 as no other token can follow it
                # Solutions to implement: 
                # If user generates certain amount of words (current behavior) -> Make last token point to the first token
                #   Source: https://www.cs.princeton.edu/courses/archive/fall14/cos126/assignments/markov.html 
                # If user does not specify amount of words to generate -> Add special "end" character 
                # Middle ground: Generate text up to certain amount of words
                #   E.g. generate up to 1000 words, but if "end" character is selected, stop generating 

                # If candidate_next_token appears in the succeeding dictionary of token,
                #   calculate the probability of the latter succeeding token (candidate_next_token count / token_total_count)  
                # If candidate_next_token does not appear in that dictionary, return 0 to designate that there is no probability it will succeed token
                # stats[token].get(candidate_next_token, 0) returns the value in the dictionary if candidate_next_token exists, otherwise 0
                self.matrix[token][candidate_next_token] = \
                    stats[token].get(candidate_next_token, 0) / token_total_count

    def __create_stats_dict(self, text):
        
        # TODO: Add description here
        stats = {} # { token str : { token_after str : count int } }

        previous_token = None
        main_token = None
        for token in text:
            # The token contains an alphanumeric token and optionally punctuation marks at the beginning or the end of the token
            # The function checks whether the token starts or ends with punctuation marks. 
            # If so, it splits the string so that the alphanumeric token and the punctuation marks (if they exist) separated
            punc_left, main_token, punc_right = self.__add_new_token(stats, token, previous_token)

            # Set the right-most token (last punctuation mark to the left, if it exists, else the token itself) as the last token checked
            previous_token = main_token if not punc_right else punc_right[-1]

        # Sort tokens alphabetically 
        self.sorted_tokens = sorted(stats.keys())

        return stats

    # punc_left, main_token, punc_right first get the string versions of the tokens
    # After that, they are gradually replaced by Token instances
    def __add_new_token(self, stats, new_token, previous_token):
        punc_left, main_token, punc_right = self.__check_for_edge_punctuation([], new_token, [])
        # for new_token="@!hello?>" => punc_left = ["@", "!"], new_token = "hello", punc_right = ["?", ">"]

        # left punctuation marks
        # 
        for left_punc_mark in punc_left:
            previous_token = self.__add_token_to_stats(stats, left_punc_mark, previous_token)

        # main token
        previous_token = self.__add_token_to_stats(stats, main_token, previous_token)

        # right punctuation marks
        for right_punc_mark in punc_right:
            previous_token = self.__add_token_to_stats(stats, right_punc_mark, previous_token)

        return punc_left, main_token, punc_right 

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
            punc_right = ["?", ">"]"""
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