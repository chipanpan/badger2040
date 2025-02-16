import badger2040
from badger2040 import WIDTH
import random

# Create a new Badger and set it to update at normal speed.
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_FAST)

words = []
definitions = []

# Load word list
PATH = "/docs/EN.txt"
with open(PATH, "r") as file:
    for line in file:
        word = line.replace("\n","").split(": ")
        words.append(word[0].upper())
        definitions.append(word[-1])
        
total = len(words)-1
x = -1

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
    |    FLASHCARD   |
    '--------- --------' 
      /\_/\ |/   
     ( o.o )      
      > ^ <       
    '''
     , -10, -10)
display.update()

# Learn a new word
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
    + "|" + f"{words[x]}".center(16) + "|"
          
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
            + "|" + f"{definitions[x]}".center(16) + "|" +
                r''' 
               '-----------------'    
                '''
     , 15, 30)
    display.update()


# ------------------------------
#       Main program loop
# ------------------------------
while True:
    display.keepalive()
    if display.pressed(badger2040.BUTTON_DOWN):
        if x < total:
            x += 1
            new_word()
        else:
            display.set_pen(0)
            display.clear()
            display.set_pen(15)
            display.text("Study session completed",30,50)
            display.update()
    if display.pressed(badger2040.BUTTON_UP):
        if x > 0:
            x -= 1
            new_word()

    #display.halt()
