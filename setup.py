import os
import lxml.etree as ET
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
    bitcoin_path = "plugins/bitcoin/src/bitcoin"
    if not os.path.exists(bitcoin_path):
        os.system("mkdir -p %s" % bitcoin_path)
        os.system("git clone https://github.com/bitcoin/bitcoin.git %s" % bitcoin_path)
    
    os.system("git -C %s checkout ." % bitcoin_path)
    os.system("git -C %s checkout v0.16.0" % bitcoin_path)
    os.system("git -C %s clean -d -f -x" % bitcoin_path)
    os.system("cd %s; ./autogen.sh; ./configure --disable-wallet; make -C src obj/build.h; make -C src/secp256k1 src/ecmult_static_context.h"% bitcoin_path)
    

def compile_bitcoin_plugin():
    build_path = "plugins/bitcoin/build"
    if not os.path.exists(build_path):
        os.system("mkdir -p %s" % build_path)

    bitcoin_path = "plugins/bitcoin/src/bitcoin"
    if not os.path.exists("plugins/bitcoin/DisableSanityCheck.patch"):
        print "No appropriate patch exists"
        exit(1)
    else:
        os.system("cd %s; git apply ../../DisableSanityCheck.patch" % bitcoin_path)

    os.system("cd %s; cmake ../; make; make install" % build_path)

def setup_multiple_node_xml(node_num):
    run_path = "plugins/bitcoin"
    baseline_xml = "plugins/bitcoin/example.xml"
    new_xml = "plugins/bitcoin/example_multiple_generated.xml"

    parser = ET.XMLParser(remove_blank_text=True, strip_cdata=False)

    tree = ET.parse(baseline_xml, parser)

    shadow = tree.getroot()

    for node in shadow.findall('node'):
        shadow.remove(node)

    node = ET.SubElement(shadow, "node", id="bcdnode0")
    ET.SubElement(node, "application", plugin="bitcoind", time="13", arguments="-datadir=./node0data -debug -printtoconsole -disablewallet=1 -server=0")

    for i in range(1,node_num):
        node_id = "bcdnode%d" % (i)
        node = ET.SubElement(shadow, "node", id=node_id)
        ET.SubElement(node, "application", plugin="bitcoind", time="13", arguments="-datadir=./node%ddata -debug -printtoconsole -listen -connect=bcdnode0 -disablewallet=1 -server=0"%i)

    tree.write(new_xml, pretty_print=True)
    
def run_shadow_bitcoin_example():
    run_path = "plugins/bitcoin"
    os.system("mkdir %s/node1data; mkdir %s/node2data;" % (run_path, run_path))
    os.system("cd %s; shadow example.xml" % run_path)
    
def run_shadow_bitcoin_multiple_node(node_num):
    run_path = "plugins/bitcoin"
    os.system("rm -rf %s/node*data" % run_path)
    for i in range(node_num):
        os.system("mkdir %s/node%ddata" % (run_path, i))
    os.system("cd %s; shadow %s | tee shadow.result/shadow_%d.result" % (run_path,"example_multiple_generated.xml", node_num))

if __name__ == '__main__':
    # setup_shadow()
    # os.system("echo 'export PATH=$PATH:%s' >> ~/.bashrc && . ~/.bashrc" % os.path.expanduser("~/.shadow/bin"))

    # setup_bitcoin()
    # compile_bitcoin_plugin()


    setup_multiple_node_xml(100)
    # run_shadow_bitcoin_example()
    run_shadow_bitcoin_multiple_node(100)

    
