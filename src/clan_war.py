from nonebot import on_command, CommandSession
from bot import *


"""
#####################################################
##                    申请出刀指令                   ##
#####################################################
                                                  """


# 申请出刀指令
@on_command('give_knife', aliases=('申请出刀', '请求出刀'), only_to_me=False)
async def give_knife(session: CommandSession):
    current_qq = session.ctx['user_id']  # 获取发送“申请出刀”的用户的qq
    current_nickname = session.ctx['sender']['card']  # 获取发送“申请出刀”的用户的群昵称

    # 判断玩家是否有群昵称，如果没有就存QQ昵称
    if current_nickname == "":
        current_nickname = session.ctx['sender']['nickname']

    # 如果当前有人正在出刀
    if MyBot.data.current_battle:

        # 判断出刀的人是否为当前用户
        if current_qq == MyBot.data.current_battle_member_qq:
            await session.send(f'你自己正在出刀哦~')
        else:
            await session.send(f'{MyBot.data.current_battle_member_nickname}正在出刀，请稍等~')

    # 如果之前没人出刀
    else:
        MyBot.data.change_current_battle()  # 更改出战状态
        MyBot.data.change_current_battle_member_qq(current_qq)  # 写入正在出战成员qq
        MyBot.data.change_current_battle_member_nickname(current_nickname)  # 写入正在出战成员群名片
        await session.send(f'{current_nickname}申请出刀成功！正在殴打第{MyBot.data.current_boss_number + 1}号BOSS！\n'
                           f'目前是第{MyBot.data.week}周目，BOSS血量为{MyBot.data.boss_blood[MyBot.data.current_boss_number]}')


"""
#####################################################
##                    完成出刀指令                   ##
#####################################################
                                                  """


# 完成出刀指令
@on_command('complete_knife', aliases='完成', only_to_me=False)
async def complete_knife(session: CommandSession):
    current_qq = session.ctx['user_id']  # 获取发送“完成出刀”的用户的qq

    # 如果之前有发送申请出刀
    if MyBot.data.current_battle:

        # 如果发送该指令的用户匹配成功（之前为该用户发送的申请出刀）
        if current_qq == MyBot.data.current_battle_member_qq:
            stripped_arg = session.current_arg_text.split()

            # 如果输入按空格分隔的元素个数为1个
            if len(stripped_arg) == 1:

                # 判断元素是否为数字
                if stripped_arg[0].isdigit():
                    MyBot.data.change_current_battle()  # 更改出战状态
                    damage_number = int(stripped_arg[0])  # 伤害值
                    MyBot.data.make_damage_to_boss(damage_number)  # 对当前boss造成伤害

                    # 如果当前boss血量小于等于0(被击杀)
                    if MyBot.data.boss_blood[MyBot.data.current_boss_number] <= 0:
                        MyBot.data.add_current_boss_number()  # boss下标加一
                        MyBot.data.kill_all_boss()  # 调用函数判断是否增加周目

                    await session.send(f'{MyBot.data.current_battle_member_nickname}完成{damage_number}的伤害，' 
                                       f'当前为第{MyBot.data.week}周目的第{MyBot.data.current_boss_number + 1}只BOSS，' 
                                       f'血量为{MyBot.data.boss_blood[MyBot.data.current_boss_number]}')

                # 判断元素是否为“击杀”
                elif stripped_arg[0] == "击杀":
                    MyBot.data.change_current_battle()  # 更改出战状态
                    MyBot.data.add_current_boss_number()  # boss下标加一
                    MyBot.data.kill_all_boss()  # 调用函数判断是否增加周目

                    await session.send(f'{MyBot.data.current_battle_member_nickname}完成击杀，'
                                       f'开始打第{MyBot.data.week}周目的第{MyBot.data.current_boss_number + 1}只BOSS，'
                                       f'血量为{MyBot.data.boss_blood[MyBot.data.current_boss_number]}')

                # 如果与前两种情况无法匹配
                else:
                    await session.send(f'请按正确格式输入，完成+空格＋伤害（或完成+空格+击杀）')

            # 输入格式有问题
            else:
                await session.send(f'请按正确格式输入，完成+空格＋伤害（或完成+空格+击杀）')

        # 指令匹配用户失败（其他用户发出指令）
        else:
            await session.send(f'请不要调皮~')


"""
#####################################################
##                     修正指令                      ##
#####################################################
                                                  """


