import time
import schedule
from datetime import datetime


def foo1():
    print('------------foo1', datetime.now())


def foo2():
    print('------------foo2', datetime.now())


if __name__ == "__main__":
    schedule.every().minute.do(foo1)
    schedule.every().minute.at(":00").do(foo2)

    while 1:
        schedule.run_pending()
        time.sleep(1)

"""
结论: foo1 会晚至少5秒才执行
"""
