import re

compile_patterns = lambda patterns: [(re.compile(pattern), repl) for pattern, repl in patterns]


class Normalizer:
    def __init__(self, space_correction=True, persian_style=True, persian_character=True, emoji=True):
        # arabic charecters and half-space
        if persian_character:
            translation_src, translation_dst = '\u0622\u0623\u0625\u0624\u064A\u0626\u06c2\u0629\u200F', \
                                               '\u0627\u0627\u0627\u0648\u06cc\u06cc\u0647\u0647\u200c'
            translation_src += '0123456789%“”'
            translation_dst += '۰۱۲۳۴۵۶۷۸۹٪""'

            maketrans = lambda A, B: dict((ord(a), b) for a, b in zip(A, B))
            self.translations = maketrans(translation_src, translation_dst)

        punc_after, punc_before = r'\.:!،؛؟»\]\)\}', r'«\[\(\{'
        self.spaces = []
        if space_correction:
            self.spaces.extend([
                (r' +', ' '),  # remove extra spaces
                (r'\n\n+', '\n\n'),  # remove extra newlines
                (r'[ـ\r]', ''),  # remove keshide, carriage returns
                ('" ([^\n"]+) "', r'"\1"'),  # remove space before and after quotation
                (' ([' + punc_after + '])', r'\1'),  # remove space before
                ('([' + punc_before + ']) ', r'\1'),  # remove space after
                ('([' + punc_after[:3] + '])([^ \d' + punc_after + '])', r'\1 \2'),  # put space after . and :
                ('([' + punc_after[3:] + '])([^ ' + punc_after + '])', r'\1 \2'),  # put space after
                ('([^ ' + punc_before + '])([' + punc_before + '])', r'\1 \2'),  # put space before
            ])
            self.spaces = compile_patterns(self.spaces)

        self.character_refinement_patterns = []
        if persian_style:
            self.character_refinement_patterns.extend([
                ('"([^\n"]+)"', r'«\1»'),  # replace quotation with gyoome
                ('([\d+])\.([\d+])', r'\1٫\2'),  # replace dot with momayez
                (r' ?\.\.\.', ' …'),  # replace 3 dots
            ])
            self.character_refinement_patterns.append(
                ('[\u0640\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0621]', ''),
                # remove KASHIDA, FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN, HAMZE
            )
            self.character_refinement_patterns = compile_patterns(self.character_refinement_patterns)

        self.emojis = []
        if emoji:
            self.emojis.append(('[\U0001F601\U0001F602\U0001F603\U0001F604\U0001F605\U0001F606\U0001F609'
                                '\U0001F60A\U0001F60B\U0001F60C\U0001F60D\U0001F60F\U0001F612]', ''),)
            self.emojis = compile_patterns(self.emojis)

    def normaliz(self, sentence):
        sentence = self.character_refinement(sentence)
        sentence = self.spacing(sentence)
        sentence = self.emoji_remover(sentence)
        return sentence

    def character_refinement(self, text):
        text = text.translate(self.translations)
        for pattern, repl in self.character_refinement_patterns:
            text = pattern.sub(repl, text)
        return text

    def spacing(self, text):
        for pattern, repl in self.spaces:
            text = pattern.sub(repl, text)
        return text

    def emoji_remover(self, text):
        for pattern, repl in self.emojis:
            text = pattern.sub(repl, text)
        return text
