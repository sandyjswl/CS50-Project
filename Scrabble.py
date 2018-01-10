import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


WORDLIST_FILENAME = "words.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordList: list of strings
    wordList = []
    for line in inFile:
        wordList.append(line.strip().lower())
    print("  ", len(wordList), "words loaded.")
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES
    """
    score=0
    for letter in word:
    	score=score+SCRABBLE_LETTER_VALUES[letter]
    score=score*len(word)	
    if len(word)==n:
    	score=score+50
    return score	


def displayHand(hand):
    """
    Displays the letters currently in the hand.
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter,end=" ")       # print all on the same line
    print()                             # print an empty line


def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.
    """
    hand={}
    numVowels = n // 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand


def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it.
    """
    newHand=hand.copy()
    for letter in word:
        newHand[letter]=newHand[letter]-1
        newHand={k:v for k, v in newHand.items() if v}
        
            

    return newHand	



def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False
    """
    newHand=hand.copy()
    count=0

    if word not in wordList:
    	return False

    for letter in word:
    	if letter in newHand:
    		newHand[letter]=newHand[letter]-1
    		count=count+1		

    listVal=newHand.values()	

    for i in listVal:
    	if i<0:
    		return False	

    if count==len(word):
    	return True
    else:
    	return False					




def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    """
    length=0
    for i in hand:
    	length=length+hand[i]
    return length	



def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."
    """
    total_score=0
    # Keep track of the total score
    
    # As long as there are still letters left in the hand:
    while  calculateHandlen(hand)>0:

        # Display the hand
        print("Current Hand: ",end=" ")
        displayHand(hand)
        # Ask user for input
        current_word=input('Enter word, or a "." to indicate that you are finished: ')
        # If the input is a single period:
        if current_word=='.':
            # End the game (break out of the loop)
            break
        else:    
        # Otherwise (the input is not a single period):
            if isValidWord(current_word,hand,wordList)==False:
            # If the word is not valid:
                print("Invalid word, please try again.\n")
                # Reject invalid word (print a message followed by a blank line)

            # Otherwise (the word is valid):
            else:   
                # Tell the user how many points the word earned, and the updated total score, in one line followed by a blank line
                total_score=total_score+getWordScore(current_word,n)
                print('"'+current_word+'"'+" earned "+str(getWordScore(current_word,n))+" points."+" Total: "+str(total_score)+" points")
                print()
                # Update the hand 
                hand=updateHand(hand,current_word)

    if current_word==".":
                    
        print("\n\nGoodbye! Total score: "+str(total_score)+" points.")
    else:
        print("Run out of letters. Total score: "+str(total_score)+" points.")
    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    



def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands
    """
    initialize=1
    while True:
    	user_input=input("Enter n to deal a new hand, r to replay the last hand, or e to end game: ")
    	
    	if user_input=='n':
    		initialize=2
    		hand=dealHand(HAND_SIZE)
    		playHand(hand,wordList,HAND_SIZE)
    	elif user_input=='r':
    		if initialize==1:
    			print("You have not played a hand yet. Please play a new hand first!")
    		else:
    			playHand(hand,wordList,HAND_SIZE)
    				
    			
    	elif user_input=='e':
    		break
    	else:
    		print("Invalid command.")	

   



#
# Build data structures used for entire session and play game
#
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)
