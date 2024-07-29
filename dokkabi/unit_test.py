
import keyboard
import hunt
import move
import finder
from kakao import kakao_message
import time

M = move.Move()
F = finder.Finder()
H = hunt.Hunt()

macro_key = False
capture_key = False
user_thd_key = False
message_key = False

def macro_test(e):
    global macro_key
    macro_key = not macro_key
    
    if not macro_key:
        print("유저 위치 파악을 정지합니다.")

def macro():
    time.sleep(0.5)
    F.find_user()
    # best_val, best_match, match_count = F.find_match(object_name='user', location=F.map_loc)
    # print("--------------------")
    # print("유저 위치 정보: ", best_match)
    # print("유저 확률: ", best_val)
    # print("타 유저 여부: ", match_count)
    # print("--------------------")


def finder_test(e):
    global capture_key
    capture_key = not capture_key
    if capture_key:
        print("신규 맵에 대한 캡쳐를 시작합니다.")

def capture():
    global capture_key

    F.new_map_capture()
    capture_key = False

def thd_test(e):
    global user_thd_key
    user_thd_key = not user_thd_key
    if user_thd_key:
        print("유저의 한계점을 재설정합니다.")

def user_thd():
    global user_thd_key
    M.set_thd(F.map_loc)
    user_thd_key = False

def moving_test(e):
    pass

def main():

    keyboard.on_press_key('1', macro_test)
    keyboard.on_press_key('2', finder_test)
    keyboard.on_press_key('3', thd_test)
    keyboard.on_press_key('4', moving_test)

    while True:

        if macro_key:
            macro()

        if capture_key:
            capture()

        if user_thd_key:
            user_thd()




if __name__ == "__main__":
    main()