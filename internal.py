#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 游戏内核

import math, database
from random import random
from copy import deepcopy

class armor:
    def __init__(self, _tuple):
        self.id = _tuple[0]
        self.name = _tuple[1]
        self.properties = {
            "p_attack" : _tuple[2],
            "p_defense" : _tuple[3],
            "m_attack" : _tuple[4],
            "m_defense" : _tuple[5],
            "accuracy" : _tuple[6],
            "agility" : _tuple[7]
            }
        self.kind = _tuple[8]
        self.price = _tuple[9]
        self.description = _tuple[10].split(sep='d')
        self.special = _tuple[11]
        if self.special is not None:
            spec = database.get_special(self.special)
            self.description.extend(spec[2].split(sep='d'))
            self.description.append("售价 {}".format(self.price))
        self.clicked = False
    def __eq__(self, another):
        return self.id == another

class bag:
    def __init__(self):
        self.keys = [0, 0, 0, 0]
        self.keys = [99, 99, 99, 0]     # test
        self.money = 20
        self.armor = []
        self.gem = 0
    def sell(self, _num):
        self.money += self.armor[_num].price
        del self.armor[_num]

class monster:
    def __init__(self, _tuple):
        self.id = _tuple[0]
        self.name = _tuple[1]
        self.life = _tuple[2]
        self.calc_properties = {
            "p_attack" : _tuple[3],
            "p_defense" : _tuple[4],
            "m_attack" : _tuple[5],
            "m_defense" : _tuple[6],
            "accuracy" : _tuple[7],
            "agility" : _tuple[8]
            }
        self.level = _tuple[9]
        self.special = (_tuple[10], )
        self.experience = 0
        self.description = []
        if self.special[0] is not None:
            spec = database.get_special(self.special[0])
            self.description.append("特效：{}".format(spec[1]))
            self.description.extend(spec[2].split(sep='d'))
    def _str(self):
        res = '''生命：{0} 等级：{1}
物攻：{2} 物防：{3}
法攻：{4} 法防：{5}
精准：{6} 敏捷：{7}
特效：'''.format(self.life, self.level, self.calc_properties["p_attack"], self.calc_properties["p_defense"], \
                   self.calc_properties["m_attack"], self.calc_properties["m_defense"],\
                   self.calc_properties["accuracy"], self.calc_properties["agility"])
        for spec in self.special:
            if spec is not None:
                name = database.get_special(spec)[1]
                res += name
                res += ' '
        res += '\n'
        return res
    def get_harm(self, _warrior):
        return fight(_warrior, self, False)[0]
    def calc_exp(self, _warrior):
        base = 2
        if 18 in _warrior.special:
            base = math.exp(1)
        self.experience = round(base ** (self.level / _warrior.level))

