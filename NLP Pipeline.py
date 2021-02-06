import pymorphy2
import re
from gensim.models import Phrases
from gensim.models.phrases import Phraser
import glob

morph = pymorphy2.MorphAnalyzer()

print('Морфологическая разметка корпуса текстов со снятой омонимией\n')

swl = open(r'D:\STUDIES\СПбГУ\Семантические анализаторы\Практическое задание\swl.txt', encoding='utf8')

swlist = []
for i in swl:
    i = i.replace('\n','')
    swlist.append(i)
    #print(swlist)

import glob  # создаем список путей к файлам
way = glob.glob("D:\TEST FILES\THESIS\НОВЫЙ КОРПУС\По постам до обработки\*.txt")

for w in way:
    stories = open(w, encoding='utf8').read()
    user = re.findall(r'[VK].+', w)
    f_wr = open(r"D:\\TEST FILES\\THESIS\\НОВЫЙ КОРПУС\\По постам после обработки\\"+str(user[0])+".txt", 'w', encoding='utf8')
    story = []
    text_list = re.findall(r'[а-яёА-ЯЁ\-]+', stories)
    for i in text_list:
        story.append(i)

    normalized = []
    for i in story:
        k = morph.parse(i)[0]
        k = k.normal_form
        if k not in swlist:
            normalized.append(k)

    tok_sent = [normalized]  # добавляем биграммы и триграммы
    bigram = Phrases(tok_sent, min_count=3, threshold = 2, delimiter=b'_')
    trigram = Phrases(bigram[tok_sent], min_count=3, threshold = 2, delimiter=b'_')

    for token in bigram[tok_sent]:
        for i in token:
            if '_' in i:
                if i not in normalized:
                    normalized.append(i)
                else:
                    continue

    for token in trigram[bigram[tok_sent]]:
        for i in token:
            if '_' in i:
                if i not in normalized:
                    normalized.append(i)
                else:
                    continue

    print(normalized, file=f_wr)
    f_wr.close()

    
