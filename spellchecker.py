#Import library to create bit arrays
from bitarray import bitarray
#Import library with the murmur hash function
import mmh3
# Import library for opening urls.
import urllib.request
# Import math for the constant e
import math
e = math.e
# Below I've hard coded in the number of bits in the array and the number of hash
# functions we'll use, but we could also leave the number of bits up to the user
# and calculate the optimum number of hash functions from that using: k = (m/n)ln(2)
# But I figured that since the dictionary was provided, I'd just shoot for a less
# than 1% false positive rate.
m = 3500640
k = 7

def fillDictionary(m):
    """
    Fill a bit array of length m with the word list provided for this exercise.
    Return the Bit Array dictionary along with the number of words contained in it.
    """
    # Create a bit arry of size m and initialize all the bits to 0 (or False).
    print("Initializing dictionary...")
    dictionary = bitarray(m)
    dictionary.setall(0)
    count = 0
    # Open the set of words provided for the exercise and save it as wordList.
    wordList = open("wordlist.txt", "r")
    # Alternatively, as commented out below, I was opening these straight from
    # the URL, but I figured I'd go with this method instead, because it's a bit
    # faster. But if you didnt want to download the word list, you could just
    # comment out the line above and uncomment the line below.
    # wordList = urllib.request.urlopen("http://codekata.com/data/wordlist.txt")

    # File through the words, adding one to the word count before trimming the
    # String and passing the result to the function that's used to add words to
    # the dictionary.
    for line in wordList:
        count += 1
        stripped = line.strip()
        addWord(stripped, dictionary)
    # Close the file when we're done working with it.
    wordList.close()
    # Return the bit array that we created along with the word count.
    return dictionary, count

def spellcheck(word, dictionary):
    """
    Check to see if the String word is in the Bit Array dictionary. If it isn't, say that
    the word is spelled wrong, offer to add it to the dictionary, and return False
    along with the number of words added to the dictionary.

    If it could be, say the probability that it is (i.e. one minus the probability
    of a false positive) and return True along with the number of words added to the dictionary (0).
    """
    # Set m to the current length of the dictionary array.
    m = dictionary.length()
    # Create a tuple of 64-bit signed Integers using a 128-bit murmur hash algorithm.
    hashTup = mmh3.hash64(word)
    # Treating the two Integers from the tuple as hashes from independent functions,
    # simulate k hash function calls using the method described in Kirsch and
    # Mitzenmacher's "Less Hashing, Same Performance: Building a Better Bloom Filter".
    for i in range(k):
        position = (hashTup[0] + (i * hashTup[1])) % m
        # If any of the bits checked are 0 or False, the word is not in the dictionary.
        # Say as much, and offer to put it in the dictionary.
        if not dictionary[position]:
            print("\nNope,", word + "'s definitely not in the dictionary. Would you like me to add it? (Y/N)")
            print("(Warning: There is no way to delete words from the dictionary, and the more you add,")
            response = input("the less certain I am when they're spelled correctly.)\n\n").lower()
            # If the word is added to the dictionary, we'll return False and the number 1 to represent the number of words added to the dictionary.
            if response == "y" or response == "yes":
                addWord(word, dictionary)
                print("\nI've added", word, "to the dictionary.")
                return False, 1
            # If the word is not added to the dictionary, we'll return False and 0, instead, because no words were added.
            else:
                print("\nCool cool. I won't add", word, "to the dictionary.")
                return False, 0
    # If all of the bits checked are 1, then it is possible that the word is in the dicionary.
    # First, calculate that probability by taking one minus the probability of a false
    # positive, print that out, and return True along with 0 (the number of words added to the dictionary).
    probability = round(((1 - ((1 - (e ** ((-k * n) / m))) ** k)) * 100), 2)
    print("\nI'm about " + str(probability) + "% sure that", word + "'s in the dictionary.")
    return True, 0

def addWord(word, dictionary):
    """
    Add the String word to the Bit Array dictionary.
    """
    # Set m to the current length of the dictionary array.
    m = dictionary.length()
    # Create a tuple of 64-bit signed Integers using a 128-bit murmur hash algorithm.
    hashTup = mmh3.hash64(word)
    # Treating the two Integers from the tuple as hashes from inependent functions,
    # simulate k hash function calls and set the bit at each hash position in Bit Array
    # dictionary to 1.
    for i in range(k):
        position = (hashTup[0] + (i * hashTup[1])) % m
        dictionary[position] = 1

# Upon starting the program, create a Bit Array dictionary with the words from the
# list provided for the exercise and set n to the number of words in the list.
dictionary, n = fillDictionary(m)
# Print a prompt for input from the user.
word = input("\nWhat word would you like me to check the spelling of?\n\n")
# Check if the input String is in the Bit Array dictionary.
boolean, count = spellcheck(word, dictionary)
# In case a word was added to the dictionary, update the value of n.
n += count
# Continue printing prompts for input until the user types "exit".
while word != "exit()":
    word = input("\nWhat word would you like me to check the spelling of now?\n(Type exit() to quit.)\n\n")
    if word == "exit()":
        break
    else:
        boolean, count = spellcheck(word, dictionary)
        n += count
