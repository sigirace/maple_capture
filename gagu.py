import cv2
import numpy as np
import pyautogui
import time
import os
import keyboard
import random

import time
from PIL import Image

base_path = "C:\\\macro\\images"

# 아래층 첫번째 275 390
# 위층 두번째 160 255
left_x = 22
right_x = 122

macro_key = False
map_check_key = False
capture_key = False

left_direction = False
right_direction = False
d_threshold = 20


def toggle_macro_key(e):
    global macro_key
    macro_key = not macro_key
    if macro_key:
        print("매크로를 시작합니다.")
    else:
        macro()
        print("매크로를 정지합니다.")
        

def toggle_capture_key(e):
    global capture_key
    capture_key = not capture_key
    if capture_key:
        print("캡쳐를 시작합니다.")

def toggle_map_check_key(e):
    global map_check_key
    map_check_key = not map_check_key
    if map_check_key:
        print("맵 체크를 시작합니다.")


def find_user():
    user = cv2.imread(os.path.join(base_path, "user.png"), cv2.IMREAD_COLOR)
    # screenshot_pillow = pyautogui.screenshot(region=(14, 145, 430, 383))
    screenshot_pillow = pyautogui.screenshot(region=(2195, 295, 140, 38), allScreens=True)

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

    return best_match

def map_check():

    best_match = find_user()
    print("유저의 위치:", best_match)
    time.sleep(1)


def capture():

    print("3초 안에 특정 위치로 마우스를 이동시키세요...")
    # 3초 동안 대기
    time.sleep(3)
    # 현재 마우스 커서의 위치 가져오기
    current_mouse_x, current_mouse_y = pyautogui.position()
    print(f"현재 마우스 커서 위치: x={current_mouse_x}, y={current_mouse_y}")


def attack():
    time.sleep(0.2)
    print("공격하라!") 
    pyautogui.keyDown('w')
    pyautogui.keyDown('q')
    pyautogui.keyUp('w')
    pyautogui.keyUp('q')

def random_attack():

    global left_direction
    global right_direction
    nansu = random.randint(0, 100)  # 0 or 1
    time_sleep = random.uniform(0.2, 0.8)  # 0.5 ~ 1.5

    if nansu < 45:
        attack_type = 0
    elif nansu >= 45 and nansu < 90:
        attack_type = 1
    elif nansu >= 90 and nansu < 95:
        attack_type = 2
    else:
        attack_type = 3

    time.sleep(time_sleep)
    if attack_type == 0:
        print("점프 공격!") 
        pyautogui.keyDown('w')
        pyautogui.keyDown('q')
        pyautogui.keyUp('w')
        pyautogui.keyUp('q')
    elif attack_type == 1:
        print("어택 땅!")
        pyautogui.keyDown('q')
        pyautogui.keyUp('q')
    elif attack_type ==2:
        print("오의 1번!")
        if left_direction:
            pyautogui.keyUp('left')
            pyautogui.keyDown('right')
            pyautogui.keyDown('w')
            pyautogui.keyUp('right')
            pyautogui.keyDown('q')
            pyautogui.keyUp('w')
            pyautogui.keyUp('q')
            pyautogui.keyDown('left')
        elif right_direction:
            pyautogui.keyUp('right')
            pyautogui.keyDown('left')
            pyautogui.keyDown('w')
            pyautogui.keyUp('left')
            pyautogui.keyDown('q')
            pyautogui.keyUp('w')
            pyautogui.keyUp('q')
            pyautogui.keyDown('right')
    elif attack_type == 3:
        print("오의 2번!")
        if left_direction:
            pyautogui.keyUp('left')
            pyautogui.keyDown('right')
            pyautogui.keyDown('q')
            pyautogui.keyUp('right')
            pyautogui.keyUp('q')
            pyautogui.keyDown('left')
        elif right_direction:
            pyautogui.keyUp('right')
            pyautogui.keyDown('left')
            pyautogui.keyDown('q')
            pyautogui.keyUp('left')
            pyautogui.keyUp('q')
            pyautogui.keyDown('right')



def direction_check():
    print("방향을 체크합니다")
    global left_direction
    global right_direction
    global macro_key
    best_match = find_user()

    # If no match found, return
    if best_match is None:
        print("No match found.")
        return

    user_x = best_match[0]

    ld = abs(user_x - left_x)
    rd =  abs(user_x - right_x)

    print("현재 유저 우치:", user_x)
    print("왼쪽 거리 차이:", ld)
    print("오른쪽 거리 차이:", rd)

    if macro_key:
        if d_threshold > ld:
            print("왼쪽 끝이기에 오른쪽으로 방향을 바꿉니다.")
            left_direction = False
            right_direction = True
        elif d_threshold > rd:
            print("오른쪽 끝이기에 왼쪽으로 방향을 바꿉니다.")
            right_direction = False
            left_direction = True
        else:
            if not left_direction and not right_direction:
                print("초기 상태이기에 오른쪽으로 이동합니다.")
                right_direction = True
                left_direction = False
            else:
                print("방향을 유지합니다.")

def moving():
    global left_direction
    global right_direction
    global macro_key

    if not macro_key:
        print("멈춥니다.")
        left_direction = False
        right_direction = False
        pyautogui.keyUp('left')
        pyautogui.keyUp('right')
        return
    else:
        if right_direction:
            print("오른쪽으로 이동합니다.")
            pyautogui.keyUp('left')
            pyautogui.keyDown('right')
        else:
            print("왼쪽으로 이동합니다.")
            pyautogui.keyUp('right')
            pyautogui.keyDown('left')
        

def attack():
    time.sleep(0.2)
    print("공격하라!") 
    pyautogui.keyDown('w')
    pyautogui.keyDown('q')
    pyautogui.keyUp('w')
    pyautogui.keyUp('q')

def macro():
    direction_check()
    moving()
    random_attack()


def main():
    keyboard.on_press_key('0', toggle_macro_key)
    keyboard.on_press_key('=', toggle_capture_key)
    keyboard.on_press_key('-', toggle_map_check_key)

    while True:
        if macro_key:
            macro()

        if capture_key:
            capture()

        if map_check_key:
            map_check()

if __name__ == "__main__":
    main()        