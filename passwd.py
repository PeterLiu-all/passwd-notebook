from random import randint
from time import sleep

from tqdm import tqdm


# 加密模块
class Passwd():
    def __init__(self, passwd: str = '') -> None:
        self.passwd = passwd
        self.key = 1

    # 加密并随机指定密钥
    def encode(self) -> str:
        # 随机指定一个密钥
        self.key = randint(11, 125)
        result = ''
        with tqdm(self.passwd, colour='blue') as t:
            for ele in t:
                t.set_description('正在加密密码')
                # 很简单的加密方法
                num = ord(ele)
                num += self.key
                seg = ''
                # 每个密码字符加上密钥量并递增地重复输出密钥次
                for i in tqdm(range(self.key), leave=False, colour='red'):
                    seg += chr(num + i)
                    # sleep(0.001)
                result += seg
        return result

    # 首先需要初始化密钥才能解密
    def decode(self) -> str:
        ans = ''
        # 切片，步长为密钥
        for part in self.passwd[::self.key]:
            if part == '\n':
                break
            ans += chr(ord(part) - self.key)
        return ans


class random_passwd():
    def __init__(self) -> None:
        # 共69个字符
        self.Dic = ['!', '#', '$', '%', '@', '&', '?'] + \
                   [chr(i) for i in range(65, 91)] + [chr(j) for j in range(97, 123)] + \
                   [str(k) for k in range(10)]

    def newPasswd(self):
        # 密码长度不超过20位， 不小于八位
        leng = randint(8, 20)
        self.passwd = ''
        with tqdm(range(leng + 1), colour='blue') as iterPass:
            for _ in iterPass:
                iterPass.set_description('正在随机生成密码')
                self.passwd += self.Dic[randint(0, 69)]
                sleep(0.01)
        return self.passwd
