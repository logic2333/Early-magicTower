#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from hello import *
from res import *
from random import randint
from os import startfile
from time import sleep

def flower_gate_0(_surface = None, _mapdata = None, _choice = None):
    # TODO: 0层出口的花型门，击败魔王后自动打开
    return False

def flower_gate_1(_surface, _mapdata, _choice):
    # 塔入口的花型门
    for i in range(5, 8):
        for j in range(5, 8):
            if _mapdata[i][j][0:4] == "mons":
                return False
    speak(_surface, ("传言道人死后要历经十八层炼狱方得新生。", ), "神秘的声音")
    if _choice == 0:
        speak(_surface, ("你曾是达官显贵，掌握生杀予夺之大权；可", "却暴戾无道，治下生灵涂炭，哀鸿遍野，手", "下的无数冤魂，可会轻易放过你？"), "神秘的声音")
    elif _choice == 1:
        speak(_surface, ("你曾是巨商大贾，纵横商海半生，春风得意", "，享尽荣华富贵。事业上的成功却挖走了你", "的仁义之心，你屈服于强权，和奸商勾结，", "为他们牟取不义之财，可曾想过多少人为之"), "神秘的声音")
        speak(_surface, ("付出了生命的代价。人血馒头好吃吗？", ), "神秘的声音")
    elif _choice == 2:
        speak(_surface, ("你曾是一名优秀的科研工作者，硕果累累，", "著作等身，本可誉满天下，却因为手下一个", "小“砖工”的自杀事件陷入了万劫不复的深", "渊。扪心自问一下，你在他的人生中扮演了"), "神秘的声音")
        speak(_surface, ("怎样的角色？严师，慈父还是刽子手？",), "神秘的声音")
    else:
        speak(_surface, ("你可能是误入了这里。不过，既来之，则安", "之，希望我们的密室能带给您难忘的体验！", "满意的话记得给五星好评哦~"), "神秘的声音")
    speak(_surface, ("希望你能活着出来。",), "神秘的声音")
    return True

def flower_gate_2(_surface, _mapdata, _choice = None):
    # 02层的花型门，隐藏怪物
    if _mapdata[1][8][0:4] != "food" and _mapdata[2][9][0:4] != "mons" and _mapdata[3][9][0:4] != "mons":
        return True
    return False

def flower_gate_3(_surface, _mapdata, _choice = None):
    # 06层，职业选择：左青龙
    _mapdata[6][9] = "barr-sky"
    _mapdata[3][6] = "barr-sky"
    _mapdata[9][6] = "barr-sky"
    return True

def flower_gate_4(_surface, _mapdata, _choice = None):
    # 06层，职业选择：右白虎
    _mapdata[6][3] = "barr-sky"
    _mapdata[3][6] = "barr-sky"
    _mapdata[9][6] = "barr-sky"
    return True

def flower_gate_5(_surface, _mapdata, _choice = None):
    # 06层，职业选择：前朱雀
    _mapdata[6][9] = "barr-sky"
    _mapdata[6][3] = "barr-sky"
    _mapdata[9][6] = "barr-sky"
    return True

def flower_gate_6(_surface, _mapdata, _choice = None):
    # 06层，职业选择：后玄武
    _mapdata[6][9] = "barr-sky"
    _mapdata[3][6] = "barr-sky"
    _mapdata[6][3] = "barr-sky"
    return True

flower_gates = []
flower_gates.append(flower_gate_0)
flower_gates.append(flower_gate_1)
flower_gates.append(flower_gate_2)
flower_gates.append(flower_gate_3)
flower_gates.append(flower_gate_4)
flower_gates.append(flower_gate_5)
flower_gates.append(flower_gate_6)

def hide_monster(_surface, _mapdata):
    _mapdata[2][9] = "mons-2"
    _mapdata[3][9] = "mons-8"
    _mapdata[3][5] = "barr-sky"
    speak(_surface, ("哈哈，来个瓮中捉鳖！",), " 怪    物 ")

