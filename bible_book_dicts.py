class Occurrences:

    word_count_per_book = [{'Ge': 0, 'Exo': 0, 'Lev': 0, 'Num': 0, 'Deu': 0, 'Josh': 0,
                     'Jdgs': 0, 'Ruth': 0, '1Sm': 0, '2Sm': 0, '1Ki': 0, '2Ki': 0,
                     '1Chr': 0, '2Chr': 0, 'Ezra': 0, 'Neh': 0, 'Est': 0, 'Job': 0,
                     'Psa': 0, 'Prv': 0, 'Eccl': 0, 'SSol': 0, 'Isa': 0, 'Jer': 0,
                     'Lam': 0, 'Eze': 0, 'Dan': 0, 'Hos': 0, 'Joel': 0, 'Amos': 0,
                     'Obad': 0, 'Jonah': 0, 'Mic': 0, 'Nahum': 0, 'Hab': 0, 'Zep': 0,
                     'Hag': 0, 'Zec': 0, 'Mal': 0}, {'Mat': 0, 'Mark': 0, 'Luke': 0,
                     'John': 0, 'Acts': 0, 'Rom': 0, '1Cor': 0, '2Cor': 0, 'Gal': 0,
                     'Eph': 0, 'Phi': 0, 'Col': 0, '1Th': 0, '2Th': 0, '1Tim': 0,
                     '2Tim': 0, 'Titus': 0, 'Phmn': 0, 'Heb': 0, 'Jas': 0, '1Pet': 0,
                     '2Pet': 0, '1Jn': 0, '2Jn': 0, '3Jn': 0, 'Jude': 0, 'Rev': 0
                     }]

    book_abbrevs = {'Ge': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus',
                     'Num': 'Numbers', 'Deu': 'Deuteronomy', 'Josh': 'Joshua',
                     'Jdgs': 'Judges', 'Ruth': 'Ruth', '1Sm': '1st Samuel',
                     '2Sm': '2nd Samuel', '1Ki': '1st Kings', '2Ki': '2nd Kings',
                     '1Chr': '1st Chronicles', '2Chr': '2nd Chronicles', 'Ezra': 'Ezra',
                     'Neh': 'Nehemiah', 'Est': 'Esther', 'Job': 'Job',
                     'Psa': 'Psalms', 'Prv': 'Proverbs', 'Eccl': 'Ecclesiastes',
                     'SSol': 'Song of Solomon', 'Isa': 'Isaiah', 'Jer': 'Jeremiah',
                     'Lam': 'Lamentations', 'Eze': 'Ezekiel', 'Dan': 'Daniel',
                     'Hos': 'Hosea', 'Joel': 'Joel', 'Amos': 'Amos',
                     'Obad': 'Obadiah', 'Jonah': 'Jonah', 'Mic': 'Micah',
                     'Nahum': 'Nahum', 'Hab': 'Habakkuk', 'Zep': 'Zephaniah',
                     'Hag': 'Haggai', 'Zec': 'Zechariah', 'Mal': 'Malachi',
                     'Mat': 'Matthew', 'Mark': 'Mark', 'Luke': 'Luke',
                     'John': 'John', 'Acts': 'Acts', 'Rom': 'Romans',
                     '1Cor': '1st Corinthians', '2Cor': '2nd Corinthians', 'Gal': 'Galatians',
                     'Eph': 'Ephesians', 'Phi': 'Philippians', 'Col': 'Colossians',
                     '1Th': '1st Thessalonians', '2Th': '2nd Thessalonians', '1Tim': '1st Timothy',
                     '2Tim': '2nd Timothy', 'Titus': 'Titus', 'Phmn': 'Philemon',
                     'Heb': 'Hebrews', 'Jas': 'James', '1Pet': '1st Peter',
                     '2Pet': '2nd Peter', '1Jn': '1st John', '2Jn': '2nd John',
                     '3Jn': '3rd John', 'Jude': 'Jude', 'Rev': 'Revelation'
                     }
