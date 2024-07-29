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
# 1931 147
# 2276 373
left_x = 50
right_x = 310

map_left_x = 1931
map_left_y = 147
map_right_x = 2276
map_right_y = 373
map_loc = (map_left_x, map_left_y, abs(map_right_x-map_left_x), abs(map_right_y-map_left_y))

g_user_x = 0
g_user_cnt= 0
buff = {'x': [180, None], 
        'c': [180, None], 
        # 'd': [180, None], 
        # 'f': [300, None], 
        'a': [600, None], 
        'v': [45, None]}

chat_loc = (1924, 932, abs(3046-1924), abs(990-932))

info_key = False
macro_key = False
map_check_key = False
capture_key = False

left_direction = False
right_direction = False
d_threshold = 20

def input_point():
    global left_x
    global right_x
    left_x = int(input("왼쪽 x 좌표를 입력하세요: "))
    right_x = int(input("오른쪽 x 좌표를 입력하세요: "))

def toggle_info_key(e):
    global info_key
    info_key = not info_key
    if info_key:
        print("현재 정보")

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

def find_dis():
    dis = cv2.imread(os.path.join(base_path, "dis.png"), cv2.IMREAD_COLOR)
    screenshot_pillow = pyautogui.screenshot(region=chat_loc, allScreens=True)
    screenshot = np.array(screenshot_pillow)

    # Convert the images to grayscale
    chat_gray = cv2.cvtColor(dis, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

    # Perform template matching at multiple scales
    best_val = 0  # Initialize best_val
    for scale in np.linspace(0.5, 1.5, 20)[::-1]:
        resized_user = cv2.resize(chat_gray, None, fx=scale, fy=scale)
        if resized_user.shape[0] > screenshot_gray.shape[0] or resized_user.shape[1] > screenshot_gray.shape[1]:
            continue
        result = cv2.matchTemplate(screenshot_gray, resized_user, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        if max_val > best_val:
            best_val = max_val
    return best_val >= 0.5


def find_user():
    
    user = cv2.imread(os.path.join(base_path, "user.png"), cv2.IMREAD_COLOR)
    # screenshot_pillow = pyautogui.screenshot(region=(14, 145, 430, 383))
    screenshot_pillow = pyautogui.screenshot(region=map_loc, allScreens=True)

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
    global map_left_x
    global map_left_y
    global map_right_x
    global map_right_y
    global map_loc
    global capture_key

    for i in range(2):
        print(i+1, "번째 캡쳐를 시작합니다.")
        print("3초 안에 특정 위치로 마우스를 이동시키세요...")
        # 3초 동안 대기
        time.sleep(3)
        # 현재 마우스 커서의 위치 가져오기
        current_mouse_x, current_mouse_y = pyautogui.position()
        print(f"현재 마우스 커서 위치: x={current_mouse_x}, y={current_mouse_y}")
        if i == 0:
            map_left_x = current_mouse_x
            map_left_y = current_mouse_y
        else:
            map_right_x = current_mouse_x
            map_right_y = current_mouse_y

    print("신규 맵 설정 완료")
    map_loc = (map_left_x, map_left_y, abs(map_right_x-map_left_x), abs(map_right_y-map_left_y))
    capture_key = False


def attack(key):
    print("점프 공격!") 
    pyautogui.keyDown('w')
    pyautogui.keyDown(key)
    pyautogui.keyUp('w')
    pyautogui.keyUp(key)

# def change_attack():
#     print("뒤돌아보면..?") 
#     global left_direction
#     global right_direction
#     if left_direction:
#         pyautogui.keyUp('left')
#         pyautogui.keyDown('right')
#         pyautogui.keyDown('w')
#         pyautogui.keyDown('q')
#         pyautogui.keyUp('w')
#         pyautogui.keyUp('q')
#         pyautogui.keyUp('right')
#         pyautogui.keyDown('left')
#     elif right_direction:
#         pyautogui.keyUp('right')
#         pyautogui.keyDown('left')
#         pyautogui.keyDown('w')
#         pyautogui.keyDown('q')
#         pyautogui.keyUp('w')
#         pyautogui.keyUp('q')
#         pyautogui.keyUp('left')
#         pyautogui.keyDown('right')


def change_attack(key):
    print("방향을 바꿔!")
    global left_direction
    global right_direction

    
    if left_direction:
        pyautogui.keyDown('w')
        pyautogui.keyUp('left')
        pyautogui.keyDown('right')
        time.sleep(0.1)
        pyautogui.keyDown(key)
        pyautogui.keyUp('w')
        pyautogui.keyUp(key)
        pyautogui.keyUp('right')
        final_attack()
        pyautogui.keyDown('left')
    elif right_direction:
        pyautogui.keyDown('w')
        pyautogui.keyUp('right')
        pyautogui.keyDown('left')
        time.sleep(0.1)
        pyautogui.keyDown(key)
        pyautogui.keyUp('w')
        pyautogui.keyUp(key)
        pyautogui.keyUp('left')
        final_attack()
        pyautogui.keyDown('right')

def flash_attack(key):
    print("플점 어택!")
    pyautogui.keyDown('w')
    pyautogui.keyDown('e')
    pyautogui.keyDown(key)
    pyautogui.keyUp('w')
    pyautogui.keyUp('e')
    pyautogui.keyUp(key)

def final_attack():
    print("마무리 공격!")
    final_attack = random.randint(0, 10)
    attack_nansu = random.randint(0, 10)
    time.sleep(0.3)

    if final_attack < 9:
        pyautogui.keyDown('r')
        pyautogui.keyUp('r')       
    else:
        return


def random_attack():
    
    time_sleep = random.uniform(0, 0.1)  # 0.5 ~ 1.5
    time.sleep(time_sleep)

    key_nansu = random.randint(0, 10)
    if key_nansu < 9:
        key = 'q'
    else:
        key = 't'

    nansu = random.randint(0, 100)
    if nansu < 70:
        attack(key)
    else:
        change_attack(key)

def dis_check():
    if find_dis():
        print("저주에 걸렸습니다.")
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        time.sleep(0.2)
        pyautogui.keyDown('z')
        time.sleep(0.2)
        pyautogui.keyUp('z')
        time.sleep(0.2)
        pyautogui.keyDown('enter')
        pyautogui.keyUp('enter')
        time.sleep(0.2)
        pyautogui.keyDown('end')
        pyautogui.keyUp('end')
        print("저주를 해제하였습니다.")


def direction_check():
    print("방향을 체크합니다")
    global left_direction, right_direction
    global macro_key, g_user_x, g_user_cnt

    best_match = find_user()

    # If no match found, return
    if best_match is None:
        print("No match found.")
        return

    user_x = best_match[0]
    
    if g_user_x == user_x:
        g_user_cnt += 1
    else:
        g_user_x = user_x
        g_user_cnt = 0

    if g_user_cnt > 3:
        print("유저가 같은 방향에 위치합니다. 다른 방향으로 이동합니다.")
        left_direction = not left_direction
        right_direction = not right_direction
        flash_attack('q')
        return
    
    ld = abs(user_x - left_x)
    rd =  abs(user_x - right_x)

    print("현재 유저 위치:", user_x)
    print("왼쪽 거리 차이:", ld)
    print("오른쪽 거리 차이:", rd)

    if macro_key:
        if user_x < left_x:
            print("왼쪽 끝이기에 오른쪽으로 방향을 바꿉니다.")
            left_direction = False
            right_direction = True
            # flash_attack('q')
        elif user_x > right_x:
            print("오른쪽 끝이기에 왼쪽으로 방향을 바꿉니다.")
            right_direction = False
            left_direction = True
            # flash_attack('q')
        else:
            if not left_direction and not right_direction:
                print("초기 상태이기에 오른쪽으로 이동합니다.")
                right_direction = True
                left_direction = False
            else:
                print("방향을 유지합니다.")

def moving():
    global left_direction, right_direction, macro_key

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
        

def buff_key(key):
    time.sleep(0.4)
    pyautogui.keyDown(key)
    pyautogui.keyUp(key)

def pet_buff_key():
    time.sleep(0.4)
    # pyautogui.keyDown('f')
    # pyautogui.keyUp('f')
    # time.sleep(0.4)
    # pyautogui.keyDown('a')
    # pyautogui.keyUp('a')
    

def buff_check():
    global buff

    for key, item in buff.items():
        if item[1] is None:
            buff_key(key)
            item[1] = time.time()
        else:
            if time.time() - item[1] >= item[0]:
                buff_key(key)
                item[1] = time.time()

def macro():
    buff_check()
    dis_check()
    direction_check()
    moving()
    random_attack()


def info():
    global info_key
    print("왼쪽 x 좌표:", left_x)
    print("오른쪽 x 좌표:", right_x)
    print("맵 정보:", map_loc)
    info_key = False
         

def main():
    keyboard.on_press_key('9', toggle_info_key)
    keyboard.on_press_key('0', toggle_macro_key)
    keyboard.on_press_key('=', toggle_capture_key)
    keyboard.on_press_key('-', toggle_map_check_key)
    

    while True:
        if info_key:
            info()

        if macro_key:
            macro()

        if capture_key:
            capture()

        if map_check_key:
            map_check()

if __name__ == "__main__":
    main()        