'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 20, 2023.
'''

import math
import re 

def norm(vec):
    '''Return the norm of a vector stored as a dictionary, as
    described in the handout for Project 3.
    '''

    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    #({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}) 

    #({"a": 1, "b": 2, "c": 3, "d": 0}, {"a":0, "b": 4, "c": 5, "d": 6}) 

    # (2 x 4 + 3 x 5) / root((1 + 4 + 9) x (16 + 25 + 36))  

    # vec1_list = list(vec1)
    # vec2_list = list(vec2) 
    # total_vec_list = []

    # for i in range (len(vec1_list)): 
    #     for j in range (len(vec2_list)): 
    #         if vec1_list[i] == vec2_list[j]: 
    #             total_vec_list += vec1_list[i] 

    cos_sim_denom_vec1 = 0 
    cos_sim_denom_vec2 = 0 
    cos_sim_num = 0 
    cos_sim_denom = 0 
    cos_sim = 0 

    #Create a list of common keys between vec1 and vec2 
    #Common keys now holds the keys that exist both in vec1 and vec2 
    common_keys = list(vec1.keys() & vec2.keys()) 

    #Compute the numerator. 
    #Take the value of vec1 at common_key k, multiplied by the value of vec2 at common_key k 
    for k in range (len(common_keys)): 
        cos_sim_num = cos_sim_num + vec1[common_keys[k]]*vec2[common_keys[k]]

    #Goes through all the values in vec1 and adds their square 
    for value1 in vec1.values(): 
        cos_sim_denom_vec1 = cos_sim_denom_vec1 + value1**2 
    
    #Goes through all the values in vec2 and adds their square 
    for value2 in vec2.values(): 
        cos_sim_denom_vec2 = cos_sim_denom_vec2 + value2**2 

    #Computes the denominator by multiplying the squared sum of all the values in vec1 by the squared sum of all the values in vec2, all square rooted 
    cos_sim_denom = (cos_sim_denom_vec1 * cos_sim_denom_vec2)**0.5  
    
    cos_sim = cos_sim_num / cos_sim_denom 

    return cos_sim 

#def build_semantic_descriptors(sentences): 
    total_dict = {}
    unique_words = []
    unique_words_in_comm_sentence = [] 
    count = 0 

    for i in range (len(sentences)): 
        #list which holds all the unique words in the passage  
        unique_words.extend(list(set(sentences[i]))) 

    for l in range (len(unique_words)): 
        common_sentence = [] 
        inner_dict = {}

        #Iterate through all the unique words in the passage. 
        #This is our key for the total (outer) dictionary 

        #Create the inner dictionary. 
        #Search for the sentences that contain the unique word and add them to a single list called common_sentence
        for j in range (len(sentences)): 
            #Look at the first sentence 
            for k in range (len(sentences[j])): 
                #If the word in the sentence contains the unique word then add the sentence to common_sentence
                if sentences[j][k] == unique_words[l]: 
                    common_sentence.extend(sentences[j]) 
                    #This sentence has been added. No need to check the rest of the words in the sentence 
                    break 
        
        #Now, we have common_sentence, which holds one list of all the words in the senteces that contain the common word 

        unique_words_in_comm_sentence = list(set(common_sentence)) 

        #Count the number of occurences of each word 
        for o in range (len(unique_words_in_comm_sentence)): 
            count = 0 
            for n in range (len(common_sentence)): 
                if unique_words_in_comm_sentence[o] == common_sentence[n]: #If the word has come up in the common sentence, increase count 
                    count += 1 
            #Create the innder dictionary 
            #Ensure we are not adding the key that is the same as the key of the total dictionary 
            if unique_words_in_comm_sentence[o] != unique_words[l]: 
                inner_dict[unique_words_in_comm_sentence[o]] = count  

        #Add to the total dictionary 
        # #The key is the unique word from the entire passage 
        #The value is the inner dictionary for that word 
        total_dict[unique_words[l]] = inner_dict 
    
    return total_dict 


def build_semantic_descriptors(sentences):
    #Create initial empty total dictionary 
    total_dict = {}

    #Loop to read one sentence at a time from the list of sentences 
    for sentence in sentences:
        #Create a new list of unique words in the sentence 
        unique_in_sentence = set(sentence)

        #Select a word one at a time from the unique list 
        for word in unique_in_sentence: 
            #Check if the word is not already in the total dicitonary, then add them in 
            # with their word as the key and an empty inner dicitonary as their value 

            #Ex. For the word man, initially add it to the total dictionary, which will be {'man': {}} 
            if word not in total_dict:
                total_dict[word] = {}

            #Create the inner dictionary, pointing to the key of the outer dictionary 
            #Updating the inner dictionary updates the value of the outer dictionary of that key 
            inner_dict = total_dict[word] #inner dictionary is the value of the totale dictionary of key word 

            #Loop again for each word in the unique list 
            for other_word in unique_in_sentence: 
                #Bypass the same word as the current key of the total dictionary  
                if other_word != word: 
                    #If the OTHER word is already in the key of the inner dictionary 
                    if other_word in inner_dict: 
                        #Update inner dictionary. Add 1 to the value to the key of the inner dictionary 
                        #Updating the inner dictionary automatically updates the outer dictionary 
                        inner_dict[other_word] += 1 
                    else:
                        #If the other word is not a key of the inner dictionary, add it to the inner dictionary with an initial value of 1 
                        inner_dict[other_word] = 1

    return total_dict


def build_semantic_descriptors_from_files(filenames):
    text = ""
    for i in range(len(filenames)):
        f = open(filenames[i], "r", encoding="latin1")
        text += f.read() + " "
        f.close()
    
    # Convert all text to lowercase
    text = text.lower()

    # Remove punctuation
    punctuation = [",", "-", "--", ":", ";"]
    for p in punctuation:
        text = text.replace(p, " ")

    # Split text into sentences using ., !, and ?
    sentences = re.split(r'[.!?]', text) 

    #Convert each sentence into a list of words
    for i in range(len(sentences)):
        sentences[i] = sentences[i].split()

    #Remove empty list at the end 
    sentences.remove([])      

    #Build and return the semantic descriptors
    return build_semantic_descriptors(sentences)  


def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    best_choice = choices[0]
    # Cosine function has a range of -1 to 1
    best_score = -2

    #If the word is not a key or has not value in semantic_descriptors 
    #This also considers if semantic descriptor dictionary is empty 
    #Ex. "man": {}  # key exists, but its value/inner dictionary is empty  
    if word not in semantic_descriptors or not semantic_descriptors[word]:
        return best_choice 
    
    word_vector = semantic_descriptors[word] 

    for i in range (len(choices)): 
        #If the choice is not a key or has not value in semantic_descriptors 
        #This also considers if semantic descritor dictionary is empty  
        if choices[i] not in semantic_descriptors or not semantic_descriptors[choices[i]]:
            similarity = -1 
        else:
            choice_vector = semantic_descriptors[choices[i]]

            similarity = similarity_fn(word_vector, choice_vector) 
        
        #Compare similarity between word and choice 
        #Greater than, NOT EQUAL. Ensures that if two choices has the same similarity, we take the first one (smallest index) 
        if similarity > best_score:
            best_choice = choices[i] 
            best_score = similarity
    
    return best_choice 


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct = 0
    total = 0 

    f = open(filename, "r", encoding="latin1")
    text = f.read()
    f.close()
    #splits the string (text) into a list of individial lines (at the line breaks)
    #Ex. text = "vexed annoyed amused frightened\ncalm peaceful angry\n" 
    # lines --> ["vexed annoyed amused frightened", "calm peaceful angry"] 
    lines = text.splitlines()

    for i in range (len(lines)): 
        #.strip() removes outer whitespace 
        #.split() separates the lines into a list of words 
        # sections (lines[0]) -> ["vexed", "annoyed", "amused", "frightened"]
        # sections (lines[1]) -> ["calm", "peaceful", "angry"] 
        sections = lines[i].strip().split() 

        #must be at least 3 words in the section, one for the comparison word, one for the answer, and min 1 guess 
        if len(sections) >= 3: 
            #first word in the section is the word were comparing 
            word = sections[0] 

            #answer is the second word in the section 
            answer = sections[1] 

            #choices is the rest of the words in the seciton 
            choices = sections[2: ] 

            guess = most_similar_word(word, choices, semantic_descriptors, similarity_fn)

            #Tracks the total number of guesses in order to comput average 
            total += 1
            #Tracks number of correct guesses 
            if guess == answer:
                correct += 1
    
    #If there were no guesses, 0% 
    if total == 0:
        return 0.0 #float 

    return (correct / total) * 100.0 #float 

if __name__ == "__main__": 
    print("Loading books...") 
    sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
    #sem_descriptors = build_semantic_descriptors_from_files(["sw.txt"])
    print("Done loading! Running test...") 
    res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
    print(res, "of the guesses were correct")  


#print (cosine_similarity({"a": 1, "b": 2, "c": 3}, {"b": 4, "c": 5, "d": 6}))   

# print (build_semantic_descriptors([
# ["i", "am", "a", "sick", "man"],
# ["i", "am", "a", "spiteful", "man"],
# ["i", "am", "an", "unattractive", "man"],
# ["i", "believe", "my", "liver", "is", "diseased"],
# ["however", "i", "know", "nothing", "at", "all", "about", "my",
# "disease", "and", "do", "not", "know", "for", "certain",
# "what", "ails", "me"]])) 

# a = (build_semantic_descriptors_from_files(["test.txt"])) 
# print (most_similar_word("vexed", ["annoyed", "amused", "frightened", "excited"], a, cosine_similarity))