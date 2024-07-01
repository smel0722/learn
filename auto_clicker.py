import pyautogui
import pyperclip
from pathlib import Path
import numpy as np
import logging
import os
import sys


logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

# 获取当前脚本的目录
current_directory = os.path.dirname(os.path.abspath(__file__))
# 获取txt文件的路径
txt_file_path = os.path.join(current_directory, 'acc.txt')



def get_current_directory():
    # 获取当前脚本的目录或者可执行文件的目录（如果打包成了可执行文件）
    if getattr(sys, 'frozen', False):
        # 打包后的运行环境
        return os.path.dirname(sys.executable)
    else:
        # 源码运行环境
        return os.path.dirname(os.path.abspath(__file__))

def getACCPWD():
    current_directory = get_current_directory()
    txt_file_path = os.path.join(current_directory, 'acc.txt')

    account_password_dict = {}
    # 打开文本文件并读取内容
    with open(txt_file_path, 'r') as file:
        lines = file.readlines()

    # 遍历每一行内容
    for line in lines:
        # 去除每行开头和结尾的空格和换行符
        line = line.strip()

        # 根据冒号分割账号和密码
        if ':' in line:
            account, password = line.split(':')
            # 添加到字典中
            account_password_dict[account] = password

    return account_password_dict

    
def find_and_click_image(template_path, region=None, confidence=0.9, rx=0, ry=0, grayscale=False):
    """
    在指定的屏幕区域内查找指定图像，并点击找到的图像中心位置。
    """
    while True:
        #time.sleep(0.1)
        try:
            print(f"Searching for image: {template_path} in region {region}")
            # 截取指定区域的屏幕截图
            if region:
                screenshot = pyautogui.screenshot(region=(region[0], region[1], region[2], region[3]))
            else:
                screenshot = pyautogui.screenshot()

            # 在截取的屏幕区域内查找图像
            location = pyautogui.locateCenterOnScreen(str(template_path), confidence=confidence, region=region, grayscale=grayscale)
        
            if location:
                # 如果找到图像，则点击图像中心位置
                print(f"Found image at: {location}")
                pyautogui.click(location.x + rx, location.y + ry)
                print(f"Clicked at: ({location.x + rx}, {location.y + ry})")
                return location
            else:
                print(f"Image '{template_path}' not found in specified region")
        except Exception as e:
            logging.error(f"Error in find_image_on_screen: {e}")
            print(template_path, region)
# 自動登入
def autologin(account_password_dict, list_a=[]):
    for i in range(12):
        account_password_list = list(account_password_dict.items())
        account, password = account_password_list[i]
        region = ((i % 4) * 480, (i // 4) * 344, ((i % 4) + 1) * 480, ((i // 4) + 1) * 344) 
        result = find_and_click_image(os.path.join(current_directory, 'img', 'login1.png'), region)
        result = find_and_click_image(os.path.join(current_directory, 'img', 'login2.png'), region, rx=50, ry=0)
        pyperclip.copy(account)
        pyautogui.hotkey("ctrl", "v")
        result = find_and_click_image(os.path.join(current_directory, 'img', 'login3.png'), region, rx=50, ry=0)
        pyperclip.copy(password)
        pyautogui.hotkey("ctrl", "v")       
        result = find_and_click_image(os.path.join(current_directory, 'img', 'login4.png'), region)
        if i in list_a:
            result = find_and_click_image(os.path.join(current_directory, 'img', 'login5.png'), region, rx=+102, ry=-42)
        else:
            result = find_and_click_image(os.path.join(current_directory, 'img', 'login5.png'), region, rx=-106, ry=-42)
        
if __name__ == "__main__":
    pass
