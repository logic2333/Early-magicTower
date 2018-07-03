#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame, database, inputbox, saving, internal, database
from pygame.locals import *
from hello import *
from res import *


def check_mouse(_pos):
    for i in range(0, 3):
        if Rect(312, 174 + 92 * i, 176, 32).collidepoint(_pos):
            return i
    return -1

def check_mouse_ask(_pos):
    for i in range(0, 4):
        if Rect(208, 130 + 79 * i, 336, 32).collidepoint(_pos):
            return i
    return -1

def show_entrance(_surface):
    txts = []
    txts.append(text("魔  塔", 200, 60, font_title))
    txts.append(text("By Logic, Ver. 1.0", 400, 90, font_title_small))
    txts.append(text("新 建 玩 家", 312, 174, font_32, Color("blue")))
    txts.append(text("玩 家 登 录", 312, 266, font_32, Color("blue")))
    txts.append(text("退 出 游 戏", 312, 358, font_32, Color("blue")))
    for txt in txts:
        txt.show(_surface)
    pygame.display.update()

def start_ask(_surface):
    empty(_surface, (0, 0, 800, 450))
    txts = []
    txts.append(text("你希望出身于怎样的家庭？", 208, 51, font_32, Color('gold')))
    txts.append(text("A. 达官显贵，权倾朝野", 208, 130, font_32, Color('blue')))
    txts.append(text("B. 巨商大贾，富甲一方", 208, 209, font_32, Color('blue')))
    txts.append(text("C. 知识分子，书香门第", 208, 288, font_32, Color('blue')))
    txts.append(text("D. 平头百姓，忠厚老实", 208, 367, font_32, Color('blue')))
    for txt in txts:
        txt.show(_surface)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEMOTION:
                p = check_mouse_ask(pygame.mouse.get_pos())
                if p != -1:
                    pygame.draw.rect(_surface, Color('white'), (208, 130 + 79 * p, 336, 32), 2)
                else:
                    for i in range(0, 4):
                        pygame.draw.rect(_surface, Color('black'), (208, 130 + 79 * i, 336, 32), 2)
                pygame.display.update()
            elif event.type == MOUSEBUTTONDOWN:
                p = check_mouse_ask(pygame.mouse.get_pos())
                if p != -1:
                    return p

