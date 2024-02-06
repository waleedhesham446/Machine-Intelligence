from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file,read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]

def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 
    '''
    dictionary_dict = {}
    for word in dictionary:
       dictionary_dict[word] = True
    result = None
    for shift in range(26):
        deciphered = ''
        for c in ciphered:
            if c == ' ':
                deciphered += ' '
            else:
                deciphered += chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
        
        miss = 0
        for d in deciphered.split(' '):
            if dictionary_dict.get(d, None) is None:
                miss += 1
        # print('[X] ', deciphered, shift, miss)
        if result is None or result[2] > miss:
            result = (deciphered, shift, miss)

    return result