# 修正指令
@on_command('correct', aliases='修正', only_to_me=False)
async def correct(session: CommandSession):
    current_qq = session.ctx['user_id']  # 获取发送“申请出刀”的用户的qq
    stripped_arg = session.current_arg_text.split()

    # 判断输入按空格分隔是否为三个元素（第几周目，第几个怪，血量）
    if len(stripped_arg) == 3:

        # 如果三次输入均合法（为数字）
        if stripped_arg[0].isdigit() and stripped_arg[1].isdigit() and stripped_arg[2].isdigit():
            MyBot.data.reset_boss_blood()  # 重置boss血量
            MyBot.data.change_week(int(stripped_arg[0]))  # 修改周目
            MyBot.data.change_current_boss_number(int(stripped_arg[1]) - 1)  # 修改当前boss下标
            MyBot.data.change_boss_blood(int(stripped_arg[1]) - 1, int(stripped_arg[2]))  # 修改当前boss血量
            await session.send(f'修正成功，当前为第{stripped_arg[0]}周目，第{stripped_arg[1]}只BOSS，血量为{stripped_arg[2]}')
        # 格式输入有误
        else:
            await session.send(f'请按正确格式输入，修正+周目数+第几只boss+修改后血量（除修正指令外请均输入阿拉伯数字）')

    # 格式输入有误
    else:
        await session.send(f'请按正确格式输入，修正+周目数+第几只boss+修改后血量（除修正指令外请均输入阿拉伯数字）')


"""
#####################################################
##                      挂树指令                     ##
#####################################################
                                                  """


# 挂树指令
@on_command('hang_on_tree', aliases='挂树', only_to_me=False)
async def hang_on_tree(session: CommandSession):
    current_qq = session.ctx['user_id']  # 获取发送“申请出刀”的用户的qq
    current_nickname = session.ctx['sender']['card']  # 获取发送“申请出刀”的用户的群昵称

    # 判断玩家是否有群昵称，如果没有就存QQ昵称
    if current_nickname == "":
        current_nickname = session.ctx['sender']['nickname']

    if MyBot.data.query_tree(current_nickname):
        await session.send(f'你已经在树上了，快喊人来救你吧~')
    else:
        MyBot.data.add_tree_member(current_nickname)
        await session.send(f'自挂东南枝成功，快喊人来救你吧~')


"""
#####################################################
##                      查树指令                     ##
#####################################################
                                                  """


# 查树指令
@on_command('look_up_tree', aliases='查树', only_to_me=False)
async def look_up_tree(session: CommandSession):
    output = """当前共""" + str(len(MyBot.data.tree)) + """人挂树:"""
    for x in MyBot.data.tree:
        output = output + '\n' + x
    await session.send(output)



"""
#####################################################
##                      查询指令                     ##
#####################################################
                                                  """


# 查询指令
@on_command('look_up_data', aliases='查询', only_to_me=False)
async def look_up_data(session: CommandSession):
    await session.send(f'当前为第{MyBot.data.week}周目的第{MyBot.data.current_boss_number + 1}只BOSS，'
                       f'血量为{MyBot.data.boss_blood[MyBot.data.current_boss_number]}')


"""
#####################################################
##                      清树指令                     ##
#####################################################
                                                  """


# 清树指令
@on_command('clean_tree', aliases='清树', only_to_me=False)
async def clean_tree(session: CommandSession):
    MyBot.data.reset_tree()
    await session.send(f'清树成功')



"""
#####################################################
##                    撤销出刀指令                    ##
#####################################################
                                                  """


# 撤销出刀指令
@on_command('get_knife_back', aliases='撤销出刀', only_to_me=False)
async def get_knife_back(session: CommandSession):

    current_qq = session.ctx['user_id']  # 获取发送“撤销出刀”的用户的qq

    # 判断当前是否有人出刀
    if MyBot.data.current_battle:

        # 判断当前用户是否为设置的管理员
        if MyBot.data.check_on_if_op(current_qq):
            MyBot.data.change_current_battle()  # 如果为管理员则更改出战状态
            await session.send(f'SUCCESS! 撤销当前玩家出刀成功，可重新申请出刀。')
        else:
            await session.send(f'SORRY! 非管理员不能撤销出刀。')

    # 若当前无人正在出刀
    else:

        await session.send(f'当前无成员申请出刀，撤了个寂寞。')
