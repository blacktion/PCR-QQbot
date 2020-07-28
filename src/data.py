from datalist import *


class AllData(object):
    """用于保存所有的数据"""
    def __init__(self):
        """初始化所有数据"""
        self.boss_number = BOSS_NUMBER
        self.current_boss_number = INITIAL - 1
        self.current_battle = CURRENT_BATTLE
        self.current_battle_member_qq = EMPTY
        self.current_battle_member_nickname = EMPTY
        self.week = INITIAL
        self.boss_blood = [0] * BOSS_NUMBER
        for i in range(BOSS_NUMBER):
            self.boss_blood[i] = BOSS_BLOOD[i]
        self.op_list = [0] * OP_NUMBER
        for i in range(OP_NUMBER):
            self.op_list[i] = OP_LIST[i]
        self.tree = set(INITIAL_SET)


# ################################################### #
# #                   重置指令集                      # #
# ################################################### #

    def reset_boss_number(self):
        """重置boss数量"""
        self.boss_number = BOSS_NUMBER

    def reset_current_boss_number(self):
        """重置当前boss下标"""
        self.current_boss_number = INITIAL - 1

    def reset_current_battle(self):
        """重置当前是否有出战的bool标志"""
        self.current_battle = CURRENT_BATTLE

    def reset_current_battle_member_qq(self):
        """重置当前申请出战的成员qq"""
        self.current_battle_member_qq = EMPTY

    def reset_current_battle_member_nickname(self):
        """重置当前申请出战的成员群名片（或昵称）"""
        self.current_battle_member_nickname = EMPTY

    def reset_boss_blood(self):
        """重置所有boss血量"""
        for i in range(5):
            self.boss_blood[i] = BOSS_BLOOD[i]

    def reset_week(self):
        """重置挑战周目"""
        self.week = INITIAL

    def reset_tree(self):
        """重置树"""
        self.tree.clear()

    def reset_bot(self):
        """重置所有数据"""
        self.reset_boss_number()
        self.reset_current_boss_number()
        self.reset_current_battle()
        self.reset_current_battle_member_qq()
        self.reset_current_battle_member_nickname()
        self.reset_boss_blood()
        self.reset_week()
        self.reset_tree()

# ################################################### #
# #                   修改指令集                      # #
# ################################################### #

    def change_boss_number(self, boss_number):
        """更改boss总数"""
        self.boss_number = boss_number

    def change_current_boss_number(self, current_boss_number):
        """更改当前boss下标"""
        self.current_boss_number = current_boss_number

    def change_current_battle(self):
        """更改当前是否有出战的bool标志"""
        self.current_battle = not self.current_battle

    def change_current_battle_member_qq(self, current_battle_member_qq):
        """更改当前申请出战成员qq"""
        self.current_battle_member_qq = current_battle_member_qq

    def change_current_battle_member_nickname(self, current_battle_member_nickname):
        """更改当前申请出战成员群名片（或昵称）"""
        self.current_battle_member_nickname = current_battle_member_nickname

    def change_boss_blood(self, current_boss_number, boss_blood):
        """更改当前boss血量"""
        self.boss_blood[current_boss_number] = boss_blood

    def change_week(self, week):
        """更改周目"""
        self.week = week

# ################################################### #
# #                   功能指令集                      # #
# ################################################### #

    def make_damage_to_boss(self, damage):
        """对当前boss造成伤害"""
        self.boss_blood[self.current_boss_number] -= damage

    def add_current_boss_number(self):
        """当前boss下标加一"""
        self.current_boss_number += 1

    def add_tree_member(self, nickname):
        """增加挂树成员"""
        self.tree.add(nickname)

    def query_tree(self, nickname):
        """查看成员是否挂树"""
        if nickname in self.tree:
            return True
        else:
            return False

    def kill_all_boss(self):
        """判断是否击杀所有boss，并更改相应数据数据"""
        # 如果击杀了所有的boss
        if self.current_boss_number >= BOSS_NUMBER:
            self.reset_current_boss_number()  # 初始化boss下标
            self.change_week(self.week + 1)  # 战斗周目加一
            self.reset_boss_blood()  # 重置所有boss血量

    def check_on_if_op(self, current_qq):
        """判断当前用户是否为设定的管理员"""
        for qq_num in self.op_list:
            if current_qq == qq_num:
                return True
        return False
