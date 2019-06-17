from pathlib import Path
import os

def get_workingdir():
    if os.name == 'posix':
        home = str(Path.home())
        wdir = home + "/.archon"

        if not os.path.exists(wdir):
            os.makedirs(wdir)

        return wdir

    elif os.name == 'nt':
        home = str(Path.home())
        wdir = home + os.sep + ".archon"

        if not os.path.exists(wdir):
            os.makedirs(wdir)

        return wdir
    
    else:
        print ("unknown os ", os.name)
    
wdir = get_workingdir()
print (wdir)
key_file = wdir + os.sep + "apikeys.toml"
print (key_file)

print (os.path.exists(key_file))
