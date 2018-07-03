#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 基本的文字、图片、动画显示

import pygame
from pygame.locals import *

def empty(_surface, _rect):
    inside = (_rect[0] + 2, _rect[1] + 2, _rect[2] - 3, _rect[3] - 3)
    _surface.fill(Color("black"), inside)
    pygame.display.update() 

class text(pygame.sprite.Sprite):
    def __init__(self, _str, _x, _y, _font, _color = Color("white")):    # _x,_y是左上角坐标
        pygame.sprite.Sprite.__init__(self)
        self.font = _font
        self.image = self.font.render(_str, 1, _color).convert_alpha()
        self.rect = self.image.get_rect().move(_x, _y)
    def show(self, _surface):
        _surface.blit(self.image, self.rect)
        
class picture(pygame.sprite.Sprite):
    def __init__(self, _src, _posit, _X, _Y, _width, _height):         
        # _posit是左上角坐标，_X,_Y,_width,_height是要显示的在原图上切出的小区域
        pygame.sprite.Sprite.__init__(self)
        rect = (_X, _Y, _width, _height)
        self.image = _src.subsurface(rect)
        self.rect = (_posit[0], _posit[1], _width, _height)
    def show(self, _surface):
        _surface.blit(self.image, self.rect)

class animation(pygame.sprite.Sprite):
    # 三种对象：怪物、门、勇士
    # 怪物：循环播放
    # 门：被勇士触碰时，如勇士有钥匙，首先播放门打开的动画，播放完毕，处理勇士的移动
    # 勇士：如移动不可行，则仅在原地播放一遍该方向上的移动动画而不做交换，或接下来播放打斗动画
    def __init__(self, _src, _posit, _row, is_cycle = True, horizontally = True):     
        # _posit是左上角坐标，对怪物来说is_cycle, horizontally，对门来说都是False
        # _src是载入的帧合集图片
        pygame.sprite.Sprite.__init__(self)
        self.all_images = _src
        self.frame_width = self.frame_height = 32
        self.rect = (_posit[0], _posit[1], 32, 32)
        self.row = _row
        self.cycle = is_cycle
        self.horizontal = horizontally
        self.last_time = 0
        self.frame = 0
        self.image = None
        if self.horizontal:
            self.image = self.all_images.subsurface((0, self.row * self.frame_height, self.frame_width, self.frame_height))
        else:
            self.image = self.all_images.subsurface((self.row * self.frame_width, 0, self.frame_width, self.frame_height))
    def update(self, current_time, remain_image, rate):
        # row是要播放的行或列，从0开始
        # remain_image是播放结束后该位置应该保留的静止图片，若is_cycle则无效
        if current_time > self.last_time + rate:
            self.frame += 1
            self.last_time = current_time
            if self.frame > 3:
                if self.cycle:
                    self.frame = 0
                else:
                    self.frame = 4
                    self.image = remain_image
                    return
            if self.horizontal:
                src_rect = (self.frame * self.frame_width, self.row * self.frame_height, self.frame_width, self.frame_height)
            else:
                src_rect = (self.row * self.frame_width, self.frame * self.frame_height, self.frame_width, self.frame_height)
            self.image = self.all_images.subsurface(src_rect)
    def show(self, _surface):
        _surface.blit(self.image, self.rect)
