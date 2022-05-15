# 一个在命令行上运行的python密码本保管脚本

使用方法

可以选择创建虚拟环境：
> 使用 conda create -n your_env_name python=X.X（2.7、3.6等)
> 命令创建python版本为X.X、名字为your_env_name的虚拟环境。your_env_name文件可以在Anaconda安装目录envs文件下找到

或者使用virtualenv也可以
python自带的模块venv也行，但是可能换不了版本

```shell
python -m venv myvenv
source myvenv/bin/activate
pip install -r ./requirements
python __main__.py
```

windows上：

```powershell
python -m venv myvenv
myvenv\Scripts\Activate.ps1
pip install -r .\requirements
python __main__.py
```

如果想要打包成exe，可以先

```shell
pip install pyinstaller
```

然后使用pyinstaller打包

```shell
pyinstaller -F __main__.py -i note.ico
```

可以把note.ico换成自己的ico图标文件
