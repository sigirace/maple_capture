import pyautogui
import common as cm

# 매크로 수행을 위한 클래스
# 이동, 사냥, 버프 등의 기능 수행

class Move():

    def __init__(self):
        self.left_direction = False
        self.right_direction = False
        self.left_thd = 65
        self.right_thd = 320
        self.maule_loc = (3536, 401)
    
    def set_thd(self, map_loc):
        positions = []
        for i in range(2):
            message = f"{i+1}번째 캡쳐를 시작합니다. 3초 안에 특정 위치로 마우스를 이동시키세요..."
            positions.append(cm.capture_mouse_position(message))

        print("이동 한계점 설정 완료")
        self.left_thd, self.right_thd = abs(map_loc[0] - positions[0][0]), abs(map_loc[0]- positions[1][0])

        print("왼쪽 한계점:", self.left_thd)
        print("오른쪽 한계점:", self.right_thd)
    
    def maul_setting(self):
        self.maule_loc = cm.capture_mouse_position()
    
    def direction_check(self, user_x):

        print("방향을 체크합니다 => USER:", user_x, "LD:", self.left_thd, "RD:", self.right_thd)

        if user_x < self.left_thd:
            print("왼쪽 끝이기에 오른쪽으로 방향을 바꿉니다.")
            self.left_direction = False
            self.right_direction = True
            
        elif user_x > self.right_thd:
            print("오른쪽 끝이기에 왼쪽으로 방향을 바꿉니다.")
            self.right_direction = False
            self.left_direction = True
        else:
            if not self.left_direction and not self.right_direction:
                print("초기 상태이기에 오른쪽으로 이동합니다.")
                self.right_direction = True
                self.left_direction = False
            else:
                print("방향을 유지합니다.")
                return False
        
        return True

    def moving(self, stop=False):

        if stop:
            print("멈춥니다.")
            self.left_direction = False
            self.right_direction = False
            pyautogui.keyUp('left')
            pyautogui.keyUp('right')
            return
        else:
            if self.right_direction:
                print("오른쪽으로 이동합니다.")
                pyautogui.keyUp('left')
                pyautogui.keyDown('right')
            else:
                print("왼쪽으로 이동합니다.")
                pyautogui.keyUp('right')
                pyautogui.keyDown('left')                