class warrior(monster):
    def __init__(self):
        monster.__init__(self, (-1, "勇士", 250, 10, 10, 0, 0, 5, 5, 1, None))    # 此处设置勇士属性
        monster.__init__(self, (-1, "勇士", 6666, 666, 666, 666, 666, 66, 66, 14, None))      # 无敌，用于测试
        self.occupation = 0
        
        self.properties = {
            "p_attack" : 666,
            "p_defense" : 666,
            "m_attack" : 666,
            "m_defense" : 666,
            "accuracy" : 66,
            "agility" : 66
            }   # test'''
        '''
        self.properties = {
            "p_attack" : 10,
            "p_defense" : 10,
            "m_attack" : 0,
            "m_defense" : 0,
            "accuracy" : 5,
            "agility" : 5
            }'''
        self.experience = 0      
        self.armor = [None, None, None, None, None]
        self.bag = bag()
        self.face = 0           # 下左右上
        self.special = [None, None, None, None, None]
    def update_properties(self):
        armor_properties = {
            "p_attack" : 0,
            "p_defense" : 0,
            "m_attack" : 0,
            "m_defense" : 0,
            "accuracy" : 0,
            "agility" : 0
            }
        for tag in armor_properties:
            for arm in self.armor:
                if arm is not None:
                    armor_properties[tag] += arm.properties[tag]
            armor_properties[tag] = round(armor_properties[tag] * (1.05 ** (self.level - 1)))     # 每提升一级装备效果提升5%
            self.calc_properties[tag] = self.properties[tag] + armor_properties[tag]
    def armor_wear(self, _arm):
        self.armor[_arm.kind] = _arm
        self.special[_arm.kind] = _arm.special
        self.update_properties()
    def armor_drop(self, _kind):
        self.armor[_kind] = None
        self.special[_kind] = None
        self.update_properties()
    def upgrade(self):
        self.level += 1
        for tag in self.properties:
            self.properties[tag] += 1
        self.life += 100
        self.update_properties()
    def p_upgrade(self):
        self.properties["p_attack"] += 5
        self.properties["p_defense"] += 5
        self.update_properties()
    def m_upgrade(self):
        self.properties["m_attack"] += 5
        self.properties["m_defense"] += 5
        self.update_properties()
    def l_upgrade(self):
        self.properties["accuracy"] += 2
        self.properties["agility"] += 2
        self.life += 250
        self.update_properties()
    def use_gem(self, _color, _num):
        self.bag.gem -= _num
        self.bag.money -= _num
        prop = ("p_attack", "p_defense", "m_attack", "m_defense")
        self.properties[prop[_color]] += 2 * _num
        self.update_properties()
    def buy_gem(self, _color, _num):
        self.bag.money -= _num * 10
        prop = ("p_attack", "p_defense", "m_attack", "m_defense")
        self.properties[prop[_color]] += 2 * _num
        self.update_properties()
    def buy_bomb(self, _num):
        self.bag.money -= _num * 50
        self.bag.keys[3] += _num
    def buy_blood(self, _num):
        self.bag.money -= _num * 10
        self.life += 100 * _num

