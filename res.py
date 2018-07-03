#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
import pickle

f = open("pic.dat", "rb")
pic_dic_tmp = pickle.load(f)
f.close()
pygame.init()
pic_dic = {}
for tag in pic_dic_tmp:
    sz = ()
    if tag == "npc_src":
        sz = (128, 256)
    elif tag[0:7] == "warrior" or tag == "doors_src" or tag[0:5] == "lava-":
        sz = (128, 128)
    elif tag == "monster_src":
        sz = (128, 1280)
    else:
        sz = (32, 32)
    pic_dic[tag] = pygame.image.frombuffer(pic_dic_tmp[tag], sz, "RGBA")
del pic_dic_tmp

font_20 = pygame.font.Font("li.ttf", 20)
font_26 = pygame.font.Font("li.ttf", 26)
font_32 = pygame.font.Font("li.ttf", 32)
font_16 = pygame.font.Font("li.ttf", 16)

font_title = pygame.font.Font("xingkai.ttf", 50)
font_title_small = pygame.font.Font("xingkai.ttf", 20)
font_death = pygame.font.Font("xingkai.ttf", 32)
