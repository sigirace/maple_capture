import keyboard
import hunt
import move
import finder
from kakao import kakao_message
import time
import common as cm
import os
import pyautogui
import alarm
import threading
import random

macro_key = False
capture_key = False
user_thd_key = False
message_key = False
prevent_key = False

red_user_time = None

h = hunt.Hunt()
m = move.Move()
f = finder.Finder()
run_time = time.time()

def toggle_prevent_key(e):
    global prevent_key
    if e.name == '=':
        prevent_key = not prevent_key
        if prevent_key:
            print("키 입력을 막습니다.")
        else:
            print("키 입력을 허용합니다.")

def toggle_macro_key(e):
    global macro_key
    global prevent_key
    global message_key

    if prevent_key:
        return
    
    if e.name == '1':
        macro_key = not macro_key
        if not macro_key:
            message_key = False
            m.moving(stop=True)
            print("매크로를 정지합니다.")
        else:
            print("매크로를 시작합니다.")

def toggle_capture_key(e):
    global capture_key
    global prevent_key

    if prevent_key:
        return
    
    if e.name == '2':
        capture_key = not capture_key
        if capture_key:
            print("신규 맵에 대한 캡쳐를 시작합니다.")

def toggle_user_thd_key(e):
    global user_thd_key
    global prevent_key

    if prevent_key:
        return
    
    if e.name == '3':
        user_thd_key = not user_thd_key
        if user_thd_key:
            print("유저의 한계점을 재설정합니다.")

def toggle_message_key(e):
    global message_key
    if e.name == ';':
        message_key = not message_key
        if message_key:
            print("카톡 설정을 초기화 합니다.")

def on_off(ns):
    now_state = "On" if ns else "Off"
    return now_state

def check():
    global macro_key
    try:
        if macro_key:
            print("=======================상태 체크=======================")
            # 저주 체크
            if f.detector(location='chat', object_name="dis"):
                h.dispell()

            for i in range(1,3):
                # 거탐 체크
                if f.detector(location='background', object_name=str(i)):
                    macro_key = False
                    m.moving(stop=True)
                    alarm.discord_send_message("거탐걸렸다!!!!")
            print("=======================체크 완료=======================")
    except Exception as e:
        print(f"check 함수에서 예외 발생: {e}")
        # 예외 발생 시에도 계속 실행되도록 macro_key를 True로 유지하거나, 적절한 조치를 취합니다.

def macro():
    global message_key
    global red_user_time
    global macro_key

    print("=======================상황 체크=======================")
    print("매크로 상태:", on_off(macro_key), "메세지 상태:", on_off(message_key), "타유저 발견 시간:", red_user_time)
    print("=====================================================")

    # 버프 체크
    h.buff()

    # 유저 위치 파악
    red_user, user_point = f.find_user()
    # 못찾을경우 중앙값 임시 대체
    if len(user_point) == 0:
        print("유저를 찾을 수 없습니다.")
        user_point = [(int((m.left_thd + m.right_thd) / 2), 0)]
    
    # 유저 방향 파악
    if m.direction_check(user_point[0][0]):
        m.moving()
        h.flash_attack()
    else:
        # 공격
        time.sleep(random.uniform(0.1, 0.3))
        direction = (m.left_direction, m.right_direction)
        h.random_attack(direction)

    print("현재 방향 => 왼쪽:", on_off(m.left_direction), "오른쪽:", on_off(m.right_direction))
    # 난입 메세지
    print("다른 유저 수: ", red_user)
    if red_user > 0 and not message_key:
        red_user_time = time.time()
        alarm.discord_send_message("다른 유저 발견!")
        message_key = True
    elif red_user == 0 and message_key:
        alarm.discord_send_message("그냥 갔네.. 휴..")
        message_key = False
        red_user_time = None

    if red_user_time is not None:
        if time.time() - red_user_time > 40:
            if message_key:
                macro_key = False
                m.moving(stop=True)
                alarm.discord_send_message("자꾸 쳐다봐서 매크로를 종료합니다. ㅡㅡ")
                maule(m.maule_loc[0], m.maule_loc[1])
                alarm.discord_send_message("마을귀환!! 튀엇~~")
            else:
                red_user_time = None
                alarm.discord_send_message("신강식의 완벽한 대응 발동!")
        # os.system('shutdown -s -f')

    # if time.time() - run_time > 3600:
    #     print("60분이 지났습니다. 종료합니다.")
    #     maule()
    #     kakao_message.run("성공적인 매크로였다..")
    #     macro_key = False
    #     os.system('shutdown -s -f')

def capture():
    global capture_key
    f.new_map_capture()
    capture_key = False

def user_thd():
    global user_thd_key
    m.set_thd(f.map_loc)
    user_thd_key = False

def find_position(e):
    if e.name == '4':
        print(cm.capture_mouse_position())

def message_check(e):
    if e.name == '5':
        alarm.discord_send_message("테스트 메세지")

def maule_setting(e):
    if e.name == '6':
        m.maul_setting()
        print(m.maule_loc)

def maule_check(e):
    if e.name == '7':
        maule(m.maule_loc[0], m.maule_loc[1])

def maule(x, y):
    pyautogui.click(x, y, clicks=10)
    pyautogui.doubleClick(x, y, interval=0.0)
    pyautogui.doubleClick(x, y, interval=0.0)
    pyautogui.doubleClick(x, y, interval=0.0)

def main():
    def periodic_check():
        while True:
            check()
            time.sleep(1)  # 1초 간격으로 체크

    check_thread = threading.Thread(target=periodic_check, daemon=True)
    check_thread.start()
    
    print(threading.enumerate())
    keyboard.on_press_key('1', toggle_macro_key)
    keyboard.on_press_key('2', toggle_capture_key)
    keyboard.on_press_key('3', toggle_user_thd_key)
    # keyboard.on_press_key(';', toggle_message_key)
    # keyboard.on_press_key('=', toggle_prevent_key)
    # keyboard.on_press_key('4', find_position)
    # keyboard.on_press_key('5', message_check)
    # keyboard.on_press_key('6', maule_setting)
    # keyboard.on_press_key('7', maule_check)

    while True:
        if macro_key:
            macro()

        if capture_key:
            capture()

        if user_thd_key:
            user_thd()
        

if __name__ == "__main__":
    main()
