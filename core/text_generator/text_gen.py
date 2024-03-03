import random 
import time 

class TextGenerator:
    #CLI init
    def __init__(self, transition_matrix, sorted_tokens, token_count_per_entry):
        generate_more=True

        while generate_more:
            num = int(input("Enter the amount of words you would like to be generated: "))
            # Generate sentences
            self.__form_sentence(transition_matrix, sorted_tokens, num, token_count_per_entry)
            #self.print_sentence(self.sentence)
            #generate_more = (input("Generate more text? (y/n): ")).lower() == "y"

    # GUI init
    def __init__(self, transition_matrix, sorted_tokens, word_num, token_count_per_entry, end_token=None):
        self.__form_sentence(transition_matrix, sorted_tokens, word_num, token_count_per_entry, end_token)

    def get_sentence(self):
        return self.sentence

    #private

    def __form_sentence(self, transition_matrix, sorted_tokens, word_num, token_count_per_entry, end_token):

        self.sentence = []
        # Return a random word from sorted_words as the first word
        # Using list comprehension guarantees that the element contains only letters (aka is a word)

        match token_count_per_entry:
            case 1:
                chosen_token, chosen_token_index = random.choice([(alpha_token, index) for index,alpha_token in enumerate(sorted_tokens) if alpha_token.isalpha()])
            # case 2:
            #     chosen_token, chosen_token_index = \
            #     random.choice([(alpha_beginning_word, index) for index,alpha_beginning_word in enumerate(sorted_tokens) if alpha_beginning_word.split(" ")[0].isalpha()])

        self.sentence.append(chosen_token)

        # If the user wants num=100 words generated, since the first word was already generated, 99 more have to be generated, hence the range [0,num-1]
        for i in range(word_num-1): 
            # Returned as a list of tuples: (probability, index)
            feasible_tokens = [(row[chosen_token_index], i) for i, row in enumerate(transition_matrix) if row[chosen_token_index]>0]
            
            # Randomly choose an index. Each index has a probability, which is interpreted as a weight by random.choices()
            chosen_token_index = random.choices([x[1] for x in feasible_tokens], weights=[x[0] for x in feasible_tokens])[0]
            # Translate index to token
            chosen_token = sorted_tokens[chosen_token_index]

            # If chosen_token is the special end token, the sentence must be prematurely ended
            if chosen_token == end_token:
                return

            self.sentence.append(chosen_token)

    """
        TODO: Check cases
        Besides printing the words in the sentence array, this function also formats the sentence to look more natural,
        by introducing spaces before or after words and punctuation marks, capitalization, etc, wherever possible
    """
    def print_sentence(self, sentence):

        previous_word = None
        single_quote_open = False
        double_quote_open = False
        capitalization_required = True
        space_before_required = True
        double_dash_started = False
        print("----------------------------------------------------------------------")

        # flush=True prints the word/phrase directly to terminal instead of waiting
        for word in sentence:
            if previous_word == None:
                print(word.capitalize(), end="", flush=True)
                capitalization_required = False
            elif word in ['!','?', '.',':']:
                print(word, end="", flush=True)
                capitalization_required = True
                space_before_required = True
            elif word in [',',';', ')']:
                print(word, end="", flush=True)
                space_before_required = True
            elif word == '(':
                print(str(" " if space_before_required else "") + word, end="", flush=True)
                space_before_required=False
            elif word == '`' and not single_quote_open:
                print(str(" " if space_before_required else "") + word, end="", flush=True)
                single_quote_open = True
                space_before_required=False
            elif word == '\'':
                print(word,end="", flush=True)
                single_quote_open = False
                space_before_required = True
            elif word == '"' and not double_quote_open:
                print(str(" " if space_before_required else "") + word, end="", flush=True)
                double_quote_open = True
                space_before_required = False
            elif word == '"' and double_quote_open:
                print(word, end="", flush=True)
                double_quote_open = False
                space_before_required = True
            elif word == '-' and not double_dash_started:
                if previous_word == '-':
                    print(word, end="", flush=True)
                    double_dash_started = True
                    space_before_required = False
                else:
                    print(str(" " if space_before_required else "") + word, end="", flush=True)
            elif word == '-' and double_dash_started:
                if previous_word == '-':
                    print(word, end="", flush=True)
                    double_dash_started = False
                    space_before_required = True
                else:
                    print(str(" " if space_before_required else "") + word, end="", flush=True)
            else:
                print(str(" " if space_before_required else "") + str(word.capitalize() if capitalization_required else word), end="", flush=True)
                capitalization_required = False
                space_before_required = True

            previous_word = word

            # Simulate "thinking" (like ChatGPT)
            time.sleep(random.uniform(0.02,0.15))

        print("\n----------------------------------------------------------------------")