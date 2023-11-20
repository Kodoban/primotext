from .model_gen import ModelGenerator
import re

class Model:
    # Case: Model .csv does not exist
    def __init__(self, name, path, source_path, token_length):
        self.name = name
        self.path = path
        self.source_path = source_path
        self.token_length = token_length

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def get_source_path(self):
        return self.source_path

    def get_source_path_basename(self):
        return re.search(r'([^/\\]+)(?=\.[^/\\]+$)', self.source_path).group(1)

    def get_token_length(self):
        return self.token_length

    def set_transition_matrix(self, transition_matrix):
        self.transition_matrix = transition_matrix

    def get_transition_matrix(self):
        return self.transition_matrix.get_matrix()

    def get_sorted_tokens(self):
        return self.transition_matrix.get_sorted_tokens()

    def create_transition_matrix(self):
        ModelGenerator(self)

    def import_transition_matrix(self):
        ModelGenerator(self, self.path)