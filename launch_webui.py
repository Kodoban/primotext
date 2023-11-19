import os
import subprocess
import sys

def launch_webui():
    if sys.platform.startswith('win'):
        os.system('start /B cmd /c "cd webui && python webui.py"')
    else:
        subprocess.call(['python3', 'webui/webui.py'])

if __name__ == "__main__":
    launch_webui()
