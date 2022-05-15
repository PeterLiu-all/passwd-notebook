import os
import re
import sys
import zipfile
from time import sleep

import pyperclip
from tqdm import tqdm

import passwd
from log import SetLogConfig
from passwd import Passwd


class Account():
    def __init__(self, tittle: str, name: str = '', passwd: str = '') -> None:
        self.tittle = tittle
        self.name = name
        self.passwd = passwd
        self.newPass = passwd
        self.filename = 'passwd'
        self.zippass = b'123456'
    # 帮助
    def help(self):
        log.info('显示帮助...')
        print('''
            本插件由Peter Liu独立制作
            使用方法如下：
            1】可以使用命令行参数输入密码本文件的名字，可以是相对路径也可以是绝对路径
                如果没有用命令行参数输入，程序会开始自动读取标准输入流
            2】请根据提示输入账户名等信息并选择相关的模式（增加、修改、读取、删除、搜索、随机生成）
            祝用的开心！
                                                                --Peter Liu
            ''')
        sys.exit(0)

    def show(self, conte: dict):
        for key, value in conte.items():
            print(key + value, end='')

    def displayAccount(self, keyword: str, display: bool = True) -> dict:
        pattern = re.compile('^(.*)' + keyword + '(.*)$')
        print('正则表达式：' + pattern.pattern)
        data = {}
        with open(self.filename, 'r', encoding='UTF-8') as f:
            cnt = 1
            print('Search-Result'.center(20, '='))
            with tqdm(f.readlines(), '正在搜索', \
                      colour='green') as t:
                for line in t:
                    eles = line.split(':')
                    pre = eles[0]
                    content = ''.join(eles[1:])
                    if pre != 'tittle' or content == '': continue
                    mo = pattern.search(content)
                    if mo is not None:
                        # tqdm.write(str(cnt)+'】'+content, end='')
                        data[str(cnt) + '】'] = content
                        cnt += 1
                    # sleep(0.01)
            if display: self.show(data)
            print('=' * 20)
            return data

    def deleteAccount(self):
        data = self.displayAccount(self.tittle, True)
        if data is not None:
            num = input('请问上述账号是否有需要删除的？若有，请输入序号！')
            if data.get(num + '】') is not None:
                log.info('将删除账号' + data[num + '】'] + '!')
                self.tittle = data[num + '】']
        else:
            log.info('找不到账户！')
            return
        with open(self.filename, 'r', encoding='UTF-8') as f1, \
                open(self.filename + '.swp', 'w', encoding='UTF-8') as f2:
            lines = f1.readlines()
            pattern = re.compile('^tittle:(.*)$')
            i = 0
            while i < len(lines):
                mo = pattern.search(lines[i])
                if mo is not None and mo.group(1) == self.tittle:
                    i += 1
                    while lines[i].split(':')[0] != 'tittle':
                        i += 1
                    continue
                f2.write(lines[i])
                i += 1
        try:
            os.remove(self.filename)
            os.rename(self.filename + '.swp', self.filename)
        except FileNotFoundError as err:
            log.info('出现错误：文件未找到' + str(err))

    def check(self) -> bool:
        with open(self.filename, 'r', encoding='UTF-8') as f:
            pattern = re.compile('^tittle:(.*)$')
            with tqdm(f.readlines(), '正在检查是否有重名', colour='green') as lines:
                for line in lines:
                    mo = pattern.search(line)
                    if mo is not None and mo.group(1) == self.tittle:
                        return True
        return False

    # 将信息添加至文件末尾
    def popInAccount(self):
        # 查重
        while self.check():
            log.info('已经存在相同标题的账户！')
            jud1 = int(input('请问是否替换原账户？(1-是 2-否)'))
            if jud1 == 1:
                self.updateAccount()
                return
            else:
                if input('请问是否修改当前账户标题？(是|否)') == '是':
                    self.tittle = input('请输入新的账户名称：')
                else:
                    log.info('已收到！任务中止！')
                    return
        pyperclip.copy(self.passwd)
        print('密码已复制！')
        # 初始化密码对象
        p = Passwd(self.passwd)
        # 获取加密后的密码
        p.passwd = p.encode()
        with open(self.filename, 'a', encoding='UTF-8') as file:
            # 填入文件
            file.writelines(['tittle:' + self.tittle + '\n', 'account name:' + self.name + '\n', \
                             'password:' + p.passwd + '\n', 'key:' + str(p.key) + '\n', '------------------\n'])

    # 更新文件内容
    def updateAccount(self):
        # 初始化密码对象
        p = Passwd(self.passwd)
        p.passwd = p.encode()
        with open(self.filename, 'r', encoding='UTF-8') as file1, \
                open(self.filename + '.bak', 'w', encoding='UTF-8') as file2:
            lines = file1.readlines()
            i = 0
            jud = True
            # 默认每次读取一行
            while i < len(lines):
                file2.write(lines[i])
                # 如果之前没有读到并且tittle相同则手动处理
                if jud and ''.join(lines[i].split(':')[1:]) == self.tittle + '\n':
                    file2.writelines(['account name:' + self.name + '\n', 'password:' + p.passwd + '\n', \
                                      'key:' + str(p.key) + '\n'])
                    print(self.tittle.center(20, '-'))
                    print('账号：' + self.name)
                    print('密码：' + self.passwd)
                    print('-' * 20)
                    i += 3
                    jud = False
                i += 1
        # 删除原文件，重命名新文件
        os.remove(self.filename)
        os.rename(self.filename + '.bak', self.filename)
        print('密码已更新！')

    def readAccount(self):
        find = False
        with open(self.filename, 'r', encoding='UTF-8') as file:
            lines = file.readlines()
            with tqdm(range(len(lines)), desc='正在读取文件', colour='green') as t:
                pat = re.compile('^(.*)' + self.tittle.lower() + '(.*)$')
                for i in t:
                    # 如果读到
                    tmp = lines[i].split(':')
                    if tmp[0] != 'tittle': continue
                    ele = (''.join(tmp[1:])).replace('\n', '')
                    Lele = ele.lower()
                    if re.search(pat, Lele) is not None:
                        find = True
                        l = len(ele)
                        tqdm.write(ele.center(l + 10, '-'))
                        tqdm.write('账号：' + ''.join(lines[i + 1].split(':')[1:]), end='')
                        p = Passwd(''.join(lines[i + 2].split(':')[1:]))
                        p.key = int(''.join(lines[i + 3].split(':')[1:len(lines[i + 3])]))
                        tqdm.write('密码：' + p.decode() + '\n', end='')
                        tqdm.write('-' * (l + 10))
                        pyperclip.copy(p.decode())
                        tqdm.write('密码已复制到剪切板！')
                    sleep(0.01)
        if find: return
        log.info('未找到账户！')
        if input('是否添加账户？（是|否）') == '是':
            self.name = input('请输入账号:')
            if input('密码是否随机生成？') == '是':
                self.newPass()
            else:
                self.passwd = input('请输入密码：')
                self.popInAccount()

    # 读取输入
    def get_input(self, mod: str = 'append'):
        if mod == 'append':
            self.popInAccount()
        else:
            if not os.path.exists(self.filename):
                log.info(self.filename + '不存在！')
                return False
            if mod == 'update':
                self.updateAccount()
            elif mod == 'read':
                self.readAccount()
            elif mod == 'delete':
                self.deleteAccount()
            elif mod == 'searchall':
                self.displayAccount('^(.*)$')
            elif mod == 'nsearch':
                self.displayAccount(input('请输入搜索关键词：'))
            else:
                log.info('未知模式名！更多模式敬请期待~')
                self.help()

    def Into_zip(self, mod: str = 'append'):
        # 如果压缩包不存在
        if not os.path.exists(self.filename):
            log.info(self.filename + '不存在')
            log.info('自动新建zip文档...')
            with zipfile.ZipFile(self.filename, 'w') as zipf:
                # 在当前目录新建文档
                f = open('passwd', 'w')
                f.close()
                zipf.write('passwd')
                # 初始化密码
                zipf.setpassword(self.zippass)
            print('密码已经成功初始化为' + str(self.zippass, encoding='UTF-8'))
        jud = False
        with zipfile.ZipFile(self.filename, 'r') as zipf:
            # 以读模式读取文件
            try:
                zipf.extract('passwd', os.curdir, self.zippass)
            except Exception:
                # 没有passwd文件的话在当前目录新建passwd
                log.info('未找到passwd文件！')
                jud = True
        if jud:
            f = open('passwd', 'w')
            f.close()
        # os.rename('passwd', 'passwd.tmp')
        zip_filename = self.filename
        self.filename = os.path.join(os.path.abspath(os.curdir), 'passwd')
        self.get_input(mod)
        self.filename = zip_filename
        # os.rename('passwd.tmp', 'passwd')
        try:
            with zipfile.ZipFile(zip_filename, 'w') as f:
                f.write('passwd')
        except PermissionError:
            # 如果在其他界面打开了压缩包就会报错
            log.info('访问出错！请关闭压缩文档窗口！')
            return
        os.remove('passwd')

    def differMod(self, mod: str = 'append') -> list[str]:
        args = [''] * 3
        if mod == 'searchall' or mod == 'nsearch':
            return args
        args[0] = input('请输入账户标题：')
        if mod == 'append' or mod == 'update':
            args[1] = input('请输入账号：')
            args[2] = passwd.random_passwd().newPasswd() \
                if input('是否随机生成密码？') == '是' \
                else input('请输入密码：')
        return args


