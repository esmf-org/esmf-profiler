import sys
import os
from datetime import datetime

def push_profile(repo_dir, profile_name):

    web_root = "https://rsdunlapiv.github.io/esmf-profile-example"
        
    # temp directory
    #tmp_dir = "./repotmp"
    #if not os.path.isdir(tmp_dir):
    #    os.makedirs(tmp_dir)
    #    print("Created tmp directory: {}".format(tmp_dir))
        
    #git_cmd = "cd {}; git checkout {}; git add {}/{};git commit -a -m\'update\';git push origin {}".format(
    #    self.artifacts_root,self.machine_name,dirbranch,self.machine_name,build_basename,self.build_hash,self.machine_name,self.machine_name)

    if not os.path.isdir(repo_dir):
        print("Not a valid repository directory: {}".format(repo_dir))
        return

    profile_dir = "out/{}".format(profile_name)
    if not os.path.isdir(profile_dir):
        print("Not a valid profile directory: {}".format(profile_dir))
        return
    
    cmd = "cd {}; git pull".format(repo_dir)
    print("CMD: {}".format(cmd))
    os.system(cmd)

    cmd = "cp -R {} {}".format(profile_dir, repo_dir)
    print("CMD: {}".format(cmd))
    os.system(cmd)

    cmd = "cd {}; git add {}/*; git commit -a -m \'update\'; git push origin".format(repo_dir, profile_name)
    print("CMD: {}".format(cmd))
    os.system(cmd)

    print("Profile URL: {}/{}/".format(web_root, profile_name))
    print("  NOTE:  It may take up to several minutes for the profile to be live.")
    
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 push_profile.py <repo_dir> <profile_name>\n")
    else:
        push_profile(sys.argv[1], sys.argv[2])
