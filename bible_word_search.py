#! python3
# bible_word_search.py - A program that allows the user to view all occurrences of a specified word in the Bible.

from bible_book_dicts import Occurrences as Oc

import sys
import os.path

import requests
import re

from PyQt5 import QtWidgets

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')


class GetKJV:
    """A method to download the KJV Bible as a .txt file. """

    path = './kjv.txt'
    if os.path.isfile(path):
        pass
    else:
        res = requests.get('https://www.o-bible.com/download/kjv.txt')
        res.raise_for_status()
        play_file = open('KJV.txt', 'wb')
        for chunk in res.iter_content(100000):
            play_file.write(chunk)

        play_file.close()

        lines = []
        with open('KJV.txt', 'r') as kjv:
            lines = kjv.readlines()

        with open('KJV.txt', 'w') as kjv:
            for number, line in enumerate(lines):
                if number not in [0]:
                    kjv.write(line)


class MplCanvas(FigureCanvasQTAgg):
    """A class to create the bar graph."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        super(MplCanvas, self).__init__(self.fig)

        # Create the x- and y- axes.
        self.axes.set_xlabel('Book', fontsize=20)
        self.axes.set_ylabel('Occurrences', fontsize=20)
        self.axes.autoscale(enable=True)

        # Determine the greatest number of occurrences of a book in the old and new testaments.
        # This will be used to determine the range of the y-axis of the graph.
        self.max_word_count = 0
        self.old_test_word_count = max(Oc.word_count_per_book[0].values())
        self.new_test_word_count = max(Oc.word_count_per_book[1].values())

        if self.old_test_word_count >= self.new_test_word_count:
            self.max_word_count = max(Oc.word_count_per_book[0].values())
        else:
            self.max_word_count = max(Oc.word_count_per_book[1].values())

        # Set colors of bars for Old and New Testament books
        self.bar_label = ['red']
        self.bar_colors = []
        for i in range(len(Oc.word_count_per_book[0].keys())):
            self.bar_colors.append('red')
        for i in range(len(Oc.word_count_per_book[1].keys())):
            self.bar_colors.append('blue')

        # Set the x-axis to display books of the Bible
        # and the y-axis to display occurrences of the search word per book.
        self.axes.bar(list(Oc.word_count_per_book[0].keys()) + list(Oc.word_count_per_book[1].keys()),
                      list(Oc.word_count_per_book[0].values()) + list(Oc.word_count_per_book[1].values()),
                      label=self.bar_label, color=self.bar_colors)


class MainWindow(QtWidgets.QMainWindow):
    """A class to create the main window, as well as all other functions of the program."""

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)

        self.setWindowTitle("Bible Word Search")
        self.setGeometry(50, 100, 1500, 700)

        # Variables used temporarily after "Search" button is clicked
        self.current_verse = []
        self.current_display_verse = ''

        # A dicionary of all occurrences of the search word, where the key is the verse reference
        # and the value is the text of the verse
        self.word_count_dict = {}

        # A variable equals to the total number of occurrences of the search word
        self.word_count = len(self.word_count_dict)

        # The book currently selected in book_list
        self.current_book = 'The Bible'

        # The searched word and the verse selected to be displayed in self.verse_label
        self.word = ''
        self.verse = []

        # Book list items other than individual books of the Bible
        self.book_list_items = ['The Bible', 'Old Testament', 'New Testament']

        # Determine whether occurrence_label will read 'occurrence' or 'occurrences'
        self.sing_or_plural = ['occurrence', 'occurrences']
        self.plurality = self.sing_or_plural[1]

        # The text box where the user will type a word to search for
        self.text_box = QtWidgets.QTextEdit()
        self.text_box.setMaximumSize(200, 35)

        plt.subplots_adjust(left=0.10, bottom=0.15, right=0.98, top=0.95)

        # The search button
        self.search_button = QtWidgets.QPushButton("Search")
        self.search_button.clicked.connect(self.search_word)
        self.search_button.setMaximumSize(80, 35)

        # Creates the list widget to display all books that contain the search word
        self.book_list = QtWidgets.QListWidget()
        self.book_list.setMinimumSize(200, 50)
        self.book_list.setMaximumSize(200, 100)
        self.book_list.itemClicked.connect(self.update_current_book)

        # Before clicking search_button, all books of the Bible are listed in book_list
        for item in self.book_list_items:
            self.book_list.addItem(item)
        for key, value in Oc.book_abbrevs.items():
            self.book_list.addItem(value)

        # Creates the list widget that displays all verse references that contain occurrences
        # of the search word
        self.occurrence_list = QtWidgets.QListWidget()
        self.occurrence_list.setMinimumSize(200, 50)
        self.occurrence_list.setMaximumSize(200, 100)
        self.occurrence_list.itemClicked.connect(self.show_verse)

        # Create the horizontal layout the separates the widgets from the graph
        layout0 = QtWidgets.QHBoxLayout()  # Separates all widgets (left) from graph (right)
        layout1 = QtWidgets.QVBoxLayout()  # Separates different vertical levels of the widgets
        layout0.addLayout(layout1)

        # Create the layout and widgets for the search function
        layout2 = QtWidgets.QHBoxLayout()  # Horizontal box layout for the word search widgets
        search_label = QtWidgets.QLabel("Type a word to search the Bible for it:")
        search_label.setMaximumSize(250, 35)
        layout1.addWidget(search_label)
        layout2.addWidget(self.text_box)
        layout2.addWidget(self.search_button)
        layout1.addLayout(layout2)

        # Create the layout and widgets for the 'Exact Match' check box
        self.exact_match_check_box = QtWidgets.QCheckBox("Exact match")
        self.exact_match_check_box.setMinimumSize(200, 25)
        self.exact_match_check_box.setMaximumSize(25, 25)
        self.exact_match_check_box.setChecked(True)
        layout1.addWidget(self.exact_match_check_box)

        # Create the layout and widgets for the 'select a book' function
        layout4 = QtWidgets.QHBoxLayout()
        select_book = QtWidgets.QLabel("Select a book:")
        select_book.setMaximumSize(250, 35)
        layout1.addWidget(select_book)
        layout4.addWidget(self.book_list)
        layout1.addLayout(layout4)

        # Create the layout and widgets for the occurrences function
        layout5 = QtWidgets.QHBoxLayout()  # Horizontal box layout for the occurrences widgets
        self.occurrence_label = QtWidgets.QLabel(f"{self.word_count} {self.plurality} in {self.current_book}:")
        self.occurrence_label.setMaximumSize(250, 35)
        layout1.addWidget(self.occurrence_label)
        layout1.addLayout(layout5)
        layout5.addWidget(self.occurrence_list)

        # Create the layout and widget for the verse display
        self.verse_label = QtWidgets.QLabel()
        self.verse_label.setStyleSheet("border-style: solid;" "border-width: 2px;")
        self.verse_label.setWordWrap(True)
        self.verse_label.setMaximumSize(300, 200)
        layout1.addWidget(self.verse_label)

        # Create a placeholder widget to hold the canvas.
        layout0.addWidget(self.sc)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout0)
        self.setCentralWidget(widget)

        self.axes = plt.subplots()

        # Set colors of bars for Old and New Testament books
        self.bar_label = ['red']
        self.bar_colors = []
        for i in range(len(Oc.word_count_per_book[0].keys())):
            self.bar_colors.append('red')
        for i in range(len(Oc.word_count_per_book[1].keys())):
            self.bar_colors.append('blue')

        self.update_graph()

        self.show()

    def update_graph(self):
        """A method to display the graph, as well as to update it to reflect word occurrences per book."""

        # Clear previous bar graph data
        self.sc.axes.cla()

        # Create the x- and y- axes.
        self.sc.axes.set_xlabel('Book', fontsize=20)
        self.sc.axes.set_ylabel('Occurrences', fontsize=20)
        self.sc.axes.autoscale(enable=True)
        self.sc.axes.tick_params(labelrotation=90)

        # Set the x-axis to display books of the Bible
        # and the y-axis to display occurrences of the search word per book.
        self.sc.axes.bar(list(Oc.word_count_per_book[0].keys()) + list(Oc.word_count_per_book[1].keys()),
                      list(Oc.word_count_per_book[0].values()) + list(Oc.word_count_per_book[1].values()),
                      label=self.bar_label, color=self.bar_colors)

        self.sc.draw()

    def search_word(self):

        # Set self.word to the text currently in self.text_box
        self.word = self.text_box.toPlainText()

        # Clear variables from previously searched word (if any)
        self.reset_book_combo_box()
        self.update_current_book()
        self.clear_verse_label()
        self.clear_word_count_dict()
        self.clear_word_count_per_book()
        self.reset_word_count()

        # Search the text of KJV.txt for all occurrences of the search word
        with open(r'KJV.txt', 'r') as fp:
            lines = fp.readlines()
            for row in lines:
                lower_verse = row.lower()
                if self.exact_match_check_box.isChecked():
                    if re.search(r'[a-zA-Z]' + self.word.lower() + r'[a-zA-Z]', lower_verse):
                        pass
                    elif re.search(self.word.lower() + r'[a-zA-Z]', lower_verse):
                        pass
                    elif re.search(r'[a-zA-Z]' + self.word.lower(), lower_verse):
                        pass
                    elif self.word.lower() in lower_verse:
                        self.search_word_functions(row, lower_verse)
                else:
                    if re.search(r'[a-zA-Z]' + self.word.lower() + r'[a-zA-Z]', lower_verse):
                        self.search_word_functions(row, lower_verse)
                    elif re.search(self.word.lower() + r'[a-zA-Z]', lower_verse):
                        self.search_word_functions(row, lower_verse)
                    elif re.search(r'[a-zA-Z]' + self.word.lower(), lower_verse):
                        self.search_word_functions(row, lower_verse)
                    elif self.word.lower() in lower_verse:
                        self.search_word_functions(row, lower_verse)

        # Methods that are executed after search_word_functions are run
        self.update_occurrence_list()
        self.update_occurrence_label()
        self.update_book_list()

        self.update_graph()

    def search_word_functions(self, row, lower_verse):
        """A method to execute methods that initially respond to "Search" button being clicked"""

        self.current_verse = row.split(' ', 1)
        self.split_ref_text()
        self.update_word_count(lower_verse)
        self.word_count_dict.update({self.current_display_verse: self.current_verse[1]})

    def split_ref_text(self):
        """A method to separate the verse reference as it appears in the .txt file into its component parts."""

        # Find the first character in the verse reference
        first_char = self.current_verse[0][0]

        # Check if the first character in the reference is a numeral (e.g. '1Cor10:31', '2Chr29:5', etc.)
        if first_char.isdigit():
            reference_sans_num = self.current_verse[0][1:]
            ref_components = re.split(r'(\d+)', reference_sans_num)
            book = first_char + ref_components[0]

        # If the first character is not a numeral:
        else:
            ref_components = re.split(r'(\d+)', self.current_verse[0])
            book = ref_components[0]

        chapter = ref_components[1]
        verse = ref_components[3]

        # Create the current_display_verse using the translate_from_book_abbrev method
        self.translate_from_book_abbrev(book, chapter, verse)

        self.update_word_count_per_book(book)

    def translate_from_book_abbrev(self, book, chapter, verse):
        """A method to update the current_display_verse using the split components of the abbreviated verse reference"""

        self.current_display_verse = Oc.book_abbrevs.get(book) + ' ' + chapter + ':' + verse

    def translate_to_book_abbrev(self, book):
        """A method to translate the display verse reference back into the abbreviated verse reference """

        # Create lists of all keys and values of the book_abbrevs dictionary
        key_list = list(Oc.book_abbrevs.keys())         # E.g. 'Ge'
        value_list = list(Oc.book_abbrevs.values())     # E.g. 'Genesis'

        value = value_list.index(book)
        self.abbreved_book = key_list[value]

    def update_word_count(self, lower_verse):
        """A method to update the total number of search word occurrences"""

        word_count_in_verse = lower_verse.count(self.word.lower())
        self.word_count += word_count_in_verse

    def update_word_count_per_book(self, book):
        """A method to update word_count_per_book list"""

        # Check if the book occurs in the OT dictionary (i.e. word_count_per_book[0])
        if book in Oc.word_count_per_book[0]:
            Oc.word_count_per_book[0][book] += 1
        # Check if the book occurs in the NT dictionary (i.e. word_count_per_book[1])
        elif book in Oc.word_count_per_book[1]:
            Oc.word_count_per_book[1][book] += 1
        else:
            pass

    def update_occurrence_list(self):
        """A method to update occurrence_list"""

        self.occurrence_list.clear()

        # If 'The Bible' is selected, allow all verses including the current word to the occurrence_list
        if self.book_list.currentItem().text() == 'The Bible':
            self.occurrence_list.addItems(self.word_count_dict.keys())
        else:
            # Find the name of the book for each item in self.word_count_dict (ie 'Genesis' from 'Genesis 1:1')
            for key, value in self.word_count_dict.items():
                first_char = key[0]

                # If book begins with a number ('2 Samuel', '1 Peter', etc.)
                if first_char.isdigit():
                    temp_book = key.split(' ', 2)
                    book = str(temp_book[0] + ' ' + temp_book[1])
                else:
                    # 'Song of Solomon' is the only book ordinarily named with three words
                    if key[:4] == 'Song':
                        temp_book = key.split(' ', 3)
                        book = temp_book[0] + ' ' + temp_book[1] + ' ' + temp_book[2]
                    else:
                        temp_book = key.split(' ', 1)
                        book = temp_book[0]

                # Check if the selected item in book_list is a book or a collection of books
                # (i.e. 'Old Testament' or 'New Testament')
                if self.book_list.currentItem().text() == book:
                    self.occurrence_list.addItem(key)
                elif self.book_list.currentItem().text() == 'Old Testament':
                    if book in Oc.old_testament:
                        self.occurrence_list.addItem(key)
                elif self.book_list.currentItem().text() == 'New Testament':
                    if book in Oc.new_testament:
                        self.occurrence_list.addItem(key)

    def update_occurrence_label(self):
        """A method to update the occurrence_label"""

        # Create variables to count the occurrences of the search word in the Old Testament and New Testament
        ot_word_count = 0
        nt_word_count = 0

        # A variable to cound occurrences in the entire Bible (i.e. total number of occurrences)
        bible_word_count = self.word_count

        # Find the sum of all occurrences for both the Old and New Testaments
        for key, value in Oc.word_count_per_book[0].items():
            ot_word_count += value
        for key, value in Oc.word_count_per_book[1].items():
            nt_word_count += value

        # Based on the current_book, determine the output for the occurrence_label
        if self.current_book == 'The Bible':
            # Determine whether occurrence_label should read "occurrence" or "occurrences
            self.update_word_plurality(bible_word_count)
            self.occurrence_label.setText(f'{bible_word_count} {self.plurality} in {self.current_book}:')
        elif self.current_book == 'Old Testament':
            self.update_word_plurality(ot_word_count)
            self.occurrence_label.setText(f'{ot_word_count} {self.plurality} in {self.current_book}:')
        elif self.current_book == 'New Testament':
            self.update_word_plurality(nt_word_count)
            self.occurrence_label.setText(f'{nt_word_count} {self.plurality} in {self.current_book}:')
        else:
            self.update_word_plurality(self.current_book)
            self.occurrence_label.setText(f'{len(self.occurrence_list)} {self.plurality} in {self.current_book}:')

    def update_word_plurality(self, search_filter):
        """A method to determine the plurality status of the occurrence_label"""

        # If there is only 1 occurrence of the search word in current_book (or one of the book_list_items),
        # occurrence_label will read "x occurrence in [book]". If there is more than 1 occurrence,
        # or if there are no occurrences, occurrence_label will read "x occurrences in [book]".

        if self.current_book in self.book_list_items:
            self.plurality = self.sing_or_plural[1]

        else:
            self.translate_to_book_abbrev(self.current_book)
            num = 0
            for i in range(2):
                try:
                    num = Oc.word_count_per_book[i][self.abbreved_book]
                except:
                    pass
            if num == 1:
                self.plurality = self.sing_or_plural[0]
            else:
                self.plurality = self.sing_or_plural[1]

    def update_book_list(self):
        """A method to add books that contain the search word to book_list"""

        # Clear all items currently in book_list
        self.book_list.clear()

        # Add default book_list items ("The Bible", "Old Testament", and "New Testament")
        for item in self.book_list_items:
            self.book_list.addItem(item)
        # Add books to book_list where key in word_count_per_book > 0
        for key, value in Oc.book_abbrevs.items():
            for book_dict in Oc.word_count_per_book:
                if book_dict.get(key, 0) > 0:
                    self.book_list.addItem(value)

    def update_current_book(self):
        """A method to update current_book based on the currently selected item in book_list"""

        self.current_book = self.book_list.currentItem().text()
        self.update_occurrence_list()
        self.update_occurrence_label()

    def update_verse(self):
        """A method to assign the verse clicked on in occurrence_list to self.verse"""

        self.verse.clear()
        for key, value in self.word_count_dict.items():
            if key == self.occurrence_list.currentItem().text():
                self.verse.append(key)
                self.verse.append(value)
            else:
                pass

    def show_verse(self):
        """A method to display self.verse in verse_label"""

        self.update_verse()

        # Set the search word in the verse to a bold font, whether it is lowercase, uppercase, or capitalized
        bold_verse = self.verse[1].replace(self.word.lower(), f'<html><b>{self.word.lower()}</b</html>')
        bold_verse = bold_verse.replace(self.word.capitalize(), f'<html><b>{self.word.capitalize()}</b</html>')
        bold_verse = bold_verse.replace(self.word.upper(), f'<html><b>{self.word.upper()}</b</html>')
        self.verse_label.setText(bold_verse)

    def clear_word_count_dict(self):
        """A method to clear word_count_dict"""

        self.word_count_dict.clear()

    def clear_word_count_per_book(self):
        """A method to reset occurrences of the word per book to zero"""

        # Set all occurrences per book in the Old Testament to zero
        for key in Oc.word_count_per_book[0].keys():
            Oc.word_count_per_book[0][key] = 0
        # Set all occurrences per book in the New Testament to zero
        for key in Oc.word_count_per_book[1].keys():
            Oc.word_count_per_book[1][key] = 0

    def clear_verse_label(self):
        """A method to clear the text of verse_label"""

        self.verse_label.clear()

    def reset_word_count(self):
        """A method to reset the word_count to zero"""

        self.word_count = 0

    def reset_book_combo_box(self):
        """A method to revert reset_book_combo_box to default settings"""

        # Set self.book_list to the first item (i.e. "The Bible")
        self.book_list.setCurrentRow(0)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
