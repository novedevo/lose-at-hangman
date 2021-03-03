from guessr import Guessr
from executionr import *
import sys

if len(sys.argv) <= 1:
    exit("Please provide arguments")

if sys.argv[1] == "--interactive":
    exe = PlayerExecutionr()
    word = "."*int(input("How many letters long is your word? "))

else:
    word = sys.argv[1].upper()
    exe = Executionr(word)

try:
    gue = Guessr("."*len(word), True)
except GameWonException as g:
    print("Your word was {}, gg ez".format(g.args[0]))
    exit(0)

in_progress = True
while in_progress:
    try:
        gue.new_information(exe.check_answer(gue.make_strategic_guess()))
    except GameWonException as g:
        print("Your word was {}, gg ez".format(g.args[0].lower()))
        exit(0)
    except GameLostException:
        print("Hacker. There's no way you played fair.")
        exit(0)
