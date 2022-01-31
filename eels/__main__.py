import os
import sys
import platform
from argparse import ArgumentParser

default_dir=os.path.abspath('.')

class _init_electrondist:
    def get_electron_url(self):
        electron_Version="9.4.4" # Use 9.4.4 because it is easy to use 'remote' module to control gui.
        electron_Source="https://npm.taobao.org/mirrors/electron"
        sys_arch=platform.machine()
        sys_platform=sys.platform
        electron_Tail=''
        if sys_platform in ['win32','win64']:
            #it is windows
            if sys_arch == "x86_64":
                electron_Tail="win32-x64"
            elif sys_arch == "i386":
                electron_Tail="win32-i386"
            elif sys_arch == "aarch64":
                electron_Tail="win32-arm64"
        elif sys_platform in ['linux']:
            #it is Linux
            if sys_arch == "x86_64":
                electron_Tail="linux-x64"
            elif sys_arch == "i386":
                electron_Tail="linux-ia32"
            elif sys_arch in ['aarch64', 'arm64']:
                electron_Tail="linux-arm64"
            elif sys_arch in ['arm','armv7l','armhf']:
                electron_Tail="linux-armv7l"
        elif sys_platform in ['darwin']:
            #it is Linux
            if sys_arch == "x86_64":
                electron_Tail="darwin-x64"
            elif sys_arch in ['aarch64', 'arm64']:
                electron_Tail="darwin-arm64"
        return "%s/%s/electron-v%s-%s.zip" % (electron_Source,electron_Version,electron_Version,electron_Tail)

    def download_file(self,url):
        print("Downloading Electron Dist: %s" % url)
        import tempfile
        import urllib.request
        dirpath=tempfile.mkdtemp()
        filepath=os.path.join(dirpath,"electron_dist.zip")
        urllib.request.urlretrieve(url,filepath)
        return filepath

    electron_path=""

    def install(self,base_path):
        electron_dir=os.path.join(base_path,'assets','electron_bin')
        electron_path=''
        if sys.platform in ['win32', 'win64']:
            electron_path = os.path.join(electron_dir,r'electron.exe')
        elif sys.platform in ['linux', 'freebsd']:
            electron_path = os.path.join(electron_dir,r'electron')
        elif sys.platform in ['darwin', 'macos']:
            electron_path = os.path.join(electron_dir,r'Electron.app','Contents','MacOS','Electron')
        if os.path.exists(os.path.abspath(electron_path)) and os.path.isfile(os.path.abspath(electron_path)):
            self.electron_path = electron_path
            return
        zippath=self.download_file(self.get_electron_url())
        import zipfile
        import subprocess
        if zipfile.is_zipfile(zippath):
            with zipfile.ZipFile(zippath, 'r') as zipf:
                if not (os.path.exists(os.path.abspath(electron_dir)) and os.path.isdir(os.path.abspath(electron_dir))):
                    os.makedirs(electron_dir)
                zipf.extractall(electron_dir)
                if sys.platform in ['linux','freebsd']:
                    subprocess.run(["chmod","a+x",os.path.join(electron_dir,"electron")])
                    subprocess.run(["chmod","a+x",os.path.join(electron_dir,"chrome-sandbox")])
                elif sys.platform in ['darwin','macos']:
                    subprocess.run(["chmod","a+x",os.path.join(electron_dir,"Electron.app","Contents","MacOS","Electron")])
        if os.path.exists(os.path.abspath(electron_path)) and os.path.isfile(os.path.abspath(electron_path)):
            self.electron_path = electron_path
            return
    
    def getElectronPath(self):
        return self.electron_path

    def __init__(self,base_path):
        electron_dir=os.path.join(base_path,'assets','electron_bin')
        electron_path=''
        if sys.platform in ['win32', 'win64']:
            electron_path = os.path.join(electron_dir,r'electron.exe')
        elif sys.platform in ['linux', 'freebsd']:
            electron_path = os.path.join(electron_dir,r'electron')
        elif sys.platform in ['darwin', 'macos']:
            electron_path = os.path.join(electron_dir,r'Electron.app','Contents','MacOS','Electron')
        self.electron_path=electron_path

#base_path=os.path.split(sys.argv[0])[0]
#view_path=os.path.join(base_path,'assets','views')
#_electron_dist=_init_electrondist(base_path)
#electron_path=_electron_dist.electron_path

