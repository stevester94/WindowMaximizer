# The target window name to maximize, will minimize all other windows

target = u'VSee Call'

import ctypes
import sys
import time


def getAllWindows():
    windows = []

    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    def foreach_window(hwnd, lParam):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            windows.append((buff.value, hwnd))
        return True
    EnumWindows(EnumWindowsProc(foreach_window), 0)

    return windows

def minimizeAllExceptTarget(target):
    windows = getAllWindows()

    for w in windows:
        if w[0] == target:
            ctypes.windll.user32.ShowWindow(w[1], 3) # Maximize
        elif w[0] == "" or w[0] == "Start":
            continue
        else:
            ctypes.windll.user32.ShowWindow(w[1], 6) # Minimize

def setCursorPosition(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

def wakeScreen():
    print "Waking screen..."
    import win32gui
    import win32con
    SC_MONITORPOWER = 0xF170
    win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND, SC_MONITORPOWER, -1)

def jitterMouse():
    print "jitterMouse called"

    setCursorPosition(0,0)
    time.sleep(0.10)
    setCursorPosition(10,10)
    time.sleep(0.10)
    setCursorPosition(0,0)
    time.sleep(0.10)
    setCursorPosition(10,10)
    time.sleep(0.10)
    setCursorPosition(0,0)
    time.sleep(0.10)
    setCursorPosition(10,10)
    time.sleep(0.10)

def checkIfTargetExists(target):
    windows = getAllWindows()

    for w in windows:
        if w[0] == target: return True

    return False


def unitTest():
    print "Printing all targets:"
    for w in getAllWindows(): print w
    print ""

    print "Target exists? " + str(checkIfTargetExists(target))
    print""

    print "Moving mouse to (0,0)"

    jitterMouse()

    print ""
    
    print "Minimizing all except target: " + target
    minimizeAllExceptTarget(target)



def mainLoop():
    while True:
        if checkIfTargetExists(target):
            print "Target exists, waking"
            # Keep screen awake (Repeated calls are necessary)
            wakeScreen()

            # Minimize all but target
            minimizeAllExceptTarget(target)
        time.sleep(0.5)

def sleepTest():
    print "Executing sleep test"
    time.sleep(70)

    while True:
        wakeScreen()
if __name__ == "__main__":
    print "test: run the unit test"
    print "list: print all windows"
    print "main: run main program"

    option = raw_input("Option: ").rstrip()

    if option == "test": unitTest()
    if option == "list": 
        for w in getAllWindows(): print w
    if option == "sleep":
        sleepTest()
    if option == "main": mainLoop()
