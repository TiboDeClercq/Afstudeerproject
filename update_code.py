import os

def update_code():
    os.system('cd')
    #path is relative, depends on vm path (so might need change on your pc)
    os.system('cd /home/kali/git_script/Afstudeerproject')
    os.system('git fetch https://github.com/TiboDeClercq/Afstudeerproject.git && git merge --no-edit master')
    #os.system('git merge -m "merge message" --no-edit https://github.com/TiboDeClercq/Afstudeerproject.git')