import pygame
import sqlite3
import sys
from need.input_api import model_input
from pygame.locals import *
from loading import *
from itertools import cycle
import random
if 'win' in sys.platform:
    from loading import music_wav as m
else:
    from loading import music_ogg as m
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
FPS = 100
SCREENWIDTH  = 288
SCREENHEIGHT = 512
base = 404
def get(num,type):
    for i in range(num):
        w=next(type)
    return w
def select_bird():
    global bird_s
    screen.blit(bg[0],(0,0))
    screen.blit(message,(50,23))
    pygame.display.update()
    bird_s=cycle(['red','yellow','blue'])
    bird_=bird_c[next(bird_s)]
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.display.quit()
            elif event.type==KEYDOWN:
                if event.key==K_DOWN:
                    bird_=bird_c[get(1,bird_s)]
                    
                if event.key==K_UP:
                    bird_=bird_c[ get(2,bird_s)]
                if event.key == K_SPACE or event.key==K_RETURN:
                    color=get(3,bird_s)  #这里默认有3只鸟
                    return color  #返回一个
        screen.blit(bg[0] , (0 , 0))
        screen.blit(message , (50 , 23))
        screen.blit(bird_,(122,188))
        moving()
        clock.tick(30)
        pygame.display.flip()

def select_level():
    global active_s,temp
    row=90  #设置列间距
    col=30  #设置行间距
    box_width=90
    box_heigh=20
    active_s=cycle(['一','二','三','四','五','六','七','八','九','十','十一','十二'])
    message_box=['一','二','三','四','五','六','七','八','九','十','十一','十二']
    active_=next(active_s)
    col_num=5  #一列的数目
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.display.quit()
            elif event.type==KEYDOWN:
                if event.key==K_LEFT and active_ not in message_box[:col_num]:
                    active_=get(len(message_box)-col_num,active_s)

                if event.key==K_RIGHT and active_ not in message_box[-col_num:]:
                    active_=get(col_num,active_s)
                if event.key==K_DOWN and active_ not in message_box[col_num-1::col_num]:
                    active_=get(1,active_s)
                if event.key==K_UP and active_ not in message_box[::col_num]:
                    active_=get(len(message_box)-1,active_s)
                if event.key == K_SPACE or event.key==K_RETURN:
                    return active_
        init_x=20
        init_y=100
        num_=1
        for i in message_box:
            level_show(font_pos=(init_x,init_y),box_pos=(init_x-10,init_y,box_width,box_heigh),active=active_,message='第'+i+'关')
            init_y+=col
            if num_%col_num==0:
                init_y=100
                init_x+=row
            num_+=1
        clock.tick(30)
def level_default():
    active_s=cycle(['简单','一般','困难'])
    active_=next(active_s)
    screen.blit(bg[0] , (0 , 0))
    while True:
        level_show(font_pos=(100,100),box_pos=(90,100,90,20),active=active_,message='简单')
        level_show(font_pos=(100,150),box_pos=(90,150,90,20),active=active_,message='一般')
        level_show(font_pos=(100,200),box_pos=(90,200,90,20),active=active_,message='困难')
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
            elif event.type == KEYDOWN:
                if event.key == K_DOWN:
                    active_ = get(1 , active_s)
                if event.key == K_UP:
                    active_ = get(2 , active_s)
                if event.key == K_SPACE or event.key==K_RETURN:
                    print(active_)
                    return active_
        clock.tick(30)

def level_show(font_pos,box_pos,active=None,message='第一关',size=18):
    
    fontobject=pygame.font.SysFont('Kaiti',size,True)
    if active in message:
        if len(active)==1 and len(message)==3 or len(active)==2 and len(message)==4:
            color=(255,0,0)
        else:
            color=(0,0,255)
    else:
        color=(0,0,255)
    if len(message)==len(active): #对困难和一般进行兼容
            if message==active:
                color=(255,0,0)
            else:
                color=(0,0,255)
    pygame.draw.rect(screen,(0,0,0),box_pos,1)
    
    pygame.draw.rect(screen,(255,255,255),box_pos,1)
    text=fontobject.render(message,True,(color))
    screen.blit(text,font_pos)
    #screen.blit(fontobject.render(message,1,(0,0,255)),(1,100))
    pygame.display.flip()

def show():
    screen.blit(bg[0],(0,0))
    name=model_input(screen)
    screen.blit(message,(0,0))
    screen.blit(bg[0],(0,0))
    level=select_level()
    default=level_default()
    bird=select_bird()
    return name,level,default,bird
