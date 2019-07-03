import pygame
pygame.init()

box_pro=0.3  #设置道具的爆率
distance_=400 #默认管道距离
box_time=600 #道具持续时间 600 == 6秒
easy=4  #关卡简单
commont=7 #g一般
difficult=10 #困难
slowed=3 #道具减速多少
#设置多种背景，可以在picture那里 设置名为bg+数字.png  格式，要顺序

def load(url='picture/',name='',type='.png'):
    return pygame.image.load(url+str(name)+type)
def load_music(url='void/',name='',type='.ogg'):
    return pygame.mixer.Sound(url+str(name)+type)
Num={}
for i in range(10):
    Num[i]=load(name=i)
bg=[]
for i in range(10):
    index='picture/'+str(i)+'.png'
    try:
        bg.append(load(name='bg'+str(i)))
    except:
        pass
message=load(name='message')
bird_c={}
bird_c['red']=load(name='red')
yellow__=load(name='yellow')
bird_c['yellow']=pygame.transform.scale(yellow__,(40,30))
blue__=load(name='blue')
bird_c['blue']=pygame.transform.scale(blue__,(37,26))
# bird={}
# bird['red']=[load(name='red_up'),load(name='red_down')]
# bird['blue']=[load(name='blue_up'),load(name='blue_down')]
# bird['yellow']=[load(name='yellow_up'),load(name='yellow_down')]

pipe={}
green=load(name='pipe_green')
pipe['green']=[green,pygame.transform.rotate(green,180)]
red=load(name='pipe_red')
pipe['red']=[red,pygame.transform.rotate(red,180)]
score_group={}
for i in range(10):
    score_group[str(i)]=load(name=str(i))
move=load(name='mov')
order=load(name='orderable')
over=load(name='gameover')
box=load(name='box')
dict_={'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10, '十一': 11, '十二': 12}



#加载音乐
music_ogg={}
music_wav={}
music_wav['die']=load_music(name='die',type='.wav')
music_wav['point']=load_music(name='point',type='.wav')
music_wav['hit']=load_music(name='hit',type='.wav')
music_wav['wing']=load_music(name='wing',type='.wav')
music_ogg['die']=load_music(name='die')
music_ogg['hit']=load_music(name='hit')
music_ogg['point']=load_music(name='point')
music_ogg['wing']=load_music(name='wing')
if __name__=='__main__':
    pass