def createproject(basefolder):
    defaultpage="""<html>
    <head>
    <title>Default Eel Python GUI</title>
    <script type="text/javascript" src="/eel.js"></script>
    </head>
    <body>
    TODO: Default GUI.The below is the example of callbacks:<br/><br/>
    <hr/>
    The link above is calling a python function and then callback to browser:<br/>
    [Page.Link] --> [Page.Func_slot_send_msg] --> [Python.Func_slot_recieve_msg] ---> [Page.Func_slot_recieve_alertbox] --> [Sys.alert]
    <br/>
    <script>
        eel.expose(slot_recieve_alertbox,"js_alertbox");
        function slot_recieve_alertbox(msg)
        {
            alert(msg);
        }
        function slot_send_msg(msg)
        {
            eel.slot_recieve_msg(msg);
        }
    </script>
    <a href="#" onclick="slot_send_msg('xx');return false;">Click to send a signal to backends</a>
    </body>
    </html>
    """
    defaultmain="""import eels
@eels.expose
def slot_recieve_msg(msg):
    print('Recieve message from frontend:%s' % msg)
    print('Sendmessage to frontend:%s' % msg)
    eels.eel.js_alertbox(msg)

def main(base_dir):
    print("Begin Main Thread")
    eel.start()
    """
    bootloader="""import os
import sys

base_dir=os.path.abspath(os.path.split(os.path.realpath(__file__))[0])
module_path=os.path.abspath(os.path.join(os.path.split(os.path.realpath(__file__))[0],"packages"))
sys.path.append(module_path)

import sources.main as main
main.main(base_dir)
    """
    print("Creating root folder...")
    folder=os.path.abspath(basefolder)
    if not os.path.exists(folder):
        os.makedirs(folder)
    if os.path.exists(folder) and os.path.isdir(folder):
        print("Creating assets folder...")
        tmp_d=os.path.join(folder,"assets")
        if not os.path.exists(tmp_d):
            os.makedirs(tmp_d)
        print("Creating assets/views folder...")
        tmp_d=os.path.join(folder,"assets","views")
        if not os.path.exists(tmp_d):
            os.makedirs(tmp_d)
        print("Creating index.html...")
        tmp_f=os.path.join(folder,"assets","views","index.html")
        if not os.path.exists(tmp_f):
            with open(tmp_f, "w", encoding="utf-8") as f:
                f.write(defaultpage)
        print("Creating assets/electron_bin folder...")
        tmp_d=os.path.join(folder,"assets","electron_bin")
        if not os.path.exists(tmp_d):
            os.makedirs(tmp_d)
        print("Creating electron dist...")
        ied=_init_electrondist(folder)
        tmp_f=ied.getElectronPath()
        if not os.path.exists(tmp_f):
            ied.install(folder)
        print("Creating sources...")
        tmp_d=os.path.join(folder,"sources")
        if not os.path.exists(tmp_d):
            os.makedirs(tmp_d)
        print("Creating sources/main.py...")
        tmp_f=os.path.join(folder,"sources","main.py")
        if not os.path.exists(tmp_f):
            with open(tmp_f, "w", encoding="utf-8") as f:
                f.write(defaultmain)
        print("Creating packages...")
        tmp_d=os.path.join(folder,"packages")
        if not os.path.exists(tmp_d):
            os.makedirs(tmp_d)
        print("Creating start.py...")
        tmp_f=os.path.join(folder,"start.py")
        if not os.path.exists(tmp_f):
            with open(tmp_f, "w", encoding="utf-8") as f:
                f.write(bootloader)
    return


def main():
    parser = ArgumentParser(description="""
    The tookit of EelS.
""")
    gaction = parser.add_mutually_exclusive_group()
    gaction.add_argument('-c','--create',action="store_true",help="To create a empty project or try to fix a broken project")
    gaction.add_argument('-C','--clean',action="store_true",help="To clean the project,remove all locally python modules and electron dist")
    gaction.add_argument('-i','--install',action="store_true",help="To Install a modules into this project")
    gaction.add_argument('-d','--deploy',action="store_true",help="To deploy program to relases mode")
    parser.add_argument('commands',type=str,help="the commands you want to do, set 'help' to see detial")
    args, unknown_args = parser.parse_known_args()
    if args.create:
        #ToDo Create
        if  args.commands=='help' :
            print('usuage: %s -c project_dir' % os.path.split(__file__)[1])
            print('\npositional arguments:')
            print('\t project_dir\tThe folder of your project which you want to create or fix.\n')
            return
        createproject(args.commands)
        return

    elif args.clean:
        #ToDo Clean
        if  args.commands=='help' :
            print('usuage: %s -C project_dir' % os.path.split(__file__)[1])
            print('\npositional arguments:')
            print('\t project_dir\tThe folder of your project which you want to Clean.after this the bin of project and cpu arch is cutted down. you should use --create to relink them.\n')
            return

    elif args.install:
        #ToDo Import
        if  args.commands=='help' :
            print('usuage: %s -i project_dir modulename' % os.path.split(__file__)[1])
            print('\npositional arguments:')
            print('\t project_dir\tThe folder of your project which you want to create or fix.')
            print('\t modulename\tThe module name you want to install.\n')

            return

    elif args.deploy:
        #ToDo Deploy
        if  args.commands=='help' :
            print('usuage: %s -d project_dir [attend_arguments]' % os.path.split(__file__)[1])
            print('\npositional arguments:')
            print('\t project_dir\tThe folder of your project which you want to create or fix.')
            print('\t attend_arguments\tThe arguments you want to pass to PyInstaller.\n')
            return


if __name__ == '__main__':
    main()
