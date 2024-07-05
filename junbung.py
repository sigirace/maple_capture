import pyautogui
import time

while True:
    pyautogui.keyDown('left')

    for i in range(4):
        time.sleep(0.8) 
        pyautogui.keyDown('w')
        pyautogui.keyDown('q')
        pyautogui.keyUp('w')
        pyautogui.keyUp('q')
        time.sleep(0.5) 
        pyautogui.keyDown('q')
        pyautogui.keyUp('q')

        
    pyautogui.keyUp('left')

    pyautogui.keyDown('right')
    for i in range(4):
        time.sleep(0.8)
        pyautogui.keyDown('w')
        pyautogui.keyDown('q')
        pyautogui.keyUp('w')
        pyautogui.keyUp('q')
        time.sleep(0.5) 
        pyautogui.keyDown('q')
        pyautogui.keyUp('q')

        
        
    pyautogui.keyUp('right')