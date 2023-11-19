import os
import subprocess
import sys

def launch_gui():
    if sys.platform.startswith('win'):
        os.system('start /B cmd /c "cd gui && python mainwindow.py"')
    else:
        subprocess.call(['python3', 'gui/mainwindow.py'])

if __name__ == "__main__":
    launch_gui()
