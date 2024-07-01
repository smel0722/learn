import win32gui
import win32con
import win32api

def adjust_window(hwnd, hwnd_list):
    idx = len(hwnd_list)
    posX = (idx % 4) * 480
    posY = (idx // 4) * 344
    hwnd_list.append(hwnd)

    style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
    style &= ~win32con.WS_CAPTION
    style &= ~win32con.WS_THICKFRAME
    win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style)
    win32gui.SetWindowPos(hwnd, None, posX, posY, 480, 344, win32con.SWP_NOZORDER | win32con.SWP_FRAMECHANGED)
def Rename_windows(hwnd,new_title):
    win32gui.SetWindowText(hwnd, new_title)
