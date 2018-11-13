#!/usr/bin/env python
# encoding: utf-8
import sys
import os
import pygame
from pygame.locals import *
 
def load_image(pic_name):
    '''
    Function:图片加载函数
    Input：pic_name 图片名称
    Output: NONE
    author: dyx1024
    blog:http://blog.csdn.net/dyx1024
    date:2012-04-15
    '''
    #获取当前脚本文件所在目录的绝对路径
    current_dir = os.path.split(os.path.abspath(__file__))[0]
    
    #指定图片目录
    path = os.path.join(current_dir, 'image', pic_name)
    
    #加载图片
    return pygame.image.load(path).convert()
 
def init_windows():
    '''
    Function:窗口初始化
    Input：NONE
    Output: NONE
    author: dyx1024
    blog:http://blog.csdn.net/dyx1024
    date:2012-04-21
    '''    
    pygame.init()
    display_surface = pygame.display.set_mode((600, 500))
    pygame.display.set_caption('游戏中的文字处理(http://blog.csdn.net/dyx1024)')
    return display_surface
 
def exit_windows():
    '''
    Function:退出处理
    Input：NONE
    Output: NONE
    author: dyx1024
    blog:http://blog.csdn.net/dyx1024
    date:2012-04-21
    '''      
    pygame.quit()
    sys.exit()
 
def main():
    '''
    Function:字体处理
    Input：NONE
    Output: NONE
    author: dyx1024
    blog:http://blog.csdn.net/dyx1024
    date:2012-04-21
    '''        
    
    screen_surface = init_windows()
    back_image = load_image('mengqiqi.jpg')
      
    color_red = (255, 0, 0)
    color_green = (0, 255, 0)
    color_blue  = (0, 0, 255)
 
    #第一组文字
    
    #创建一个Font对象，其中LOWRBI__.TTF为下载的字体库
    fontObj =  pygame.font.SysFont('Microsoft YaHei', 23)
    
    #创建一个存放文字surface对象，
    textSurfaceObj = fontObj.render(u'HELLO MONCHHICHI', False, color_green)
    
    #文字图像位置
    textRectObj = textSurfaceObj.get_rect()
    
    #第二组文字
    fontObj2 = pygame.font.SysFont('Microsoft YaHei', 23)
    
    #添加下画线
    fontObj2.set_underline(True)
    textSurfaceObj2 = fontObj2.render(u'很萌，有木有！', False, color_red)
    textRectObj2 = textSurfaceObj2.get_rect()
    textRectObj2.center = (80, 480)
    
    #第三组文字
    
    #使用系统字体
    fontObj3 = pygame.font.SysFont('Microsoft YaHei', 23)
    
    #加粗
    fontObj3.set_bold(True)
    
    #斜体
    fontObj3.set_italic(True)
    
    #文字具有蓝色背景
    textSurfaceObj3 = fontObj3.render(u'又到凌晨了，睡', True, color_red, color_blue)
    textRectObj3 = textSurfaceObj3.get_rect()
    textRectObj3.center = (500, 10)
    
 
    while True:
        #绘图
        screen_surface.blit(back_image, (0, 0))
        screen_surface.blit(textSurfaceObj, textRectObj)
        screen_surface.blit(textSurfaceObj2, textRectObj2)
        screen_surface.blit(textSurfaceObj3, textRectObj3)
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_windows()
        pygame.display.update()

 
if __name__ == '__main__':
    main()
