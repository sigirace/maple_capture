import pyautogui
import time

def capture_mouse_position(message='마우스 위치를 캡쳐합니다. 3초 후에 캡쳐됩니다.'):
    print(message)
    time.sleep(3)  # 3초 동안 대기
    return pyautogui.position()  # 현재 마우스 커서의 위치 반환

def key_input(key, sleep=0.0):
    time.sleep(sleep)
    pyautogui.keyDown(key)
    pyautogui.keyUp(key)

def chatting(start_message='채팅을 입력합니다.', end_message='채팅을 보냈습니다.', chat_key='z'):

    print(start_message)
    pyautogui.keyDown('f2')
    pyautogui.keyUp('f2')
    time.sleep(0.2)
    pyautogui.keyDown(chat_key)
    time.sleep(0.2)
    pyautogui.keyUp(chat_key)
    time.sleep(0.2)
    pyautogui.keyDown('enter')
    pyautogui.keyUp('enter')
    time.sleep(0.2)
    print(end_message)