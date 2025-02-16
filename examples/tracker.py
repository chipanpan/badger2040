import badger2040
import badger_os
import jpegdec

# Set constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT
PATH = "/images/water.jpg"

x = 90
y = HEIGHT-5
height = int(HEIGHT*0.8)

num_parts = 5
height_step = int(height / num_parts)
bottom_base_length = 50
top_base_length = 90


def draw_tracker():
    
    # Draw white background
    display.set_pen(15)
    display.clear()
    display.rectangle(0, 0, WIDTH, HEIGHT)

    # Draw an empty glass of water
    display.set_pen(0) 
    display.polygon([
      (x, y),
      (x + 50, y),
      (x + 70, y-height-2),
      (x-20, y-height-2),
    ])

    if state["level"] > 0:
        # Draw filled glass
        current_height = state["level"] * height_step
        current_base_length = int(bottom_base_length + (top_base_length - bottom_base_length) * (current_height / height))
        current_offset = int((bottom_base_length - current_base_length) / 2)
        display.set_pen(15)
        display.polygon([
          (x+5, y-5),
          (x + 50-5, y-5),
          (x + current_offset + current_base_length-5, y-current_height),
          (x + current_offset+5, y-current_height),
        ])

        # Generate horizontal lines for division
        x_division_coords = []
        y_division_coords = []

        for i in range(1, state["level"]+1):
            current_height = i * height_step
            # Compute the length of the current horizontal segment (interpolation between top and bottom bases)
            current_base_length = int(bottom_base_length + (top_base_length - bottom_base_length) * (current_height / height))
            current_offset = int((bottom_base_length - current_base_length) / 2)
            x_division_coords.append([current_offset, current_offset + current_base_length])
            y_division_coords.append([current_height, current_height])

        # Draw division lines
        display.set_pen(0)
        for i in range(state["level"]):
            display.line(x_division_coords[i][0]+x+4, y-y_division_coords[i][0],x_division_coords[i][1]+x-4, y-y_division_coords[i][1],4)

    # Draw illustration
    jpeg = jpegdec.JPEG(display.display)
    jpeg.open_file(PATH)
    jpeg.decode(int(WIDTH*0.6), 0)

    # Draw text
    display.set_pen(0)
    display.set_font("bitmap16")
    display.text("Stay hydrated",40,0)

    display.update()

# ----------------
# Main starts here
# ----------------

changed = True
state = {
    # Level is from 0 to 5
    "level": 0
}
badger_os.state_load("tracker", state)

display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_FAST)
display.set_thickness(1)

while True:
    # Don't go to sleep while we're doing stuff
    display.keepalive()
    
    # Increase by 1 level
    if display.pressed(badger2040.BUTTON_DOWN):
        if state["level"] >= 1:
            state["level"] -= 1
            changed = True
            
    # Decrease by 1 level
    if display.pressed(badger2040.BUTTON_UP):
        if state["level"] < 5:
            state["level"] += 1
            changed = True
    
    # Reset tracker
    if display.pressed(badger2040.BUTTON_C):
        state["level"] = 0
        changed = True
        
    # Update the tracker
    if changed:
        draw_tracker()
        badger_os.state_save("tracker", state)
        changed = False

    # Go to sleep if on battery
    display.halt()