def hint_0(_surface, _mapdata):
    speak(_surface, ("此地氛围诡异……", ), " 提   示 ")

def hint_1(_surface, _mapdata = None):
    speak(_surface, ("这个老人会随机将你传送至神秘法阵的某一", "侧。找他之前，想清楚可能的后果。"), " 提   示 ")

def hint_2(_surface, _mapdata = None):
    speak(_surface, ("骷髅是一种群居生物，它们很喜欢开party", "╮(~▽~)╭它们会热烈欢迎你的参加←_←"), " 提    示 ")

def hint_3(_surface, _mapdata = None):
    speak(_surface, ("左青龙，右白虎，前朱雀，后玄武……", "神奇的阵法……"), " 提    示 ")

def hint_4(_surface, _mapdata = None):
    speak(_surface, ("风萧萧兮易水寒……", "真正的试炼还未开始……"), " 提    示 ")

def npc_0(_surface, _mapdata, _warrior_posit):
    speak(_surface, ("嘛咪嘛咪轰~", ), " 神秘老人 ")
    k = randint(0, 2)
    posits = ([1, 10], [3, 8], [3, 10])
    _mapdata[_warrior_posit[0]][_warrior_posit[1]] = "empty"
    _mapdata[posits[k][0]][posits[k][1]] = "warrior"
    
hints = []
hints.append(hint_0)
hints.append(hint_1)
hints.append(hint_2)
hints.append(hint_3)
hints.append(hint_4)

npcs = []
npcs.append(npc_0)

def ChengGuan(_surface, _bag):
    speak(_surface, ("我是塔管大队的，我们队长想请你陪他喝喝", "茶，你想去吗←_←"), " 塔管队员 ")
    speak(_surface, ("(用键盘数字键选择)", "1. 额，小的不敢……", "2. 好啊，那我就不客气啦"), " 猛    士 ", True)
    res_1 = 0
    while True:
        if res_1 != 0:
            break
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_1:
                    res_1 = 1
                    break
                elif event.key == K_2:
                    res_1 = 2
                    break
    if res_1 == 1:
        serve = randint(0, 3)
        serve_txt = ("3把黄钥匙", "2把蓝钥匙", "1把红钥匙", "60个金币")
        speak(_surface, ("什么？不去？竟然敢不给大队长面子！那你", "总得给我点面子吧！交出{}，就放你".format(serve_txt[serve]), "一马！"), " 塔管队员 ")
        res_2 = 0
        if serve < 3:
            speak(_surface, ("(我有{0}{1})".format(_bag.keys[serve], serve_txt[serve][1:]), "1. 来，给你！", "2. 小的，小的……没有啊"), " 猛    士 ", True)
        else:
            speak(_surface, ("(我有{0}个金币)".format(_bag.money), "1. 来，给你！", "2. 小的，小的……没有啊"), " 猛    士 ", True)
        while True:
            if res_2 != 0:
                break
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_1:
                        res_2 = 1
                        break
                    elif event.key == K_2:
                        res_2 = 2
                        break
        beat = False
        if serve < 3:
            if _bag.keys[serve] < int(serve_txt[serve][0]):
                if res_2 == 1:
                    # 没有也说给，扁一顿
                    speak(_surface, ("嘿你这小鬼，敢耍老子？看来是欠教训了。", ), " 塔管队员 ")
                    beat = True
                else:
                    # 没有，不给，暂且饶过
                    speak(_surface, ("穷光蛋，赶紧给老子滚！瞧你以前那么牛气", "哄哄的呢？"), " 塔管队员 ")           
            else:
                if res_2 == 1:
                    # 有，给了，乖
                    speak(_surface, ("嗯，真乖。这块黑石头算大人赏你的，拿回", "家慢慢玩哦"), " 塔管队员 ")
                    _bag.keys[serve] -= int(serve_txt[serve][0])
                    _bag.gem += 1
                else:
                    # 有，不给，不听话，扁一顿
                    speak(_surface, ("既然你这么不给本大人面子，就休怪本大人", "不客气了。"), " 塔管队员 ")
                    beat = True
        else:
            if _bag.money < 60:
                if res_2 == 1:
                    # 没有也说给，扁一顿
                    speak(_surface, ("嘿你这小鬼，敢耍老子？看来是欠教训了。", ), " 塔管队员 ")
                    beat = True
                else:
                    # 没有，不给，暂且饶过
                    speak(_surface, ("穷光蛋，赶紧给老子滚！瞧你以前那么牛气", "哄哄的呢？"), " 塔管队员 ")           
            else:
                if res_2 == 1:
                    # 有，给了，乖
                    speak(_surface, ("嗯，真乖。这块黑石头算大人赏你的，拿回", "家慢慢玩哦"), " 塔管队员 ")
                    _bag.keys[serve] -= int(serve_txt[serve][0])
                    _bag.gem += 1
                else:
                    # 有，不给，不听话，扁一顿
                    speak(_surface, ("既然你这么不给本大人面子，就休怪本大人", "不客气了。"), " 塔管队员 ")
                    beat = True
        return (beat, serve)

