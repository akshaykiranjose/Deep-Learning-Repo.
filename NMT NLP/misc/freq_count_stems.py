import re
import os
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.stem import SnowballStemmer
from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = (10,7)

class TokenizeIt(object):
    """Class TokenizeIt has the 'fname' as an attribute(assign2), the 'path' where the folder and the .py file is saved,
        'files' is a list of text files in the folder . 'tokens' are the tokenized list of all the words in the text files
        in the folder excluding the stopwords"""
    def __init__(self, foldername :str):
        self.fname = foldername
        self.path = str(os.getcwd())+ "\\" + self.fname
        self.files = []
        self.tokens = []

    def tokenize_it(self, filename):
        """
        the member function called from 'do_tokenize(self)' does the tokenization manually and thus updates the 
        member attribute tokens
        """

        stops = list(set(stopwords.words('english')))
        remove = "[0-9\[\]*&^\",_\-%$#@!:;?/>.)(\\n\\t]"        
        path = self.path +'\\'+ filename
        with open(path, 'r') as f:
            string_read = f.read().casefold()           
        string_read_replaced = re.sub(remove, " ", string_read)           
        string_split = string_read_replaced.split(" ")
        tokenized = [i for i in string_split if i != ''] 
        tokens = []
        for _ in tokenized:
            if _ not in stops and len(_) > 2:
                tokens.append(_)            
        return tokens

    def do_tokenize(self):
        """member function that finds the text files inside of the folder and passes each to be made into tokens"""
        files_in_folder = os.listdir(self.path)
        self.files = [file for file in files_in_folder if '.txt' in file]       
        for file in self.files:
            self.tokens += self.tokenize_it(file)
            
    def __str__(self):
        """stringified to return the tokens in a list"""
        return self.tokens()

    def get_fname(self):
        return self.fname
                 
    def get_token(self):
        """Once the tokens are made, this is how it is made accessible to other classes"""
        self.do_tokenize()
        return self.tokens

class FreqDistToken(object):
    """ a FrequncyDistribution(object): instance will have the tokens from another object and 
    works on finding the distribution of words and stem words in the given token list and has features to plot and
    stem """


    def __init__(self, T):
        """Once an object is created, call is made to the find_distribution to update the values of 
        'self.fdist' and 'self.fdist_20' member attributes"""
        self.tokens = T.get_token()
        self.fname = T.get_fname()
        self.stem_dict = {} # {stem: {freq} {words as a set}}
        self.fdist = FreqDist()
        self.len = len(self.fdist)
        self.fdist_20 = FreqDist()
        self.find_distribution()
        
      
    def find_distribution(self):
        """update the values of self.fdist and self.fdist_20 member attributes and makes call to find the stem
        of the words in the token list and update the member attribute 'self.stem' """
        ss = SnowballStemmer('english')
        stem = {}
        words_list = self.tokens  
        for word in words_list:
            stem[ss.stem(word)] = {'freq':0,'words':set()}           
        for word in words_list:
            stem[ss.stem(word)]['freq']+=1
            stem[ss.stem(word)]['words'].add(word)       
        self.stem_dict = stem
    
        for word in list(set(words_list)):
            self.fdist[word] = self.stem_dict[ss.stem(word)]['freq']            
        self.len = len(self.fdist)
        self.fdist_20 = self.fdist.most_common(20)
            
        
    def write(self):
        """ Write the contents to the file """
        freq_dist = dict(self.fdist.most_common(self.len))
        with open(f"190020003_WordFreq_{self.fname}.txt", 'w') as f: 
            for key, value in freq_dist.items(): 
                f.write('%s:%s\n' % (key, value))
        
    def plot(self):      
        """ Plot the top 20 words """
        font1 = {'family':'serif','color':'blue','size':20}
        font2 = {'family':'serif','color':'darkred','size':15}
        x = [l[0] for l in self.fdist_20]
        y = [l[1] for l in self.fdist_20]
        plt.bar(x,y,color = "#4CAF50")
        plt.title("The 20 most common words by frequency (stem counted)", fontdict = font1,loc = 'left')
        plt.xlabel("words", fontdict = font2)
        plt.ylabel("frequency", fontdict = font2)
        plt.show()


if __name__ == "__main__":
    """ Main function of the code"""
    folder = input("Enter Folder Name:")
    T1 = TokenizeIt(folder)
    FDT1 = FreqDistToken(T1)
    FDT1.write()
    FDT1.plot()