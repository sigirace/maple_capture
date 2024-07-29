import pyautogui
import time
import random
import common as cm

class Hunt:
    def __init__(self):
        self.buff_list = {'x': [180, None], 
                    'c': [180, None], 
                    # 'd': [180, None], 
                    # 'f': [300, None], 
                    'a': [600, None], 
                    'v': [55, None]}

    def jump_attack(self, key='q'):
        print("점프 공격!") 
        pyautogui.keyDown('w')
        pyautogui.keyDown(key)
        pyautogui.keyUp('w')
        pyautogui.keyUp(key)
    
    def flash_attack(self, key='q'):
        print("플점 어택!")
        pyautogui.keyDown('w')
        pyautogui.keyDown('e')
        pyautogui.keyDown(key)
        pyautogui.keyUp('w')
        pyautogui.keyUp('e')
        pyautogui.keyUp(key)
    
    def final_attack(self, key='r'):
        print("마무리 공격!")
        final_attack = random.randint(0, 10)
        time.sleep(0.3)

        if final_attack < 9:
            pyautogui.keyDown(key)
            pyautogui.keyUp(key)       
        else:
            return

    def change_attack(self, now_direction, key='q'):
        left_direction, right_direction = now_direction
        
        rand_time = random.uniform(0, 0.15)

        if left_direction:
            pyautogui.keyDown('w')
            pyautogui.keyUp('left')
            pyautogui.keyDown('right')
            time.sleep(rand_time)
            pyautogui.keyDown(key)
            pyautogui.keyUp('w')
            pyautogui.keyUp(key)
            pyautogui.keyUp('right')
            self.final_attack()
            pyautogui.keyDown('left')
        elif right_direction:
            pyautogui.keyDown('w')
            pyautogui.keyUp('right')
            pyautogui.keyDown('left')
            time.sleep(rand_time)
            pyautogui.keyDown(key)
            pyautogui.keyUp('w')
            pyautogui.keyUp(key)
            pyautogui.keyUp('left')
            self.final_attack()
            pyautogui.keyDown('right')
    
    def random_attack(self, direction):
    
        time_sleep = random.uniform(0.1, 0.2)  # 0.5 ~ 1.5
        time.sleep(time_sleep)

        key_nansu = random.randint(0, 10)
        if key_nansu < 9:
            key = 'q'
        else:
            key = 't'

        nansu = random.randint(0, 100)
        if nansu < 70:
            self.jump_attack(key)
        else:
            self.change_attack(direction, key)

    def buff(self):
        for key, item in self.buff_list.items():
            if item[1] is None:
                cm.key_input(key, 0.4)
                item[1] = time.time()
            else:
                if time.time() - item[1] >= item[0]:
                    cm.key_input(key, 0.4)
                    item[1] = time.time()
    
    def dispell(self):

        cm.chatting(start_message='저주에 걸렸습니다', end_message='저주를 해제하였습니다.')
        cm.key_input('end', 0.2)