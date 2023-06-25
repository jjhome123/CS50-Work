import csv, string, math, json
from cs50 import SQL
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
    db = SQL('sqlite:///words.db')

    if request.method == 'POST':
        str = request.form.get('input')  # original input
        new_str = clean_input(str) + ' '
        wordList = load_words(new_str)
        filteredList = list(set(check_words(wordList, db)))
        indexes = []
        for word in filteredList:
            for i in range(len(wordList)):
                if wordList[i] in filteredList:
                    indexes.append(i)

        synonyms = {}
        if request.form.get('thesaurus') == 'enable':
            with open('thesaurus/en_thesaurus.jsonl', 'r') as thesaurus:
                t = thesaurus.readlines()
                for word in filteredList:
                    result = lookup(word, t)
                    synonyms[word] = result
                return render_template('result.html', synonyms=synonyms, wordList=wordList, indexes=indexes, str=str)
        else:
            return render_template('result.html', wordList=wordList, indexes=indexes, str=str)
    return render_template('layout.html')


def clean_data(db):  # Resets words.db. Overwrites clean.csv and uses it to INSERT 'cleaner' data into words.db.
    db = SQL('sqlite:///words.db')
    db.execute('DELETE FROM examples')
    db.execute('DELETE FROM words')

    file = 'wlist.csv'
    with open(file, "r", encoding='utf-8-sig') as wordList:
        with open('clean.csv', 'w') as updatedFile:
            reader = csv.DictReader(wordList)
            fields = ['id','word','usage','meaning', 'example']
            writer = csv.DictWriter(updatedFile, fieldnames = fields)
            header = {'id': 'id', 'word': 'word', 'usage': 'usage', 'meaning': 'meaning', 'example': 'example'}
            writer.writerow(header)
            for row in reader:
                row['word'] = row['word'].strip().replace('\n','').lower()
                row['usage'] = row['usage'].strip().replace('\n','')
                row['meaning'] = row['meaning'].strip().replace('\n','')
                row['example'] = row['example'].strip().replace('\n','')
                writer.writerow(row)
    with open('clean.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            db.execute('INSERT INTO words (word, usage, meaning) VALUES (?, ?, ?)', row['word'], row['usage'], row['meaning'])
            db.execute('INSERT INTO examples (example) VALUES (?)', row['example'])


def check_words(wordList, db):
    bad = []
    exception = ['dont','wasnt','doesnt', 'youre','theyre','wont', 'werent', 'andor', 'isnt']
    for word in wordList:
        form_check = db.execute('SELECT meaning FROM words WHERE meaning LIKE ?', '%' + word + '%')
        if form_check:
            continue
        if word[-3:] in ['ies', 'ing', 'ied'] or word[-4:] == 'ning':
            #print(f'-ies or -ing check for {word}')
            check = db.execute('SELECT * FROM words WHERE word = ?', word[:-3] + 'y')
            if check:
                #print(f'Different form of {word} found in Habatan dictionary')
                continue
            check = db.execute('SELECT * FROM words WHERE word = ?', word[:-3] + 'e')
            if check:
                #print(f'Different form of {word} found in Habatan dictionary')
                continue
            check = db.execute('SELECT * FROM words WHERE word = ?', word[:-3])
            if check:
                #print(f'Different form of {word} found in Habatan dictionary')
                continue
            check = db.execute('SELECT * FROM words WHERE word = ?', word[:-4])
            if check:
                #print(f'Different form of {word} found in Habatan dictionary')
                continue
        if word[-1:] == 's' or word[-1:] == 'd' and len(word) > 2:
            #print(f'-s or -d check for {word}')
            check = db.execute('SELECT * FROM words WHERE word = ?', word[:-1])
            if check:
                #print(f'Different form of {word} found in Habatan dictionary: {word[:-1]}')
                continue
        if word[-2:] in ['es', 'ed'] and len(word) > 3:
            #print(f'-es or -ed check for {word}')
            check = db.execute('SELECT * FROM words WHERE word = ?', word[:-2])
            if check:
                #print(f'Different form of {word} found in Habatan dictionary: {word[:-2]}')
                continue
        check = db.execute('SELECT * FROM words WHERE word = ?', word)
        if not check and word not in exception:
            #print(f'{word} was not found in Habatan Dictionary...')
            bad.append(word)
    return bad


def clean_input(text):
    text = text.lower().replace('\r\n', ' ').replace('\n', ' ').replace(',','').replace(':',' ')
    punc = string.punctuation.replace('-','') + "‘’“”–'"
    new_text = text.translate(str.maketrans('', '', punc))
    while '  ' in text:
        text = text.replace('  ', ' ')
    return new_text


def load_words(text):
    words = []
    word = ''
    for char in text:
        if char not in [' ']:
            word += char
        elif word != '':
            words.append(word)
            word = ''
    return words


def lookup(word, t):
    num_lines = sum(1 for line in t)
    mid = math.floor(num_lines/2)
    index = json.loads(t[mid])
    if num_lines == 1 and word != index['word'] or index['synonyms'] == []:
        return ''
    elif word < index['word'] and num_lines > 1:
        return lookup(word, t[:mid])
    elif word > index['word'] and num_lines > 1:
        return lookup(word, t[mid:])
    else:
        return index['synonyms']