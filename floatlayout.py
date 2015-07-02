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
from kivy.uix.floatlayout import FloatLayout

class FloatLayoutApp(App):
    def build(self):
        return FloatLayout()

if __name__ == '__main__':
    FloatLayoutApp().run()

