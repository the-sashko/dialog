import re

from markov import dictionary

#to-do: refactoring code syle
#to-do: add logs
class Formatter():
    __dictionary = None

    def __init__(self):
        self.__dictionary = dictionary.Dictionary()

    def get_formatted_raw_text(self, raw_text: str) -> str:
        formatted_text = re.sub(r'([\w]+)', r' \g<1> ', raw_text)
        formatted_text = re.sub(r'\n+', '<br>', formatted_text)
        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        formatted_text = re.sub(r'((^\s)|(\s$))', '', formatted_text)
        formatted_text = re.sub(r'((\s\.)|(\.\s))', '.', formatted_text)
        formatted_text = formatted_text.replace('...', ' … ')
        formatted_text = re.sub(r'[\.]+', '.', formatted_text)
        formatted_text = re.sub(r'((^\.)|(\.$))', '', formatted_text)
        formatted_text = formatted_text.lower()
        formatted_text = formatted_text.replace('’', '\'')
        formatted_text = self.__dictionary.start + ' ' + formatted_text + ' ' + self.__dictionary.end
        formatted_text = formatted_text.replace('.', ' ' + self.__dictionary.end + ' ' + self.__dictionary.start + ' ')
        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        formatted_text = re.sub(r'((^\s)|(\s$))', '', formatted_text)
        formatted_text = formatted_text.replace(' \' ', '\'')
        formatted_text = formatted_text.replace('”', '"')
        formatted_text = formatted_text.replace('“', '"')
        formatted_text = formatted_text.replace('«', '"')
        formatted_text = formatted_text.replace('»', '"')
        formatted_text = formatted_text.replace('<br> ', '<br>')
        formatted_text = formatted_text.replace(' <br>', '<br>')
        formatted_text = formatted_text.replace(self.__dictionary.end + ' ' + self.__dictionary.start + '<br>', '<br>')
        formatted_text = formatted_text.replace(self.__dictionary.start + '<br>', '<br>')
        formatted_text = formatted_text.replace('<br> ', '<br>')
        formatted_text = formatted_text.replace(' <br>', '<br>')
        formatted_text = formatted_text.replace('<br>' + self.__dictionary.end + ' ' + self.__dictionary.start, '<br>')
        formatted_text = formatted_text.replace('<br>' + self.__dictionary.end, '<br>')
        formatted_text = formatted_text.replace('<br> ', '<br>')
        formatted_text = formatted_text.replace(' <br>', '<br>')
        formatted_text = re.sub(r'<br>', '\n', formatted_text)
        formatted_text = re.sub(r'\n+', '<br>', formatted_text)
        formatted_text = re.sub(r'^<br>', self.__dictionary.start + ' ', formatted_text)
        formatted_text = re.sub(r'<br>$', ' ' + self.__dictionary.end, formatted_text)
        formatted_text = formatted_text.replace('<br>', ' ' + self.__dictionary.end + ' ' + self.__dictionary.stop + ' ' + self.__dictionary.start + ' ')

        return formatted_text

    def get_formatted_tokenized_text(self, tokenized_text: list) -> str:
        formatted_text = ' '.join(tokenized_text)

        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        formatted_text = re.sub(r'((^\s)|(\s$))', '', formatted_text)
        formatted_text = re.sub(r'((\s\.)|(\.\s))', '.', formatted_text)

        formatted_text = re.sub(r'' + self.__dictionary.stop + '', '\n', formatted_text)
        formatted_text = re.sub(r'\n+', '\n', formatted_text)
        formatted_text = re.sub(r'\s\n', '\n', formatted_text)
        formatted_text = re.sub(r'\n\s', '\n', formatted_text)
        formatted_text = re.sub(r'\n+', '\n', formatted_text)
        formatted_text = re.sub(r'^\n', '', formatted_text)
        formatted_text = re.sub(r'\n$', '', formatted_text)

        formatted_text = formatted_text.split('\n')
        formatted_text = formatted_text[0]

        formatted_text = formatted_text.replace('...', ' … ')
        formatted_text = formatted_text.replace('?', '?.')
        formatted_text = formatted_text.replace('!', '!.')
        formatted_text = formatted_text.replace(',.', '.')
        formatted_text = formatted_text.replace('…', '….')
        formatted_text = re.sub(r'[\.]+', '.', formatted_text)
        formatted_text = re.sub(r'((^\.)|(\.$))', '', formatted_text)

        formatted_text = formatted_text.split('.')

        for sentence_count_index, sentence in enumerate(formatted_text) :
            sentence = re.sub(r'\s+', ' ', sentence)
            sentence = re.sub(r'((^\s)|(\s$))', '', sentence)
            sentence = re.sub(r'\s([,;:?!]{1})', r'\g<1>', sentence)
            sentence = re.sub(r'^- ', '', sentence)
            sentence = re.sub(r'^– ', '', sentence)
            sentence = sentence.capitalize()

            formatted_text[sentence_count_index] = sentence

        formatted_text = '. '.join(formatted_text)# + '.'

        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        formatted_text = re.sub(r'((^\s)|(\s$))', '', formatted_text)

        formatted_text = formatted_text.replace('?.', '?')
        formatted_text = formatted_text.replace('!.', '!')
        formatted_text = formatted_text.replace('….', '…')
        formatted_text = formatted_text.replace(',-', ' -')

        formatted_text = re.sub(r'\s+', ' ', formatted_text)
        formatted_text = re.sub(r'((^\s)|(\s$))', '', formatted_text)

        formatted_text = re.sub(r'" ([^"]+) "', r'"\g<1>"', formatted_text)
        formatted_text = re.sub(r'\( ([^\(\)]+) \)', r'(\g<1>)', formatted_text)

        return formatted_text
