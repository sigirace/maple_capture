import keyboard
import hunt
import move
import finder
from kakao import kakao_message
import time

m = move.Move()
f = finder.Finder()
h = hunt.Hunt()

test_state = False
capture_key = False

def toggle_capture_map_key(e):
    print("신규 맵에 대한 캡쳐를 시작합니다.")
    f.new_capture('map')
            
def toggle_capture_chat_key(e):
    print("신규 채팅에 대한 캡쳐를 시작합니다.")
    f.new_capture('chat')            

def toggle_capture_back_key(e):
    print("신규 채팅에 대한 캡쳐를 시작합니다.")
    f.new_capture('background')     

def toggle_test(e):
    global test_state
    test_state = not test_state
    print(f"Test state toggled: {test_state}")

def test():
    # red_user, user_point = f.find_user()
    # print("red_user:", red_user)
    # print("user_point:", user_point)
    for i in range(1,3):
        # 거탐 체크f
        val = f.detector(location='background', object_name='damu_{}'.format(str(i)))
        print(val)
        if val >= 0.795:
            print(val)
            print("대나무 무사 등장!!!!")

            # alarm.discord_send_message("대나무 무사 등장!!!!")
    print("test")

def main():
    keyboard.on_press_key('1', toggle_test)
    keyboard.on_press_key('2', toggle_capture_map_key)
    keyboard.on_press_key('3', toggle_capture_chat_key)
    keyboard.on_press_key('4', toggle_capture_back_key)

    while True:
        if test_state:
            test()
        time.sleep(0.1)  # Add a small delay to prevent high CPU usage

if __name__ == "__main__":
    main()