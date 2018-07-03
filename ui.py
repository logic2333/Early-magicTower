#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, saving, plot
from time import sleep
from pygame.locals import *
from hello import *
from res import *
from internal import *
from os import startfile
from database import update_life, get_life
import floors

pygame.init()
surface = pygame.display.set_mode((800, 450), SRCALPHA)
IS_SHOPPING = False         # 是否在商店
FRAME = 50                  # 帧率
SECTION_NAME = ("堕 入", "试 炼", "涅 槃")
OCCUPATION_NAME = {
    0 : "",
    'A' : "青  龙",
    'B' : "白  虎",
    'C' : "朱  雀",
    'D' : "玄  武"
}
OCCUPATION_COLOR = {
    0 : Color("white"),
    'A' : Color("cyan"),
    'B' : Color("white"),
    'C' : Color("red"),
    'D' : Color("grey")
}
POLICE_PROB = 0.01
police_defeated = 0
police_served = 0
now_floor = None
_now_floor = 0
now_map = None
walk_dir = ((1, 0), (0, -1), (0, 1), (-1, 0))       # 下左右上
newbie = warrior()
CHOICE = -1         # 开场选择的出身
ID = None           # 用户名
life_left = 3       # 剩余复活次数


def show_map(_map):
    global surface
    _map.warrior_sprite.show(surface)
    _map.door_container.draw(surface)
    _map.active_container.draw(surface)
    for sprite in _map.static_container:
        surface.blit(pic_dic["empty"], sprite.rect)
    _map.static_container.draw(surface)
    pygame.display.update()

def show_floor(_floor):
    global newbie, surface, SECTION_NAME, OCCUPATION_NAME, OCCUPATION_COLOR
    empty(surface, (610, 0, 190, 350))
    floor_txt_1 = text("第 {} 层".format(_floor), 641, 15, font_32, Color('gold'))
    section = 0
    if int(_floor[1:]) > 15:
        floor_txt_1 = text("第 {} 层".format(_floor[1:]), 641, 15, font_32, Color('gold'))
        section = 2
    elif int(_floor[1:]) > 6:
        section = 1
    floor_txt_2 = text("{0} 区  {1}".format(section, SECTION_NAME[section]), 617, 62, font_32, Color('gold'))
    floor_txt_3 = text(OCCUPATION_NAME[newbie.occupation], 657, 109, font_32, OCCUPATION_COLOR[newbie.occupation])
    floor_txt_1.show(surface)
    floor_txt_2.show(surface)
    floor_txt_3.show(surface)
    pygame.display.update()

def show_warrior(_warrior):
    global surface, newbie
    warrior_pic = None
    is_warrior = (_warrior.id == -1)
    if is_warrior:
        empty(surface, (0, 0, 190, 181))
        warrior_pic = picture(pic_dic["warrior_{}_src".format(_warrior.occupation)], (31, 15), 0, 0, 32, 32)
    else:
        empty(surface, (610, 0, 190, 350))
        warrior_pic = picture(pic_dic["monster_src"], (641, 15), 0, 32 * int(_warrior.id[5:]), 32, 32)
    warrior_pic.show(surface)
    texts = []
    texts.append(text("{} 级".format(_warrior.level), 95, 15, font_32))
    texts.append(text("物攻 {}".format(_warrior.calc_properties["p_attack"]), 10, 57, font_20))
    texts.append(text("物防 {}".format(_warrior.calc_properties["p_defense"]), 105, 57, font_20))
    texts.append(text("法攻 {}".format(_warrior.calc_properties["m_attack"]), 10, 87, font_20))
    texts.append(text("法防 {}".format(_warrior.calc_properties["m_defense"]), 105, 87, font_20))
    texts.append(text("精准 {}".format(_warrior.calc_properties["accuracy"]), 10, 117, font_20))
    texts.append(text("敏捷 {}".format(_warrior.calc_properties["agility"]), 105, 117, font_20))
    texts.append(text("生命 {}".format(_warrior.life), 10, 147, font_20))
    if not is_warrior:
        for i in range(0, len(texts)):
            texts[i].rect[0] += 610
    exp_txt = None
    if is_warrior:
        exp_txt = text("经验 {}".format(_warrior.experience), 105, 147, font_20)
        for i in range(0, 5):
            empty(surface, (5 + 37 * i, 181, 32, 32))
            pygame.draw.rect(surface, Color('white'), (5 + 37 * i, 181, 32, 32), 2)
            if _warrior.armor[i] is not None:
                armor_pic = picture(pic_dic[_warrior.armor[i].id], (5 + 37 * i, 181), 0, 0, 32, 32)
                armor_pic.show(surface)
    else:
        _warrior.calc_exp(newbie)
        exp_txt = text("经验 {}".format(_warrior.experience), 715, 147, font_20)
        harm_txt = text("可能受伤 {}".format(_warrior.get_harm(newbie)), 620, 177, font_20)
        harm_txt.show(surface)
        show_description(_warrior, False)
    exp_txt.show(surface)
    for txt in texts:
        txt.show(surface)
    pygame.display.update()

