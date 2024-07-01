import subprocess
import time
import win32api
import win32con
import win32gui
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from threading import Thread
from utils_window_utils import *
from auto_clicker import *

class WindowManager(QMainWindow):
    def __init__(self, filePath=""):
        super().__init__()
        self.filePath = filePath
        self.hwnd_list = []

        # 設定窗口標題和大小
        self.setWindowTitle('App Manager')
        self.setGeometry(100, 100, 400, 200)
        self.setStyleSheet("background-color: #f0f0f0;")  # 設定背景色

        # 中央小部件和佈局
        centralWidget = QWidget()
        layout = QVBoxLayout(centralWidget)
        layout.setSpacing(10)  # 設定部件間距

        # 狀態標籤
        self.status_label = QLabel('Ready')
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont('Arial', 12))  # 設定字體和大小
        self.status_label.setStyleSheet("color: #333333; margin-top: 20px;")
        layout.addWidget(self.status_label)

        # 按鈕
        self.file_dialog_btn = QPushButton('Select File')
        self.start_btn = QPushButton('Start Applications')
        self.enumerate_btn = QPushButton('Enumerate Windows')
        self.ww_btn = QPushButton('Execute ww')
        self.rename_btn = QPushButton('ReName')  # 新增的按鈕

        # 設定按鈕樣式
        buttons = [self.file_dialog_btn, self.start_btn, self.enumerate_btn, self.ww_btn, self.rename_btn]
        for btn in buttons:
            btn.setFont(QFont('Arial', 10, QFont.Weight.Bold))
            btn.setStyleSheet(
                "QPushButton { background-color: #007bff; color: white; border-radius: 8px; padding: 5px; }"
                "QPushButton:hover { background-color: #0056b3; }"
                "QPushButton:pressed { background-color: #003785; }"
            )
            layout.addWidget(btn)

        # 連接按鈕的點擊事件
        self.file_dialog_btn.clicked.connect(self.select_file)
        self.start_btn.clicked.connect(self.start_applications)
        self.enumerate_btn.clicked.connect(self.enumerate_windows)
        self.ww_btn.clicked.connect(self.ww)
        self.rename_btn.clicked.connect(self.rename_action)  # 新增的按鈕點擊事件

        self.setCentralWidget(centralWidget)

    def select_file(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Executable File", "", "Executable Files (*.exe);;All Files (*)")
        if filePath:
            self.filePath = filePath
            self.status_label.setText(f"Selected file: {filePath}")

    def enumerate_windows(self):
        self.hwnd_list = []  # 初始化
        win32gui.EnumWindows(self.enum_windows_callback, None)
        self.status_label.setText("Windows Enumerated")

    def enum_windows_callback(self, hwnd, lParam):
        title = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title == "飄流幻境M":
            try:
                adjust_window(hwnd, self.hwnd_list)
            except Exception as e:
                self.status_label.setText("Window Enumeration ERROR")
                
                
    def Rename_windows_callback(self, hwnd, lParam):
        title = win32gui.GetWindowText(hwnd)
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd) and title == "飄流幻境M":
            try:
                Rename_windows(hwnd,"newWLM")
            except Exception as e:
                self.status_label.setText("Window Rename ERROR")
                
                            
    def start_applications(self):
        if not self.filePath:
            self.status_label.setText("File path not specified.")
            return
        for i in range(12):
            time.sleep(0.5)
            try:
                subprocess.Popen(['start', '', self.filePath], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            except Exception as e:
                self.status_label.setText(f"Error starting application: {e}")
                return
        self.status_label.setText("Applications Started")

    def ww(self):
        self.status_label.setText("Starting ww action...")
        account_password_dict = getACCPWD()
        autologin(account_password_dict,)
        self.status_label.setText("ww action completed")

    def rename_action(self):
        self.hwnd_list = []  # 初始化
        win32gui.EnumWindows(self.Rename_windows_callback, None)
        self.status_label.setText("Windows Rename")

    def get_hwnd_list(self):
        return self.hwnd_list

    def get_window_rect(self, hwnd):
        return win32gui.GetWindowRect(hwnd)
