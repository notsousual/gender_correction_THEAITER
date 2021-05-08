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

    searched_form = 'ERROR'
    current_sentence = str_to_post_edit
    all = [str(str_to_post_edit)]


    my_response = requests.get("http://lindat.mff.cuni.cz/services/morphodita/api/tag?data=" + all[0] + "&convert_tagset=pdt_to_conll2009&output=json")
    my_response.encoding = 'utf8'

    tagged = json.loads(my_response.text)

    tagged_sentence = []

    for i in tagged['result']:
        tagged_sentence.append(i)

    # тут 2 + листа с тегами в листе

    tagged_sentences = []

    #merging multiple tagged sentences into one list without list-in-a-list structure

    for lists in tagged_sentence:
        for element in lists:
            tagged_sentences.append(element)

    sentences_list_to_change = tagged_sentences.copy()

    # print(sentences_list_to_change)

    for index in range(len(tagged_sentences)):
        verb = 'POS=V' in tagged_sentences[index]['tag']
        past_tense = 'Ten=R' in tagged_sentences[index]['tag']
        # num = 'Num=S' in tagged_sentences[index]['tag']

        if verb and past_tense:
            female = 'Gen=Q' in tagged_sentences[index]['tag'] or 'Gen=F' in tagged_sentences[index]['tag']
            male = 'Gen=Y' in tagged_sentences[index]['tag'] or 'Gen=Y' in tagged_sentences[index]['tag'] or 'Gen=I' in tagged_sentences[index]['tag']

            if index > 0:
                if tagged_sentences[index - 1]['token'] == 'jsi' or tagged_sentences[index - 1]['token'] == 'bys' or tagged_sentences[index - 1]['token'] == 'ses' or tagged_sentences[index + 1]['token'] == 'sis' or tagged_sentences[index - 1]['token'] == 'jste' or tagged_sentences[index - 1]['token'] == 'byste':
                   
                    if YOU == 'F' and male: 
                        sentences_list_to_change[index]['token'] = str(tagged_sentences[index]['token']) + 'a'
                        
                    if YOU == 'M' and female:
                        sentences_list_to_change[index]['token'] = tagged_sentences[index]['token'][:-1] 

                if tagged_sentences[index - 1]['token'] == 'jsem' or tagged_sentences[index - 1]['token'] == 'bych':

                    if ME == 'F' and male: 
                        sentences_list_to_change[index]['token'] = str(tagged_sentences[index]['token']) + 'a'

                    if ME == 'M' and female:
                        sentences_list_to_change[index]['token'] = tagged_sentences[index]['token'][:-1] 
      


            if index < len(tagged_sentences):
                if tagged_sentences[index + 1]['token'] == 'jsi' or tagged_sentences[index + 1]['token'] == 'bys' or tagged_sentences[index + 1]['token'] == 'ses' or tagged_sentences[index + 1]['token'] == 'sis' or tagged_sentences[index + 1]['token'] == 'jste' or tagged_sentences[index + 1]['token'] == 'byste':
                    if YOU == 'F' and male: 
                        sentences_list_to_change[index]['token'] = str(tagged_sentences[index]['token']) + 'a'
                    
                    if YOU == 'M' and female:
                        sentences_list_to_change[index]['token'] = tagged_sentences[index]['token'][:-1] 

                if tagged_sentences[index + 1]['token'] == 'jsem' or tagged_sentences[index + 1]['token'] == 'bych':
                    if ME == 'F' and male: 
                        sentences_list_to_change[index]['token'] = str(tagged_sentences[index]['token']) + 'a'
                    
                    if ME == 'M' and female:
                        sentences_list_to_change[index]['token'] = tagged_sentences[index]['token'][:-1] 
                        
     
    final_string_list = []

    for item in sentences_list_to_change:
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
