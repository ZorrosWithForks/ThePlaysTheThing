from distutils.core import setup
import py2exe
import os
from os.path import basename

# origIsSystemDLL = py2exe.build_exe.isSystemDLL
# def isSystemDLL(pathname):
   # if basename(pathname) in ('OldNewspaperTypes.ttf'):
      # return 0
   # return origIsSystemDLL(pathname)
# py2exe.build_exe.isSystemDLL = isSystemDLL

myDataFiles = [('', ['OldNewspaperTypes.ttf'])]
#myDataFiles = []
for file in os.listdir('ImageFiles\\'):
   f1 = 'ImageFiles\\' + file
   if os.path.isfile(f1):
      f2 = 'ImageFiles', [f1]
      myDataFiles.append(f2)
for file in os.listdir('Sounds\\'):
   f1 = 'Sounds\\' + file
   if os.path.isfile(f1):
      f2 = 'Sounds', [f1]
      myDataFiles.append(f2)

setup(
   windows = [
      {
         "script": "main_menu.py",
         "icon_resources": [(0, "ImageFiles\\Shortcut.ico")]
      }
   ],
   data_files = myDataFiles
)