class battle:
    def __init__(self, _A, _B):
        self.A = _A
        self.B = _B
        self.B_ori_life = _B.life
        self.acc_p_harm = 0
        self.acc_m_harm = 0
    def check_shot(self):       # 试验A对B的攻击是否命中
        if self.A.calc_properties["accuracy"] == 0:
            return False
        return random() < self.A.calc_properties["accuracy"] / (self.A.calc_properties["accuracy"] + self.B.calc_properties["agility"])
    def check_resist(self):     # 试验A对B的特效是否命中
        res = self.A.level / (self.A.level + self.B.level)
        if 6 in self.B.special:
            res *= res
        return random() < res
    def magic_attack(self):     # A对B发动法术攻击
        res = [0, False]    # 伤害值，是否眩晕
        if self.check_shot():
            res[0] = self.A.calc_properties["m_attack"] - self.B.calc_properties["m_defense"]
            if res[0] < 0:
                res[0] = 0
            if 20 in self.A.special:                        # 机关
                res[0] += 200 - self.B.calc_properties["m_defense"]
            if res[0] < 0:
                res[0] = 0
            if 2 in self.A.special:                         # 灼烧
                res[0] += round(self.B.life * 0.1)
            if 1 in self.A.special and res[0] > 0:          # 石化
                self.B.calc_properties["agility"] -= 5
                self.B.calc_properties["accuracy"] -= 5
                if self.B.calc_properties["agility"] < 0:
                    self.B.calc_properties["agility"] = 0
                if self.B.calc_properties["accuracy"] < 0:
                    self.B.calc_properties["accuracy"] = 0
            elif 14 in self.A.special and res[0] > 0:       # 风暴
                self.B.calc_properties["m_defense"] = round(self.B.calc_properties["m_defense"] * 0.9)
            elif 3 in self.A.special:                       # 雷霆
                if random() < self.A.level / 15:
                    res[0] = round(self.A.calc_properties["m_attack"] * 1.5) - self.B.calc_properties["m_defense"]
                    if self.check_resist():
                        res[1] = True
            if 0 in self.A.special:
                self.A.life += round(res[0] * 0.5)
        return res
    def physical_attack(self):    # A对B发动物理攻击
        res = [0, False]          # 伤害值，是否眩晕
        if self.check_shot():
            res[0] = self.A.calc_properties["p_attack"] - self.B.calc_properties["p_defense"]
            if res[0] < 0:
                res[0] = 0
            if 20 in self.A.special:                        # 机关
                res[0] += 500 - self.B.calc_properties["p_defense"]
            if res[0] < 0:
                res[0] = 0
        return res
    def true_attack(self):              # A对B发动真实伤害
        res = [0, False]                # 伤害值，是否眩晕
        if 4 in self.A.special:         # 暴戾
            if self.check_shot():
                res[0] = round(self.A.life * 0.1)
                self.A.life -= res[0]
                if self.check_resist():
                    res[1] = True
                    self.B.calc_properties["accuracy"] = round(self.B.calc_properties["accuracy"] * 0.9)
                    self.B.calc_properties["agility"] = round(self.B.calc_properties["agility"] * 0.9)
        elif 8 in self.A.special:       # 惩戒
            if self.check_shot():
                res[0] = 1
                if self.A.level > self.B.level:
                    res[0] = 10 * (self.A.level - self.B.level)
        return res
    def magic_defense(self, _harm):       # B对A发动的法术伤害进行还击
        res = [0, False]            # 伤害值，是否眩晕
        if 11 in self.B.special:        # 法力寒潮
            if random() < _harm[0] / self.B.life * (1.05 ** self.B.level):
                res[1] = True
        self.B.life -= _harm[0]
        self.acc_m_harm += _harm[0]
        return res
    def physical_defense(self, _harm):        # B对A发动的物理伤害进行还击
        res = [0, False]                # 伤害值，是否眩晕
        if 13 in self.B.special:        # 物理寒潮
            if random() < _harm[0] / self.B.life * (1.05 ** self.B.level):
                res[1] = True
        elif 7 in self.B.special:           # 灵性
            res[0] = round(_harm[0] * 0.1) - self.A.calc_properties["m_defense"]
            if res[0] < 0:
                res[0] = 0
            _harm[0] = round(_harm[0] * 0.9)
        self.B.life -= _harm[0]
        self.acc_p_harm += _harm[0]
        return res
    def physical_round(self):
        # A对B的一个物理回合包括：A对B物理攻击，B对A物理反击，返回二者眩晕情况
        A_B_harm = self.physical_attack()
        B_A_harm = self.physical_defense(A_B_harm)
        self.A.life -= B_A_harm[0]
        return (B_A_harm[1], A_B_harm[1])
    def magic_round(self):
        # A对B的一个法术回合包括：A对B法术攻击，B对A法术反击，返回二者眩晕情况
        A_B_harm = self.magic_attack()
        B_A_harm = self.magic_defense(A_B_harm)
        self.A.life -= B_A_harm[0]
        return (B_A_harm[1], A_B_harm[1])
    def round(self):
        # A对B的一个回合包括：A对B物理攻击，B对A物理反击，A对B法术攻击，B对A法术反击，A对B真实攻击
        A_fall = False
        B_fall = False
        if 10 in self.A.special:          # 震慑
            if self.check_resist():
                for tag in self.B.calc_properties:
                    self.B.calc_properties[tag] = round(0.8 * self.B.calc_properties[tag])
        elif 5 in self.A.special:         # 双工
            if random() < 0.5:
                fall = self.physical_round()
                A_fall = fall[0] or A_fall
                B_fall = fall[1] or B_fall
        # 物理回合
        fall = self.physical_round()
        A_fall = fall[0] or A_fall
        B_fall = fall[1] or B_fall
        # 法术回合
        fall = self.magic_round()
        A_fall = fall[0] or A_fall
        B_fall = fall[1] or B_fall
        # 真实攻击
        true_harm = self.true_attack()
        self.B.life -= true_harm[0]
        B_fall = true_harm[0] or B_fall
        if 15 in self.A.special:        # 法力霜冻
            if self.acc_m_harm >= round(self.B_ori_life * 0.25):
                self.acc_m_harm -= round(self.B_ori_life * 0.25)
                self.B.life = round(self.B.life * 0.8)
                B_fall = True
        if 16 in self.A.special:        # 物理霜冻
            if self.acc_p_harm >= round(self.B_ori_life * 0.25):
                self.acc_p_harm -= round(self.B_ori_life * 0.25)
                self.B.life = round(self.B.life * 0.8)
                B_fall = True
        if 6 in self.B.special:         # 笃定
            self.B.life += round((self.B_ori_life - self.B.life) / 16)
        if 20 in self.A.special:        # 机关
            self.A.life += 88
        return (A_fall, B_fall)           

