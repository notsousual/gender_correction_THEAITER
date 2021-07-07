INSTRUCTION: gender_correction_skript.py

This script changes gender distinction between 2 characters in the scenarios.

Copy-paste your scenario into dialog.txt
The final output will be in result.txt as well as in the console

PROBLEMS:
-

Particular qualities:
- works with adjectives; verbs with the 1st/2nd person
- Mít rád case is done


Function gender_corrector(str_to_post_edit, YOU, ME)

The first parameter is a string you want to post-edit.
The second parameter is gender for the 2nd person in this string.
The third parameter is gender for the 1st person in this string.
Don't forget to 'import requests, json'