def drop_armor(_warrior):
    global surface
    for i in range(0, 5):
        if _warrior.armor[i] is not None and _warrior.armor[i].clicked:
            _warrior.armor[i].clicked = False
            _warrior.bag.armor.append(_warrior.armor[i])
            _warrior.armor_drop(i)
            show_warrior(_warrior)
            pygame.draw.rect(surface, Color('white'), (5 + 37 * i, 181, 32, 32), 2)
            empty(surface, (5 + 37 * i, 181, 32, 32))
    if IS_SHOPPING:
        show_shop(_warrior)
    pygame.display.update()

def show_shop(_warrior):
    global surface
    empty(surface, (190, 15, 420, 420))
    bei_txt = text("背", 309, 35, font_32)
    bao_txt = text("包", 459, 35, font_32)
    bei_txt.show(surface)
    bao_txt.show(surface)
    for i in range(0, len(_warrior.bag.armor)):
        rect = (210 + 50 * (i % 8), 85 + 50 * (i // 8), 32, 32)
        pygame.draw.rect(surface, Color("white"), rect, 2)
        empty(surface, rect)
        armor_pic = picture(pic_dic[_warrior.bag.armor[i].id], (210 + 50 * (i % 8), 85 + 50 * (i // 8)), 0, 0, 32, 32)
        armor_pic.show(surface)
    item_pic = []
    item_pic.append(picture(pic_dic["item-yellow_key"], (210, 333), 0, 0, 32, 32))
    item_pic.append(picture(pic_dic["item-blue_key"], (310, 333), 0, 0, 32, 32))
    item_pic.append(picture(pic_dic["item-red_key"], (410, 333), 0, 0, 32, 32))
    item_pic.append(picture(pic_dic["item-bomb"], (210, 383), 0, 0, 32, 32))
    item_pic.append(picture(pic_dic["item-black_gem"], (310, 383), 0, 0, 32, 32))
    item_pic.append(picture(pic_dic["item-money"], (410, 383), 0, 0, 32, 32))
    item_txt = []
    item_txt.append(text(str(_warrior.bag.keys[0]), 260, 333, font_20))
    item_txt.append(text(str(_warrior.bag.keys[1]), 360, 333, font_20))
    item_txt.append(text(str(_warrior.bag.keys[2]), 460, 333, font_20))
    item_txt.append(text(str(_warrior.bag.keys[3]), 260, 383, font_20))
    item_txt.append(text(str(_warrior.bag.gem), 360, 383, font_20))
    item_txt.append(text(str(_warrior.bag.money), 460, 383, font_20))
    for i in range(0, 6):
        item_pic[i].show(surface)
        item_txt[i].show(surface)
    buttons = []
    buttons.append(text("使用黑石", 510, 327, font_20, Color("blue")))
    buttons.append(text("购买物品", 510, 352, font_20, Color("blue")))
    buttons.append(text("佩戴装备", 510, 377, font_20, Color("blue")))
    buttons.append(text("出售装备", 510, 402, font_20, Color("blue")))
    for button in buttons:
        button.show(surface)
    pygame.display.update()

def sell_armor(_warrior):
    global newbie, POLICE_PROB, police_defeated, CHOICE, police_served, surface, _now_floor
    for i in range(0, len(_warrior.bag.armor)):
        if _warrior.bag.armor[i].clicked:
            hint_txt = text("出售 {0} 售价 {1} ".format(_warrior.bag.armor[i].name, _warrior.bag.armor[i].price), 210, 295, font_20)
            confirm_txt = text("确定", 460, 295, font_20, Color("blue"))
            hint_txt.show(surface)
            confirm_txt.show(surface)
            pygame.display.update()
            while True:
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONDOWN:
                        if Rect(460, 295, 40, 20).collidepoint(pygame.mouse.get_pos()):
                            newbie.bag.sell(i)
                            show_shop(newbie)
                            return
                        else:
                            return
                    elif event.type == MOUSEMOTION:
                        mousemove_show_armor(newbie)
                    elif event.type == QUIT:
                        doc = saving.document(newbie, _now_floor, floors.floors, POLICE_PROB, police_defeated, CHOICE, police_served)
                        doc.save(_id)
                        exit()
    else:
        hint_txt = text("请先在背包中选中装备！", 210, 295, font_20)
        hint_txt.show(surface)

def play_animation(_anim, _time):
    global surface
    for i in range(0, 4):
        _time.tick(FRAME)
        ticks = pygame.time.get_ticks()
        _anim.update(ticks, None, FRAME)
        _anim.show(surface)
        pygame.display.update()

class mymap:
    def __init__(self, _data):
        self.data = _data
        self.warrior_posit = None
        self.active_container = pygame.sprite.Group()
        self.door_container = pygame.sprite.Group()
        self.static_container = pygame.sprite.Group()
        self.warrior_sprite = None
    def reload(self, _warrior):
        global _now_floor
        self.warrior_posit = None
        self.active_container = pygame.sprite.Group()
        self.door_container = pygame.sprite.Group()
        self.static_container = pygame.sprite.Group()
        if _now_floor != 6:
            self.data[13] = True        # arrived
        self.warrior_sprite = None
        for i in range(0, 13):
            for j in range(0, 13):
                if self.data[i][j] == "warrior":
                    self.warrior_posit = [i, j]
                    self.warrior_sprite = animation(pic_dic["warrior_{}_src".format(newbie.occupation)], (192 + 32 * j, 17 + 32 * i), newbie.face, True, True)
                elif self.data[i][j] == "lava-warrior":
                    self.warrior_posit = [i, j]
                    self.warrior_sprite = animation(pic_dic["lava-warrior_{}_src".format(newbie.occupation)], (192 + 32 * j, 17 + 32 * i), newbie.face, True, True)
                elif self.data[i][j][0:4] == "door":
                    self.door_container.add(animation(pic_dic["doors_src"], (192 + 32 * j, 17 + 32 * i), int(self.data[i][j][5]), False, False))
                elif self.data[i][j][0:3] == "npc":
                    self.active_container.add(animation(pic_dic["npc_src"], (192 + 32 * j, 17 + 32 * i), int(self.data[i][j][4]), True, True))
                elif self.data[i][j][0:4] == "mons" and self.data[i][j][5] != 'c':
                    self.active_container.add(animation(pic_dic["monster_src"], (192 + 32 * j, 17 + 32 * i), int(self.data[i][j][5:]), True, True))
                elif self.data[i][j][0:4] == "hint":
                    self.static_container.add(picture(pic_dic["hint"], (192 + 32 * j, 17 + 32 * i), 0, 0, 32, 32))
                else:
                    self.static_container.add(picture(pic_dic[self.data[i][j]], (192 + 32 * j, 17 + 32 * i), 0, 0, 32, 32))
    def door_open(self, _time):
        global surface
        for door in self.door_container:
            if door.rect[0] == self.warrior_posit[0] and door.rect[1] == self.warrior_posit[1]:
                play_animation(door, _time, surface)
                break
    def mousemove_show_monster(self):
        global surface, now_floor
        p = get_mouse_in_floor(pygame.mouse.get_pos())
        empty(surface, (610, 0, 190, 350))
        empty(surface, (5, 253, 180, 189))
        if p != -1:
            thing = self.data[p[0]][p[1]][0:4]
            if thing == "mons":
                mons = monster(database.get_monster(self.data[p[0]][p[1]]))
                show_warrior(mons)
            elif thing == "othe" or thing == "swor" or thing == "book" or thing == "shie" or thing == "staf" or thing == "cloa" or thing == "boot":
                arm = armor(database.get_armor(self.data[p[0]][p[1]]))
                show_description(arm)
                show_floor(now_floor)
            else:                
                show_floor(now_floor)
        else:
            show_floor(now_floor)
    def walk(self, _dir, _frame):
        global newbie, surface, police_defeated, police_served, _now_floor, ID, life_left, CHOICE
        old_posit = tuple(self.warrior_posit)
        self.warrior_posit[0] += walk_dir[_dir][0]
        self.warrior_posit[1] += walk_dir[_dir][1]
        newbie.face = _dir
        walkable = True
        upstairs = downstairs = False
        framerate = pygame.time.Clock()
        if self.warrior_posit[0] < 0 or self.warrior_posit[0] > 12 or self.warrior_posit[1] < 0 or self.warrior_posit[1] > 12:
            walkable = False
        elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:4] == "mons":
            if self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "29" and _now_floor < 16:
                # 是城管，触发plot
                if _now_floor != 8 or CHOICE == 3:
                    plot_end = plot.ChengGuan(surface, newbie.bag)
                    if plot_end[0]:
                        res = fight_wrap(newbie, monster(database.get_monster(self.data[self.warrior_posit[0]][self.warrior_posit[1]])))
                        with open('last_battle.log', "w") as f:
                            f.write(res[1])
                        if res[0] == "???":
                            # 被城管揍了，东西抢走，留一滴血
                            newbie.life = 1
                            if plot_end[1] == 3:
                                newbie.bag.money = 0
                            else:
                                newbie.bag.keys[plot_end[1]] = 0
                            plot.ChengGuan_end_1(surface)
                        else:
                            # 打赢了城管
                            police_defeated += 1
                            plot.ChengGuan_end_2(surface)
                    else:
                        # 乖乖地交了东西
                        police_served += 1
                else:
                    plot.floor8_1(surface)
                    sleep(1)
                    res = fight_wrap(newbie, monster(database.get_monster(self.data[self.warrior_posit[0]][self.warrior_posit[1]])))
                    with open('last_battle.log', "w") as f:
                            f.write(res[1])
                    if res[0] == "???":
                        # 败于城管
                        newbie.life = 1
                        if plot.floor8_fail_ask(surface, CHOICE):
                            # 回答正确
                            plot.floor8_answer_right(surface)
                            newbie.bag.gem += 1
                        else:
                            plot.floor8_answer_wrong(surface, CHOICE)
                            # 回答错误，死亡
                            walkable = False
                            life_left -= 1
                            update_life(ID, life_left)
                            to_exit = (life_left <= 0)
                            k = plot.death(surface, to_exit, life_left)
                            if k == 1:
                                surface.fill(Color('black'))
                                frame()
                                parse_doc(saving.load(ID))
                                go_stairs()
                            elif k == 2:
                                exit()
                    else:
                        plot.floor8_success(surface)
            else:
                res = fight_wrap(newbie, monster(database.get_monster(self.data[self.warrior_posit[0]][self.warrior_posit[1]])))
                with open('last_battle.log', "w") as f:
                    f.write(res[1])
                if res[0] == "???":
                    # 死了，触发plot
                    walkable = False
                    life_left -= 1
                    update_life(ID, life_left)
                    to_exit = (life_left <= 0)
                    k = plot.death(surface, to_exit, life_left)
                    if k == 1:
                        surface.fill(Color('black'))
                        frame()
                        parse_doc(saving.load(ID))
                        go_stairs()
                    elif k == 2:
                        exit()
        elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:4] == "empt" and _now_floor < 16:
            if random() < POLICE_PROB:
                self.data[self.warrior_posit[0]][self.warrior_posit[1]] = "mons-29"
                walkable = False
        elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:4] == "barr":
            walkable = False
        elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:4] == "lava":
            newbie.life = round(newbie.life * 0.8)      # 每一步踏上熔岩，生命值损失20%
        elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:4] == "door":
            if int(self.data[self.warrior_posit[0]][self.warrior_posit[1]][5]) < 3:
                if newbie.bag.keys[int(self.data[self.warrior_posit[0]][self.warrior_posit[1]][5])] > 0:
                    newbie.bag.keys[int(self.data[self.warrior_posit[0]][self.warrior_posit[1]][5])] -= 1
                else:
                    if newbie.bag.keys[3] > 0:
                        if hint_bomb(self) == -1:
                            walkable = False
                        else:
                            newbie.bag.keys[3] -= 1
                    else:
                        walkable = False
            else:
                # 花型门
                num = int(self.data[self.warrior_posit[0]][self.warrior_posit[1]][6:])
                # 06层选择职业的花型门
                if num < 7 and num > 2:
                    newbie.occupation = chr(num - 3 + ord('A'))
                walkable = plot.flower_gates[num](surface, self.data, CHOICE)
            if walkable:
                self.door_open(framerate)
        elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:4] == "stai":
            if self.data[self.warrior_posit[0]][self.warrior_posit[1]][7] == 'd':
                downstairs = True
            else:
                upstairs = True
        elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:4] == "item":
            if self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "black_gem":
                newbie.bag.gem += 1
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "bomb":
                newbie.bag.keys[3] += 1
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "money":
                newbie.bag.money += 50    # 暂定一个金块=50金
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "yellow_key":
                newbie.bag.keys[0] += 1
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "blue_key":
                newbie.bag.keys[1] += 1
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "red_key":
                newbie.bag.keys[2] += 1
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "key_box":
                newbie.bag.keys[0] += 1
                newbie.bag.keys[1] += 1
                newbie.bag.keys[2] += 1
        elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:4] == "food":
            if self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "red_gem":
                newbie.properties["p_attack"] += 2
                newbie.update_properties()
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "blue_gem":
                newbie.properties["p_defense"] += 2
                newbie.update_properties()
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "yellow_gem":
                newbie.properties["m_attack"] += 2
                newbie.update_properties()
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "green_gem":
                newbie.properties["m_defense"] += 2
                newbie.update_properties()
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "feather":
                newbie.upgrade()
                if self.warrior_posit == [1, 8]:
                    # 02层的羽毛，触发隐藏怪物
                    plot.hide_monster(surface, self.data)
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "small_blood":
                newbie.life += 100
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "big_blood":
                newbie.life += 250
            elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:] == "special_blood":
                newbie.life *= 2
        elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:3] == "npc":
            # TODO: 触发相应剧情或提示
            walkable = False
            plot.npcs[int(self.data[self.warrior_posit[0]][self.warrior_posit[1]][4:])](surface, self.data, old_posit)
        elif self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:4] == "hint":
            walkable = False
            plot.hints[int(self.data[self.warrior_posit[0]][self.warrior_posit[1]][5:])](surface, self.data)
        else:
            arm = armor(database.get_armor(self.data[self.warrior_posit[0]][self.warrior_posit[1]]))
            newbie.bag.armor.append(arm)
        # 播放动画
        play_animation(self.warrior_sprite, framerate)
        if walkable:
            # 更改新位
            if upstairs:
                _now_floor -= 1
            elif downstairs:
                _now_floor += 1
            else:
                if self.data[self.warrior_posit[0]][self.warrior_posit[1]][0:4] == "lava":
                    self.data[self.warrior_posit[0]][self.warrior_posit[1]] = "lava-warrior"
                else:
                    self.data[self.warrior_posit[0]][self.warrior_posit[1]] = "warrior"
                # 更改原位
                if self.data[old_posit[0]][old_posit[1]][0:4] == "lava":
                    self.data[old_posit[0]][old_posit[1]] = "lava"
                else:
                    self.data[old_posit[0]][old_posit[1]] = "empty"
        # TODO: 注意更新显示！
        self.reload(newbie)
        go_stairs()

