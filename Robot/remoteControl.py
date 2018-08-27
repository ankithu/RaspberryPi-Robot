# import curses and GPIO
import curses
import driveManager


# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho() 
curses.cbreak()
screen.keypad(True)
driveManager.init()
steer = 0

try:
        while True:   
            char = screen.getch()
            if char == ord('q'): 
            	break                
            elif char == curses.KEY_UP:
                driveManager.forward(60)               
            elif char == curses.KEY_DOWN:
                driveManager.backward(60)   
            elif char == curses.KEY_RIGHT:
            	steer = steer + 5
                driveManager.steer(steer)    
            elif char == curses.KEY_LEFT:
            	steer = steer - 5
            	driveManager.steer(steer)	
            else:
            	driveManager.stop()

                
             
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    
