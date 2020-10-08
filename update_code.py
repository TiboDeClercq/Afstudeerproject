import os
import git

def update_code():
    g=git.cmd.Git('')
    g.pull()