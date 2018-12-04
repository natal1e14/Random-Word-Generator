#!/usr/bin/env python

__version__ = "2.0"
 

import kivy
import webbrowser


from kivy.utils import platform



def launch_webbrowser(url):
    import webbrowser
    if platform == 'android':
        from jnius import autoclass, cast
        def open_url(url):
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            browserIntent = Intent()
            browserIntent.setAction(Intent.ACTION_VIEW)
            browserIntent.setData(Uri.parse(url))
            currentActivity = cast('android.app.Activity', activity)
            currentActivity.startActivity(browserIntent)

        # Web browser support.
        class AndroidBrowser(object):
            def open(self, url, new=0, autoraise=True):
                open_url(url)
            def open_new(self, url):
                open_url(url)
            def open_new_tab(self, url):
                open_url(url)

        webbrowser.register('android', AndroidBrowser, None, -1)

    webbrowser.open(url)





from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock



import random
#from nltk.corpus import words as dictionary
#from nltk.corpus import wordnet


#wordList = dictionary.words()


wordList = []
dictionary = []

from kivy.core.window import Window
Window.clearcolor = (255,255,255,255)

show = False
started = False
#
#fit = open("wrds.txt","w+")
#for i in range(len(wordList)):
#    deff = wordnet.synsets(str(wordList[i]))
#    if len(deff) == 0:
#        defs = "N/A"
#    elif len(deff) == 1:
#        defs = deff[0].definition()
#    else:
#        defs = []
#        for i in (0,len(deff)-1):
#            #print deff[i].definition()
#            defs.append(deff[i].definition())
#    fit.write(str(wordList[i])+"    "+str(defs)+"\n")
#fit.close()
#



fit = open("wrds.txt","r")#/Users/Natalie/Desktop/PygameApps/randomWord/wrds.txt","r")
lines = fit.readlines()
fit.close()


fit = open("wrds.txt","r")   #/Users/Natalie/Desktop/PygameApps/randomWord/wrds.txt","r")
for i in range(len(lines)):
    line = fit.readline()
    line = line.split("    ")
    deff = line[1]
    wordList.append(line[0])
    if deff == "N/A\n":
        deff = deff.split('\n')
        dictionary.append(deff[0])
    elif deff[0] == "[":
        diff = []
        splt = deff[1:len(deff)-2]
        spelt = splt.split(", u")
        for i in range(len(spelt)):
            current = spelt[i]
            if current[0] == "u":
                diff.append(current[2:-1])
            else:
                diff.append(current[1:-1])
        dictionary.append(diff)
    else:
        line = deff.split("\n")
        dictionary.append(line[0])
       # print line
fit.close()



class RandomMain(Widget):
    
    def btn_click(self):
        global started
        num = random.randint(0,len(wordList)-1)
        started = True
        self.current = wordList[num]
        self.derf = dictionary[num]
        self.lbl1.text = self.current

        
        ##Label(text='Text\na longer line', halign='left')

        self.showDef()
        
        
    def isTrue(self):
        global show
        if show == False:
            show = True
        else:
            show = False
            self.ya.x = 5000
            self.ya.disabled = True
        
        self.showDef()
    
    def search(self):
        query = self.current
        url = "https://www.google.ca/search?q=define+"+str(query)+"&oq=define+"+str(query)+"&aqs=chrome..69i57j69i60l3j0l2.1635j0j4&sourceid=chrome&ie=UTF-8"
        #webbrowser.open(url)
        launch_webbrowser(url)

    def showDef(self):
        global show
        if show == True and started == True:

            self.showBut.text = "Hide Definition"
            #deff = wordnet.synsets(str(self.current))
            if self.derf == "N/A": #len(deff) == 0:
                self.deff.text = '''No definition available in database.
            Open a browser with more definitions?'''
                self.ya.center_x = Window.width//2
                self.ya.disabled = False

            elif ("]" in str(self.derf)) == True:   #len(deff) == 1:
                defFont = ""
               # self.derf = self.derf[1:len(self.derf)-2]
                for i in range(len(self.derf)):
                    #print deff[i].definition()
        
                    defFont = defFont + str(self.derf[i]) + ";\n"
                    #print defFont
                
                self.deff.text = defFont
                self.ya.x = 5000
                self.ya.disabled = True

            else:
                
                self.deff.text = str(self.derf)
                #defFont = ""
                #
                #for i in (0,len(deff)-1):
                #    #print deff[i].definition()
                #    d = deff[i].definition()
                #    print d
                #    defFont = defFont + str(d) + "\n"
                #    #print defFont
               # self.deff.text = defFont
                self.ya.x = 5000
                self.ya.disabled = True


        else:
            self.deff.text = ""
            self.showBut.text = "Show Definition"



class RandomApp(App):
    
    def build(self):
        icon = 'icon.png'
        return RandomMain()
        
        #screen = RandomMain()


if __name__ == "__main__":
    RandomApp().run()