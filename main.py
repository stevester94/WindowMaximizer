# The target window name to maximize, will minimize all other windows

target = u'C:\\Windows\\system32\\cmd.exe'

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
    setCursorPosition(0,0)
    print ""
    
    print "Minimizing all except target: " + target
    minimizeAllExceptTarget(target)



def mainLoop():
    while True:
        if checkIfTargetExists(target):
            # Jitter mouse
            setCursorPosition(0,0)
            setCursorPosition(1,1)

            # Minimize all but target
            minimizeAllExceptTarget(target)
        time.sleep(1)

if __name__ == "__main__":
    print "test: run the unit test"
    print "list: print all windows"
    print "main: run main program"

    option = raw_input("Option: ").rstrip()

    if option == "test": unitTest()
    if option == "list": 
        for w in getAllWindows(): print w
    if option == "main": mainLoop()