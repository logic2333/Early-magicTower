# Early-magicTower
早期作品-魔塔游戏

'Early' means before my graduate period, when my major was not CS-related. These codes show little concept of 'software engineering', or say 'architecture', though some of them can be called 'project'.

“早期”指的是在我的研究生阶段之前（我本科所学专业与信息类完全无关）。这些代码很少有“软件工程”的概念，或者说很少有“架构设计”，尽管其中有几个的规模使得它们还是足以能被称为“工程项目”。

These codes are too troublesome to review, so i put them here merely for recording. To see my progress.

这些代码要review起来着实费劲，所以我把它们放在这里仅仅是为了记录。嗯，记录自己的成长历程哈哈哈。

This one is large enough to be called a 'toy project'. Game designing, UI designing and coding are all done by myself. Pitifully i didn't finish it. It is designed to have 19(0-18) floors, but i have only finished 11(0-10). On floor 10 is designed to be a small boss; but literally it becomes the final one. i have finished designing floor 11-18 on paper, but feel bored to put them into practice. It is coded with Pygame module.

这一个足以被称作一个“娱乐型工程项目”。从游戏策划、界面设计到编码都是我一人进行的。很遗憾没能做完它。本来设计了19（0-18）层，但程序只完成到了第10层。第10层是个小boss，这下变成了事实上的大boss。11-18层仅在纸上完成了设计，写这种繁杂的业务还是让我感到了无聊，就没兴趣做完它了。用了Pygame模块。

You should put game data onto a PostgreSQL server(localhost) before running the game, though user.csv is not necessary(which includes info of some users specially designed for test). Run ui.py or header.py to start the game. header.py includes user registration, hardness selection and more; while ui.py just starts the game anonymously in the hardest mode.

在运行游戏之前你需要将游戏数据上传到本地的PostgreSQL服务器（localhost），尽管user.csv不是必须的（它包含有一些测试用的用户数据）。要启动游戏，运行ui.py或header.py。运行header.py会启动完整版的游戏，包含用户注册及难度选择等；而运行ui.py仅匿名地进行游戏，且直接进入最难的模式。

This magictower game differs from those traditional ones because it involves in randomness--how much life you lose when you defeat a monster is not certain, so is whether you can defeat the monster. You may get a game-over if you are defeated by a monster--unlike the case in traditional ones, monsters will do nothing but just block your way if you cannot defeat them. So please be cautious about every single step.

本魔塔不同于传统魔塔之处在于它引入了随机性——你打败一个怪物所损失的生命值是不确定的，当然，你能不能打得过它都是个未知数。如果你被怪物打败了，你可能就game over了——不像在那些传统魔塔中那样，你所打不过的怪物们只是单纯的挡住你的去路。所以，每一步都请慎重。

