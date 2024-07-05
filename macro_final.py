import cv2
import numpy as np
import pyautogui
import time
import threading
import pytesseract
import re
import os

base_path = "C:\\\macro\\images"

# ---------- 캐릭터 인식작업 수행 함수----------------


def find_character_coordinates():
    print("캐릭터 인식 작업 수행중..")
    left_character_image = cv2.imread(
        os.path.join(base_path, "left_char2.png"), cv2.IMREAD_COLOR)
    
    right_character_image = cv2.imread(
        os.path.join(base_path, "right_char2.png"), cv2.IMREAD_COLOR)
    
    character_x, character_y, character_direction_left = None, None, None
    
    while True:
        screenshot_pillow = pyautogui.screenshot()
        screenshot = np.array(screenshot_pillow)

        left_result = cv2.matchTemplate(
            screenshot, left_character_image, cv2.TM_CCOEFF_NORMED)
        right_result = cv2.matchTemplate(
            screenshot, right_character_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        print("left:", cv2.minMaxLoc(left_result)[1])
        print("right:", cv2.minMaxLoc(right_result)[1])
        left_similarity = cv2.minMaxLoc(left_result)[1] if cv2.minMaxLoc(left_result)[
            1] >= threshold else 0
        right_similarity = cv2.minMaxLoc(right_result)[1] if cv2.minMaxLoc(
            right_result)[1] >= threshold else 0

        if left_similarity > right_similarity:
            character_location = cv2.minMaxLoc(left_result)[3]
            character_x, character_y = character_location[0], character_location[1]
            character_direction_left = True
            print(f"좌측 면 캐릭터가 인식되었습니다. 좌표: ({character_x}, {character_y})")
            break
        elif right_similarity > left_similarity:
            character_location = cv2.minMaxLoc(right_result)[3]
            character_x, character_y = character_location[0], character_location[1]
            character_direction_left = False
            print(f"우측 면 캐릭터가 인식되었습니다. 좌표: ({character_x}, {character_y})")
            break

        # 인식 실패 시 왼쪽으로 이동
        pyautogui.keyDown("left")
        pyautogui.keyDown("alt")
        time.sleep(3)
        pyautogui.keyUp("left")
        pyautogui.keyUp("alt")

        # 인식 실패 시 우측으로 이동
        pyautogui.keyDown("right")
        pyautogui.keyDown("alt")
        time.sleep(3)
        pyautogui.keyUp("right")
        pyautogui.keyUp("alt")

        print("캐릭터 인식 실패. 좌측으로 이동 후 다시 시도합니다.")

    print("캐릭터 인식이 종료되었습니다.")
    return character_x, character_y, character_direction_left


# ---------- 캐릭터 이동 함수----------------
def move_character(character_x, target_x, character_direction_left):
    distance = abs(character_x - target_x)
    # 캐릭터가 바라보는 방향과 이동 방향이 일치할 때
    if (character_x > target_x and character_direction_left) or (character_x < target_x and not character_direction_left):
        movement_time = distance / 117 * 0.35
    else:
        # 반대면일 경우 이동할 좌표에서 16을 뺍니다.
        movement_time = (distance - 16) / 117 * 0.35

    direction = "left" if character_x > target_x else "right"
    print(f"캐릭터를 {direction}로 이동합니다. 예상 시간: {movement_time:.2f}초")
    pyautogui.keyDown('z')
    pyautogui.keyDown(direction)
    time.sleep(movement_time)
    pyautogui.keyUp(direction)
    pyautogui.keyUp('z')


# ---------- 채널 변경 함수----------------
def change_channel():
    print("채널 변경 작업 수행중..")
    time.sleep(3.0)
    # 1. 좌표 1681, 98 클릭
    pyautogui.click(1681, 98)
    time.sleep(1.5)

    # 2. 좌표 1681, 175 클릭
    pyautogui.click(1681, 175)
    time.sleep(1.5)

    # 3. C:\dump\ch.png 이미지를 찾아서 클릭
    ch_image_location = pyautogui.locateOnScreen(
        os.path.join(base_path,"ch.png"), confidence=0.7)
    if ch_image_location:
        ch_x, ch_y = pyautogui.center(ch_image_location)
        pyautogui.click(ch_x, ch_y)
        time.sleep(1.5)
    else:
        print("ch.png 이미지를 찾지 못했습니다.")

    # 4. 좌표 1081, 714 클릭
    pyautogui.click(1081, 714)
    time.sleep(1.5)

    # 5. 좌표 1072, 635 클릭
    pyautogui.click(1072, 635)
    time.sleep(1.5)

    # 6. 약 3분간 대기
    time.sleep(180)
    ch_image_location = pyautogui.locateOnScreen(
        os.path.join(base_path,"mainch.png"), confidence=0.7)
    while True:
        if ch_image_location:
            ch_x, ch_y = pyautogui.center(ch_image_location)
            pyautogui.click(979, 709)
            time.sleep(5)
            pyautogui.click(579, 805)
            time.sleep(2)
            pyautogui.click(1396, 532)
            time.sleep(20)
            pyautogui.click(1400, 766)
            break
        else:
            time.sleep(30)

# ---------- 유저 감지 및 채널 변경 호출----------------


def check_for_channel_change():
    while True:
        # 스크린샷을 캡쳐합니다.
        screenshot_pillow = pyautogui.screenshot(
            region=(12, 67, 282 - 12, 374 - 67))
        screenshot = np.array(screenshot_pillow)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # 템플릿 이미지를 로드합니다 (경로는 적절히 설정해야 함).
        reduser_image = cv2.imread(os.path.join(base_path,"reduser.png"), cv2.IMREAD_COLOR)

        # 템플릿 매칭을 수행합니다.
        result = cv2.matchTemplate(
            screenshot, reduser_image, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8

        # 매칭 결과에서 최대값과 그 위치를 찾습니다.
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # 임계값을 기준으로 결과를 확인합니다.
        if max_val >= threshold:
            print("reduser.png 이미지가 발견되었습니다. 채널을 변경합니다.")
            change_channel()  # 채널 변경 함수 호출
        else:
            print("유저감지 되지 않음")

        time.sleep(10)  # 1초마다 이미지 확인


# ---------- 포션 함수 ----------------
def portion():
    # Tesseract-OCR 설치 경로 설정
    pytesseract.pytesseract.tesseract_cmd = r'C:\macro\ocr\tesseract.exe'

    while True:
        # 체력 게이지가 있는 화면 영역 캡처
        hpscreenshot = pyautogui.screenshot(region=(401, 978, 150, 21))
        mpscreenshot = pyautogui.screenshot(region=(611, 979, 150, 20))
        # 이미지에서 텍스트 추출
        hp_text = pytesseract.image_to_string(hpscreenshot, config='--psm 6')
        mp_text = pytesseract.image_to_string(mpscreenshot, config='--psm 6')

        # 정규 표현식 수정: 다양한 오류를 포함
        # 여는 괄호 대신 |, [, { 또는 공백이 인식될 수 있음
        # 닫는 괄호 대신 |, ], } 또는 공백이 인식될 수 있음
        # '/' 문자도 공백으로 처리될 수 있음
        hpmatch = re.search(
            r'[|\[\({\s]?\s*(\d+)\s*[/\s]?\s*(\d+)[|\]\)}\s]?', hp_text)
        mpmatch = re.search(
            r'[|\[\({\s]?\s*(\d+)\s*[/\s]?\s*(\d+)[|\]\)}\s]?', mp_text)
        if hpmatch:
            # 공백으로 분할하여 현재 HP와 최대 HP 추출
            current_hp, max_hp = map(int, hpmatch.groups())
            # 체력의 비율을 백분율로 계산
            hp_percentage = (current_hp / max_hp) * 100
            # 결과 출력
            hpresult = f"{current_hp}/{max_hp} ({hp_percentage:.2f}%)"
            print("HP:", hpresult)
            # HP가 30% 미만이면 END 버튼 누르기
            if hp_percentage < 50:
                if hp_percentage < 20 and str(max_hp)[0] == '4':
                    print("예외")
                else:
                    pyautogui.press('del')
        else:
            print("HP 값을 찾을 수 없음:", hp_text)

        if mpmatch:
            # 공백으로 분할하여 현재 HP와 최대 HP 추출
            current_mp, max_mp = map(int, mpmatch.groups())
            # 체력의 비율을 백분율로 계산
            mp_percentage = (current_mp / max_mp) * 100
            # 결과 출력
            mpresult = f"{current_mp}/{max_mp} ({mp_percentage:.2f}%)"
            print("MP:", mpresult)
            # MP가 30% 미만이면 PageDown 버튼 누르기
            if mp_percentage < 30:
                if mp_percentage < 20 and str(max_mp)[0] == '4':
                    print("예외")

                else:
                    pyautogui.press('end')
        else:
            print("MP 값을 찾을 수 없음:", mp_text)

        time.sleep(1)  # 1초마다 반복

# ----------몬스터 인식 및 공격 함수 ----------------


def main_logic():
    while True:
        while True:
            closest_monster = None  # 가장 가까운 몬스터의 좌표를 저장할 변수
            min_distance = float("inf")  # 가장 가까운 몬스터와의 거리를 저장할 변수
            # 현재 캐릭터 위치 다시 확인
            character_x, character_y, character_direction_left = find_character_coordinates()
            print(f"캐릭터의 현재 좌표: ({character_x}, {character_y}, {character_direction_left})")

            for monster_image_path in monster_images:
                
                # 사용자가 제공한 몬스터 이미지 로드
                monster = cv2.imread(monster_image_path, cv2.IMREAD_COLOR)
                

                # 스크린샷 캡처
                screenshot = pyautogui.screenshot()

                # 스크린샷을 numpy 배열로 변환
                screenshot_np = np.array(screenshot)

                # OpenCV를 사용하여 BGR 형식으로 이미지 로드
                screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

                # 이미지 매칭
                result = cv2.matchTemplate(
                    screenshot_bgr, monster, cv2.TM_CCOEFF_NORMED)

                # 매칭 결과에서 최대 값과 위치 찾기
                loc = np.where(result >= 0.8)

                # 매칭 결과를 반복하여 모든 몬스터의 위치 확인
                for pt in zip(*loc[::-1]):
                    # 같은 층에 있는 몬스터만 필터링
                    if character_y is not None and abs(character_y - pt[1]) < 60:
                        # 현재 몬스터와 캐릭터의 거리 계산
                        distance = abs(character_x - pt[0])

                        # 현재까지 가장 가까운 몬스터보다 더 가까운 몬스터인지 확인
                        if distance < min_distance:
                            min_distance = distance
                            closest_monster = pt

            # 가장 가까운 몬스터가 있을 때 공격
            if closest_monster is not None:
                        print(f"가장 가까운 몬스터를 찾았습니다. 좌표: {closest_monster}")
                        # X축 이동 거리 계산
                        print(closest_monster[0])
                        print(character_x)
                        x_difference = closest_monster[0] - character_x
                        print(x_difference)
                        
                        # 몬스터와의 거리를 50픽셀로 설정
                        distance_to_monster = 30
                        
                        # 이동 방향 및 시간에 따라 처리
                        if x_difference < 0:
                            pyautogui.keyDown("z")
                            pyautogui.keyDown("left")
                            # 음수 값을 방지하기 위해 max 함수를 사용하여 0 미만이 되지 않도록 조정합니다.
                            time.sleep(
                                max(0, (abs(x_difference) - distance_to_monster) / 117 * 0.5))
                            pyautogui.keyUp("left")
                        else:
                            pyautogui.keyDown("z")
                            pyautogui.keyDown("right")
                            # 음수 값을 방지하기 위해 max 함수를 사용하여 0 미만이 되지 않도록 조정합니다.
                            time.sleep(
                                max(0, (abs(x_difference) - distance_to_monster) / 117 * 0.5))
                            pyautogui.keyUp("right")

                        # 컨트롤키를 눌러 공격
                        pyautogui.keyDown("ctrl")
                        time.sleep(4.5)  # 공격 후 잠시 대기
                        pyautogui.keyUp("ctrl")
                        time.sleep(0.5)  # 공격 후 잠시 대기

            # 같은 층에 몬스터가 더이상 없을 경우
            else:
                        print("같은 층에 몬스터가 더이상 없습니다.")
                        rope_image = cv2.imread(
                            os.path.join(base_path, "rope.png"), cv2.IMREAD_COLOR)
                        rope_result = cv2.matchTemplate(
                            screenshot_bgr, rope_image, cv2.TM_CCOEFF_NORMED)
                        rope_loc = np.where(rope_result >= 0.7)

                        if len(rope_loc[0]) > 0:
                            # 모든 로프의 좌표를 저장합니다.
                            rope_coordinates = list(zip(rope_loc[1], rope_loc[0]))
                            print(f"{rope_coordinates}")

                            # 로프와 캐릭터 간의 y축 200 이상인 로프 제외
                            valid_ropes = [rope for rope in rope_coordinates if abs(
                                character_y - rope[1]) < 200]

                            if len(valid_ropes) > 0:
                                # 가장 가까운 로프 선택
                                closest_rope = min(
                                    valid_ropes, key=lambda rope: abs(
                                        character_x - rope[0])
                                )
                                rope_x, rope_y = closest_rope
                                print(f"로프가 발견되었습니다. 좌표: ({rope_x}, {rope_y})")

                                # 로프와 캐릭터 간의 거리 계산
                                distance_to_rope = abs(character_x - rope_x)
                                print("로프와 캐릭터 간의 거리:", distance_to_rope)

                                # 로프와 캐릭터의 x축 거리에 따라 이동 시작
                                if distance_to_rope <= 40:
                                    print("로프와 캐릭터 간의 거리가 40 이내입니다. 위로 이동합니다.")
                                    # 위 방향키와 Alt 키를 누름
                                    if rope_x <= character_x:
                                        pyautogui.keyDown("left")
                                        time.sleep(0.1)
                                        pyautogui.keyUp("left")
                                        pyautogui.keyDown("up")
                                        pyautogui.keyDown("alt")
                                        time.sleep(3.5)  # 0.5초 동안 이동 (조정 가능)
                                        pyautogui.keyUp("up")
                                        pyautogui.keyUp("alt")
                                    if rope_x >= character_x:
                                        pyautogui.press("left")
                                        pyautogui.keyDown("up")
                                        pyautogui.keyDown("alt")
                                        time.sleep(3.5)  # 0.5초 동안 이동 (조정 가능)
                                        pyautogui.keyUp("up")
                                        pyautogui.keyUp("alt")
                                # 로프 쪽으로 이동
                                else:
                                    print(f"로프와 캐릭터 간의 거리: {distance_to_rope}")
                                    if rope_x < character_x:
                                        print(f"캐릭터를 로프쪽으로 이동합니다")
                                        move_character(
                                            character_x, rope_x, character_direction_left=True)
                                    else:
                                        print(f"캐릭터를 로프쪽으로 이동합니다")
                                        move_character(
                                            character_x, rope_x, character_direction_left=False)

                        else:
                            print("로프가 발견되지 않았거나 모든 로프의 y축 거리가 350 이상입니다. 계속 몬스터를 탐색합니다.")
                            pyautogui.keyDown("right")
                            time.sleep(5)  # 0.25초 동안 이동 (조정 가능)
                            pyautogui.keyUp("right")

            print("한 바퀴 돌았습니다. 다시 시작합니다.")

            # 매 30분마다 오른쪽 방향으로 2초 이동 후 우측 방향으로 3초 이동
            current_time = time.localtime()
            if (current_time.tm_min % 10 == 0) and (current_time.tm_sec < 11):
                pyautogui.press('pageup')
            if (current_time.tm_min % 30 == 0) and (current_time.tm_sec < 11):
                pyautogui.press('home')


# 메인로직 시작!

if __name__ == "__main__":
    monster_images = [
        os.path.join(base_path,"leftjoo.png"),
        os.path.join(base_path,"rightjoo.png"),
        os.path.join(base_path,"leftblue.png"),
        os.path.join(base_path,"rightblue.png"),
        os.path.join(base_path,"leftslime.png"),
        os.path.join(base_path,"rightslime.png"),
        os.path.join(base_path,"leftstump.png"),
        os.path.join(base_path,"rightstump.png"),
        os.path.join(base_path,"leftgreen.png"),
        os.path.join(base_path,"rightgreen.png"),
        os.path.join(base_path,"rightred.png"),
        os.path.join(base_path,"leftred.png"),
        os.path.join(base_path,"leftgreenbu.png"),
        os.path.join(base_path,"rightgreenbu.png"),
        os.path.join(base_path,"joo3.png"),
        os.path.join(base_path,"joo1.png"),
        os.path.join(base_path,"joo2.png"),
        os.path.join(base_path,"slime.png"),
        os.path.join(base_path,"slime2.png"),
        os.path.join(base_path,"stump.png"),
        os.path.join(base_path,"greenbu.png"),
        os.path.join(base_path,"greenbu2.png"),
    ]

    # 메인 스레드와 별도의 스레드로 채널 변경 여부를 확인
    # channel_check_thread = threading.Thread(target=check_for_channel_change, daemon=True)
    # channel_check_thread.start()

    # 포션 쓰레드
    # portion_thread = threading.Thread(target=portion, daemon=True)
    # portion_thread.start()

    # 주 로직 실행
    main_logic()