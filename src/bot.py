from data import AllData
import nonebot
import config


class QQBot(object):
    """我的机器人"""

    def __init__(self):
        """初始化我的机器人"""
        self.data = AllData()

    def reset(self):
        """重置机器人"""
        self.data.reset_bot()


MyBot = QQBot()

if __name__ == '__main__':
    nonebot.init(config)
    nonebot.load_plugin('clan_war')
    nonebot.load_plugin('scheduler')
    nonebot.run()






