class CaesarCipher(object):
    """ A CaesarCpher class blueprint with the functionalities"""

    def __init__(self):
        """ letter_freq: a dict of letters as keys and corresponding probability as value """
        self.letter_freq = {}
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.set_letter_dict()
    
    def set_letter_dict(self):
        """ sets letter frequency in english words as probabilities"""
        prob_letter = [8.2,1.5,2.7,4.7,13,2.2,2,6.2,6.9,0.16,0.81,4,2.7,6.7,7.8,1.9,0.11,5.9,6.2,9.6,2.7,0.97,2.4,0.15,2,0.078]
        for i,j in zip(self.alphabet, prob_letter): 
            self.letter_freq[i] = round(j/100,6)
            
    def decryx(self, txt):
        """decryx(self, txt) is called by a helper function from main with the string as parameter"""
        l = len(txt)
        chi_sq = {} # dictionary to store the shift index, shifted string 

        for i in range(25):       
            """ Makes 26 strings, each shifted accordingly and finds the chi squared value for each and is stored in chi_sq = {} """    
            
            #finds the shifted result as a list comprehension
            shifted = ''.join([self.alphabet[self.alphabet.index(ch.upper()) - i] if ch.upper() in self.alphabet else ch for ch in txt])
            
            #finds chi squared values as a list comprehension
            chi = sum([(shifted.count(_)-self.letter_freq[_]*l)**2 / (self.letter_freq[_]*l) for _ in self.alphabet])

            chi_sq[chi]=(i, shifted)     

        chi_sort =  sorted(chi_sq.keys())   # sorted in order of chi squared value
        _, best_shift = chi_sq[chi_sort[0]]   # returns the string with the least chi squared value
        
        return best_shift

#class definition ends here        

def decrypt_cipher(text):
    """creates a Caesar object and passes the string, this function acts as a helper function"""
    c = CaesarCipher()
    return c.decryx(text)

# trial run:
# if __name__  == "__main__":
#     text = "efgfoe uif fbtu xbmm pg uif dbtumf"
#     print(decrypt_cipher(text))