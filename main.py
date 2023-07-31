from cefpython3 import cefpython as cef
import os
import platform
import subprocess
import sys

try:
    from PIL import Image
except ImportError:
    print("PIP is not installed"
          "Install using: pip install PIP")
    sys.exit(1)

def main(url, width, height):
    global VIEWPORT_SIZE, URL, SCREENSHOT_PATH
    URL = url
    VIEWPORT_SIZE = (width, height)
    SCREENSHOT_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                   "SCREENSHOT.png")
    check_versions()
    sys.excepthook = cef.ExceptHook()

    if os.path.exists(SCREENSHOT_PATH):
        print("Remove Old Screenshot")
        os.remove(SCREENSHOT_PATH)

    command_line_arguments()

    settings = {
        "windowless_rendering_enabled": True,
    }

    switches = {
        "disable-gpu": "",
        "disable-gpu-compositing": "",
        "enable-begin-frame-scheduling": "",
        "disable-surfaces": ""
    }

    browser_settings = {
        "windowless_frame_rate": 30,
    }

    cef.Initialize(settings=settings, switches=switches)
    create_browser(browser_settings)
    cef.MessageLoop()
    cef.Shutdown()
    print("Opening your screenshow with the default application")
    open_with_default_application(SCREENSHOT_PATH)


def check_versions():
    ver = cef.GetVersion()
    print("CEF Python {ver}".format(ver=ver["version"]))
    print("Chromium {ver}".format(ver=ver["chrome_version"]))
    print("CEF {ver}".format(ver=ver["cef_version"]))
    print("Python {ver} {arch}".format(ver=platform.python_version(), arch=platform.architecture()[0]))
    assert cef.__version__ >= "57.0", "CEF Python v57.0+ required to run this app"


def command_line_arguments():
    if len(sys.argv) == 4:
        url = sys.argv[1]
        width = int(sys.argv[2])
        height = int(sys.argv[3])
        if url.startswith("http://") or url.startswith("https://"):
            global URL
            URL = url
        else:
            print("Error: Invalid URL Entered")
        if width > 0 and height > 0:
            global VIEWPORT_SIZE
            VIEWPORT_SIZE = (width, height)
        else:
            print("Error: Invalid width and height")
            sys.exit(1)
    elif len(sys.argv) > 1:
        print("Error: Expected Arguments Not Received"
              "Expected Arguments are URL, width and height")


def create_browser(settings):
    global VIEWPORT_SIZE, URL
    parent_window_handle = 0
    window_info = cef.WindowInfo()
    window_info.SetAsOffScreen(parent_window_handle)
    print("Viewport size: {size}".format(size=str(VIEWPORT_SIZE)))
    print("Loading URL: {url}".format(url=URL))
    browser = cef.CreatreBrowserSync(window_info=window_info, settings=settings, url=URL)
    browser.SetClientHandler(LoadHandler())
    browser.SetClientHandler(RenderHandler())
    browser.SendFocusEvent(True)
    browser.WasResized()



import tkinter as tk

root = tk.Tk()
root.geometry("400x200")


class Widgets:
    def __init__(self, lab_text, set_variable):
        self.lab = tk.Label(root, text=lab_text)
        self.lab.pack()
        self.v = tk.StringVar()
        self.entry = tk.Entry(root, textvariable=self.v)
        self.entry.pack()
        self.v.set(set_variable)


object_1 = Widgets("Enter Website Name: ", "https://www.google.com")
object_2 = Widgets("Enter Width: ", "1024")
object_3 = Widgets("Enter Height: ", "2048")
root.bind("<Return>", lambda x: main(object_1.v.get()), int(object_2.v.get()), int(object_3.v.get()))
label_4 = tk.Label(root, text="")
label_4.pack()
label_5 = tk.Label(root, text="Press the Enter key to create a screenshot")
label_5.pack()

root.mainloop()