import requests, json

f = open("dialog.txt", "r")
#appending all sentences to a list
test_data = []
bugs = []

for line in f:
    stripped_line = line.strip()
    test_data.append(stripped_line)
    # if stripped_line != '':
    #     all.append(stripped_line)
f.close()

YOU = 'M'
ME = 'M'

YOU = input('What gender do you want to use for the second person ("you"/"ty")? Enter either F or M: ')
ME = input('What gender do you want to use for the first person ("já"/"I")? Enter either F or M: ')

'/ / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / '

def gender_corrector(str_to_post_edit, YOU, ME):
    # the first parameter is a string you want to post-edit
    # the second parameter is gender for 2nd person in this sring.
    # the third parameter is gender for 1st person in this sring.
    # don't forget to 'import requests, json'

    my_response = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/tag?data=" + str(str_to_post_edit) + "&convert_tagset=pdt_to_conll2009&output=json")
    my_response.encoding = 'utf8'

    tagged = json.loads(my_response.text)
    #merging multiple tagged sentences into one list without list-in-a-list structure

    original_tagged_sentences = []

    for bracket in tagged['result']:
        for element in bracket:
            original_tagged_sentences.append(element)
    
    sentences_to_change = original_tagged_sentences.copy()

    length = len(original_tagged_sentences)
 
    our_range = 4

    for cur in range(length):

        verb = 'POS=V' in original_tagged_sentences[cur]['tag']
        past_tense = 'Ten=R' in original_tagged_sentences[cur]['tag']

        # if the word is already changed = don't change it condition
        word_is_not_changed = True if original_tagged_sentences[cur]['token'] == sentences_to_change[cur]['token'] else False

        for step in range(1, our_range):
            female = 'Gen=Q' in original_tagged_sentences[cur]['tag'] or 'Gen=F' in original_tagged_sentences[cur]['tag']
            male = 'Gen=Y' in original_tagged_sentences[cur]['tag'] or 'Gen=I' in original_tagged_sentences[cur]['tag'] or 'Gen=M' in original_tagged_sentences[cur]['tag']

            backwards = True if cur - step >= 0 else False
            further = True if cur + step < length else False
            #cur_less_than_zero =  True if step >= 0 else False

            # JSEM-JSI RÁD CASE
            if original_tagged_sentences[cur]['token'].lower() == 'jsi' and further:
                if original_tagged_sentences[cur + step]['token'].lower() == 'ráda' and YOU == 'M':
                    sentences_to_change[cur + step]['token'] = str(original_tagged_sentences[cur + step]['token'])[:-1]
                    word_is_not_changed = True if original_tagged_sentences[cur + step]['token'] == sentences_to_change[cur + step]['token'] else False

                if original_tagged_sentences[cur + step]['token'].lower() == 'rád' and YOU == 'F':
                    sentences_to_change[cur + step]['token'] = str(original_tagged_sentences[cur + step]['token']) + 'a'
                    word_is_not_changed = True if original_tagged_sentences[cur + step]['token'] == sentences_to_change[cur + step]['token'] else False

            if original_tagged_sentences[cur]['token'].lower() == 'jsem' and further:
                if original_tagged_sentences[cur + step]['token'].lower() == 'ráda' and YOU == 'M':
                    sentences_to_change[cur + step]['token'] = str(original_tagged_sentences[cur + step]['token'])[:-1]
                    word_is_not_changed = True if original_tagged_sentences[cur + step]['token'] == sentences_to_change[cur + step]['token'] else False

                if original_tagged_sentences[cur + step]['token'].lower() == 'rád' and YOU == 'F':
                    sentences_to_change[cur + step]['token'] = str(original_tagged_sentences[cur + step]['token']) + 'a'
                    word_is_not_changed = True if original_tagged_sentences[cur + step]['token'] == sentences_to_change[cur + step]['token'] else False
            
            
            # MÍT RÁD CASE - .... missing/to be done

            # ADJECTIVES

            if original_tagged_sentences[cur]['token'].lower() in ('buď','buďte','jsi','jsem') and further:
           
                male_2 = 'Gen=M' in original_tagged_sentences[cur + step]['tag']
                female_2 = 'Gen=F' in original_tagged_sentences[cur + step]['tag'] or 'Gen=Q' in original_tagged_sentences[cur + step]['tag']

                if 'POS=A' in original_tagged_sentences[cur + step]['tag'] and YOU == 'F' and male_2 and word_is_not_changed:
                    sentences_to_change[cur + step]['token'] = str(original_tagged_sentences[cur + step]['token'])[:-1] + 'á'
                    word_is_not_changed = True if original_tagged_sentences[cur + step]['token'] == sentences_to_change[cur + step]['token'] else False
                if 'POS=A' in original_tagged_sentences[cur + step]['tag'] and YOU == 'M' and female_2 and word_is_not_changed:
                    sentences_to_change[cur + step]['token'] = str(original_tagged_sentences[cur + step]['token'])[:-1] + 'ý'
                    word_is_not_changed = True if original_tagged_sentences[cur + step]['token'] == sentences_to_change[cur + step]['token'] else False
                
                if 'POS=A' in original_tagged_sentences[cur + step]['tag'] and ME == 'F' and male_2 and word_is_not_changed and original_tagged_sentences[cur + step]['token'] != 'rád':
                    sentences_to_change[cur + step]['token'] = str(original_tagged_sentences[cur + step]['token'])[:-1] + 'á'
                    word_is_not_changed = True if original_tagged_sentences[cur + step]['token'] == sentences_to_change[cur + step]['token'] else False
                if 'POS=A' in original_tagged_sentences[cur + step]['tag'] and ME == 'M' and female_2 and word_is_not_changed and original_tagged_sentences[cur + step]['token'] != 'ráda':
                    sentences_to_change[cur + step]['token'] = str(original_tagged_sentences[cur + step]['token'])[:-1] + 'ý'
                    word_is_not_changed = True if original_tagged_sentences[cur + step]['token'] == sentences_to_change[cur + step]['token'] else False


            word_is_not_changed = True

            # VERBS
            if verb and past_tense:

                if backwards and word_is_not_changed:
                    if original_tagged_sentences[cur - step]['token'].lower() in ('jsi', 'jste', 'bys', 'byste', 'sis', 'ses'):
                               
                        if YOU == 'F' and male: 
                            sentences_to_change[cur]['token'] = str(original_tagged_sentences[cur]['token']) + 'a'
                            word_is_not_changed = True if original_tagged_sentences[cur]['token'] == sentences_to_change[cur]['token'] else False
                            
                        if YOU == 'M' and female: 
                            sentences_to_change[cur]['token'] = original_tagged_sentences[cur]['token'][:-1]
                            word_is_not_changed = True if original_tagged_sentences[cur]['token'] == sentences_to_change[cur]['token'] else False

                    if original_tagged_sentences[cur - step]['token'].lower() in ('jsem','bych'):

                        if ME == 'F' and male: 
                            sentences_to_change[cur]['token'] = str(original_tagged_sentences[cur]['token']) + 'a'
                            word_is_not_changed = True if original_tagged_sentences[cur]['token'] == sentences_to_change[cur]['token'] else False

                        if ME == 'M' and female:
                            sentences_to_change[cur]['token'] = original_tagged_sentences[cur]['token'][:-1] 
                            word_is_not_changed = True if original_tagged_sentences[cur]['token'] == sentences_to_change[cur]['token'] else False
                        
                
                
                if further and word_is_not_changed:
                    if original_tagged_sentences[cur + step]['token'].lower() in ('jste','jsi', 'bys', 'byste', 'ses', 'sis'):
                    
                        if YOU == 'F' and male: 
                            sentences_to_change[cur]['token'] = str(original_tagged_sentences[cur]['token']) + 'a'
                            word_is_not_changed = True if original_tagged_sentences[cur]['token'] == sentences_to_change[cur]['token'] else False
                            
                        if YOU == 'M' and female:
                            sentences_to_change[cur]['token'] = original_tagged_sentences[cur]['token'][:-1] 
                            word_is_not_changed = True if original_tagged_sentences[cur]['token'] == sentences_to_change[cur]['token'] else False

                    if original_tagged_sentences[cur + step]['token'].lower() in ('jsem','bych'):

                        if ME == 'F' and male: 
                            sentences_to_change[cur]['token'] = str(original_tagged_sentences[cur]['token']) + 'a'
                            word_is_not_changed = True if original_tagged_sentences[cur]['token'] == sentences_to_change[cur]['token'] else False

                        if ME == 'M' and female:
                            sentences_to_change[cur]['token'] = original_tagged_sentences[cur]['token'][:-1]
                            word_is_not_changed = True if original_tagged_sentences[cur]['token'] == sentences_to_change[cur]['token'] else False
                        
                 
    final_string_list = []

    for item in sentences_to_change:
        final_string_list.append(item['token'])
        if 'space' in item:
            final_string_list.append(item['space'])
    
    final_string = ''.join(final_string_list)

    print('final string returned: ' + final_string)
    return final_string
'/ / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / / '

ttt = open("result.txt", "w")

for string in test_data:
    ttt.write(gender_corrector(string, YOU, ME) + '\n')
    
ttt.close()
