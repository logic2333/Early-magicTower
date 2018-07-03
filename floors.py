#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
原计划本塔有18层，8层的是小boss，写得实在无聊便弃坑了，就把8层的当大boss吧。。。
后面在纸上都设计好了，有一些剧情，不过也没啥技术含量。。
就是调接口，还有就是把画在纸上的每一层像下面这样输入（要是搞个图像识别拍照输入也好，可是我纸上的图大概也只有我自己能看懂了）。
切身体会到了写“业务逻辑”的无聊，当然也可能是自己架构设计得不是太好。
反正就是很无聊，到处微调接口，这里要多传一个参数，那里要保存到存档里……烦不胜烦。还好python灵活，要是cpp炸得还要早……
还不如毕设有意思╯︵╰
'''


floors = {}

floors["00"] = [
        ["lava", "lava", "lava", "lava", "lava", "lava", "stairs-down", "lava", "lava", "lava", "lava", "lava", "lava"], 
        ["lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "barr-sky", "barr-sky", "door-31", "barr-sky", "barr-sky", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "barr-sky", "mons-0", "mons-1", "mons-0", "barr-sky", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "barr-sky", "mons-0", "warrior", "mons-0", "barr-sky", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "barr-sky", "mons-0", "mons-0", "mons-0", "barr-sky", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "barr-sky", "barr-sky", "door-30", "barr-sky", "barr-sky", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "lava", "lava", "empty", "lava", "lava", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "lava", "lava", "empty", "lava", "lava", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "lava", "lava", "npc-3", "lava", "lava", "lava", "lava", "lava", "lava"],
        ["lava", "lava", "lava", "lava", "lava", "lava", "stairs-up", "lava", "lava", "lava", "lava", "lava", "lava"]
        , False
]

floors["01"] = [
        ["empty", "empty", "mons-0", "mons-1", "mons-2", "empty", "empty", "empty", "empty", "empty", "food-big_blood", "item-yellow_key", "stairs-down"],
        ["empty", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-0", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-1", "barr-yellow_wall", "barr-yellow_wall"],
        ["item-black_gem", "barr-yellow_wall", "empty", "empty", "mons-8", "empty", "item-black_gem", "barr-yellow_wall", "others-2", "mons-8", "empty", "empty", "empty"],
        ["item-black_gem", "barr-yellow_wall", "item-yellow_key", "empty", "food-green_gem", "empty", "empty", "barr-yellow_wall", "mons-8", "empty", "empty", "item-black_gem", "food-yellow_gem"],
        ["item-black_gem", "barr-yellow_wall", "item-blue_key", "empty", "mons-12", "empty", "mons-4", "door-0", "empty", "empty", "empty", "food-green_gem", "item-blue_key"],
        ["item-black_gem", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-0", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-0", "barr-yellow_wall", "barr-yellow_wall"],
        ["empty", "barr-yellow_wall", "food-green_gem", "empty", "empty", "empty", "food-small_blood", "barr-yellow_wall", "empty", "item-yellow_key", "mons-2", "empty", "mons-2"],
        ["empty", "barr-yellow_wall", "food-blue_gem", "empty", "mons-1", "empty", "empty", "door-0", "mons-2", "empty", "item-yellow_key", "mons-18", "empty"],
        ["door-0", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-1", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "item-yellow_key", "mons-2"],
        ["mons-13", "mons-12", "mons-12", "mons-12", "food-small_blood", "food-red_gem", "mons-1", "barr-yellow_wall", "food-big_blood", "item-money", "mons-16", "empty", "item-yellow_key"],
        ["mons-12", "food-big_blood", "mons-4", "mons-12", "barr-yellow_wall", "barr-yellow_wall", "door-2", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-1", "barr-yellow_wall", "door-2"],
        ["mons-12", "mons-4", "item-key_box", "mons-12", "barr-yellow_wall", "item-red_key", "warrior", "food-feather", "barr-yellow_wall", "food-big_blood", "mons-13", "item-black_gem", "item-black_gem"],
        ["mons-12", "mons-12", "mons-12", "mons-13", "barr-yellow_wall", "barr-sky", "stairs-up", "barr-sky", "barr-yellow_wall", "sword-1", "mons-5", "item-black_gem", "item-black_gem"]
        , False
]

floors["02"] = [
        ["stairs-up", "barr-yellow_wall", "food-small_blood", "barr-yellow_wall", "item-key_box", "barr-yellow_wall", "hint-0", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "food-big_blood", "item-blue_key"],
        ["warrior", "barr-yellow_wall", "empty", "barr-yellow_wall", "empty", "barr-yellow_wall", "item-black_gem", "barr-yellow_wall", "food-feather", "empty", "barr-yellow_wall", "mons-16", "lava"],
        ["empty", "door-1", "item-black_gem", "barr-yellow_wall", "item-black_gem", "barr-yellow_wall", "empty", "barr-yellow_wall", "barr-yellow_wall", "empty", "barr-yellow_wall", "empty", "lava"],
        ["empty", "barr-yellow_wall", "item-black_gem", "mons-5", "item-black_gem", "door-0", "mons-0", "empty", "empty", "empty", "door-32", "empty", "lava"],
        ["mons-1", "barr-yellow_wall", "empty", "mons-4", "mons-4", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "mons-1", "lava"],
        ["mons-4", "barr-yellow_wall", "door-0", "barr-yellow_wall", "door-2", "barr-yellow_wall", "food-small_blood", "empty", "empty", "empty", "mons-1", "mons-2", "lava"],
        ["mons-1", "barr-yellow_wall", "mons-8", "item-black_gem", "cloak-1", "barr-yellow_wall", "empty", "lava", "lava", "lava", "lava", "lava", "lava"],
        ["empty", "barr-yellow_wall", "item-black_gem", "mons-9", "item-black_gem", "door-1", "mons-2", "empty", "item-black_gem", "item-black_gem", "item-black_gem", "empty", "lava"],
        ["mons-12", "door-0", "mons-2", "item-black_gem", "mons-8", "barr-yellow_wall", "empty", "lava", "lava", "lava", "lava", "lava", "lava"],
        ["door-0", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-1", "barr-yellow_wall", "food-small_blood", "empty", "mons-2", "mons-2", "mons-2", "empty", "lava"],
        ["mons-0", "empty", "empty", "item-black_gem", "mons-1", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "empty", "lava", "lava"],
        ["item-yellow_key", "empty", "food-big_blood", "empty", "item-black_gem", "barr-yellow_wall", "empty", "empty", "empty", "empty", "mons-8", "lava", "item-bomb"],
        ["mons-1", "item-yellow_key", "empty", "empty", "mons-0", "mons-18", "item-blue_key", "empty", "empty", "mons-13", "food-small_blood", "mons-5", "stairs-down"]
        , False
]

floors["03"] = [
        ["shield-1", "mons-16", "item-black_gem", "barr-yellow_wall", "hint-1", "empty", "empty", "barr-sky", "barr-sky", "barr-sky", "stairs-down", "barr-sky", "barr-sky"],
        ["lava", "food-big_blood", "empty", "barr-yellow_wall", "empty", "empty", "empty", "empty", "npc-0", "barr-sky", "empty", "barr-sky", "food-feather"],
        ["lava", "empty", "empty", "door-1", "mons-13", "empty", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "food-big_blood"],
        ["lava", "empty", "empty", "barr-yellow_wall", "item-blue_key", "mons-8", "empty", "barr-sky", "empty", "barr-sky", "empty", "empty", "mons-9"],
        ["lava", "empty", "empty", "barr-yellow_wall", "barr-yellow_wall", "door-0", "barr-sky", "barr-sky", "item-red_key", "barr-sky", "barr-sky", "barr-sky", "door-0"],
        ["lava", "door-2", "empty", "barr-yellow_wall", "mons-13", "mons-13", "mons-18", "mons-13", "mons-13", "mons-14", "item-key_box", "item-money", "stairs-down"],
        ["lava", "lava", "door-0", "barr-yellow_wall", "mons-13", "barr-yellow_wall", "mons-13", "food-big_blood", "item-black_gem", "mons-13", "barr-yellow_wall", "barr-yellow_wall", "door-0"],
        ["item-black_gem", "food-big_blood", "mons-13", "mons-13", "mons-13", "barr-yellow_wall", "mons-13", "item-black_gem", "food-big_blood", "mons-13", "barr-yellow_wall", "item-black_gem", "item-black_gem"],
        ["empty", "hint-2", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "mons-16", "mons-13", "mons-13", "mons-31", "door-0", "item-black_gem", "item-black_gem"],
        ["mons-5", "empty", "empty", "empty", "empty", "barr-yellow_wall", "barr-yellow_wall", "door-0", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "empty", "empty"],
        ["barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "empty", "door-1", "mons-2", "empty", "mons-16", "item-black_gem", "barr-yellow_wall", "empty", "empty"],
        ["warrior", "empty", "empty", "empty", "mons-8", "barr-yellow_wall", "empty", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "item-yellow_key", "item-yellow_key"],
        ["stairs-up", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "empty", "empty", "mons-18", "food-big_blood", "door-1", "item-yellow_key", "item-yellow_key"]
        , False
]

floors["04"] = [
        ["mons-31", "food-small_blood", "mons-3", "food-small_blood", "mons-31", "barr-yellow_wall", "barr-yellow_wall", "item-bomb", "barr-yellow_wall", "barr-yellow_wall", "food-feather", "empty", "empty"],
        ["food-small_blood", "mons-31", "empty", "mons-31", "food-small_blood", "barr-yellow_wall", "item-money", "mons-14", "item-money", "barr-yellow_wall", "door-2", "barr-yellow_wall", "mons-17"],
        ["mons-2", "empty", "empty", "empty", "mons-2", "barr-yellow_wall", "mons-9", "item-black_gem", "mons-9", "barr-yellow_wall", "mons-31", "empty", "mons-6"],
        ["empty", "empty", "mons-13", "empty", "empty", "barr-yellow_wall", "empty", "mons-9", "empty", "barr-yellow_wall", "empty", "mons-9", "empty"],
        ["barr-yellow_wall", "barr-yellow_wall", "door-0", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-1", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-2", "barr-yellow_wall"],
        ["stairs-up", "warrior", "mons-16", "mons-9", "empty", "item-red_key", "empty", "mons-16", "empty", "item-yellow_key", "empty", "mons-16", "stairs-down"],
        ["barr-yellow_wall", "barr-yellow_wall", "door-0", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-1", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "door-2", "barr-yellow_wall"],
        ["empty", "empty", "mons-13", "empty", "empty", "barr-yellow_wall", "empty", "mons-9", "empty", "barr-yellow_wall", "empty", "mons-9", "empty"],
        ["mons-13", "food-green_gem", "food-green_gem", "food-green_gem", "mons-12", "barr-yellow_wall", "mons-9", "item-black_gem", "mons-9", "barr-yellow_wall", "empty", "empty", "empty"],
        ["food-red_gem", "mons-13", "food-green_gem", "mons-12", "food-blue_gem", "barr-yellow_wall", "empty", "mons-6", "empty", "barr-yellow_wall", "empty", "empty", "empty"],
        ["food-red_gem", "food-red_gem", "mons-14", "food-blue_gem", "food-blue_gem", "barr-yellow_wall", "mons-18", "food-big_blood", "mons-18", "barr-yellow_wall", "mons-31", "empty", "mons-3"],
        ["food-red_gem", "mons-12", "food-yellow_gem", "mons-13", "food-blue_gem", "barr-yellow_wall", "item-blue_key", "mons-20", "item-blue_key", "barr-yellow_wall", "door-2", "barr-yellow_wall", "mons-14"],
        ["mons-12", "food-yellow_gem", "food-yellow_gem", "food-yellow_gem", "mons-13", "barr-yellow_wall", "barr-yellow_wall", "item-key_box", "barr-yellow_wall", "barr-yellow_wall", "cloak-2", "empty", "empty"]
        , False
]

floors["05"] = [
        ["empty", "empty", "empty", "empty", "empty", "empty", "barr-yellow_wall", "empty", "empty", "empty", "empty", "empty", "empty"],
        ["empty", "empty", "item-black_gem", "item-black_gem", "item-black_gem", "empty", "barr-yellow_wall", "empty", "empty", "mons-8", "empty", "barr-sky", "empty"],
        ["empty", "empty", "item-black_gem", "item-black_gem", "item-black_gem", "empty", "door-2", "empty", "empty", "mons-9", "empty", "barr-sky", "empty"],
        ["empty", "empty", "item-black_gem", "item-black_gem", "item-black_gem", "empty", "barr-yellow_wall", "empty", "empty", "mons-8", "empty", "barr-sky", "empty"],
        ["barr-yellow_wall", "barr-yellow_wall", "mons-14", "empty", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "empty", "empty", "empty", "empty"],
        ["stairs-up", "barr-yellow_wall", "door-0", "barr-yellow_wall", "barr-yellow_wall", "empty", "item-money", "empty", "barr-yellow_wall", "empty", "empty", "empty", "empty"],
        ["warrior", "empty", "empty", "empty", "door-0", "mons-21", "stairs-down", "mons-20", "door-1", "mons-18", "mons-34", "mons-18", "barr-sky"],
        ["empty", "barr-yellow_wall", "door-0", "barr-yellow_wall", "barr-yellow_wall", "empty", "item-money", "empty", "barr-yellow_wall", "empty", "empty", "empty", "empty"],
        ["barr-yellow_wall", "barr-yellow_wall", "mons-17", "empty", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "barr-yellow_wall", "empty", "empty", "empty", "empty"],
        ["barr-yellow_wall", "empty", "item-black_gem", "item-black_gem", "item-black_gem", "empty", "barr-yellow_wall", "empty", "empty", "mons-13", "empty", "barr-sky", "empty"],
        ["empty", "empty", "item-black_gem", "item-black_gem", "item-black_gem", "empty", "door-2", "empty", "empty", "mons-14", "empty", "barr-sky", "empty"],
        ["empty", "empty", "item-black_gem", "item-black_gem", "item-black_gem", "empty", "barr-yellow_wall", "empty", "empty", "mons-13", "empty", "barr-sky", "empty"],
        ["empty", "empty", "empty", "empty", "empty", "empty", "barr-yellow_wall", "empty", "empty", "empty", "empty", "empty", "empty"]
        , False
]

floors["06"] = [
        ["stairs-down", "barr-sky", "food-yellow_gem", "food-yellow_gem", "food-yellow_gem", "empty", "empty", "empty", "empty", "barr-sky", "mons-14", "mons-14", "stairs-down"],
        ["mons-6", "barr-sky", "food-yellow_gem", "food-yellow_gem", "food-yellow_gem", "empty", "empty", "empty", "empty", "barr-sky", "mons-14", "barr-sky", "barr-sky"],
        ["empty", "empty", "food-yellow_gem", "food-yellow_gem", "food-yellow_gem", "empty", "book-2", "empty", "empty", "barr-sky", "food-red_gem", "food-red_gem", "food-red_gem"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "door-35", "barr-sky", "barr-sky", "barr-sky", "food-red_gem", "food-red_gem", "food-red_gem"],
        ["empty", "empty", "empty", "barr-sky", "hint-3", "empty", "mons-31", "empty", "food-feather", "barr-sky",  "food-red_gem", "food-red_gem", "food-red_gem"],
        ["empty", "empty", "empty", "barr-sky", "empty", "empty", "empty", "empty", "empty", "barr-sky", "empty", "empty", "empty"],
        ["empty", "empty", "staff-1", "door-33", "mons-31", "empty", "warrior", "empty", "mons-31", "door-34", "sword-2", "empty", "empty"],
        ["empty", "empty", "empty", "barr-sky", "empty", "empty", "empty", "empty", "empty", "barr-sky", "empty", "empty", "empty"],
        ["food-red_gem", "food-red_gem", "food-yellow_gem", "barr-sky", "food-feather", "empty", "mons-31", "empty", "hint-4", "barr-sky", "empty", "empty", "empty"],
        ["food-red_gem", "food-feather", "food-yellow_gem", "barr-sky", "barr-sky", "barr-sky", "door-36", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["food-red_gem", "food-yellow_gem", "food-yellow_gem", "barr-sky", "empty", "empty", "others-1", "empty", "food-big_blood", "food-big_blood", "food-big_blood", "mons-20", "mons-20", "mons-20"],
        ["barr-sky", "barr-sky", "empty", "barr-sky",  "empty", "empty", "empty", "empty", "food-big_blood", "food-big_blood", "food-big_blood", "barr-sky", "mons-20"],
        ["stairs-down", "mons-3", "empty", "barr-sky", "empty", "empty", "empty", "empty", "food-big_blood", "food-big_blood", "food-big_blood", "barr-sky", "stairs-down"]
        , False
]

floors["A7"] = [
        ["item-black_gem", "item-black_gem", "item-black_gem", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "stairs-down"],
        ["item-black_gem", "food-feather", "item-black_gem", "door-2", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "mons-18"], 
        ["item-black_gem", "item-black_gem", "item-black_gem", "barr-grey_wall", "mons-32", "door-1", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"], 
        ["barr-grey_wall", "door-2", "barr-grey_wall", "barr-grey_wall", "empty", "barr-grey_wall", "mons-11", "door-1", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "mons-32", "empty", "item-red_key", "barr-grey_wall", "empty", "barr-grey_wall", "mons-10", "door-0", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "door-1", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-6", "barr-grey_wall", "empty", "barr-grey_wall", "mons-20", "door-0", "mons-17"],
        ["food-small_blood", "empty", "empty", "mons-11", "empty", "mons-6", "item-money", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-1", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-14", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "empty", "empty", "mons-10", "empty", "empty", "mons-14", "item-blue_key", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-0", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-31", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "empty", "empty", "empty", "mons-20", "empty", "empty", "empty", "mons-31", "item-yellow_key", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-0", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "empty"],
        ["stairs-up", "warrior", "empty", "empty", "empty", "mons-17", "empty", "empty", "empty", "empty", "empty", "empty", "mons-3"]
        , False
]

floors["B7"] = [
        ["food-red_gem", "food-red_gem", "food-red_gem", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "stairs-down"],
        ["food-red_gem", "sword-3", "food-blue_gem", "door-2", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "mons-18"], 
        ["food-blue_gem", "food-blue_gem", "food-blue_gem", "barr-grey_wall", "mons-32", "door-1", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"], 
        ["barr-grey_wall", "door-2", "barr-grey_wall", "barr-grey_wall", "empty", "barr-grey_wall", "mons-11", "door-1", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "mons-32", "empty", "item-red_key", "barr-grey_wall", "empty", "barr-grey_wall", "mons-10", "door-0", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "door-1", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-6", "barr-grey_wall", "empty", "barr-grey_wall", "mons-20", "door-0", "mons-17"],
        ["food-small_blood", "empty", "empty", "mons-11", "empty", "mons-6", "item-money", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-1", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-14", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "empty", "empty", "mons-10", "empty", "empty", "mons-14", "item-blue_key", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-0", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-31", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "empty", "empty", "empty", "mons-20", "empty", "empty", "empty", "mons-31", "item-yellow_key", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-0", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "empty"],
        ["stairs-up", "warrior", "empty", "empty", "empty", "mons-17", "empty", "empty", "empty", "empty", "empty", "empty", "mons-3"]
        , False
]

floors["C7"] = [
        ["food-yellow_gem", "food-yellow_gem", "food-yellow_gem", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "stairs-down"],
        ["food-yellow_gem", "food-feather", "food-green_gem", "door-2", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "mons-18"], 
        ["food-green_gem", "food-green_gem", "food-green_gem", "barr-grey_wall", "mons-32", "door-1", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"], 
        ["barr-grey_wall", "door-2", "barr-grey_wall", "barr-grey_wall", "empty", "barr-grey_wall", "mons-11", "door-1", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "mons-32", "empty", "item-red_key", "barr-grey_wall", "empty", "barr-grey_wall", "mons-10", "door-0", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "door-1", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-6", "barr-grey_wall", "empty", "barr-grey_wall", "mons-20", "door-0", "mons-17"],
        ["food-small_blood", "empty", "empty", "mons-11", "empty", "mons-6", "item-money", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-1", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-14", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "empty", "empty", "mons-10", "empty", "empty", "mons-14", "item-blue_key", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-0", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-31", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "empty", "empty", "empty", "mons-20", "empty", "empty", "empty", "mons-31", "item-yellow_key", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-0", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "empty"],
        ["stairs-up", "warrior", "empty", "empty", "empty", "mons-17", "empty", "empty", "empty", "empty", "empty", "empty", "mons-3"]
        , False
]

floors["D7"] = [
        ["food-small_blood", "food-small_blood", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "food-small_blood", "barr-grey_wall", "stairs-down"],
        ["food-small_blood", "food-feather", "food-small_blood", "door-2", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "mons-18"], 
        ["food-small_blood", "food-small_blood", "food-small_blood", "barr-grey_wall", "mons-32", "door-1", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"], 
        ["barr-grey_wall", "door-2", "barr-grey_wall", "barr-grey_wall", "empty", "barr-grey_wall", "mons-11", "door-1", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "mons-32", "empty", "item-red_key", "barr-grey_wall", "empty", "barr-grey_wall", "mons-10", "door-0", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "door-1", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-6", "barr-grey_wall", "empty", "barr-grey_wall", "mons-20", "door-0", "mons-17"],
        ["food-small_blood", "empty", "empty", "mons-11", "empty", "mons-6", "item-money", "barr-grey_wall", "empty", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-1", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-14", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "empty", "empty", "mons-10", "empty", "empty", "mons-14", "item-blue_key", "barr-grey_wall", "empty", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-0", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "mons-31", "barr-grey_wall", "empty"],
        ["food-small_blood", "empty", "empty", "empty", "empty", "mons-20", "empty", "empty", "empty", "mons-31", "item-yellow_key", "barr-grey_wall", "empty"],
        ["barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "door-0", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "barr-grey_wall", "empty"],
        ["stairs-up", "warrior", "empty", "empty", "empty", "mons-17", "empty", "empty", "empty", "empty", "empty", "empty", "mons-3"]
        , False
]

floors["A8"] = floors["B8"] = floors["C8"] = floors["D8"] = [
        ["stairs-up", "warrior", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "lava", "item-bomb"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "empty", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "mons-29", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"],
        ["barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "stairs-down", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky", "barr-sky"]
        , False
]