def main():
    global log
    log = SetLogConfig()
    account = Account('')
    print('欢迎进入密码本存储程序！')
    try:
        mod = int(input('请输入选择的模式：(1-添加，2-修改，3-读取，4-删除，\
5-显示所有账户名，6-关键字搜索，7-帮助)'))
    except Exception:
        log.info('出错啦！请重试！')
    mods = ['append', 'update', 'read', 'delete', 'searchall', 'nsearch', 'help']
    if mod <= 0 or mod > 7:
        log.info('未知的选项！自动显示帮助！')
        account.help()
    if mods[mod - 1] == 'help':
        account.help()
        # 输入压缩包名字
    read_file = lambda x: x + '.zip' if x != '' else 'passwd.zip'
    read_abs_file = lambda x: os.path.abspath(read_file(x))
    account.filename = read_abs_file(input('请输入密码本的名称(默认为passwd)'))
    # 得到密码
    make_zippass = lambda x: bytes(x, encoding='UTF-8') if x != '' else b'123456'
    account.zippass = make_zippass(input('请输入密码本密码:'))
    account.tittle, account.name, account.passwd = account.differMod(mods[mod - 1])
    account.Into_zip(mods[mod - 1])
    while mods[mod - 1] == 'searchall' or mods[mod - 1] == 'nsearch':
        print('搜索完成！')
        if input('是否重新开始任务？(是|否)') != '是':
            break
        else:
            try:
                mod = int(input('请输入选择的模式：(1-添加，2-修改，3-读取，4-删除，\
5-显示所有账户名，6-关键字搜索，7-帮助)'))
            except Exception:
                log.info('出错啦！请重试！')
            if mod < 5:
                account.tittle, account.name, account.passwd = account.differMod(mods[mod - 1])
            elif mods[mod - 1] == 'help':
                account.help()
            account.Into_zip(mods[mod - 1])


def savemain():
    try:
        main()
    except Exception as exc:
        log.error('出现错误:' + str(exc))
    finally:
        input('按任意键退出...')