def Entrance(_surface):
    # 得到存档。修改后的初始存档或读取的存档
    # 存档包括：warrior, floors, now_floor, POLICE_PROB
    show_entrance(_surface)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                doc = saving.document(newbie, _now_floor, floors, POLICE_PROB, police_defeated)
                doc.save(_id)
                exit()
            elif event.type == MOUSEMOTION:
                p = check_mouse(pygame.mouse.get_pos())
                if p != -1:
                    pygame.draw.rect(_surface, Color('white'), (312, 174 + 92 * p, 176, 32), 2)
                else:
                    for i in range(0, 3):
                        pygame.draw.rect(_surface, Color('black'), (312, 174 + 92 * i, 176, 32), 2)
                pygame.display.update()
            elif event.type == MOUSEBUTTONDOWN:
                p = check_mouse(pygame.mouse.get_pos())
                if p == 0:
                    # 注册账号
                    empty(_surface, (0, 170, 800, 280))
                    name_txt = text("猛士，尊姓大名？按回车确认", 192, 202, font_32, Color('gold'))
                    name_txt.show(_surface)
                    username = inputbox.ask(_surface, (192, 326, 416, 32), False)
                    while username == '':
                        empty(_surface, (0, 170, 800, 280))
                        hint_txt = text("猛士当青史留名，不可做无名英雄也。", 128, 202, font_32, Color('gold'))
                        hint_txt.show(_surface)
                        username = inputbox.ask(_surface, (192, 326, 416, 32), False)
                    while username == 'origin' or username == 'Logic':
                        empty(_surface, (0, 170, 800, 280))
                        hint_txt = text("此名不可用。", 304, 202, font_32, Color('gold'))
                        hint_txt.show(_surface)
                        username = inputbox.ask(_surface, (192, 326, 416, 32), False)
                    while database.get_user(username) is not None:                        
                        empty(_surface, (0, 170, 800, 280))
                        hint_txt = text("猛士岂可寄他人名下？此名已存在，请重新输入", 64, 202, font_32, Color('gold'))
                        hint_txt.show(_surface)
                        username = inputbox.ask(_surface, (192, 326, 416, 32), False)
                    empty(_surface, (0, 170, 800, 280))
                    pswd_txt = text("您的神圣存档不容他人侵犯。请设定密码", 112, 202, font_32, Color('gold'))
                    pswd_txt.show(_surface)
                    password = inputbox.ask(_surface, (192, 326, 416, 32), True)
                    while password == '':
                        empty(_surface, (0, 170, 800, 280))
                        hint_txt = text("总有一些地方是不能随便给别人看的。", 128, 202, font_32, Color('gold'))
                        hint_txt.show(_surface)
                        password = inputbox.ask(_surface, (192, 326, 416, 32), True)
                    empty(_surface, (0, 170, 800, 280))
                    pswd_confirm_txt = text("请再次输入以确认密码", 240, 202, font_32, Color('gold'))
                    pswd_confirm_txt.show(_surface)
                    password_confirm = inputbox.ask(_surface, (192, 326, 416, 32), True)
                    while password_confirm != password:
                        empty(_surface, (0, 170, 800, 280))
                        hint_txt = text("如此大意可是要被小怪兽吃掉的哦。重新确认密码", 48, 202, font_32, Color('gold'))
                        hint_txt.show(_surface)
                        password_confirm = inputbox.ask(_surface, (192, 326, 416, 32), True)
                    database.register(username, password)
                    load_game(_surface, username, True)
                elif p == 1:
                    # 登录账号
                    empty(_surface, (0, 170, 800, 280))
                    name_txt = text("猛士，告诉我您的大名，按回车确认", 144, 202, font_32, Color('gold'))
                    name_txt.show(_surface)
                    username = inputbox.ask(_surface, (192, 326, 416, 32), False)
                    user = database.get_user(username)
                    while user is None:                        
                        empty(_surface, (0, 170, 800, 280))
                        hint_txt = text("查无此人，请重新输入", 240, 202, font_32, Color('gold'))
                        hint_txt.show(_surface)
                        username = inputbox.ask(_surface, (192, 326, 416, 32), False)
                        user = database.get_user(username)
                    empty(_surface, (0, 170, 800, 280))
                    pswd_txt = text("密码是？", 336, 202, font_32, Color('gold'))
                    pswd_txt.show(_surface)
                    password = inputbox.ask(_surface, (192, 326, 416, 32), True)
                    while password != user[1]:
                        empty(_surface, (0, 170, 800, 280))
                        hint_txt = text("密码错误，请重新输入", 240, 202, font_32, Color('gold'))
                        hint_txt.show(_surface)
                        password = inputbox.ask(_surface, (192, 326, 416, 32), True)
                    empty(_surface, (0, 170, 800, 280))
                    if user[4] != 0:
                        resume_txt = text("继续上次游戏", 304, 202, font_32, Color('blue'))
                        resume_txt.show(_surface)
                    else:
                        resume_txt = text("您的复活次数已用完。", 240, 202, font_32, Color('white'))
                        resume_txt.show(_surface)
                    restart_txt = text("从头来过", 336, 326, font_32, Color('blue'))
                    restart_txt.show(_surface)
                    pygame.display.update()
                    doc = None
                    while True:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                exit()
                            elif event.type == MOUSEMOTION:
                                mouse_pos = pygame.mouse.get_pos()
                                if Rect(304, 202, 192, 32).collidepoint(mouse_pos) and user[4] != 0:
                                    pygame.draw.rect(_surface, Color('white'), (304, 202, 192, 32), 2)
                                elif Rect(336, 326, 128, 32).collidepoint(mouse_pos):
                                    pygame.draw.rect(_surface, Color('white'), (336, 326, 128, 32), 2)
                                else:
                                    pygame.draw.rect(_surface, Color('black'), (304, 202, 192, 32), 2)
                                    pygame.draw.rect(_surface, Color('black'), (336, 326, 128, 32), 2)
                            elif event.type == MOUSEBUTTONDOWN:
                                mouse_pos = pygame.mouse.get_pos()
                                if Rect(304, 202, 192, 32).collidepoint(mouse_pos) and user[4] != 0:
                                    load_game(_surface, username, False)
                                elif Rect(336, 326, 128, 32).collidepoint(mouse_pos):
                                    database.reset_life(username)
                                    database.commit()
                                    load_game(_surface, username, True)
                            pygame.display.update()
                elif p == 2:
                    exit()

def load_game(_surface, _username, is_origin):
    doc = None
    if is_origin:
        doc = saving.load('origin')
        # 进入开篇剧情，提问出身
        choice = start_ask(_surface)
        if choice == 0:
            doc.warrior.bag.armor.append(internal.armor(database.get_armor('sword-4')))     # 达官显贵
        elif choice == 1:
            doc.warrior.bag.money += 100                                                    # 巨商大贾
            doc.warrior.bag.armor.append(internal.armor(database.get_armor('book-4')))
        elif choice == 2:
            doc.warrior.bag.armor.append(internal.armor(database.get_armor('book-1')))      # 知识分子
        elif choice == 3:
            doc.POLICE_PROB = 0.001                                                         # 平头百姓
        doc.choice = choice
        doc.save(_username)
    else:
        doc = saving.load(_username)
    import ui
    ui.ID = _username
    ui.parse_doc(doc)
    database.commit()
    ui.main(_username, is_origin)

def main():
    pygame.init()
    surface = pygame.display.set_mode((800, 450), SRCALPHA)
    Entrance(surface)

if __name__ == '__main__':
    main()
