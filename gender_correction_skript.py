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

    for index in range(len(original_tagged_sentences)):

        verb = 'POS=V' in original_tagged_sentences[index]['tag']
        past_tense = 'Ten=R' in original_tagged_sentences[index]['tag']
        # num = 'Num=S' in original_tagged_sentences[index]['tag']

        if verb and past_tense:
            female = 'Gen=Q' in original_tagged_sentences[index]['tag'] or 'Gen=F' in original_tagged_sentences[index]['tag']
            male = 'Gen=Y' in original_tagged_sentences[index]['tag'] or 'Gen=Y' in original_tagged_sentences[index]['tag'] or 'Gen=I' in original_tagged_sentences[index]['tag']

            if index > 0:
                if original_tagged_sentences[index - 1]['token'] == 'jsi' or original_tagged_sentences[index - 1]['token'] == 'bys' or original_tagged_sentences[index - 1]['token'] == 'ses' or original_tagged_sentences[index + 1]['token'] == 'sis' or original_tagged_sentences[index - 1]['token'] == 'jste' or original_tagged_sentences[index - 1]['token'] == 'byste':
                   
                    if YOU == 'F' and male: 
                        sentences_to_change[index]['token'] = str(original_tagged_sentences[index]['token']) + 'a'
                        
                    if YOU == 'M' and female:
                        sentences_to_change[index]['token'] = original_tagged_sentences[index]['token'][:-1] 

                if original_tagged_sentences[index - 1]['token'] == 'jsem' or original_tagged_sentences[index - 1]['token'] == 'bych':

                    if ME == 'F' and male: 
                        sentences_to_change[index]['token'] = str(original_tagged_sentences[index]['token']) + 'a'

                    if ME == 'M' and female:
                        sentences_to_change[index]['token'] = original_tagged_sentences[index]['token'][:-1] 
      


            if index < len(original_tagged_sentences):
                if original_tagged_sentences[index + 1]['token'] == 'jsi' or original_tagged_sentences[index + 1]['token'] == 'bys' or original_tagged_sentences[index + 1]['token'] == 'ses' or original_tagged_sentences[index + 1]['token'] == 'sis' or original_tagged_sentences[index + 1]['token'] == 'jste' or original_tagged_sentences[index + 1]['token'] == 'byste':
                    if YOU == 'F' and male: 
                        sentences_to_change[index]['token'] = str(original_tagged_sentences[index]['token']) + 'a'
                    
                    if YOU == 'M' and female:
                        sentences_to_change[index]['token'] = original_tagged_sentences[index]['token'][:-1] 

                if original_tagged_sentences[index + 1]['token'] == 'jsem' or original_tagged_sentences[index + 1]['token'] == 'bych':
                    if ME == 'F' and male: 
                        sentences_to_change[index]['token'] = str(original_tagged_sentences[index]['token']) + 'a'
                    
                    if ME == 'M' and female:
                        sentences_to_change[index]['token'] = original_tagged_sentences[index]['token'][:-1] 
                        
     
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
