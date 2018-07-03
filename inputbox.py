#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pygame
from pygame.locals import *
from hello import *
from res import *


def get_key():
  while True:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key

def display_box(screen, rect, cont, is_pswd):
  empty(screen, rect)
  pygame.draw.rect(screen, Color("white"), rect, 2)
  if is_pswd:
    cont = '*' * len(cont)
  txt = text(cont, rect[0], rect[1], font_32)
  txt.show(screen)
  pygame.display.update()

def ask(screen, rect, is_pswd):
  current_string = []
  display_box(screen, rect, '', is_pswd)
  while True:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, rect, "".join(current_string), is_pswd)
  return "".join(current_string)
