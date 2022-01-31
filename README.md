# EelS -- Eel Scaffold
This is a scaffold for Eel to let you use electron as GUI of python easy.

the functions is as same as eel with a little different:

* How to run:

In Eel you must install Chrome/Edge/NodeJS first.and then you can use Eel.It is depends by softwares you had been installed.
If you want to use electron,you need do like this
```
import eel
import browsers
eel.init('web_static_folder')
eel.browsers.set_path('electron','.........../electron')
eel.start('index.html',mode='electron')
```
and then you need to download a electron dist and copy your gui to web_static_folder and do a lot of work.

But in EelS,you just need
```
import eels
eels.start()
```

the electron is download automately,and if your gui file and main thread is not found,it will create a demo in it.
all project tree is formal
```
project-root
|-assets
|   |-views            <------ your gui htmls,css,js
|   |-electron-bin     <------ electron dist,it will be auto download,if you move to a 
|                              new arch computer,it will auto update
|
|-main.py              <------ loader of your project(you can write it by yourself, this 
|                              folder is inited if you use EelS Toolkit to create project)
|-packages             <------ python modules (if you use EelS to manage your package,it 
|                              will install python modules here.
|-sources              <------ yourself modules and other python codes ( you can write it
                               by your self, this folder is created if you use EelS Toolkit
                               to create project)
```
* Exchage message via Electron and python
 
 1.Electron to Python
  the declare which is send message from electron(gui,js) to python is as same as EelS
```
<!-- HTML SIDE -->
<html>
<head>
<script type="text/javascript" src="/eel.js"></script>
<body>
<script>
    function send2Py(msg){
        eel.slot_py(msg);
    }
</script>
</body>
```

```
#Python SIDE
import eels

@eels.expose
def slot_py(msg):
    print('recieved:%s' % msg)
```

  2.Python to Electron
 
  the declare which is send message from python to electron(gui,js) is quit a little different.cause EelS import and package latest version Eel. so you must use the function jscall() to invoke the Eel functions (you can also use const declare eel to call eel module directly).
```
<!-- HTML SIDE -->
<html>
<head>
<script type="text/javascript" src="/eel.js"></script>
<body>
<script>
    eel.expose(recievePy,'js_alertbox');
    function recievePy(msg){
        alert(msg);
    }
</script>
</body>
```

```
#Python SIDE
import eels

#One way to call frontside js
def callAlert_way1(msg):
    eels.eel.js_alertbox(msg)
    
#Another way to call frontside js
def callAlert_way2(msg):
    eels.jscall().js_alertbox(msg)
```
 
* sleep and spwan functions
 
  the declare of those is as same as EelS


* Where is the toolkit:
  like Eel,Eels include a toolkit to let you use it easy.
  if you installed EelS as global.you can run the tookit via:
```
python3 -m eels [arguments]
```
  if you didn't install EelS toolkit and want to use it directly,you can do this:
  1.confirm you installed python and pip3
  2.download tookit file (<this respository>/eels/__main__.py) and rename to eelstool.py
  3.run the tookia via
```
python3 ./eelstool.py [arguments]
```

* How to init a empty project
 
  To init a empty project.you could do like this:
  1.prepare toolkit
  2.prepare a project folder (a empty folder will be better),for example: ~/eelproject
  3.run "--create" command via tookit:
```
python3 ./eelstool.py --create ~/eelproject
```

* How to clean a runable project
 
  If you want to publish your sources code,you need to remove the electron_dist and packages.one way is use .gitignore to ignore folder assets/electron_bin and packages.but there is another way:to use tookit to remove them. when you want to use them again, you should use --create command to call them back:
  1.prepare toolkit
  2.chdir to a project folder ,for example: ~/eelproject
  3.run "--clean" command via tookit:
```
python3 ./eelstool.py --clean ~/eelproject
```

* How to install a modules
 
  You can use pip3 command to install a modules directly.but if you want to use the suggest project struct or you don't want to change anything in os(with out virtualenv and etc.),you can use this command:

  1.chdir to the root of your project , for example ~/eelproject
  
  2.run "--install" command: (use paddlehub module as example)
```
cd ~/eelproject
python3 ./eelstool --install paddlehub
```

* How to deploy project:
 
 As same as eel,Eel tookit was also have delopy function.you can use those command to deploy
```
cd ~/eelproject
python3 ./eelstool --deploy
```
* More function see Eel Documets.you can call them via eels.jscall().xxxx or eels.eel.xxxx as same as eel.xxxx [Documents](http://github.com/ChrisKnott/Eel)
