import cv2
import numpy as np
import pyautogui
import time
import threading
import pytesseract
import re
import os
import keyboard

import time
from PIL import Image

base_path = "C:\\\macro\\images"

# 아래층 첫번째 275 390
# 위층 두번째 160 255
left_x = 75
right_x = 150
macro_key = False
left_direction = False
right_direction = True

def moving():
    if left_direction:
        pyautogui.keyUp('left')
    elif not left_direction:
        pyautogui.keyDown('left')
    if right_direction:
        pyautogui.keyUp('right')
    elif not right_direction:
        pyautogui.keyDown('right')

def all_key_up():
    pyautogui.keyUp('left')
    pyautogui.keyUp('right')

def toggle_macro_key(e):
    global macro_key

    macro_key = not macro_key
    if not macro_key:
        all_key_up()

def find_user():
    user = cv2.imread(os.path.join(base_path, "user.png"), cv2.IMREAD_COLOR)
    screenshot_pillow = pyautogui.screenshot(region=(14, 145, 430, 383))
    screenshot_pillow2 = pyautogui.screenshot(allScreens=True)

    screenshot_pillow2.save("all_screen.png")
    screenshot = np.array(screenshot_pillow)

    # Convert the images to grayscale
    user_gray = cv2.cvtColor(user, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Perform template matching at multiple scales
    best_match = None
    best_val = -np.inf
    for scale in np.linspace(0.5, 1.5, 20)[::-1]:
        resized_user = cv2.resize(user_gray, None, fx=scale, fy=scale)
        if resized_user.shape[0] > screenshot_gray.shape[0] or resized_user.shape[1] > screenshot_gray.shape[1]:
            continue
        result = cv2.matchTemplate(screenshot_gray, resized_user, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        if max_val > best_val:
            best_val = max_val
            best_match = (max_loc[0], max_loc[1])

    # Calculate the region to capture
    # left = max(0, best_match[0] - 30)
    # right = min(screenshot_pillow.width, best_match[0] + 30)
    # top = max(0, best_match[1] - 30)
    # bottom = min(screenshot_pillow.height, best_match[1] + 30)

    # # Crop the screenshot
    # cropped_screenshot = screenshot_pillow.crop((left, top, right, bottom))

    # # Save the cropped screenshot
    # cropped_screenshot.save("cropped_screenshot.png")

    return best_match

    
def map_check():
    count = 0
    while True:
        best_match = find_user()
        print("user position:", best_match)
        time.sleep(1)
        if count > 30:
            break

def attack():
    time.sleep(0.2)
    print("공격하라!") 
    pyautogui.keyDown('w')
    pyautogui.keyDown('q')
    pyautogui.keyUp('w')
    pyautogui.keyUp('q')

def macro():
    global left_direction, right_direction

    print("macro start")
    best_match = find_user()

    # If no match found, return
    if best_match is None:
        print("No match found.")
        return

    user_x = best_match[0]

    left_distance = abs(user_x - left_x)
    right_distance =  abs(user_x - right_x)

    print(user_x)
    print("portal distance: ", left_distance)
    print("wall distance: ",right_distance)
    
    if right_direction:
        if right_distance < 15:
            right_direction = False
            left_direction = True
           
    elif left_direction:
        if left_distance < 15:
            right_direction = True
            left_direction = False

    moving()
    attack()

        # if portal_distance < 30 and right_direction:
        #     right_direction = False
        #     left_direction = True
        #     print("오른쪽 키 떼!")
        #     pyautogui.keyUp('right')
        #     pyautogui.keyDown('left')

        # elif wall_distance < 30 and left_direction:
        #     left_direction = False
        #     right_direction = True
        #     print("왼쪽 키 떼!")
        #     pyautogui.keyUp('left')
        #     pyautogui.keyDown('right')

        # else:
        #     # time.sleep(0.4)
        #     # print("이동1!") 
        #     # pyautogui.keyDown('q')
        #     # pyautogui.keyUp('q')
        #     time.sleep(0.2)
        #     print("이동2!") 
        #     pyautogui.keyDown('w')
        #     pyautogui.keyDown('q')
        #     pyautogui.keyUp('w')
        #     pyautogui.keyUp('q')

        # # If 9 minutes have passed since the last key press, press 'd' and 'f'
        # if time.time() - last_press_time >= 9 * 60:
        #     pyautogui.press('d')
        #     pyautogui.press('f')
        #     pyautogui.press('a')
        #     last_press_time = time.time()  
        
        # If the delay time has passed, shutdown the computer
        # if time.time() >= shutdown_time:
        #     os.system("shutdown /s /t 1")
        #     break

def capture():
    while True:
        try:
            print("5초 안에 특정 위치로 마우스를 이동시키세요...")

            # 5초 동안 대기
            time.sleep(5)

            # 현재 마우스 커서의 위치 가져오기
            current_mouse_x, current_mouse_y = pyautogui.position()

            print(f"현재 마우스 커서 위치: x={current_mouse_x}, y={current_mouse_y}")

        except KeyboardInterrupt:
            print("프로그램이 사용자에 의해 중단되었습니다.")
            break


def main():
    keyboard.on_press_key('`', toggle_macro_key)
    

    while True:
        if macro_key:
            macro()

if __name__ == "__main__":
    main()        