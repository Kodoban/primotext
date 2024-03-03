#!/usr/bin/python

# TODO IMPORTANT
# Choose variable casing


# This Python file uses the following encoding: utf-8
import sys
import os
import random
import time

from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QListWidgetItem
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
from ui_form import Ui_MainWindow

# Get the path to the core module (core directory)
core_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'core')
sys.path.append(core_dir_path)
import core

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.action_addModel.triggered.connect(lambda x: self.add_new_model_action())

        self.ui.pushButton_generateText.clicked.connect(lambda x: self.generate_text_button_clicked())

        existing_models = core.get_existing_models()
        for model in existing_models:
            self.add_model_to_list_widget(model)

    def add_model_to_list_widget(self, model):
        # Add the file name to the list view
        item = QListWidgetItem(model.get_name())

        # TODO: Show path from a separate column in the listView
        item.setData(Qt.UserRole, model)
        item.setToolTip(f"Location: {model.get_path()}\nSource file: {model.get_source_path()}")

        self.ui.listWidget_generatedModels.addItem(item)

        return item

    def add_new_model_action(self):
        # Create a file dialog object
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Choose text file to create a model")
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Text Files (*.txt)")

        #file_path, _ = QFileDialog.getOpenFileName(None, "Select a file")


        # Show the file dialog window and get the selected source file path
        if file_dialog.exec() == QFileDialog.Accepted:

            user_source_file_path = file_dialog.selectedFiles()[0]
            #print("Selected file:", file_path)
            #file_path, _ = file_dialog.getOpenFileName()
            if user_source_file_path:

                # Check if file model has already been created
                token_length = self.ui.spinBox_tokensPerEntry.value()
                model_name, model_path, source_file_path, create_new_list_item = core.check_add_model(user_source_file_path, token_length)

                # Add entry to list if it does not exist already, and make it the selected choice
                # TODO: Differentiate between models with the same name (e.g. using last modified date on file)

                if create_new_list_item:
                    new_item = self.add_model_to_list_widget(core.generate_model(model_name, model_path, source_file_path, token_length))
                    self.ui.listWidget_generatedModels.setCurrentItem(new_item)

    def generate_text_button_clicked(self):

        selected_item = self.ui.listWidget_generatedModels.currentItem()

        if selected_item:
            word_generate_num = self.ui.spinBox_wordCounter.value()
            token_count_per_entry = self.ui.spinBox_tokensPerEntry.value()

            chosen_model = selected_item.data(Qt.UserRole)
            core.check_create_model(chosen_model)
            generated_sentence = core.generate_sentence(chosen_model, word_generate_num, token_count_per_entry)

            # Print generated sentence
            self.ui.textEdit_generatedText.clear()        
            for token in generated_sentence:
                self.ui.textEdit_generatedText.insertPlainText(token + " ")
                self.ui.textEdit_generatedText.repaint()
                QApplication.processEvents()

                # time.sleep(random.uniform(0.05,0.3))
                time.sleep(random.uniform(0.02,0.15))
        else:
            print("Please select an item first!")

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())
