import ctypes
import time

from ctypes import wintypes
from threading import Thread
from threading import Event

user32 = ctypes.WinDLL('user32', use_last_error=True)

INPUT_MOUSE    = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2

KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP       = 0x0002
KEYEVENTF_UNICODE     = 0x0004
KEYEVENTF_SCANCODE    = 0x0008

MAPVK_VK_TO_VSC = 0

# hexcodes
# https://docs.microsoft.com/en-us/windows/desktop/inputdev/virtual-key-codes
# msdn.microsoft.com/en-us/library/dd375731
VK_TAB  = 0x09
VK_MENU = 0x12
VK_ESCAPE = 0x18
VK_LSHIFT = 0xa0
VK_RETURN = 0x0d

VK_OEM2 = 0xbf

VK_N = 0x4e
VK_X = 0x58

# C struct definitions

wintypes.ULONG_PTR = wintypes.WPARAM

class MOUSEINPUT(ctypes.Structure):
    _fields_ = (("dx",          wintypes.LONG),
                ("dy",          wintypes.LONG),
                ("mouseData",   wintypes.DWORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

class KEYBDINPUT(ctypes.Structure):
    _fields_ = (("wVk",         wintypes.WORD),
                ("wScan",       wintypes.WORD),
                ("dwFlags",     wintypes.DWORD),
                ("time",        wintypes.DWORD),
                ("dwExtraInfo", wintypes.ULONG_PTR))

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        # some programs use the scan code even if KEYEVENTF_SCANCODE
        # isn't set in dwFflags, so attempt to map the correct code.
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk,
                                                 MAPVK_VK_TO_VSC, 0)

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (("uMsg",    wintypes.DWORD),
                ("wParamL", wintypes.WORD),
                ("wParamH", wintypes.WORD))

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT),
                    ("mi", MOUSEINPUT),
                    ("hi", HARDWAREINPUT))
    _anonymous_ = ("_input",)
    _fields_ = (("type",   wintypes.DWORD),
                ("_input", _INPUT))

LPINPUT = ctypes.POINTER(INPUT)

def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (wintypes.UINT, # nInputs
                             LPINPUT,       # pInputs
                             ctypes.c_int)  # cbSize

# Functions

def PressKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    x = INPUT(type=INPUT_KEYBOARD,
              ki=KEYBDINPUT(wVk=hexKeyCode,
                            dwFlags=KEYEVENTF_KEYUP))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))

def EnterKey(keycode):
    PressKey(keycode)
    ReleaseKey(keycode)

def AltTab():
    """Press Alt+Tab and hold Alt key for 2 seconds
    in order to see the overlay.
    """
    PressKey(VK_MENU)   # Alt
    PressKey(VK_TAB)    # Tab
    ReleaseKey(VK_TAB)  # Tab~
    time.sleep(2)
    ReleaseKey(VK_MENU) # Alt~

def InputKey_X():
    EnterKey(VK_X)
    EnterKey(VK_RETURN)

def InputKey_N():
    EnterKey(VK_N)
    EnterKey(VK_RETURN)

def InputKey_Question():
    PressKey(VK_LSHIFT)
    PressKey(VK_OEM2)
    ReleaseKey(VK_OEM2)
    ReleaseKey(VK_LSHIFT)
    EnterKey(VK_RETURN)

def MenuDance():
    EnterKey(VK_MENU)
    time.sleep(3)
    EnterKey(VK_ESCAPE)

class ThreadKeystrokes(Thread):
    '''Thread to imitate keyboard-strokes to main thread
    after specified time-delay in sec.
    It will call the func() which correspond to keys pattern.
    '''
    def __init__(self, delay, func, stop_event, exit_event):
        Thread.__init__(self)
        self.delay = delay
        self.func = func
        self.event = stop_event
        self.exit = exit_event
        
    def run(self):
        try:
            counter = 0
            while not self.event.is_set():
                time.sleep(1)
                counter += 1
                if counter >= self.delay: 
                    counter = 0
                    self.func()
                # elif counter % 9 == 0:
                #     print('.', end='', flush=True)
        finally:
            self.exit.set()
            

def mygenerator():
    c = 0
    while True:
        c = 1 if c == 1440 else c + 1
        yield c


def func(x):
    if (x == 'n') or (x == 'N') or (x == 'Y'): x = 'y'
    return x


if __name__ == "__main__":
    stop_event = Event()
    exit_event = Event()

    ks = ThreadKeystrokes(60, InputKey_Question, stop_event, exit_event)
    ks.start()
    count = mygenerator()

    try:
        # count = 0
        # while True:
        #     count += 1            
        #     s = f'{count:04} press Ctrl+C to exit <y/n>: '
        #     val = input(s)

        # replacing while-loop with function-prog style
        funcFP = lambda: func(input(f'{next(count):04} to exit Ctrl+C/y/n: ')) == 'y' \
            or funcFP()
        funcFP()
    except KeyboardInterrupt:
        print("\n[=] user interrupt caught, exiting...")
    finally:
        stop_event.set()
        print("waiting for threads to exit")
        exit_event.wait()
        ks.join()
    
# --END--