def ChengGuan_end_1(_surface):
    speak(_surface, ("哼，东西给你拿走了，好让你小子长点记性", "，下次见到本大人该怎么做，知道了吗？"), " 塔管队员 ")

def ChengGuan_end_2(_surface):
    speak(_surface, ("可怕可怕，后生可畏啊！我得赶紧向塔总汇", "报去……"), " 塔管队员 ")

def floor8_1(_surface):
    speak(_surface, ("咱们又见面了。我倒要来好好看看你小子修", "炼得怎样了。扒开你那禽兽般的衣冠，看清", "你的罪孽。"), " 塔管队员 ")

def floor8_success(_surface):
    speak(_surface, ("强悍如斯，后生可畏。希望你经过本塔的洗", "练，能够摒除罪恶，涅槃重生。"), " 塔管队员 ")

def floor8_fail_ask(_surface, _choice):
    if _choice == 0:
        speak(_surface, ("兴，百姓__；亡，百姓__。", "1. 兴，兴  2. 兴，苦", "3. 苦，兴  4. 苦，苦"), " 塔管队员 ", True)        
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEMOTION:
                    mousemove_show_armor(newbie)
                elif event.type == KEYDOWN:
                    if event.key == K_1 or event.key == K_2 or event.key == K_3:
                        return False
                    elif event.key == K_4:
                        return True
    elif _choice == 1:
        speak(_surface, ("君子爱财，________。", "1. 取之无尽  2. 失之吾命", "3. 取之有道  4. 得之吾幸"), " 塔管队员 ", True)        
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEMOTION:
                    mousemove_show_armor(newbie)
                elif event.type == KEYDOWN:
                    if event.key == K_1 or event.key == K_2 or event.key == K_4:
                        return False
                    elif event.key == K_3:
                        return True
    elif _choice == 2:
        speak(_surface, ("大声说出那六个字：", "1. 爸我永远爱您  2. 请你立即去世", "3. 表示无可奉告  4. 给我带份外卖"), " 塔管队员 ", True)        
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEMOTION:
                    mousemove_show_armor(newbie)
                elif event.type == KEYDOWN:
                    if event.key == K_2 or event.key == K_3 or event.key == K_4:
                        return False
                    elif event.key == K_1:
                        return True

def floor8_answer_right(_surface):
    speak(_surface, ("嗯，这块黑石头赏给你，在认识自己错误的", "道路上你又前进了一步。希望你经过本塔的", "洗练，能够摒除罪孽，涅槃重生。"), " 塔管队员 ")

