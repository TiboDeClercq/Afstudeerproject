import os
import git

def update_code():
    os.system('cd')
    #path is relative, depends on vm path (so might need change on your pc)
    g = git.cmd.Git('/home/kali/git_script/Afstudeerproject')
    g.pull()
    # os.system('cd /home/kali/git_script/Afstudeerproject')
    # os.system('git pull --no-edit https://github.com/TiboDeClercq/Afstudeerproject.git')