# -*- coding: utf-8 -*-
"""
Created on Mon 18 April 12:33:32 202
@author: Ahti Lohk

*** Test-patterns_occurrences_in_ENC2019_without_estnltk_corpus_processing_module ***

The aim of the program is to go through the ENC2019 sub-corpus of each text corpus 
sentence by sentence and to find all occurrences of test words in the given patterns.
The test-patterns statistics are saved in an Excel-file.

The files of the sub-corpora can be found here: 
https://entu.keeleressursid.ee/shared/7769/N66ZdfvwzQuXWIvIjnhVuX74oWmi1zrruZ1VpN8QE1Hj6jbfq5oMBxm8YQDrugyM
"""

import xlsxwriter

def read_file(file_name):
    with open(file_name, mode = "r", encoding = "utf-8") as file_input:
        lines = file_input.readlines()
    words = [word.strip() for word in lines]
    return words

def compose_test_patterns(prev_postag, next_postag, sentence, position):
    patterns = []
    if next_postag == 'S':
        patterns.append('test_S')
        if prev_postag == '.':
            patterns.append('SB_test_S')
        if sentence[position][3] == sentence[position+1][3]:
            patterns.append('test_S_INFL')
        if (position - 2) >= 0 and sentence[position - 2][1] == 'V':
            patterns.append('V_?_test_S')
    if position > 0:
        if sentence[position-1][0].lower() == 'ei':
            patterns.append('EI_test')
        elif sentence[position-1][1] == 'D':
            patterns.append('D_test')
        elif sentence[position-1][2].lower() == 'olema':
            patterns.append('olema_test')
    if position > 1:
        if sentence[position-2][2].lower() == 'olema':
            if sentence[position-1][1] == 'D':
                patterns.append('olema_D_test')
            
    return patterns

def find_test_patterns(test_words, comparatives, patterns_labels, file_names, path):
    
    sentence_started = False
    sentence = []
    test_word_in_sent = False
    taken_flag = False
    position_nr = 0
    positions = []
    words_seq = []

    pattern_dict = {word:{} for word in test_words}
    test_pattern_dict = {word:{} for word in test_words}
    comparative_freq_dict = {word:0 for word in comparatives}

    for file in file_names:
        file = open(path + file, mode = "r", encoding="utf-8")
        print("FILE:", file)
        for line in file:
			
            if sentence_started:
                if "</s>" in line:
                    sentence_started = False
				
                    if test_word_in_sent:
										
                        for i, position in enumerate(positions):
                            prev_position = position - 1
                            next_position = position + 1
							
                            if position == 0:
                                prev_postag = '.'
                            else:
                                prev_postag = sentence[prev_position][1]
								
                            if position == len(sentence) - 1:
                                next_postag = '.'
                            else:
                                next_postag = sentence[next_position][1]
		
                            pattern = prev_postag + "+test+" + next_postag
												
                            pattern_dict[words_seq[i]][pattern] = pattern_dict[words_seq[i]].get(pattern, 0) + 1
							
                            test_patterns = compose_test_patterns(prev_postag, next_postag, sentence, position)
                            if len(test_patterns) > 0:
                                for pattern in test_patterns:
									
                                    try:
                                        test_pattern_dict[words_seq[i]][pattern] = test_pattern_dict[words_seq[i]].get(pattern, 0) + 1
                                    except:
                                        pass
								
                    test_word_in_sent = False
                    position_nr = -1
					
                else:
                    try:
                        word_info = line.split("\t")
                        word = word_info[0].lower()
                        postag = word_info[1][0]
                        form = word_info[1][1:]
                        lemma = word_info[2][:-2].lower()
                        sentence.append((word, postag, lemma, form))
                        
                        taken_flag = False
                        
                        if len(word) > 3 and word[-3:] in ['nud', 'dud', 'tud'] and word in test_words:
                            position_nr = len(sentence) - 1
                            positions.append(position_nr)
                            words_seq.append(word)
                            test_word_in_sent = True
                            taken_flag = True
                        
                        if not taken_flag and lemma in test_words:
                            position_nr = len(sentence) - 1
                            positions.append(position_nr)
                            words_seq.append(lemma)
                            test_word_in_sent = True
						
                        if lemma in comparatives:
                            comparative_freq_dict[lemma] += 1
							
                    except:
                        pass
            else:
					
                if "<s>" in line:
                    sentence_started = True
                    sentence = []
                    position_nr = -1
                    positions = []
                    words_seq = []
                else:
                    pass
		
        file.close()

    return test_pattern_dict, comparative_freq_dict

def write_results_to_Excel_file(test_words, comparatives, pattern_labels, test_pattern_dict, comparative_freq_dict, file_name):

	workbook = xlsxwriter.Workbook(file_name)
	worksheet = workbook.add_worksheet()

	worksheet.write(0, 0, 'WORD')
	for j, pattern in enumerate(pattern_labels):
		worksheet.write(0, j+1, pattern)
		
	i = 0
	for key, values in test_pattern_dict.items():
		i += 1
		worksheet.write(i, 0, key)
		
		for j, pattern in enumerate(pattern_labels):
		   
			worksheet.write(i, j+1, test_pattern_dict[key].get(pattern, 0))
			
			total_freq = sum(test_pattern_dict[key].values())
			prop_80 = 0.8 * total_freq
			ordered_dict = sorted(test_pattern_dict[key].items(), key=lambda x: x[1], reverse=True)
			
			if len(ordered_dict) > 0:
				total = 0
				
				for k, item in enumerate(ordered_dict):
					total += item[1]
					if total > prop_80:
						worksheet.write(i, len(pattern_labels) + 1, str(total_freq) + ": " + str(ordered_dict[:k+1]))
						break

	i = len(test_words) + 2
	for word in comparatives:
		i+=1
		worksheet.write(i, 0, word)
		worksheet.write(i, 1, comparative_freq_dict[word])

	workbook.close()

	return


if __name__ == "__main__":

    test_words = read_file("test_words.txt")   
    comparatives = read_file("comparatives_of_test_words.txt")
	
    output_filename = "test_patterns_results.xlsx"
    
    path = r"C:\Users\ahti.lohk\Documents\Anaconda Projects\Projekt_PSG227\Corpus_ENC2019\\"
    pattern_labels = ['test_S', 'test_S_INFL', 'SB_test_S', 'V_?_test_S', 'D_test', 'EI_test', 'olema_test', 'olema_D_test']
	
    file_names = ['etnc19_doaj.vert', 'etnc19_balanced_corpus.vert', 'etnc19_wikipedia_2019.vert', 
	'etnc19_wikipedia_2017.vert', 'etnc19_reference_corpus.vert', 'etnc19_web_2013.vert', 
	'etnc19_web_2019.vert', 'etnc19_web_2017.vert']
	
    test_pattern_dict, comparative_freq_dict = find_test_patterns(test_words, comparatives, pattern_labels, file_names, path)
    write_results_to_Excel_file(test_words, comparatives, pattern_labels, test_pattern_dict, comparative_freq_dict, output_filename)
