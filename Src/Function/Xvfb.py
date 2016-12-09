# coding=utf-8
# SongErwei
# 需要pip install pyvirtualdisplay

from pyvirtualdisplay import Display
import platform

class Xvfb:
    def __init__(self):
        if platform.system() == "Linux":
            self.is_linux = True
        else:
            self.is_linux = False 

    def load(self):
        if self.is_linux: 
            self.display = Display(visible=0, size=(800, 600))
            self.display.start() # now Firefox will run in a virtual display. you will not see the driver.

    def unload(self):
        if self.is_linux: 
            self.display.stop() 

