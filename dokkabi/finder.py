import pyautogui
import cv2
import os
import numpy as np
import common as cm

# Define the color ranges for yellow and red dots
yellow_lower = np.array([20, 100, 100], np.uint8)
yellow_upper = np.array([30, 255, 255], np.uint8)

red_lower = np.array([0, 100, 100], np.uint8)
red_upper = np.array([10, 255, 255], np.uint8)

class Finder:
    def __init__(self, chat=(1924, 932, 3046, 990), map=(1938, 147, 2318, 256), background=(1920, 0, 3830, 920)):
        self.base_path = "C:\\macro\\images"
        self.chat_loc = self.calculate_location(*chat)
        self.map_loc = self.calculate_location(*map)
        self.background_loc = self.calculate_location(*background)

    def calculate_location(self, left_x, left_y, right_x, right_y):
        width = abs(right_x - left_x)
        height = abs(right_y - left_y)
        return (left_x, left_y, width, height)

    def new_map(self, lx, ly, rx, ry):
        self.map_loc = self.calculate_location(lx, ly, rx, ry)

    def new_map_capture(self):
        positions = []
        for i in range(2):
            message = f"{i+1}번째 캡쳐를 시작합니다. 3초 안에 특정 위치로 마우스를 이동시키세요..."
            positions.append(cm.capture_mouse_position(message))

        print("신규 맵 설정 완료")
        print("왼쪽 좌표:", positions[0])
        print("오른쪽 좌표:", positions[1])
        self.map_loc = self.calculate_location(*positions[0], *positions[1])

    def screenshot(self, loc):
        screenshot_pillow = pyautogui.screenshot(region=loc, allScreens=True)
        screen_image = np.array(screenshot_pillow)
        screen_image = cv2.cvtColor(screen_image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(os.path.join(self.base_path, 'screenshot_tmp.png'), screen_image)
        return screen_image
    
    def make_masked_map(self):
        screen_image = self.screenshot(self.map_loc)
        hsv_screenshot = cv2.cvtColor(screen_image, cv2.COLOR_BGR2HSV)

        # Find the yellow dot
        yellow_mask = cv2.inRange(hsv_screenshot, yellow_lower, yellow_upper)

        # Find the red dots
        red_mask = cv2.inRange(hsv_screenshot, red_lower, red_upper)

        # Save the results for debugging
        yellow_result = cv2.bitwise_and(screen_image, screen_image, mask=yellow_mask)
        red_result = cv2.bitwise_and(screen_image, screen_image, mask=red_mask)
        cv2.imwrite(os.path.join(self.base_path, 'yellow_result.png'), yellow_result)
        cv2.imwrite(os.path.join(self.base_path, 'red_result.png'), red_result)

        return yellow_result, red_result

    def remove_overlapping_matches(self, coordinates, w, h):
        filtered_coords = []
        for coord in coordinates:
            if not any([np.linalg.norm(np.array(coord) - np.array(existing)) < min(w, h) // 2 for existing in filtered_coords]):
                filtered_coords.append(coord)
        return filtered_coords


    def find_match(self, template, target_name,threshold=0.8):
        # Load the template and target images
        
        target_path = os.path.join(self.base_path, "{}.png".format(target_name))
        target = cv2.imread(target_path, cv2.IMREAD_COLOR)
        
        # Convert images to grayscale
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        
        # Get dimensions of the template image
        w, h = template_gray.shape[::-1]
        
        # Perform template matching
        result = cv2.matchTemplate(target_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        
        # Initialize coordinates list
        coordinates = []
        
        # Store all coordinates where match is found
        for pt in zip(*locations[::-1]):
            coordinates.append((pt[0], pt[1]))  # Get the center of the match
        
        # Remove overlapping matches
        coordinates = self.remove_overlapping_matches(coordinates, w, h)

        # Return the count of matches
        return len(coordinates), coordinates

    def find_user(self):
        yellow_result, red_result = self.make_masked_map()
        red_user_cnt, _ = self.find_match(red_result, 'reduser')
        _, user = self.find_match(yellow_result, 'user')

        return red_user_cnt, user


    def detector(self, location='chat' ,object_name='dis'):

        if location == 'chat':
            location = self.chat_loc
        elif location == 'background':
            location = self.background_loc

        screen_image = self.screenshot(location)
        screenshot_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)

        dis = cv2.imread(os.path.join(self.base_path, "{}.png".format(object_name)), cv2.IMREAD_COLOR)
        # Convert the images to grayscale
        chat_gray = cv2.cvtColor(dis, cv2.COLOR_BGR2GRAY)
        

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

        return best_val >= 0.55