def getHitmask(image):
    mask = []
    print(image)
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask
def check_crash(bird,xs,uppers,lowers='',img=''):
    bird_width=bird.get_width()*0.71
    bird_height=bird.get_height()*0.71
    bird_rect=pygame.Rect(bird_x,bird_y,bird_width,bird_height)
    if lowers:
        for x,up,low in zip(xs,uppers,lowers):
            u_Rect=pygame.Rect(x,up,52,320)
            l_Rect=pygame.Rect(x,low,52,320)

            #get hitmask
            bHiMask=mask['bird'][0]
            uHiMask=mask['pipe'][0]
            lHiMask=mask['pipe'][1]
            #if bird
            uCollide=pixelCollision(bird_rect,u_Rect,bHiMask,uHiMask)
            lCollide=pixelCollision(bird_rect,l_Rect,bHiMask,lHiMask)
            if uCollide or lCollide:
                return [True,False],up,low,x

    else:
        for x,up in zip(xs,uppers):
            u_Rect=pygame.Rect(x,up,img.get_width(),img.get_height())
            bHiMask=mask['bird']
            uHiMask=mask['box']
            uCollide=pixelCollision(bird_rect,u_Rect,bHiMask,uHiMask)
            if uCollide:
                return [True,False],x,up
    return [False,False],'1','1'
def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    rect = rect1.clip(rect2)
    if rect.width == 0 or rect.height == 0:
        return False
    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y
    for x in range(rect.width):
        for y in range(rect.height):
            try:
                if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                    return True
            except:
                return True
    return False

def moving(): #装载底部移动模块
    global temp
    temp=-((-temp+4)%48)
    screen.blit(move,(temp,base))
    # clock.tick(30 )  #此处是控制 下面的速度的
    # pygame.display.flip()
def MainGame(info):#主游戏模块
    global distance,bird_x,bird_y,mask,temp
    name , level , default , color = info
    real_bg=random.choice(bg)
    level=dict_[level]
    mask ={}
    upper_img=pipe['green'][0]# 获得图像
    lower_img = pygame.transform.rotate(upper_img , 180)#翻转图像
     #管道距离
    mask['bird'] = (
        getHitmask(bird_c[color]))
    mask['pipe'] = (
        getHitmask(pipe['green'][0]) ,
        getHitmask(pipe['green'][1]) ,
    )
    mask['box']=(
        getHitmask(box)
    )

    score=57#分数
    distance = distance_-level*20 #每个的距离
    bet=200-10*level
    count=distance #为了pipe距离一致进行的计算
    bird_x = 57  #鸟的初始坐标
    bird_y=190
    if default=='简单':
        far=easy #设置画面速度
    elif default=='一般':
        far=commont
    else:
        far=difficult
    rotate=60 #角度
    v=0 #加速度
    g_v=0.5 #设置画面加速度
    g_v_=2 #起始下落速度
    cc=bird_c[color]#鸟的颜色
    box_x=[]
    box_y=[]
    x=[]
    far_=far
    u_y=[]
    l_y=[]
    v_=0
    counter=0
    while True:
        screen.blit(real_bg , (0 , 0))
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.display.quit()
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                m['wing'].play()
                v=8
                v_=rotate
                g_v_=2
        if v>0:
            cc=pygame.transform.rotate(bird_c[color],v_/2)
            bird_y-=v
            v_-=8
            v-=1
        else:
            v_-=1
            cc=pygame.transform.rotate(bird_c[color],v_)
            g_v_+=g_v
            bird_y+=(g_v_)

        #上面是飞行机制
        if count>=distance:
            count=0
            x.append(388)
            u_yy,l_yy=get_pipe(bet)
            u_y.append(u_yy)
            l_y.append(l_yy)
            #下面定义道具出现在俩个管道之间
            b_count = random.randint(1 , 10)
            if b_count < 10 * box_pro:
                box_x.append(random.randint(440 , 440 + distance-70))
                box_y.append(random.randint(100 , 300))
        #贴上管道
        if counter>0:
            if big:
                cc=pygame.transform.scale2x(cc)  #处于大状态
            if fast:
                pass
            if small:
                cc=pygame.transform.scale(cc, (17, 12))
        else:
            far=far_
            fast=False
            big=False
        for x_,u_y_,l_y_ in zip(x,u_y,l_y):
            if x_<-100:
                del x[0],u_y[0],l_y[0]

            screen.blit(upper_img,(x_,u_y_))
            screen.blit(lower_img,(x_,l_y_))
        for i in range(len(x)):
            x[i]-=far
        #贴上道具
        box_crash =check_crash(cc,box_x,box_y,img=box)
        if box_crash[0][0]:
            for b_x,b_y in zip(box_x,box_y):
                if b_x>55 and b_x<130:
                    del box_x[box_x.index(box_crash[1])],box_y[box_y.index(box_crash[2])]
                    far=far_
                    big=False
                    small=False
                    tmp=random.randint(1,3)
                    if tmp==1:
                        big=True
                    elif tmp==2:
                        fast=True
                        far_=far
                        far-=slowed
                    else:
                        small=True
                    counter=box_time
        count+=far
        for b_x,b_y in zip(box_x,box_y):
            if b_x<-100:
                del box_x[0],box_y[0]
            screen.blit(box,(b_x,b_y))
        for i in range(len(box_x)):
            box_x[i]-=far
        score+=far
        rel_score=int((score-438+distance)/(distance))
        if rel_score<=0:
            rel_score=0;rel_score_=0
        if rel_score>rel_score_:
            m['point'].play()
            rel_score_=rel_score
        index=0
        for i in str(rel_score):
            screen.blit(score_group[i],(200+index*30,10))
            index+=1

        counter-=4
        crash_test=check_crash(cc,x,u_y,l_y)
        if crash_test[0][0] and big==False:
            m['die'].play()
            return cc,bird_x,bird_y,name , level , default,rel_score_ #返回鸟的坐标
        if crash_test[0][0] and big==True:
            del u_y[u_y.index(crash_test[1])],l_y[l_y.index(crash_test[2])],x[x.index(crash_test[3])]
            rel_score+=distance
        if cc.get_height()+bird_y>=410 or bird_y<=0:
            m['die'].play()
            return cc,bird_x,bird_y,name , level , default,rel_score_
        screen.blit(cc,(bird_x,bird_y))
        temp = -((-temp + 4) % 48)
        screen.blit(move , (temp , base))
        clock.tick(30)
        pygame.display.update()