def go_stairs(by_key = False):
    global now_floor, now_map, newbie, _now_floor
    if _now_floor == 6:
        now_floor = "06"
    else:
        now_floor = "{}{}".format(newbie.occupation, _now_floor)
    if by_key and not floors.floors[now_floor][13]:
        return False
    now_map = mymap(floors.floors[now_floor])
    now_map.reload(newbie)
    show_map(now_map)
    show_floor(now_floor)
    return True

def hint_bomb(_map):
    global surface
    empty(surface, (192, 293, 416, 140))
    pygame.draw.aaline(surface, Color("gold"), (192, 293), (608, 293))
    hint_txt_1 = text("没有钥匙了，使用炸弹炸开这扇门？按ENTER", 210, 303, font_20)
    hint_txt_2 = text("确认，鼠标点击任意位置取消", 210, 333, font_20)
    hint_txt_1.show(surface)
    hint_txt_2.show(surface)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                mousemove_show_armor(newbie)
            elif event.type == MOUSEBUTTONDOWN:
                show_map(now_map)
                return -1
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    show_map(now_map)
                    return 0

def Upgrade(_warrior):
    global surface
    empty(surface, (192, 293, 416, 140))
    pygame.draw.aaline(surface, Color("gold"), (192, 293), (608, 293))
    txts = []
    txts.append(text("1. 升一级 六大属性 +1 生命 +100", 210, 303, font_20))
    txts.append(text("2. 物理专修 物攻 +5 物防 +5", 210, 333, font_20))
    txts.append(text("3. 法术专修 法攻 +5 法防 +5", 210, 363, font_20))
    txts.append(text("4. 气血专修 精准 +2 敏捷 +2 生命 +250", 210, 393, font_20))
    for txt in txts:
        txt.show(surface)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                mousemove_show_armor(newbie)
            elif event.type == MOUSEBUTTONDOWN:
                return
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    _warrior.experience -= 100
                    _warrior.upgrade()
                    return
                elif event.key == K_2:
                    _warrior.experience -= 100
                    _warrior.p_upgrade()
                    return
                elif event.key == K_3:
                    _warrior.experience -= 100
                    _warrior.m_upgrade()
                    return
                elif event.key == K_4:
                    _warrior.experience -= 100
                    _warrior.l_upgrade()
                    return

