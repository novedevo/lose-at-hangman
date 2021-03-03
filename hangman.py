from guessr import Guessr
from executionr import * # two different executioners and exception classes
import sys

# Requires arguments to determine mode of operation
if len(sys.argv) <= 1:
    exit("Please provide arguments")

# interactive mode
if sys.argv[1] == "--interactive":
    exe = PlayerExecutionr() # player-controlled executioner instead of the bot
    word = "." * int(input("How many letters long is your word? "))

# headless mode
else:
    word = sys.argv[1].upper()
    exe = Executionr(word)

try:
    gue = Guessr("." * len(word), True)
except GameWonException as g: # special case, only one word in our memory is of that length
    print("Your word was {}, gg ez".format(g.args[0]))
    exit(0)

in_progress = True
while in_progress: # game logic loop
    try:
        # nested function calls! <3 
        # guessr makes a guess, which is passed to the executionr to check the answer
        # executionr returns a new regex pattern, which is passed back to the guessr to complete the feedback loop
        gue.new_information(exe.check_answer(gue.make_strategic_guess()))
    except GameWonException as g:
        print("Your word was {}, gg ez".format(g.args[0].lower()))
        exit(0)
    except GameLostException:
        print("Hacker. There's no way you played fair.") # >:-(
        exit(0)