def floor8_answer_wrong(_surface, _choice):
    if _choice == 0:
        speak(_surface, ("吾之一炬，可怜焦土！"), " 塔管队员 ")
    elif _choice == 1:
        speak(_surface, ("就送你去你推荐给别人的那几家医院吧，看", "看他们能不能治好你。哦对要是治愈出院了", "记得去豫章书院补一补国学~"), " 塔管队员 ")
    elif _choice == 2:
        speak(_surface, ("知识越多越反动，只愿这不是真的。"), " 塔管队员 ")
    
def starter(_surface):
    speak(_surface, ("这是哪儿？我怎么会在这里？这都是什么东", "西……好可怕~~~"), " 猛    士 ")

def death(_surface, _exit, _life_left):
    _surface.fill(Color('red'))
    pygame.display.update()
    sleep(0.1)
    empty(_surface, (0, 0, 800, 450))
    pygame.display.update()
    sleep(0.9)
    txts = []
    txts.append(text("真 敢 敢", 118, 17, font_death))
    txts.append(text("的 于 于", 118, 65, font_death))
    txts.append(text("猛 直 正", 118, 113, font_death))
    txts.append(text("士 面 视", 118, 161, font_death))
    txts.append(text(" 惨 淋", 150, 209, font_death))
    txts.append(text(" 淡 漓", 150, 257, font_death))
    txts.append(text(" 的 的", 150, 305, font_death))
    txts.append(text(" 人 鲜", 150, 353, font_death))
    txts.append(text(" 生 血", 150, 401, font_death))
    txts.append(text("看看我是怎么死的", 396, 100, font_32, Color('blue')))
    if not _exit:
        txts.append(text("读取上一次保存的存档", 364, 209, font_32, Color('blue')))
    txts.append(text("退出游戏", 460, 318, font_32, Color('blue')))
    txts.append(text("剩余复活次数：{}".format(_life_left), 640, 430, font_title_small))
    for txt in txts:
        txt.show(_surface)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == MOUSEMOTION:
                p = check_mouse_death(pygame.mouse.get_pos())
                if p == 0:
                    pygame.draw.rect(_surface, Color('white'), (396, 100, 256, 32), 2)
                elif p == 1 and not _exit:
                    pygame.draw.rect(_surface, Color('white'), (364, 209, 320, 32), 2)
                elif p == 2:
                    pygame.draw.rect(_surface, Color('white'), (460, 318, 128, 32), 2)
                else:
                    pygame.draw.rect(_surface, Color('black'), (396, 100, 256, 32), 2)
                    pygame.draw.rect(_surface, Color('black'), (364, 209, 320, 32), 2)
                    pygame.draw.rect(_surface, Color('black'), (460, 318, 128, 32), 2)
                pygame.display.update()
            elif event.type == MOUSEBUTTONDOWN:
                p = check_mouse_death(pygame.mouse.get_pos())
                if p == 0:
                    startfile('last_battle.log')
                elif p == -1:
                    pass
                elif p == 1 and _exit:
                    pass
                else:
                    return p
            

def speak(_surface, words, speaker, is_choice = False):
    empty(_surface, (190, 290, 420, 140))
    empty(_surface, (192, 253, 140, 40))
    pygame.draw.aaline(_surface, Color("gold"), (192, 293), (608, 293))
    pygame.draw.rect(_surface, Color("gold"), (192, 253, 140, 40), 2)
    speaker_txt = text(speaker, 212, 263, font_20, Color('gold'))
    speaker_txt.show(_surface)
    color = Color('white')
    if is_choice:
        color = Color('blue')
    for i in range(0, len(words)):
        txt = text(words[i], 210, 303 + 30 * i, font_20, color)
        txt.show(_surface)
    pygame.display.update()
    if not is_choice:
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        return

def save_success(_surface):
    speak(_surface, ("保存成功！", ), "")

def check_mouse_death(_pos):
    if Rect(396, 100, 256, 32).collidepoint(_pos):
        return 0
    elif Rect(364, 209, 320, 32).collidepoint(_pos):
        return 1
    elif Rect(460, 318, 128, 32).collidepoint(_pos):
        return 2
    return -1
