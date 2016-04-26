import os
import shutil
from tkinter.filedialog import asksaveasfilename, askopenfilename

fname = askopenfilename(filetypes=(("Template files", "*.tplate"), ("HTML files", "*.html;*.htm"), ("All files", "*.*") ))
print(fname)
shutil.copyfile(fname, os.path.split(os.path.realpath(__file__))[0]+'/filename.txt')