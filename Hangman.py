from __future__ import print_function
import numpy

my_list = ["hello", "foxtrot", "ball", "power", "aardvark", "dictionary"]
my_word = numpy.random.choice(my_list)
print("Welcome to hangman!")
print('  |---------|')
print('  |         |')
print('  |')
print('  |')
print('  |')
print('  |')
print('  |')
print('  |')
print('  |')
print('  |')
print('-------------')
for letter in my_word:
    print("_" + " ", end ="")

guess = ""
while guess == "":
    guess = raw_input("Guess a letter: ")
print(guess)
if guess[0] in my_word:
    print(guess[0])
else:
    print("")
exit(0)

