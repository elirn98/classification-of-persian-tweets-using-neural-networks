import re
from preprocessing.constances import ConstantVars

compile_patterns = lambda patterns: [(re.compile(pattern), repl) for pattern, repl in patterns]


class Tokenizer:
    def __init__(self):
        self.alphabet = ['پ', 'چ', 'ج', 'ح', 'خ', 'ه', 'ع', 'غ', 'ف', 'ق', 'ث', 'ص', 'ض', 'گ', 'ک', 'م', 'ن', 'ت', 'ا',
                         'ل', 'ب', 'آ',
                         'ی', 'س', 'ش', 'و', 'ئ', 'د', 'ذ', 'ر', 'ز', 'ط', 'ظ', 'أ', 'ژ', '\u200c', 'ُ', 'ّ', 'ة', 'ۀ',
                         'ؤ', 'ء', 'إ']
        self.constants = ConstantVars()

        self.after_verbs = {'ام', 'ای', 'ایم', 'اید', 'اند'}

        self.before_verbs = {'می', 'نمی'}

        self.suffixes = {'ی', 'ای', 'ها', 'های', 'تر', 'تری', 'ترین', 'گر', 'گری', 'ام', 'ات', 'اش'}

        self.expression = []
        self.expression.extend(
            [('علی ای حال', 'علی\u200cای\u200cحال'), ('بنا بر این', 'بنابراین'), ('بنابر این', 'بنابراین'),
             ('مع ذالک', 'مع\u200cذالک'),
             ('فی ما بین', 'فی\u200cمابین'), ('فی مابین', 'فی\u200cمابین'), ('چنان چه', 'چنان\u200cچه'),
             ('در واقع', 'درواقع'), ('فی کل حال', 'فی\u200cکل\u200cحال'), ])
        self.expression = compile_patterns(self.expression)

    def word_tokenize(self, sentence):
        sentence = self.expression_corrector(sentence)
        splits = sentence.split(' ')
        sentence = ' '.join(self.token_spacing(splits))
        splits = sentence.split(' ')
        split = []
        i = 0
        j = 0
        for s in splits:
            if s != '':
                string = ''
                string2 = ''
                for w in s:
                    if w in self.alphabet:
                        string = string + w
                    else:
                        string2 = string2 + w
                if s[0] in self.alphabet:
                    if string != '':
                        split.append(string)
                    if string2 != '':
                        string2 = re.sub(r'(.)\1+', r'\1', string2, re.UNICODE)
                        count = 0
                        for st in string2:
                            if st in self.constants.punctuations() + ['\"', '!']:
                                count += 1
                        if count == len(string2):
                            for st in string2[:len(string2)]:
                                split.append(st)
                        else:
                            split.append(string2)
                else:
                    if string2 != '':
                        string2 = re.sub(r'(.)\1+', r'\1', string2, re.UNICODE)
                        count = 0
                        for st in string2:
                            if st in self.constants.punctuations() + ['\"', '!']:
                                count += 1
                        if count == len(string2):
                            for st in string2[:len(string2)]:
                                split.append(st)
                        else:
                            split.append(string2)
                    if string != '':
                        split.append(string)
        return split

    def token_spacing(self, tokens):
        result = []
        for t, token in enumerate(tokens):
            joined = False
            token_pair = ''
            if result:
                token_pair = result[-1] + '\u200c' + token

                if token in self.suffixes:
                    joined = True

                elif result[-1] in self.before_verbs:
                    joined = True

                elif token in self.after_verbs:
                    joined = True

            if joined:
                result.pop()
                result.append(token_pair)
            else:
                result.append(token)

        return result

    def expression_corrector(self, text):
        for pattern, repl in self.expression:
            text = pattern.sub(repl, text)
        return text
