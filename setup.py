import os

def setup_shadow():
    if os.path.exists(os.path.expanduser("~/.shadow/bin")):
        print "Shadow simulator is already installed"
    else:
        print "Installing..."
    

if __name__ == '__main__':
    setup_shadow()

    

    
