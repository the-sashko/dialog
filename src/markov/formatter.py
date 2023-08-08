import re

from markov import dictionary

#to-do: refactoring code syle
#to-do: add logs
class Formatter():
    __dictionary = None

    def __init__(self):
        self.__dictionary = dictionary.Dictionary()

    def getFormattedRawText(self, rawText: str) -> str:
        formattedText = re.sub(r'([\w]+)', r' \g<1> ', rawText)
        formattedText = re.sub(r'\n+', '<br>', formattedText)
        formattedText = re.sub(r'\s+', ' ', formattedText)
        formattedText = re.sub(r'((^\s)|(\s$))', '', formattedText)
        formattedText = re.sub(r'((\s\.)|(\.\s))', '.', formattedText)
        formattedText = formattedText.replace('...', ' … ')
        formattedText = re.sub(r'[\.]+', '.', formattedText)
        formattedText = re.sub(r'((^\.)|(\.$))', '', formattedText)
        formattedText = formattedText.lower()
        formattedText = formattedText.replace('’', '\'')
        formattedText = self.__dictionary.start + ' ' + formattedText + ' ' + self.__dictionary.end
        formattedText = formattedText.replace('.', ' ' + self.__dictionary.end + ' ' + self.__dictionary.start + ' ')
        formattedText = re.sub(r'\s+', ' ', formattedText)
        formattedText = re.sub(r'((^\s)|(\s$))', '', formattedText)
        formattedText = formattedText.replace(' \' ', '\'')
        formattedText = formattedText.replace('”', '"')
        formattedText = formattedText.replace('“', '"')
        formattedText = formattedText.replace('«', '"')
        formattedText = formattedText.replace('»', '"')
        formattedText = formattedText.replace('<br> ', '<br>')
        formattedText = formattedText.replace(' <br>', '<br>')
        formattedText = formattedText.replace(self.__dictionary.end + ' ' + self.__dictionary.start + '<br>', '<br>')
        formattedText = formattedText.replace(self.__dictionary.start + '<br>', '<br>')
        formattedText = formattedText.replace('<br> ', '<br>')
        formattedText = formattedText.replace(' <br>', '<br>')
        formattedText = formattedText.replace('<br>' + self.__dictionary.end + ' ' + self.__dictionary.start, '<br>')
        formattedText = formattedText.replace('<br>' + self.__dictionary.end, '<br>')
        formattedText = formattedText.replace('<br> ', '<br>')
        formattedText = formattedText.replace(' <br>', '<br>')
        formattedText = re.sub(r'<br>', '\n', formattedText)
        formattedText = re.sub(r'\n+', '<br>', formattedText)
        formattedText = re.sub(r'^<br>', self.__dictionary.start + ' ', formattedText)
        formattedText = re.sub(r'<br>$', ' ' + self.__dictionary.end, formattedText)
        formattedText = formattedText.replace('<br>', ' ' + self.__dictionary.end + ' ' + self.__dictionary.stop + ' ' + self.__dictionary.start + ' ')

        return formattedText

    def getFormattedTokenizedText(self, tokenizedText: list) -> str:
        formattedText = ' '.join(tokenizedText)

        formattedText = re.sub(r'\s+', ' ', formattedText)
        formattedText = re.sub(r'((^\s)|(\s$))', '', formattedText)
        formattedText = re.sub(r'((\s\.)|(\.\s))', '.', formattedText)

        formattedText = re.sub(r'' + self.__dictionary.stop + '', '\n', formattedText)
        formattedText = re.sub(r'\n+', '\n', formattedText)
        formattedText = re.sub(r'\s\n', '\n', formattedText)
        formattedText = re.sub(r'\n\s', '\n', formattedText)
        formattedText = re.sub(r'\n+', '\n', formattedText)
        formattedText = re.sub(r'^\n', '', formattedText)
        formattedText = re.sub(r'\n$', '', formattedText)

        formattedText = formattedText.split('\n')
        formattedText = formattedText[0]

        formattedText = formattedText.replace('...', ' … ')
        formattedText = formattedText.replace('?', '?.')
        formattedText = formattedText.replace('!', '!.')
        formattedText = formattedText.replace(',.', '.')
        formattedText = formattedText.replace('…', '….')
        formattedText = re.sub(r'[\.]+', '.', formattedText)
        formattedText = re.sub(r'((^\.)|(\.$))', '', formattedText)

        formattedText = formattedText.split('.')

        for sentenceCountIndex, sentence in enumerate(formattedText) :
            sentence = re.sub(r'\s+', ' ', sentence)
            sentence = re.sub(r'((^\s)|(\s$))', '', sentence)
            sentence = re.sub(r'\s([,;:?!]{1})', r'\g<1>', sentence)
            sentence = re.sub(r'^- ', '', sentence)
            sentence = re.sub(r'^– ', '', sentence)
            sentence = sentence.capitalize() 

            formattedText[sentenceCountIndex] = sentence

        formattedText = '. '.join(formattedText)# + '.'

        formattedText = re.sub(r'\s+', ' ', formattedText)
        formattedText = re.sub(r'((^\s)|(\s$))', '', formattedText)

        formattedText = formattedText.replace('?.', '?')
        formattedText = formattedText.replace('!.', '!')
        formattedText = formattedText.replace('….', '…')
        formattedText = formattedText.replace(',-', ' -')

        formattedText = re.sub(r'\s+', ' ', formattedText)
        formattedText = re.sub(r'((^\s)|(\s$))', '', formattedText)

        formattedText = re.sub(r'" ([^"]+) "', r'"\g<1>"', formattedText)
        formattedText = re.sub(r'\( ([^\(\)]+) \)', r'(\g<1>)', formattedText)

        return formattedText