def fight(_warrior, _monster, _record):
    warrior_copy = deepcopy(_warrior)
    if 9 in _monster.special:           # 洞察
        for i in range(0, 5):
            warrior_copy.armor[i] = None
            warrior_copy.special[i] = None
        warrior_copy.update_properties()
    if 12 in _warrior.special:          # 魅惑
        _monster.calc_properties["accuracy"] = round(0.5 * _monster.calc_properties["accuracy"])
        _monster.calc_properties["agility"] = round(0.5 * _monster.calc_properties["agility"])
    W2M = battle(warrior_copy, _monster)
    M2W = battle(_monster, warrior_copy)
    round_2 = (False, False)
    victory = False
    log = None
    if _record:
        log = '猛士：\n'
        log += _warrior._str()
        log += '\n'
        log += '怪物：'
        log += _monster.name
        log += '\n'
        log += _monster._str()
        log += '\n'
    round_cnt = 0
    while round_cnt < 101:
        warrior_agility = warrior_copy.calc_properties["agility"]
        monster_accuracy = _monster.calc_properties["accuracy"]                         
        round_1 = W2M.round()
        if warrior_copy.life <= 0:
            break
        if _monster.life <= 0:
            victory = True
            break
        if round_2[0]:
            _monster.calc_properties["agility"] = monster_agility
        if round_2[1]:
            warrior_copy.calc_properties["accuracy"] = warrior_accuracy
        # TODO: 注意是否要从battle对象中拷贝生命值！
        if round_1[0] or round_1[1]:
            if round_1[0]:
                warrior_copy.calc_properties["agility"] = 0
            if round_1[1]:
                _monster.calc_properties["accuracy"] = 0
        warrior_accuracy = warrior_copy.calc_properties["accuracy"]
        monster_agility = _monster.calc_properties["agility"]
        round_2 = M2W.round()
        if _record:
            log += "{0} {1}".format(warrior_copy.life, _monster.life)
            log += '\n'
        if warrior_copy.life <= 0:
            break
        if _monster.life <= 0:
            victory = True
            break
        if round_1[0]:
            warrior_copy.calc_properties["agility"] = warrior_agility
        if round_1[1]:
            _monster.calc_properties["accuracy"] = monster_accuracy       
        if round_2[0] or round_2[1]:
            if round_2[0]:
                _monster.calc_properties["agility"] = 0
            if round_2[1]:
                warrior_copy.calc_properties["accuracy"] = 0
        round_cnt += 1
    res = 0
    if _warrior.life > warrior_copy.life:
        res = _warrior.life - warrior_copy.life
    if not victory:
        return ("???", log)                # 打不过
    else:
        return (res, log)

def fight_wrap(_warrior, _monster):
    monster_copy = deepcopy(_monster)
    res = fight(_warrior, monster_copy, True)
    if 19 in _warrior.special:
        for i in range(0, _warrior.level):
            monster_copy = deepcopy(_monster)
            temp = fight(_warrior, monster_copy, True)
            if temp[0] < res[0]:
                res = temp
    if res[0] != "???":
        _monster.calc_exp(_warrior)
        _warrior.experience += _monster.experience
        _warrior.life -= res[0]
    return res          

def test(_monster):
    mons = monster(database.get_monster(_monster))
    newbie = warrior()
    arm = armor(database.get_armor('others-2'))
    newbie.armor_wear(arm)
    print(fight(newbie, mons, True)[1])
