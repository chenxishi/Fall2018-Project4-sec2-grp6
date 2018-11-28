import os


# Function to get the file end with .txt
def Get_FileNames(path):

    File_Lists = list()

    for ground_truth_file in os.listdir(path):
        if ground_truth_file.endswith(".txt"):
            File_Lists.append(ground_truth_file)

    return(File_Lists)

# Clean the words
def clean_word(w):
    out = []
    for c in w:
        c = c.lower()
        # searching set is faster than list: O(1) vs. O(n=26)
        if c.isalpha():
            out.append(c)
    return ''.join(out)


# Check the length of the words
def clean_word2(w):
    if len(w) < 21 and len(w) >1:
        return True
    else:
        return False

# Get the word with length n
def filter_word(n):
    def filter(word):
        if len(word) == n:
            return True
        else:
            return False
    return(filter)

# wordFilter = filter_word(5)
#
# print(set(filter(wordFilter, Ground_Truth_Words)))



Ground_Truth_Path = "../data/ground_truth/"

Tesseract_Path = "../data/tesseract/"

Ground_Truth_Files = Get_FileNames(Ground_Truth_Path)

File_Names = [filename[: -4] for filename in Ground_Truth_Files]

Ground_Truth_Words = set()

for FileName in File_Names:
    File_Dir = Ground_Truth_Path + FileName + ".txt"
    with open(File_Dir, 'r') as file:
        file_Content = file.read()
        uncleaned_word = file_Content.split()
        Ground_Truth_Words = Ground_Truth_Words.union(set(map(clean_word,uncleaned_word)))


Ground_Truth_Words = set(filter(clean_word2, Ground_Truth_Words))



# Intert the letter into specific position in the string
def Insert_Letter(String, Letter, Position):
    if Position <= 0:
        return(Letter + String)
    elif Position >= (len(String)-1):
        return(String + Letter)
    else:
        return(String[:Position] + Letter + String[Position:])


# Delete the letter from specific position in the string
def Delete_Letter(String, Position):
    if Position < 0 or Position > (len(String)-1):
        return(String)
    else:
        return(String[:Position] + String[Position+1:])

# Substitute the letter from specific position with new letter in the string
def Substitute_Letter(String, Letter, Position):
    if Position < 0 or Position > (len(String)-1) or Letter.isalpha() == False:
        return(String)
    else:
        return(String[:Position] + Letter.lower() + String[Position+1:])

# Reverse the letter between two specific positions in the string
def Reverse_Letter(String, Position1, Position2):
    pre_index = min(Position1, Position2)
    pos_index = max(Position1, Position2)
    if pre_index < 0 or pos_index < 0 or pre_index > (len(String)-1) or pos_index > (len(String)-1) or pre_index == pos_index:
        return(String)
    else:
        return(String[:pre_index] + String[pos_index] + String[pre_index+1:pos_index] + String[pre_index] + String[pos_index+1:])



# function for find the possibile candidates with inertation
def Find_Candidates_Insertion(Typo):
    '''

    '''
    Candidates = list()
    Candidates_Length = len(Typo) - 1
    PossibleWords = set(filter(filter_word(Candidates_Length), Ground_Truth_Words))
    for index in range(len(Typo)):
        for String in PossibleWords:
            Temp_String  = Insert_Letter(String, Typo[index], index)
            if Typo == Temp_String:
                Candidates.append((String, Typo[index], index))
    return(Candidates)

# Next create table dictionary for deletion for each words
Deletion_Dic = dict()

for ground_truth_word in Ground_Truth_Words:
    for index in range(len(ground_truth_word)):
        temp_typo = Delete_Letter(ground_truth_word, index)
        if temp_typo in Deletion_Dic:
            Deletion_Dic[temp_typo].append((ground_truth_word, index))
        else:
            Deletion_Dic[temp_typo] = list()
            Deletion_Dic[temp_typo].append((ground_truth_word, index))

# function for find the possibile candidates with deletion
def Find_Candidates_Deletion(Typo):
    if Typo in Deletion_Dic:
        return(Deletion_Dic[Typo])
    else:
        return([])



# Next create tables
