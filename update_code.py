import os

def update_code():
    os.system('cd')
    #path is relative, depends on vm path (so might need change on your pc)
    os.system('cd /home/kali/git_script/Afstudeerproject')
    os.system('git pull --ff-only https://github.com/TiboDeClercq/Afstudeerproject.git')