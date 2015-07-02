#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mfell
#
# Created:     02/04/2015
# Copyright:   (c) Canadian Malartic Corporation 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import kivy
kivy.require('1.9.0')
from kivy.app import App
from kivy.uix.button import Label

class HelloApp(App):
    def build(self):
        return Label(text='Hello World!')

if __name__ == '__main__':
    HelloApp().run()

