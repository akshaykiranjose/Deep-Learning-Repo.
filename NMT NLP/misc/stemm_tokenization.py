
# to read the stem file conatined in folder 'assign1' and make a list of tuples
def read_stem(stem_file: str)-> list:
    with open(stem_file,'r') as f:  # reading the file in 'r' mode
        stem_str = f.read().casefold()
    for ch in "[]()!?.:;-\"":   # getting rid of all characters present in the string
        stem_str = stem_str.replace(ch, "")
    stem_list = stem_str.split(",") # returns a list from a string
    words = stem_list[0::2]
    stems = stem_list[1::2]
    roots = list(zip(words,stems))
    roots = list(set(roots))
    roots = [i for i in roots if len(i[1]) > 1] #remove any unwanted single characters
    return roots


# to read the stop file in folder 'assign1' and make a list of them
def read_stop(stop_file: str)-> list:
    with open(stop_file, 'r') as f:
        stop = f.read().casefold()
    stop = stop.replace("\t", "").replace(" ", "") # there are some pattern irregulatrities like tab spaces and new line commands
    stop = stop.rsplit("\n")                       # we remove all the irregulatrities and makes the string into a list
    stop = [ i for i in stop if i != '' ]
    return stop


# to read the text file in folder 'assign1' and make a list out of them
def read_text(text_file: str)-> list:
    with open(text_file, 'r') as f:
        text_str = f.read().casefold()
    for ch in "[](),:_?!-;\n\"":  # getting rid of all characters present in the string
        text_str = text_str.replace(ch, " ")
    text_str = text_str.replace('.', "")
    text = text_str.split(" ")
    text = [i for i in text if i != ''] # making finer adjustments
    return text

# adjusting the text file by removing all the stop words from it
def adjust_text(text: str, stops: str)->list: # since we are not supposed to count root words, I have decided to make a new list
    text_to_search_in = []         # such that i only have to search through words that are not in the stop words list
    for word in text:
        if(word not in stops):
            text_to_search_in += [word]
    return text_to_search_in


def counts(text, root):
    counts_list = []
    for tup in root: # takes a tuple from stem and does processing on its behalf
        counts = {}  # have to reinitialize the dictionary for each iteration
        counts = {tup[0]:0} # initializing count to 0
        for word in text:
            if(tup[1] in word):
                counts[tup[0]]+=1 # whenever the root word of a file is present in a word, it is counted as the
        if(counts[tup[0]]>0):     # as the occurence of the word itself
            counts_list.append(counts)
    return counts_list


def cs324_assign1(folder, prefix):

    result_file = open(prefix+"_word_freq.txt","w") # opens a file to write the content in the end, opened in append mode

    text = []; # to keep all the text files read as a long list of strings

    # to open all files in the folder 'assign1' and extract text files out of it.
    import os
    files_in_folder = os.listdir(str(os.getcwd())+'/'+folder)
    text_files_in_folder = [file for file in files_in_folder if '.txt' in file]

    for file in text_files_in_folder:
        filename = folder+'/'+file
        if(file == 'stem.txt'):
             roots = read_stem(filename)
        elif(file == 'stop.txt'):
             stops = read_stop(filename)
        else:
             text+=(read_text(filename)) #reads files other than the above into the list

    text_to_search_in = adjust_text(text, stops) # reducing the set of words to search in by removing stop words

    counts_list = counts(text_to_search_in, roots) # the count of frequency as a list of dictionaries

    result_file.write(str(counts_list)) # writing the contents to the file.



#defining file names for files inside of the folder 'assign1'
folder = 'assign1'   # it is named so, because the run of the script requires this script to be in a folder containing another folder
                     # by the name 'assign1' (that's why the '/' in the end) which contains the stop.txt, stem.txt and the word files, whatever name they have
                     # have chosen the file names as per the sample folder given.
prefix = "190020003" # this is the roll number

cs324_assign1(folder, prefix) # should nothing go wrong, a text file by the name '190020003_word_freq.txt' will be created and
                              # will have the output as a list of dictionaries
