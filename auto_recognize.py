from lcd_library import my_lcd as lcd
from openalpr import Alpr
import re
import numpy as np
import cv2
import sys
import time

def entrance_recognize_and_indicate(picture_path):
    alpr = Alpr("us", "/usr/local/src/openalpr/src/config/openalpr.conf", "/usr/local/src/openalpr/runtime_data")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)
    
    alpr.set_top_n(20)
    alpr.set_default_region("md")

    results = alpr.recognize_file(picture_path)
    i = 0

    for plate in results['results']:
        i += 1
        #print("Plate #%d" % i)
        #print("   %12s %12s" % ("Plate", "Confidence"))
        for candidate in plate['candidates']:
            prefix = "-"
            if candidate['matches_template']:
                prefix = "*"
            break
        break
            #print("  %s %12s%12f " % (prefix, candidate['plate'], candidate['confidence']))

    the_plate = candidate['plate']
    print(the_plate)
    # Call when completely done to release memory
    
    return the_plate

def exit_recognize_and_indicate(picture_path):
    alpr = Alpr("us", "/usr/local/src/openalpr/src/config/openalpr.conf", "/usr/local/src/openalpr/runtime_data")
    if not alpr.is_loaded():
        print("Error loading OpenALPR")
        sys.exit(1)
    
    alpr.set_top_n(20)
    alpr.set_default_region("md")

    results = alpr.recognize_file(picture_path)
    i = 0

    for plate in results['results']:
        i += 1
        #print("Plate #%d" % i)
        #print("   %12s %12s" % ("Plate", "Confidence"))
        for candidate in plate['candidates']:
            prefix = "-"
            if candidate['matches_template']:
                prefix = "*"
            break
        break
            #print("  %s %12s%12f " % (prefix, candidate['plate'], candidate['confidence']))

    the_plate = candidate['plate']
    print(the_plate)
    # Call when completely done to release memory
    
    return the_plate


def lcd_car_in(the_plate):
    lcd.init()              # Basic HW system setup - port directions on the expander and reset the display
    lcd.clearDisplay(0)     # Complete deletion of the display

    lcd.initTextMode()     # Switch to text mode

    lcd.printStringTextMode("Lisence Number:",0,0)   # Display the text in the text mode at specified coordinates
    lcd.printStringTextMode(the_plate,0,1)
    lcd.printStringTextMode("Welcome!",0,2)
    time.sleep(5)
    lcd.clearDisplay(0)     # Complete deletion of the display
    
def lcd_car_out(the_plate):
    lcd.init()              # Basic HW system setup - port directions on the expander and reset the display
    lcd.clearDisplay(0)     # Complete deletion of the display

    lcd.initTextMode()     # Switch to text mode

    lcd.printStringTextMode("Lisence Number:",0,0)   # Display the text in the text mode at specified coordinates
    lcd.printStringTextMode(the_plate,0,1)
    lcd.printStringTextMode("Thank you!",0,2)
    time.sleep(5)
    lcd.clearDisplay(0)     # Complete deletion of the display    
    
def show_remain_place(now_place,reserved_place):
    lcd.init()              # Basic HW system setup - port directions on the expander and reset the display
    lcd.clearDisplay(0)     # Complete deletion of the display

    lcd.initTextMode()     # Switch to text mode

    lcd.printStringTextMode("Remain Place :",0,0)   # Display the text in the text mode at specified coordinates
    lcd.printStringTextMode(str(now_place),0,1)
    lcd.printStringTextMode("Reserved Place :",0,2)   # Display the text in the text mode at specified coordinates
    lcd.printStringTextMode(str(reserved_place),0,3)

if __name__ == '__main__':
    entrance_recognize_and_indicate('/home/pi/pytest/final_project/5978YA.jpg')
    