def frame():
    global surface
    for i in range(0, 5):
        pygame.draw.rect(surface, Color('white'), (5 + 37 * i, 181, 32, 32), 2)
    detach_txt = text("装备选中点此", 15, 223, font_20)
    detach_txt.show(surface)
    detach_txt_2 = text("拆卸", 135, 223, font_20, Color("blue"))
    detach_txt_2.show(surface)
    pygame.draw.rect(surface, Color('gold'), (190, 15, 420, 420), 2)
    pygame.draw.rect(surface, Color('white'), (5, 253, 180, 189), 2)        # 装备描述
    # pygame.draw.rect(surface, Color('white'), (615, 213, 180, 135), 2)    # 怪物描述
    show_battle_txt = text("查看上一次战斗过程", 615, 356, font_20, Color("blue"))
    show_battle_txt.show(surface)
    key_txt = []
    key_txt.append(text("S 存档  R 读档", 649, 384, font_16, Color("gold")))
    key_txt.append(text("P 商店与背包 U 升级", 629, 404, font_16, Color("gold")))
    key_txt.append(text("PgUp 上楼 PgDn 下楼", 629, 424, font_16, Color("gold")))
    for txt in key_txt:
        txt.show(surface)
    pygame.display.update()

def show_description(_thing, is_armor = True):
    global surface
    if not is_armor:
        pygame.draw.rect(surface, Color('white'), (615, 213, 180, 135), 2)
    for i in range(0, len(_thing.description)):
        color = Color("white")
        if i == 0:
            color = Color("gold")
        txt = text(_thing.description[i], 615, 213 + i * 27, font_20, color)
        if is_armor:
            txt = text(_thing.description[i], 5, 253 + i * 27, font_20, color)
        txt.show(surface)
    pygame.display.update()

