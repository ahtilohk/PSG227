# The aim of the program is to go through each sub-corpus of the text corpus ENC2019 
# sentence by sentence and to find the frequencies of test words in the given patterns.

from estnltk.corpus_processing.parse_enc import parse_enc_file_iterator
import os

with open("test_words.txt", mode = "r", encoding = "utf-8-sig") as f_in:
    words = f_in.readlines()
    test_words = [word.strip() for word in words]

special_words = ['hakanud', 'keeranud', 'pandud', 'osanud', 'tahtnud']

leena_words = "ainult|alati|algul|alla|alles|alt|ammu|edasi|edaspidi|eelkõige|eemale|ees|ega|ehk|ei|eile|eks|enamasti|enam|enne|eriti|esialgu|esile|esiteks|esmalt|ette|harva|heaks|hiljem|homme|ikkagi|ikka|ilmselt|isegi|ise|jalga|ja|juba|just|juurde|ju|jälle|järele|ka|kaasa|kas|kauaks|kaua|kinni|kohale|kohapeal|kohe|kokku|kord|kuhugi|kuhu|kui|kuidagi|kuidas|kuigi|kunagi|kus|kusagil|kusagilt|kusjuures|kuskilt|kust|kõige|kõigepealt|kõrvale|külge|küll|las|ligi|läbi|maha|miks|mil|millal|mistõttu|mitte|muidugi|muidu|mullu|mõnikord|mööda|nagu|niisiis|nii|nimelt|nõnda|näiteks|nüüd|ometi|otsa|paraku|peagi|peale|pealt|pigem|praegu|pärast|ringi|sageli|samas|samuti|sealhulgas|seal|sealt|see-eest|seega|seejuures|seejärel|seekord|seepärast|seetõttu|sellepärast|seni|siia|siiani|siin|siinkohal|siis|siiski|siit|sinna|sisse|sugugi|taas|taga|tagant|tagasi|tahes|tegelikult|tihti|tulenevalt|tõesti|täis|tänaseks|täna|tänavu|vahele|vahel|vahepeal|vaid|vaja|varem|varsti|vastu|veel|vist|võib-olla|võibolla|või|välja|väljas|ära|ülal|üldse|üleeile|üle|üles|üleval|ümber"

leena_words = leena_words.split('|')

path = r'C:\Users\ahti.lohk\Documents\Anaconda Projects\Projekt_PSG227\Corpus_ENC2019'

k = 0
for root, dirs, files in os.walk(path):
    for input_file in files:
        print(input_file)  # print subcorpora name
        with open(input_file[:-5] + "_V2.txt", mode = 'w', encoding='utf-8') as f_output:

            # iterate over corpus and extract Text objects one-by-one
            for text_obj in parse_enc_file_iterator(path + '\\' + input_file, line_progressbar='ascii', tokenization='preserve', original_layer_prefix='original_', restore_morph_analysis=True):
                
                for sentence in text_obj.original_sentences:
                    words = sentence.original_words.text
                    
                    lemmas = sentence.original_morph_analysis.lemma
                    lemmas = [lemma[0] for lemma in lemmas]
                    
                    postags = sentence.original_morph_analysis.partofspeech
                    postags = [postag[0] for postag in postags]
                    
                    forms = sentence.original_morph_analysis.form
                    forms = [form[0] for form in forms]
                    
                    n = len(words)
    
                    for i in range(0, n):
                        
                        if i < n-1:
                        
                            if isinstance(lemmas[i], str):
                            
                                if lemmas[i].lower() in test_words or words[i].lower() in special_words:
                                    
                                    word_lemma = words[i].lower() if words[i].lower() in special_words else lemmas[i].lower() 
                           
                                    if postags[i+1] == 'S':
                                    
                                        if forms[i] == forms[i+1]:
                                            result = "test+S_INFL:" + words[i] + ' ' + words[i+1] + "|" + word_lemma + ' ' + forms[i]
                                            f_output.write(result + "\n")
                                        
                                        if i == 0:
                                            result = "SB_test+S:" + words[i] + ' ' + words[i+1] + "|" + word_lemma
                                            f_output.write(result + "\n")
                                            
                                        result = "test+S:" + words[i] + ' ' + words[i+1] + "|" + word_lemma
                                        f_output.write(result + "\n")

                                
                            if isinstance(lemmas[i+1], str): 
                                
                                word_lemma = words[i+1].lower() if words[i+1].lower() in special_words else lemmas[i+1].lower() 
                                                                
                                if postags[i] == 'D' and  (lemmas[i+1].lower() in test_words or words[i+1].lower() in special_words):
                                    
                                    result = "D+test:" + words[i] + ' ' + words[i+1] + "|" + word_lemma 
                                    f_output.write(result + "\n")
                                
                                if postags[i] == 'D' and words[i].lower() not in leena_words and  (lemmas[i+1].lower() in test_words or words[i+1].lower() in special_words):
                                    
                                    result = "D+test(L):" + words[i] + ' ' + words[i+1] + "|" + word_lemma 
                                    f_output.write(result + "\n")
     
                                if words[i].lower() == "ei" and (lemmas[i+1].lower() in test_words or words[i+1].lower() in special_words):
                                    f_output.write(result + "\n")
                                    result = "EI+test:" + words[i] + ' ' + words[i+1] + "|" + word_lemma 
                               
                            if i < n-3 and isinstance(words[i+1], str) and isinstance(lemmas[i+1], str) and \
                                           isinstance(words[i+2], str) and isinstance(lemmas[i+2], str) and \
                                           isinstance(words[i+3], str) and isinstance(lemmas[i+3], str):
                                
                                if postags[i] == "V" and postags[i+3] == "S" and lemmas[i+2] in test_words:
                                    result = "V+{}+test+S:".format(postags[i+1]) + words[i] + ' ' + words[i+1] + ' ' + words[i+2] + ' ' + words[i+3] + "|" + lemmas[i+2] 
                                    f_output.write(result + "\n")
