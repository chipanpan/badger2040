import badger2040
from badger2040 import WIDTH
import random
import badger_os

# Create a new display and set it to update fast
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_FAST)

# Create lists to store words and definitions
words = []
definitions = []

# Load word list
PATH = "/wordlists/EN.txt"
with open(PATH, "r") as file:
    for line in file:
        word = line.replace("\n","").split(": ")
        words.append(word[0].upper())
        definitions.append(word[-1])
        
# Count number of words        
total = len(words)-1

# Draw new word
def new_word():
    display.set_pen(0)
    display.clear()
    display.set_font("sans")
    display.set_thickness(3)
    display.set_pen(0)
    display.rectangle(0, 0, WIDTH, 16)
    display.set_pen(15)
    display.set_font("bitmap8")
    display.text(r'''
    .------------------.
    '''
    + "|" + f"{words[state["index"]]}".center(16), -10,-10)
    display.text (r'''
     
    '''+
     '''                   |'''
          
    + r'''
    '--------- --------' 
      /\_/\ |/   
     ( o.o )      
      > ^ <       
    '''
     , -10, -10)

    display.text(r'''
                               /|
               .--------------- -.
               '''
            + "|" + f"{definitions[state["index"]]}".center(16) 
     , 15, 30)
    display.text(r'''


               '''
            + '''                  |''' +
                r''' 
               '-----------------'    
                '''
     , 15, 30)
    display.update()


# ------------------------------
#       Main program loop
# ------------------------------

changed = True
state = {
    "index": -1
}
badger_os.state_load("word_index", state)

while True:
    
    display.keepalive()
    # Next word
    if display.pressed(badger2040.BUTTON_DOWN):
        if state["index"] < total:
            state["index"] += 1
            changed = True
        else:
            display.set_pen(0)
            display.clear()
            display.set_pen(15)
            display.text("Study session completed!\nPress A to restart",30,50)
            display.update()
            
    # Previous word
    if display.pressed(badger2040.BUTTON_UP):
        if state["index"] > 0:
            state["index"] -= 1
            changed = True
    
    # Restart learning
    if display.pressed(badger2040.BUTTON_A):
        state["index"] = 0
        changed=True
        
    # Update word
    if changed:
        new_word()
        badger_os.state_save("word_index", state)
        changed=False

    display.halt()