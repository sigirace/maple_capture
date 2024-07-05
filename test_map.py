import cv2
import numpy as np
import pyautogui
import time
import threading
import pytesseract
import re
import os
import keyboard

base_path = "C:\\\macro\\images"

macro_key = False
map_check_key = False
capture_key = False

upper_x = 1994
upper_y = 142
lower_x = 2112
lower_y = 279

def toggle_map_check_key(e):
    global map_check_key
    map_check_key = not map_check_key
    if map_check_key:
        print("맵 체크를 시작합니다.")
    else:  
        print("맵 체크를 정지합니다.")

def toggle_capture_key(e):
    global capture_key
    capture_key = not capture_key
    if capture_key:
        print("캡쳐를 시작합니다.")
    else:
        print("캡쳐를 정지합니다.")


def find_user():

    global upper_x, upper_y, lower_x, lower_y

    user = cv2.imread(os.path.join(base_path, "user.png"), cv2.IMREAD_COLOR)
    # screenshot_pillow = pyautogui.screenshot(region=(14, 145, 430, 383))
    # print("start point: ", upper_x, upper_y)
    # print("size: ", lower_x-upper_x, lower_y-upper_y)
    screenshot_pillow = pyautogui.screenshot(region=(upper_x, upper_y, lower_x-upper_x, lower_y-upper_y), allScreens=True)

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


def moving():
    global map_check_key
    
    print("유저를 찾습니다.")
    best_match = find_user()
    print("유저의 위치:", best_match)

    print("목표 위치는 +100 입니다.")

    user_x = best_match[0]
    target_x = user_x + 100

    print("5초 안에 메이플을 클릭해주세요...")
    time.sleep(5)
    print("이동을 시작합니다.")
    start_time = time.time()
    pyautogui.keyDown('right')
    while True:
        now_user = find_user()
        print("현재 유저의 위치:", now_user)
        if now_user[0] >= target_x:
            print("도착했습니다.")
            pyautogui.keyUp('right')
            end_time = time.time()            
            break
    
    end_user = find_user()
    print("유저의 위치:", end_user)
    print("이동 소요 시간:", end_time-start_time)
    map_check_key = False

def moving_test():
    global map_check_key
    print(1)
    time_moving()
    map_check_key = False


def time_moving():
    print(2)
    pyautogui.keyDown('left')
    time.sleep(2)
    pyautogui.keyUp('left')

def moving_jump():
    target = [30, 62]
    
    print("유저를 찾습니다.")
    best_match = find_user()
    print("유저의 위치:", best_match)

    print("5초 안에 메이플을 클릭해주세요...")
    time.sleep(5)
    
    if target[0] < best_match[0]:
        if side_moving('left', target) and jump_moving('up', target):
            return True
        else:
            return False
    else:
        if side_moving('right', target) and jump_moving('up', target):
            return True
        else:
            return False



def side_moving(direction, target, threshold=1):
    print("목표 위치는 {} 입니다.".format(direction))
    if direction == 'left':
        other_side = 'right'
    else:
        other_side = 'left'
    
    cnt = 0
    before_value = 0
    pyautogui.keyDown(direction)
    while True:
        user_loc = find_user()
        now_value = abs(user_loc[0] - target[0])
        print("현재 유저의 위치:", user_loc)
        if now_value <= threshold:
            pyautogui.keyUp(direction)
            pyautogui.keyDown(other_side)
            pyautogui.keyUp(other_side)
            print(now_value, threshold)
            print("도착했습니다.")
            return True
        if before_value >= now_value - 3 and before_value <= now_value + 3:
            print("잘못움직인듯..?")
            cnt += 1
        
        if cnt > 10:
            print("이동 실패...")
            return False


def jump_moving(direction, target, threshold=1):
    print("목표 위치는 {} 입니다.".format(direction))

    cnt = 0
    before_value = 0
    pyautogui.keyDown('w')
    while True:
        user_loc = find_user()
        now_value = abs(user_loc[1] - target[1])
        print("현재 유저의 위치:", user_loc)
        if now_value <= threshold:
            pyautogui.keyUp('w')
            print(now_value, threshold)
            print("도착했습니다.")
            return True
        if before_value >= now_value - 12 and before_value <= now_value + 12:
            print("잘못움직인듯..?")
            cnt += 1
        
        if cnt > 10:
            print("이동 실패...")
            return False


def map_check():

    best_match = find_user()
    print("유저의 위치:", best_match)
    time.sleep(1)


def capture():

    global capture_key
    global upper_x, upper_y, lower_x, lower_y

    for i in range(2):
        print(i+1, "번째 캡쳐를 시작합니다.")
        print("3초 안에 특정 위치로 마우스를 이동시키세요...")
        # 3초 동안 대기
        time.sleep(3)
        # 현재 마우스 커서의 위치 가져오기2
        current_mouse_x, current_mouse_y = pyautogui.position()
        print(f"현재 마우스 커서 위치: x={current_mouse_x}, y={current_mouse_y}")

        if i == 0:
            upper_x = current_mouse_x
            upper_y = current_mouse_y
        else:
            lower_x = current_mouse_x
            lower_y = current_mouse_y

    capture_key = False
    print("캡쳐를 종료합니다.")



def main():
    keyboard.on_press_key('=', toggle_capture_key)
    keyboard.on_press_key('-', toggle_map_check_key)

    while True:
        if capture_key:
            capture()

        if map_check_key:
            moving_test()
        
        map_check()

if __name__ == "__main__":
    main()        