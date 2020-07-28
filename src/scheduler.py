from datetime import datetime
from bot import *

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError


# 商店更新提醒，提示购买药剂和结晶
@nonebot.scheduler.scheduled_job('cron', hour='0,6,12,18')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=941819447, auto_escape=False,
                                 message="[CQ:image,file=poison.jpg]")
    except CQHttpError:
        pass


# 出刀提醒
@nonebot.scheduler.scheduled_job('cron', hour='23')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))

    try:
        await bot.send_group_msg(group_id=941819447, auto_escape=True,
                                 message=f'ATTENTION-已经{now}点了，hxd们别忘了出刀呦！')

        await bot.send_group_msg(group_id=941819447, auto_escape=False,
                                 message="[CQ:image,file=look.jpg]")
    except CQHttpError:
        pass
