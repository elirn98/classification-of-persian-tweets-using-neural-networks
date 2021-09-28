from os import path

data_path = path.join(path.dirname(__file__), 'data')
print(data_path)
default_words = path.join(data_path, 'words.dat')
default_verbs = path.join(data_path, 'verbs.dat')


class Lematizer():
    def __init__(self):
        self.verbs = {}
        self.words = default_words
        self.verbs['است'] = '#است'
        default_verb = open('./data/verbs.dat', 'r', newline='\n', encoding='utf-8')

        for verb in default_verb:
            for tense in self.conjugations(verb):
                self.verbs[tense] = verb
        self.after_verbs = {'ام', 'ای', 'است', 'ایم', 'اید', 'اند', 'بودم', 'بودی', 'بود', 'بودیم', 'بودید', 'بودند',
                            'باشم', 'باشی', 'باشد', 'باشیم', 'باشید', 'باشند', 'شده_ام', 'شده_ای', 'شده_است', 'شده_ایم',
                            'شده_اید', 'شده_اند', 'شده_بودم', 'شده_بودی', 'شده_بود', 'شده_بودیم', 'شده_بودید',
                            'شده_بودند', 'شده_باشم', 'شده_باشی', 'شده_باشد', 'شده_باشیم', 'شده_باشید', 'شده_باشند',
                            'نشده_ام', 'نشده_ای', 'نشده_است', 'نشده_ایم', 'نشده_اید', 'نشده_اند', 'نشده_بودم',
                            'نشده_بودی', 'نشده_بود', 'نشده_بودیم', 'نشده_بودید', 'نشده_بودند', 'نشده_باشم', 'نشده_باشی',
                            'نشده_باشد', 'نشده_باشیم', 'نشده_باشید', 'نشده_باشند', 'شوم', 'شوی', 'شود', 'شویم', 'شوید',
                            'شوند', 'شدم', 'شدی', 'شد', 'شدیم', 'شدید', 'شدند', 'نشوم', 'نشوی', 'نشود', 'نشویم',
                            'نشوید', 'نشوند', 'نشدم', 'نشدی', 'نشد', 'نشدیم', 'نشدید', 'نشدند', 'می‌شوم', 'می‌شوی',
                            'می‌شود', 'می‌شویم', 'می‌شوید', 'می‌شوند', 'می‌شدم', 'می‌شدی', 'می‌شد', 'می‌شدیم',
                            'می‌شدید', 'می‌شدند', 'نمی‌شوم', 'نمی‌شوی', 'نمی‌شود', 'نمی‌شویم', 'نمی‌شوید', 'نمی‌شوند',
                            'نمی‌شدم', 'نمی‌شدی', 'نمی‌شد', 'نمی‌شدیم', 'نمی‌شدید', 'نمی‌شدند', 'خواهم_شد', 'خواهی_شد',
                            'خواهد_شد', 'خواهیم_شد', 'خواهید_شد', 'خواهند_شد', 'نخواهم_شد', 'نخواهی_شد', 'نخواهد_شد',
                            'نخواهیم_شد', 'نخواهید_شد', 'نخواهند_شد'}

        self.before_verbs = {'خواهم', 'خواهی', 'خواهد', 'خواهیم', 'خواهید', 'خواهند', 'نخواهم', 'نخواهی', 'نخواهد',
                             'نخواهیم', 'نخواهید', 'نخواهند'}

        for verb in default_verbs:
            bon = verb.split('#')[0]
            for after_verb in self.after_verbs:
                self.verbs[bon + 'ه_' + after_verb] = verb
                self.verbs['ن' + bon + 'ه_' + after_verb] = verb
            for before_verb in self.before_verbs:
                self.verbs[before_verb + '_' + bon] = verb

    def lemmatize(self, word):
        if word in self.verbs:
            return self.verbs[word][:len(self.verbs[word])-2]
        return word

    def conjugations(self, verb):
        past, present = verb.split('#')
        present = present[:len(present)-2]
        ends = ['م', 'ی', '', 'یم', 'ید', 'ند']

        if verb == '#هست':
            return ['هست' + end for end in ends] + ['نیست' + end for end in ends]

        past_simples = [past + end for end in ends]
        past_imperfects = ['می‌' + item for item in past_simples]
        ends = ['ه‌ام', 'ه‌ای', 'ه', 'ه‌ایم', 'ه‌اید', 'ه‌اند']
        past_narratives = [past + end for end in ends]

        imperatives = ['ب' + present, 'ن' + present]

        if present.endswith('ا') or present in ('آ', 'گو'):
            present = present + 'ی'

        ends = ['م', 'ی', 'د', 'یم', 'ید', 'ند']
        present_simples = [present + end for end in ends]
        present_imperfects = ['می‌' + item for item in present_simples]
        present_subjunctives = [item if item.startswith('ب') else 'ب' + item for item in present_simples]
        present_not_subjunctives = ['ن' + item for item in present_simples]

        with_nots = lambda items: items + list(map(lambda item: 'ن' + item, items))
        aa_refinement = lambda items: list(map(lambda item: item.replace('بآ', 'بیا').replace('نآ', 'نیا'), items)) if \
        items[0].startswith('آ') else items
        return aa_refinement(
            with_nots(past_simples) + with_nots(present_simples) + with_nots(past_imperfects) + with_nots(
                past_narratives) + with_nots(present_simples) + with_nots(
                present_imperfects) + present_subjunctives + present_not_subjunctives + imperatives)
