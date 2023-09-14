# bible-word-search

Bible Word Search is a simple, user-friendly GUI application for searching the Bible for user-inputted text. With the exception of a few brief uses of HTML, it uses Python 3. 

![bible-word-search_screenshot-01](https://github.com/jack-lincoln/bible-word-search/assets/65179426/40eda47b-9c98-4498-a3ad-b33d4c2d81c6)


## Requirements
Bible Word Search requires the following packages to run:<br />
* Requests<br />
* PyQt5<br />
* Matplotlib<br />

## How to use

Before the GUI is launched, kjv.txt (The King James Bible) is downloaded from 'https://www.o-bible.com', given that it is not already downloaded (King James Version, or 'KJV', is used exclusively because it it the most widely-used, non-copyrighted translation of the Bible). 

After the download is complete, the user is prompted to input a word they desire to search for in the text. They may choose to check "Exact match", which is default, or uncheck it. If checked, the word "top" will only result in searching the text for "top". If unchecked, the program will yield any result of t-o-p, such as "top", "stop", or "stopped".

Once the text is inputted by the user, they must click the "Search" button to proceed. A few things happen as a result, the most obvious of which is the autofilling of the bar graph. The graph displays the total number of occurrences of the search word in each book of the Bible.
Also, the book list is updated to list only books in which the search word appears (also listed are "The Bible", "Old Testament", and "New Testament"). Below the book list is a label that reflects the total number of appearances of the selected book. If the user chooses to select an item other than "The Bible" from the book list, only occurrences from the selected book will be listed in the occurrence list.

When the user clicks on an item (i.e. verse reference) from the occurrence list, the text of the selected verse will be displayed in the verse label. Any occurrence of the search word will be bolded when appearing in the verse label.

![bible-word-search_screenshot-02](https://github.com/jack-lincoln/bible-word-search/assets/65179426/7760d5f0-1680-4d38-972f-7b872e0b770f)
