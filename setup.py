import os
from subprocess import check_output

def setup_shadow():
    if os.path.exists(os.path.expanduser("~/.shadow/bin")):
        print "Shadow simulator is already installed"
    else:
        print "Installing..."
        os.system("sudo apt-get install -y gcc g++ libglib2.0-0 libglib2.0-dev libigraph0 libigraph0-dev cmake make xz-utils")
        os.system("sudo apt-get install libc-dbg")
        os.system("sudo apt-get install -y python python-matplotlib python-numpy python-scipy python-networkx python-lxml")
        os.system("sudo apt-get install -y git dstat screen htop")

        if "Ubuntu 14.04" in check_output(["bash", "-c", "cat /etc/lsb-release | grep DESCRIPTION"]):
            print "Installing glib manually..."
            os.system("wget http://ftp.gnome.org/pub/gnome/sources/glib/2.42/glib-2.42.1.tar.xz")
            os.system("tar xaf glib-2.42.1.tar.xz")
            os.system("cd glib-2.42.1; ./configure --prefix=%s; make; make install" % os.path.expanduser("~/.shadow"))

        
        if not os.path.exists("./shadow"):
            os.system("git clone https://github.com/shadow/shadow.git")
        os.system("cd shadow; ./setup build --clean --debug --test")
        os.system("cd shadow; ./setup install")
        os.system("cd shadow; ./setup test")
    

def setup_bitcoin():
    if Not os.path.exists("./bitcoin"):
        os.system("git clone https://github.com/bitcoin/bitcoin.git")
    

if __name__ == '__main__':
    # setup_shadow()
    # os.system("echo 'export PATH=$PATH:%s' >> ~/.bashrc && . ~/.bashrc" % os.path.expanduser("~/.shadow/bin"))

    setup_bitcoin()

    
