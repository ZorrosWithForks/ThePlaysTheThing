import os
import shutil

dir_src = 'pygame-1.9.2a0-cp34-none-win_amd64.whl'
dir_dst = 'C:\\Python34\Scripts\pygame-1.9.2a0-cp34-none-win_amd64.whl'

shutil.copy(dir_src, dir_dst)

os.chdir('C:\\Python34\Scripts')
os.system('pip install pygame-1.9.2a0-cp34-none-win_amd64.whl')