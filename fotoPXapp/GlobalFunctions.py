import re


def ReplacePolishCharacters(text):
    polishChars = ['ą', 'ć', 'ę', 'ł', 'ń', 'ó', 'ś', 'ż', 'ź']
    replaceChar = ['a', 'c', 'e', 'l', 'n', 'o', 's', 'z', 'z']
    i = 0
    while i < 9:
        text = text.replace(polishChars[i], replaceChar[i])
        i = i + 1
    return text


def RemoveSpecialCharacters(text):
    text = re.sub('[^A-Za-z0-9ąćęłńóśżź]+', ' ', text)
    return text
