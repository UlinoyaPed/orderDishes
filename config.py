from qfluentwidgets import *


class MyConfig(QConfig):
    """ Config of application """
    pass


# 创建配置实例并使用配置文件来初始化它
cfg = MyConfig()
qconfig.load('config/config.json', cfg)
