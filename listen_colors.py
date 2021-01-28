import sys, select, tty, termios
#import matplotlib.pyplot as plt
import re
import cv2 as cv
import numpy as np
import subprocess

old_attr = termios.tcgetattr(sys.stdin)
tty.setcbreak(sys.stdin.fileno())   
print('Please input keys, press Ctrl + C to quit')

arr = []

def drawImage(color):
    print("color =", color)
    
    r = int(color[1:3], 16)
    g = int(color[3:5], 16)
    b = int(color[5:7], 16)
    
    b_channel = np.ones((300, 300), dtype=np.uint8) * b
    g_channel = np.ones((300, 300), dtype=np.uint8) * g
    r_channel = np.ones((300, 300), dtype=np.uint8) * r
    image = cv.merge((b_channel, g_channel, r_channel))
    filePath = './'+color+'.png'
    cv.imwrite(filePath, image)
    subprocess.call(['open', filePath])

    

def judgeAndShow(str):
    print(str)
    if (len(str) == 7 and re.match('^#[0-9a-fA-F]+', str)):
        drawImage(str.upper())
        return True
        
    return False
    
def listenKeyboard():
    
    while(1):
        if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
            a = sys.stdin.read(1)
            if len(arr)>=7:
                del arr[0]
            pattern = re.match(r'[0-9a-fA-F#]', a, re.I)
#            print(a, pattern)
            if pattern and len(a) == 1:
                arr.append(a)
                str = ''.join(arr)
                if judgeAndShow(str):
                    arr.clear()

            
        
listenKeyboard()
termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)