def get_pipe(bet):#获取管道参数
#管道  头20， 总长320 宽50  画面400 宽288
    zz=(400-bet)/2
    if -zz*0.5< zz*0.5:
        t=random.randint(int(-zz*0.5),int(zz*0.5))
    else:
        t=random.randint(int(zz*0.5),int(-zz*0.5) )
    u_y=zz+t-320
    l_y=400-zz+t
    return l_y,u_y

def main():#游戏入口函数
    global screen,clock,temp
    temp=0
    pygame.init() #初始化
    clock=pygame.time.Clock()

    screen=pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT)) #设置屏幕大小
    pygame.display.set_caption('Flappy Bird')  #设置标题
    while True:
        info = show()
        info=MainGame(info)
        GameOver(info)
def GameOver(info):
    global cursor
    bird,bird_x,bird_y,name , level , default,score=info
    first,second,third=search(conn=conn,name=name,score=score)
    while True:
        moving()
        screen.blit(bird , (bird_x , bird_y))
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.display.quit()
            if event.type==KEYDOWN and event.key==K_RETURN:
                return None

        font_=pygame.font.SysFont('arial',22,True)
        text=font_.render(first[0],True,(0,0,0))
        text1=font_.render(second[0],True,(0,0,0))
        text2=font_.render(third[0],True,(0,0,0))

        screen.blit(over,(50,50))
        screen.blit(order,(10,150))
        screen.blit(text , (130 , 150))
        screen.blit(text1 , (130 , 200))
        screen.blit(text2 , (130 , 247))
        level_show(font_pos=(210 , 152) , box_pos=(200 , 152 , 60 , 25) , active=str(first[1]) , message=str(first[1]),size=20)
        level_show(font_pos=(210 , 200) , box_pos=(200 , 200 , 60 , 25) , active=str(second[1]) , message=str(second[1]),size=20)
        level_show(font_pos=(210 , 245) , box_pos=(200 , 245 , 60 , 25) , active=str(third[1]) , message=str(third[1]),size=20)

        clock.tick(30)
        pygame.display.update()

def search(conn,name,score):
    id = cursor.execute("select count(*) from score").fetchone()[0] + 1
    cursor.execute("insert into score values(%d, '%s', %d);" % (id , name , score))
    alldata = cursor.execute("select * from score").fetchall()
    paihang = {}
    for i in range(len(alldata)):
        paihang[alldata[i][1]] = alldata[i][2]
    result = sorted(paihang.items() , key=lambda item: int(item[1]) , reverse=True)
    conn.commit()
    return result[0] , result[1] , result[2]


    return '1','2','3'
if __name__=='__main__':
    main()
    conn.close()