def check_mouse_pos(_pos, _bag):
    global IS_SHOPPING
    if IS_SHOPPING:
        for i in range(0, len(_bag.armor)):
            if Rect(210 + 50 * (i % 8), 85 + 50 * (i // 8), 32, 32).collidepoint(_pos):
                return (1, i)    # (IN_SHOP, num)
        if Rect(510, 327, 80, 20).collidepoint(_pos):
            return (3, 0)       # 使用黑石
        if Rect(510, 352, 80, 20).collidepoint(_pos):
            return (4, 0)       # 购买物品
        if Rect(510, 377, 80, 20).collidepoint(_pos):
            return (5, 0)       # 佩戴装备
        if Rect(510, 402, 80, 20).collidepoint(_pos):
            return (6, 0)       # 出售装备
    for i in range(0, 5):
        if Rect(5 + 37 * i, 181, 32, 32).collidepoint(_pos):
            return (2, i)       # (IN_ARMOR, num)
    if Rect(135, 227, 40, 20).collidepoint(_pos):
        return (7, 0)           # 拆卸
    if Rect(615, 356, 180, 20).collidepoint(_pos):   # 查看上一次战斗过程
        return (8, 0)
    return (0, -1)

def clear_clicked(_warrior):
    global surface, IS_SHOPPING
    for i in range(0, 5):
        if _warrior.armor[i] is not None and _warrior.armor[i].clicked:
            _warrior.armor[i].clicked = False
            pygame.draw.rect(surface, Color('white'), (5 + 37 * i, 181, 32, 32), 2)
    if IS_SHOPPING:
        for i in range(0, len(_warrior.bag.armor)):
            if _warrior.bag.armor[i].clicked:
                _warrior.bag.armor[i].clicked = False
                pygame.draw.rect(surface, Color('white'), (210 + 50 * (i % 8), 85 + 50 * (i // 8), 32, 32), 2)

def use_black_gem(_warrior, _time):
    global newbie, POLICE_PROB, police_defeated, CHOICE, police_served, surface, _now_floor
    colors = ('红', '蓝', '黄', '绿')
    empty(surface, (208, 293, 385, 25))      # 清除提示语
    hint_txt = text("请键入需要转为{}宝石的个数（1金币/个）".format(colors[_time]), 210, 295, font_20)
    hint_txt.show(surface)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                mousemove_show_armor(newbie)
            elif event.type == QUIT:
                doc = saving.document(newbie, _now_floor, floors.floors, POLICE_PROB, police_defeated, CHOICE, police_served)
                doc.save(_id)
                exit()
            elif event.type == KEYDOWN:
                num = event.key - K_0
                if num >= 0 and num < 10:
                    if num <= _warrior.bag.gem and num <= _warrior.bag.money:
                        _warrior.use_gem(_time, num)
                        show_shop(_warrior)
                        show_warrior(_warrior)
                    else:
                        empty(surface, (208, 293, 385, 25))      # 清除提示语
                        hint_txt = text("黑宝石或金币不足！", 210, 295, font_20)
                        hint_txt.show(surface)
                        pygame.display.update()
                        sleep(1)
                    return 0
            elif event.type == MOUSEBUTTONDOWN:
                return -1

def buy(_warrior, _time):
    global newbie, POLICE_PROB, police_defeated, CHOICE, police_served, surface, _now_floor
    things = ("炸弹", "红宝石", "蓝宝石", "黄宝石", "绿宝石", "小血瓶")
    prices = (50, 10, 10, 10, 10, 10)
    empty(surface, (208, 293, 385, 25))      # 清除提示语
    hint_txt = text("请键入需要购买{0}的个数（{1}金币/个）".format(things[_time], prices[_time]), 210, 295, font_20)
    hint_txt.show(surface)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                mousemove_show_armor(newbie)
            elif event.type == QUIT:
                doc = saving.document(newbie, _now_floor, floors.floors, POLICE_PROB, police_defeated, CHOICE, police_served)
                doc.save(_id)
                exit()
            elif event.type == KEYDOWN:
                num = event.key - K_0
                if num >= 0 and num < 10:
                    if num * prices[_time] <= _warrior.bag.money:
                        if _time == 0:
                            _warrior.buy_bomb(num)
                            show_shop(_warrior)
                        elif _time == 5:
                            _warrior.buy_blood(num)
                            show_shop(_warrior)
                            show_warrior(_warrior)
                        else:
                            _warrior.buy_gem(_time - 1, num)
                            show_shop(_warrior)
                            show_warrior(_warrior)
                    else:
                        empty(surface, (208, 293, 385, 25))      # 清除提示语
                        hint_txt = text("金币不足！", 210, 295, font_20)
                        hint_txt.show(surface)
                        pygame.display.update()
                        sleep(1)
                    return 0
            elif event.type == MOUSEBUTTONDOWN:
                return -1

def mousemove_show_armor(_warrior):
    global surface
    p = check_mouse_pos(pygame.mouse.get_pos(), newbie.bag)
    if p[0] == 1:
        empty(surface, (5, 253, 180, 189))
        if newbie.bag.armor[p[1]] is not None:
            show_description(newbie.bag.armor[p[1]])
    elif p[0] == 2:
        empty(surface, (5, 253, 180, 189))
        if newbie.armor[p[1]] is not None:
            show_description(newbie.armor[p[1]])

def get_mouse_in_floor(_pos):
    global IS_SHOPPING
    if not IS_SHOPPING and Rect(192, 17, 416, 416).collidepoint(_pos):
        return ((_pos[1] - 17) // 32, (_pos[0] - 192) // 32)
    else:
        return -1

def main(_id, is_origin):
    global surface, IS_SHOPPING, newbie, FRAME, POLICE_PROB, police_defeated, now_map, CHOICE, ID, police_served, _now_floor
    ID = _id
    surface.fill(Color('black'))
    frame()
    go_stairs()
    show_warrior(newbie)
    if is_origin:
        plot.starter(surface)
        show_map(now_map)
    framerate = pygame.time.Clock()
    while True:
        framerate.tick(FRAME)
        ticks = pygame.time.get_ticks()
        if not IS_SHOPPING:
            now_map.active_container.update(ticks, pic_dic["empty"], FRAME)
            now_map.active_container.draw(surface)
        for event in pygame.event.get():
            if event.type == QUIT:
                if newbie.life > 0:
                    doc = saving.document(newbie, _now_floor, floors.floors, POLICE_PROB, police_defeated, CHOICE, police_served)
                    doc.save(_id)
                exit()
            elif event.type == MOUSEMOTION:
                # 显示装备信息/怪物信息
                now_map.mousemove_show_monster()
                mousemove_show_armor(newbie)
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # 注意点到”出售装备“”佩戴装备“时，不能将clicked清除！
                if IS_SHOPPING:
                    empty(surface, (208, 293, 385, 25))      # 清除提示语
                p = check_mouse_pos(mouse_pos, newbie.bag)
                if p[0] == 7:       # 拆卸
                    drop_armor(newbie)
                    clear_clicked(newbie)
                elif p[0] == 5:       # 佩戴装备
                    for i in range(0, len(newbie.bag.armor)):
                        if newbie.bag.armor[i].clicked:
                            if newbie.armor[newbie.bag.armor[i].kind] is not None:
                                newbie.armor[newbie.bag.armor[i].kind].clicked = True
                                drop_armor(newbie)
                            newbie.bag.armor[i].clicked = False
                            newbie.armor_wear(newbie.bag.armor[i])
                            del newbie.bag.armor[i]
                            show_warrior(newbie)
                            show_shop(newbie)
                            break
                    else:
                        hint_txt = text("请先在背包中选中装备！", 210, 295, font_20)
                        hint_txt.show(surface)
                elif p[0] == 6:     # 出售装备
                    sell_armor(newbie)
                    empty(surface, (208, 293, 385, 25))      # 清除提示语
                elif p[0] == 3:     # 使用黑石
                    for i in range(0, 4):
                        if use_black_gem(newbie, i) < 0:
                            empty(surface, (208, 293, 385, 25))      # 清除提示语
                            break
                elif p[0] == 4:     # 购买物品
                    for i in range(0, 6):
                        if buy(newbie, i) < 0:
                            empty(surface, (208, 293, 385, 25))      # 清除提示语
                            break
                elif p[0] == 1:     # 选中包里的装备
                    clear_clicked(newbie)
                    if newbie.bag.armor[p[1]] is not None:
                        newbie.bag.armor[p[1]].clicked = True
                        pygame.draw.rect(surface, Color('gold'), (210 + 50 * (p[1] % 8), 85 + 50 * (p[1] // 8), 32, 32), 2)
                elif p[0] == 2:     # 选中穿上的装备
                    clear_clicked(newbie)
                    if newbie.armor[p[1]] is not None:
                        newbie.armor[p[1]].clicked = True
                        pygame.draw.rect(surface, Color('gold'), (5 + 37 * p[1], 181, 32, 32), 2)
                elif p[0] == 8:     # 查看上一次战斗记录
                    startfile('last_battle.log')
                else:               # 按了其他地方
                    clear_clicked(newbie)
                pygame.display.update()
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    if IS_SHOPPING:
                        empty(surface, (190, 15, 420, 420))
                        IS_SHOPPING = False
                        show_map(now_map)
                    else:
                        show_shop(newbie)
                        IS_SHOPPING = True
                elif event.key == K_s:
                    if newbie.life > 0:
                        doc = saving.document(newbie, _now_floor, floors.floors, POLICE_PROB, police_defeated, CHOICE, police_served)
                        doc.save(_id)
                        plot.save_success(surface)
                        show_map(now_map)
                elif event.key == K_r:
                    surface.fill(Color('black'))
                    frame()
                    parse_doc(saving.load(_id))
                    go_stairs()
                elif not IS_SHOPPING:
                    if event.key == K_LEFT:
                        now_map.walk(1, FRAME)
                    elif event.key == K_RIGHT:
                        now_map.walk(2, FRAME)
                    elif event.key == K_UP:
                        now_map.walk(3, FRAME)
                    elif event.key == K_DOWN:
                        now_map.walk(0, FRAME)
                    elif event.key == K_u and newbie.experience >= 100:
                        Upgrade(newbie)
                        show_map(now_map)
                    elif event.key == K_PAGEUP:
                        if _now_floor > 0 and _now_floor != 6 and _now_floor < 16:
                            _now_floor -= 1
                            if not go_stairs(True):
                                _now_floor += 1
                                now_floor = "{}{}".format(newbie.occupation, _now_floor)
                    elif event.key == K_PAGEDOWN:
                        if _now_floor < 18:
                            _now_floor += 1
                            if not go_stairs(True):
                                _now_floor -= 1
                                now_floor = "{}{}".format(newbie.occupation, _now_floor)
                show_warrior(newbie)
        pygame.display.update()

def parse_doc(_doc):
    global newbie, POLICE_PROB, police_defeated, CHOICE, police_served, _now_floor, life_left, ID
    newbie = _doc.warrior
    _now_floor = _doc.now_floor
    floors.floors = _doc.floors
    POLICE_PROB = _doc.POLICE_PROB
    police_defeated = _doc.police_defeated
    police_served = _doc.police_served
    CHOICE = _doc.choice
    if ID != 'origin':
        life_left = get_life(ID)

if __name__ == '__main__':
    main('origin', True)
