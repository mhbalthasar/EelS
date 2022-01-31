import eel
import eel.browsers
import os
import sys
import platform
import socket
from urllib.parse import urljoin

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

    def __init__(self,base_path):
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

base_path=os.path.split(sys.argv[0])[0]
view_path=os.path.join(base_path,'assets','views')
_electron_dist=_init_electrondist(base_path)
electron_path=_electron_dist.electron_path


def init(allowed_extensions=['.js', '.html', '.txt', '.htm',
    '.xhtml', '.vue'], js_result_timeout=10000):
    eel.init(os.path.abspath(view_path), allowed_extensions, js_result_timeout)
    #eel.browsers.set_path('electron', electron_path);
    eel._start_args['mode']='custom'
    eel._start_args['cmdline_args']=[os.path.abspath(electron_path),"http://www.github.com"]
    eel._start_args['inited']=1
    eel._start_args['port']=0

def start(start_urls='.', **kwargs):
    if not 'inited' in eel._start_args:
        init()
    eel._start_args.update(kwargs)
    if 'options' in kwargs:
        if eel._start_args['suppress_error']:
            eel._start_args.update(kwargs['options'])
        else:
            raise RuntimeError(api_error_message)

    if eel._start_args['port'] == 0:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        eel._start_args['port'] = sock.getsockname()[1]
        sock.close()
    eel._start_args['cmdline_args'][1]=urljoin(eel.browsers._build_urls('.',eel._start_args)[0],'index.html')
    eel.start()

def sleep(seconds):
    eel.sleep(seconds)

def spawn(function, *args, **kwargs):
    return eel.spawn(function, *args, **kwargs)

def show(*start_urls):
    eel.show(*start_urls)

def jscall():
    return eel

def expose(name_or_function=None):
    return eel.expose(name_or_function)