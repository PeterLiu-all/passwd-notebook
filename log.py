import datetime
import logging
import sys


def SetLogConfig(grade: int = logging.DEBUG) -> logging.Logger:
    # 初始化日志
    log = logging.getLogger()
    log.info('开始输出日志信息...')
    log.setLevel(grade)

    # 日志文件控制器
    fle = logging.FileHandler('log.txt', encoding='UTF-8')
    fle.setLevel(grade)
    # 设置格式
    formater = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fle.setFormatter(formater)

    # 在屏幕上显示日志的控制器
    scr = logging.StreamHandler(sys.stdout)
    scr.setFormatter(formater)
    scr.setLevel(grade)

    # 添加两个控制器
    log.addHandler(fle)
    log.addHandler(scr)

    log.info('运行时间：' + str(datetime.datetime.now()))
    log.info('完成！')
    return log
