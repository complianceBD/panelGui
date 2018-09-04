from cx_Freeze import setup, Executable
import os
import sys
#os.environ['TCL_LIBRARY'] = r'C:\Users\XBBNQVM\Anaconda3\tcl\tcl8.6'
#os.environ['TK_LIBRARY'] = r'C:\Users\XBBNQVM\Anaconda3\tcl\tk8.6'


base = None
packages=['pandas', 'numpy', 'tia','bnyCompliance',
           'bloombergBooks', 'os', 'sys', 'win32com', 'file_functions','glob', 'webbrowser']

#includes = ['pandas', 'numpy', 'tia','bnyCompliance',
#           'bloombergBooks', 'os', 'sys', 'win32com', 'file_functions','glob', 'webbrowser']
excludes = ['tkinter','sqlite3', 'tia.rlab.sample', 'tornado','ipython-genutils',
            'decorator', 'traitlets', 'jupyter-core', 'pyzmq', 'jupyter-client',
            'backcall', 'parso', 'jedi', 'simplegeneric', 'pickleshare', 'colorama', 'pygments', 'wcwidth',
            'prompt-toolkit', 'ipython', 'ipykernel', 'pyte']

            
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('compliance-manager.py', base=base, icon="icon_cgf_icon.ico")
]

setup(name='compliance-manager',
      version='0.7',
      description='Sample cx_Freeze wxPython script',
      options = {"build_exe": {#"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             }
               },
      executables=executables
      )