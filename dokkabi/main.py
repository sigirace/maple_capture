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
message_key = False
check_thread = None

h = hunt.Hunt()
m = move.Move()
f = finder.Finder()

def toggle_message_key(e):
    global message_key
    message_key = not message_key
    print("메세지 상태를 변경합니다.")

def toggle_macro_key(e):
    global macro_key
    global message_key
    global check_thread

    if e.name == '1':
        macro_key = not macro_key
        if not macro_key:
            message_key = False
            m.moving(stop=True)
            print("매크로를 정지합니다.")
        else:
            print("매크로를 시작합니다.")
            if check_thread is None or not check_thread.is_alive():
                check_thread = threading.Thread(target=periodic_check, daemon=True)
                check_thread.start()

def toggle_capture_map_key(e):
    print("신규 맵에 대한 캡쳐를 시작합니다.")
    f.new_capture('map')
            
def toggle_capture_chat_key(e):
    print("신규 채팅에 대한 캡쳐를 시작합니다.")
    f.new_capture('chat')            

def toggle_capture_back_key(e):
    print("신규 전체 화면에 대한 캡쳐를 시작합니다.")
    f.new_capture('background')     

def toggle_user_thd_key(e):
    print("유저의 한계점을 재설정합니다.")
    m.set_thd(f.map_loc) 

def on_off(ns):
    now_state = "On" if ns else "Off"
    return now_state

def check():
    global macro_key
    try:
        if macro_key:
            print("=======================상태 체크=======================")
            # 저주 체크
            val = f.detector(location='chat', object_name="dis")
            if val >= 0.45:
                print("저주 발동! ,", val)
                h.dispell()

            # 대나무 무사 체크
            for i in range(1,3):
                # 매크로 방지몹 체크
                val = f.detector(location='background', object_name='damu_{}'.format(str(i)))
                print(val)
                if val >= 0.86:
                    print("대나무 무사 등장! ,",val)
                    #copilot 작성
                    alarm.discord_send_message("대나무 무사 등장!!!!")
                    macro_key = False
                    m.moving(stop=True)
                    print("매크로를 정지합니다.")
            print("=======================체크 완료=======================")
    except Exception as e:
        print(f"check 함수에서 예외 발생: {e}")
        # 예외 발생 시에도 계속 실행되도록 macro_key를 True로 유지하거나, 적절한 조치를 취합니다.

def periodic_check():
    while True:
        check()
        time.sleep(1)  # 1초 간격으로 체크

def macro():
    global message_key
    global macro_key

    print("=======================상황 체크=======================")
    print("매크로 상태:", on_off(macro_key), "메세지 상태:", on_off(message_key))
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
        alarm.discord_send_message("다른 유저 발견!")
        message_key = True
    elif red_user == 0 and message_key:
        alarm.discord_send_message("그냥 갔네.. 휴..")
        message_key = False

def main():
    global check_thread
    if check_thread is None or not check_thread.is_alive():
        check_thread = threading.Thread(target=periodic_check, daemon=True)
        check_thread.start()
    
    print(threading.enumerate())
    keyboard.on_press_key('1', toggle_macro_key)
    keyboard.on_press_key('2', toggle_capture_map_key)
    keyboard.on_press_key('3', toggle_capture_chat_key)
    keyboard.on_press_key('4', toggle_capture_back_key)
    keyboard.on_press_key('5', toggle_user_thd_key)
    keyboard.on_press_key(';', toggle_message_key)

    while True:
        if macro_key:
            macro()
        

if __name__ == "__main__":
    main()