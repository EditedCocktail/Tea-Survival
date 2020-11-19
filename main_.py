import pygame as p
import random,datetime
import pygame.gfxdraw
import sys
from random import *
from pygame.locals import *
import pythonforandroid as p4a
import time
from math import atan2, degrees, cos, sin, radians
from math import *
sys.setrecursionlimit(5000)
root=p.display.set_mode((2000,700))
p.init()
from PIL import Image
import gen_world
#Изображения
images={
'stone-axe':p.image.load('Images/tool_0000.png'),
'stone-pick':p.image.load('Images/tool_0001.png'),
'grass':p.transform.scale(p.image.load('Images/grass.png'),(128,128)),
'black-screen':p.image.load('Images/black.png'),
'white0':p.image.load('Images/white0.png'),
'white1':p.image.load('Images/white1.png'),
'tree':p.image.load('Images/tree1.png'),
'water':p.image.load('Images/water.png'),
'settings':p.image.load('Images/settings.png'),
'pause':p.image.load('Images/pause.png'),
'arrowleft':p.transform.scale(p.image.load('Images/goleft.png'),(128,128)),
'arrowright':p.transform.scale(p.image.load('Images/goright.png'),(128,128)),
'arrowup':p.transform.scale(p.image.load('Images/goup.png'),(128,128)),
'arrowdown':p.transform.scale(p.image.load('Images/godown.png'),(128,128)),
'secret0':p.transform.scale(p.image.load('Images/secret1.png'),(128,128)),
'secret1':p.transform.scale(p.image.load('Images/secret2.png'),(128,128))}
locate='main'
__version__='0.0.2'

class Joystick:
	def __init__(self, x, y, r, color, stick_color):
		self.is_move = False
		self.color = color
		self.stick_color = stick_color
		self.x = x
		self.y = y
		self.r = r
		self.stick_r = r // 3
		self.stick_x = x
		self.stick_y = y
	
	def _move_stick(self, x, y):
		distance = abs(self.x - x) + abs(self.y - y)
		if(distance > self.r):
			distance = self.r
		
		self.stick_x = int(self.x + distance * cos(radians(self.angle)))
		self.stick_y = int(self.y + distance * sin(radians(self.angle)))
	
	
	def _find_angle(self, x, y):
		delta = [1,0]
		
		vector=[self.x-x, self.y-y]
		#print('mouse pos',(x,y),'angle',degrees(atan2(delta[0] * vector[1] + delta[1] * vector[0], delta[0] * vector[0] - delta[1] * vector[1])),'vectors',vector)
		self.angle = degrees(atan2(delta[0] * vector[1] + delta[1] * vector[0], delta[0] * vector[0] - delta[1] * vector[1]))
		self.angle -= 180
	
	def draw(self, surface):
		pygame.draw.circle(surface, self.color, (self.x, self.y), self.r)
		pygame.draw.circle(surface, self.stick_color, (self.stick_x, self.stick_y), self.stick_r)
	
	
	def on_touch(self, event):
		if(event.type == MOUSEBUTTONDOWN):
			x, y = list(map(int, pygame.mouse.get_pos()))
			if(abs(self.stick_x - x) + abs(self.stick_y - y) <= self.stick_r):
				self.is_move = True
			else:
				self.is_move = False
			return x,y
		elif(event.type == MOUSEMOTION):
			if(self.is_move):
				x, y = list(map(int, pygame.mouse.get_pos()))
				
				self._find_angle(x, y)
				self._move_stick(x, y)
				
				return x,y
		elif(event.type == MOUSEBUTTONUP):
			self.is_move = False
			self.stick_x = self.x
			self.stick_y = self.y
			return 0,0
		return 0,0
			
	@property
	def distance(self):
		return abs(self.x - self.stick_x) + abs(self.y - self.stick_y)
j=Joystick(root.get_width()-(root.get_width()-100),root.get_height()-100,100,(25,255,255),(255,255,255))
class Button():
	def __init__(self,fromc,toc,loc,code):
		self.rect=[fromc,toc]
		self.loc=loc
		self.code=code
	def collide(self,point):
		#if point in self.rect: но без создания двумерного списка)
		if point[0]>self.rect[0][0]-1 and point[0]<self.rect[1][0]-1 and point[1]>self.rect[0][1]-1 and point[1]<self.rect[1][1]-1:
			return 1
		return 0
	def result(self):
		exec(self.code)

class Tile():
	def __init__(self,breaktime,tool,place,name,speed=1):
		self.breaktime=breaktime
		self.place=place
		self.tool=tool
		self.speed=speed
		self.name=name
tiles={
'tree':Tile(30,'axe',{'x':0,'y':-128},'tree'),
'grass':Tile(10,'shovel',{'x':0,'y':0},'grass'),
'water':Tile(-1,'bucket',{'x':0,'y':0},"water",0.3)}
class World():
	def gen_plants(self):
		for i in range(len(self.map)):
			for j in range(len(self.map[i])-1,0,-1):
				if self.map[i][j]==tiles['grass']:
					if randint(0,10)==10:
						self.builds.append([i*128,j*128,tiles['tree']])
						
	def __init__(self,name,map=[],players={},builds=[]):
		self.name=name
		self.map=[[tiles[i]  for i in j] for j in map]
		self.builds=[]
		self.players=players
		self.gen_plants()
def player(string):
	return globals()['pl'].world.players[string]
worlds=[]

class Source():
	locate='main'
	world=0
	name='coctail'
	language='en'

class shrift():
	def __init__(self,size):
		self.font=p.font.SysFont("dejavusans",size)
	def size(self,text):
		return self.font.size(text)
	def render(self,text,color):
		return self.font.render(text,1,color)

pl=Source()
he='white'
if pl.name=='coctail':
	he='secret'
anim=images[he+"0"]
plus=[10,0]
count=0
inp=[0,'']

class Player():
	def __init__(self,hp,maxhp,attack,critchance,x,y,inventory=[],name='tea'):
		self.hp=hp
		self.maxhp=maxhp
		self.attack=attack
		self.inventory=inventory
		self.x,self.y=x,y
		self.spawn=[256,256]
		self.name=name
		self.counter=0
		self.anim=images[he+"0"]
	def regen(self,count):
		if not count+self.hp>self.maxhp:
			return exec('self.hp+=count')
		self.hp=self.maxhp

# Хранение дизайна :3
def main():
	global count,plus,inp,game,world
	def new_world():
		global locs
		seed=locs['main-create-world'][-1][3]
	game=0
	if pl.language=='ru':
		locs={
		'main':
			[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+
			[[root.get_width()//2-(shrift(100).size('Tea Survival')[0])//2,root.get_height()//5,shrift( 100).render('Tea Survival',(20,255,255))],
			[root.get_width()//2+(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],
			[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],
			[root.get_width()//2-shrift(75).size('Сервера')[0]//2,root.get_height()//5+100,shrift(75).render('Сервера',(25,255,255))],
			[root.get_width()//2-shrift(75).size('Локал')[0]//2,root.get_height()//5+200,shrift(75).render('Локал',(25,255,255))],[0,root.get_height()-70,shrift( 70).render('Выход',(20,255,255))],[500,100,images['white0']]],
		'main-exit':
			[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+
			[[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,shrift( 100).render('Tea Survival',(20,255,255))],
			[root.get_width()//2+(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],
			[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],
			[root.get_width()//2-shrift(75).size('Сервера')[0]//2,root.get_height()//5+100,shrift(75).render('Сервера',(25,255,255))],
			[root.get_width()//2-shrift(75).size('Локал')[0]//2,root.get_height()//5+200,shrift(75).render('Локал',(25,255,255))],
			[0,root.get_height()-70,shrift( 70).render('Выход',(20,255,255))],[root.get_width()//2-250,0,p.transform.scale(images['black-screen'],(500,root.get_height()))],[root.get_width()//2-200,100,shrift(50).render('Вы точно хотите выйти?',(20,255,255))],[root.get_width()//2-200,root.get_height()//2,shrift(50).render('Да',(255,0,0))],[root.get_width()//2+50,root.get_height()//2,shrift(50).render('Нет',(0,255,0))]],
		'main-player':[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,shrift( 100).render('Tea Survival',(20,255,255))],[root.get_width()//2+(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-shrift(75).size('Сервера')[0]//2,root.get_height()//5+100,shrift(75).render('Сервера',(25,255,255))],[root.get_width()//2-shrift(75).size('Локал')[0]//2,root.get_height()//5+200,shrift(75).render('Локал',(25,255,255))],[0,root.get_height()-70,shrift( 70).render('Выход',(20,255,255))],[root.get_width()//2-250,0,p.transform.scale(images["black-screen"],(500,root.get_height()))],[root.get_width()//2-shrift(50).size('Чайные миры')[0]//2,50,shrift(50).render('Чайные миры',(25,255,255))],[root.get_width()//2-250,75,shrift(25).render('Закрыть',(0,255,0))],[root.get_width()//2-shrift(50).size('Создать новый мир')[0]//2,root.get_height()-100,shrift(50).render('Создать новый мир',(25,255,255))]]+[[root.get_width()//2-256,(i+1)*128,shrift(128).render(worlds[i].name,(25,255,255))] for i in range(len(worlds))],
		"main-create-world":[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,shrift( 100).render('Tea Survival',(20,255,255))],[root.get_width()//2+(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-shrift(75).size('Сервера')[0]//2,root.get_height()//5+100,shrift(75).render('Сервера',(25,255,255))],[root.get_width()//2-shrift(75).size('Локал')[0]//2,root.get_height()//5+200,shrift(75).render('Локал',(25,255,255))],[0,root.get_height()-70,shrift( 70).render('Выход',(20,255,255))],[root.get_width()//2-256,0,p.transform.scale(images["black-screen"],(512,root.get_height()))],[root.get_width()//2-256,100,shrift(50).render('Название:',(25,255,255))],[root.get_width()//2-shrift(75).size("Создание мира")[0]//2,20,shrift(50).render('Создание мира',(25,255,255))],[root.get_width()//2-256,root.get_height()-100,shrift(75).render('Создать',(0,255,0))],[root.get_width()//2-256+shrift(50).size('Название:')[0]+20,110,shrift(30).render(str(randint(10000,100000)),(25,255,255)),'']],'game':[(0,0,p.transform.scale(images['pause'],(128,128)))],
		'main-settings':[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+
		[[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,shrift( 100).render('Tea Survival',(20,255,255))],
		[root.get_width()//2+(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],
		[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],
		[root.get_width()//2-shrift(75).size('Сервера')[0]//2,root.get_height()//5+100,shrift(75).render('Сервера',(25,255,255))],
		[root.get_width()//2-shrift(75).size('Локал')[0]//2,root.get_height()//5+200,shrift(75).render('Локал',(25,255,255))],[0,root.get_height()-70,shrift( 70).render('Выход',(20,255,255))]]}
	elif pl.language=='en':
		locs={
		'main':
			[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+
			[[root.get_width()//2-(shrift(100).size('Tea Survival')[0])//2,root.get_height()//5,shrift( 100).render('Tea Survival',(20,255,255))],
			[root.get_width()//2+(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],
			[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],
			[root.get_width()//2-shrift(75).size('Servers')[0]//2,root.get_height()//5+100,shrift(75).render('Servers',(25,255,255))],
			[root.get_width()//2-shrift(75).size('Локал')[0]//2,root.get_height()//5+200,shrift(75).render('Local',(25,255,255))],[0,root.get_height()-70,shrift( 70).render('Exit',(20,255,255))],[500,100,images['white0']]],
		'main-exit':
			[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+
			[[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,shrift( 100).render('Tea Survival',(20,255,255))],
			[root.get_width()//2+(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],
			[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],
			[root.get_width()//2-shrift(75).size('Servers')[0]//2,root.get_height()//5+100,shrift(75).render('Servers',(25,255,255))],
			[root.get_width()//2-shrift(75).size('Local')[0]//2,root.get_height()//5+200,shrift(75).render('Local',(25,255,255))],
			[0,root.get_height()-70,shrift( 70).render('Exit',(20,255,255))],[root.get_width()//2-250,0,p.transform.scale(images['black-screen'],(500,root.get_height()))],[root.get_width()//2-200,100,shrift(50).render('Do you realy wanna exit?',(20,255,255))],[root.get_width()//2-200,root.get_height()//2,shrift(50).render('Yes',(255,0,0))],[root.get_width()//2+50,root.get_height()//2,shrift(50).render('No',(0,255,0))]],
		'main-player':[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,shrift( 100).render('Tea Survival',(20,255,255))],[root.get_width()//2+(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-shrift(75).size('Servers')[0]//2,root.get_height()//5+100,shrift(75).render('Servers',(25,255,255))],[root.get_width()//2-shrift(75).size('Local')[0]//2,root.get_height()//5+200,shrift(75).render('Local',(25,255,255))],[0,root.get_height()-70,shrift( 70).render('Exit',(20,255,255))],[root.get_width()//2-250,0,p.transform.scale(images["black-screen"],(500,root.get_height()))],[root.get_width()//2-shrift(50).size('Tea worlds')[0]//2,50,shrift(50).render('Tea worlds',(25,255,255))],[root.get_width()//2-250,75,shrift(25).render('Exit',(0,255,0))],[root.get_width()//2-shrift(50).size('Create new world')[0]//2,root.get_height()-100,shrift(50).render('Create new world',(25,255,255))]]+[[root.get_width()//2-256,(i+1)*128,shrift(128).render(worlds[i].name,(25,255,255))] for i in range(len(worlds))],
		"main-create-world":[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+[[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,shrift( 100).render('Tea Survival',(20,255,255))],[root.get_width()//2+(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],[root.get_width()//2-shrift(75).size('Servers')[0]//2,root.get_height()//5+100,shrift(75).render('Servers',(25,255,255))],[root.get_width()//2-shrift(75).size('Local')[0]//2,root.get_height()//5+200,shrift(75).render('Local',(25,255,255))],[0,root.get_height()-70,shrift( 70).render('Exit',(20,255,255))],[root.get_width()//2-256,0,p.transform.scale(images["black-screen"],(512,root.get_height()))],[root.get_width()//2-256,100,shrift(50).render('Name: ',(25,255,255))],[root.get_width()//2-shrift(75).size('World creator')[0]//2,20,shrift(50).render('World creator',(25,255,255))],[root.get_width()//2-256,root.get_height()-100,shrift(75).render('Create',(0,255,0))],[root.get_width()//2-256+shrift(50).size('Name: ')[0]+20,110,shrift(30).render(str(randint(10000,100000)),(25,255,255)),'']],'game':[(0,0,p.transform.scale(images['pause'],(128,128)))],
		'main-settings':[[i*128,j*128,images['grass']] for i in range(0,root.get_width()//128+1) for j in range(0,root.get_height()//128+1)]+
		[[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,shrift( 100).render('Tea Survival',(20,255,255))],
		[root.get_width()//2+(shrift( 100).size('Tea Survival')[0])//2,root.get_height()//5,p.transform.scale(images['stone-axe'],(128,128))],
		[root.get_width()//2-(shrift( 100).size('Tea Survival')[0])//2-128,root.get_height()//5,p.transform.scale(p.transform.flip(images['stone-pick'],1,0),(128,128))],
		[root.get_width()//2-shrift(75).size('Сервера')[0]//2,root.get_height()//5+100,shrift(75).render('Servers',(25,255,255))],
		[root.get_width()//2-shrift(75).size('Local')[0]//2,root.get_height()//5+200,shrift(75).render('Local',(25,255,255))],[0,root.get_height()-70,shrift( 70).render('Exit',(20,255,255))]]}

	buttons=[Button([0,root.get_height()-70],[shrift( 70).size('Выход')[0],root.get_height()],'main','pl.locate="main-exit"'),Button((root.get_width()//2-200,root.get_height()//2),(root.get_width()//2-100,root.get_height()+50),'main-exit','quit()'),Button((root.get_width()//2+50,root.get_height()//2),(root.get_width()//2+200,root.get_height()//2+50),'main-exit','pl.locate="main"'),Button((root.get_width()//2-shrift(75).size('Локал')[0]//2,root.get_height()//5+200),(root.get_width()//2+shrift(75).size('Локал')[0]//2,root.get_height()//5+275),'main','pl.locate="main-player"'),Button([root.get_width()//2-250,50],[root.get_width()//2-250+shrift(50).size("Закрыть")[0],100],'main-player','pl.locate="main"'),Button([root.get_width()//2-shrift(50).size("Создать новый мир")[0]//2,root.get_height()-120],[root.get_width()//2+shrift(50).size("Создать новый мир")[0]//2,root.get_height()-70],'main-player','pl.locate="main-create-world"'),Button([root.get_width()//2-256+shrift(50).size('Название:')[0]+10,100],[root.get_width()//2-256+shrift(50).size('Название:')[0]+200,150],'main-create-world','p.key.start_text_input();inp[0]=1'),Button([root.get_width()//2-256,root.get_height()-100],[root.get_width()//2-256+shrift(75).size('Создать')[0],root.get_height()],'main-create-world','worlds.append(World(inp[1],map=gen_world.new_world2(il=[256]),players={pl.name:Player(50,50,0,2,128*128,128*128,name=pl.name)}));pl.locate="main-player";main2();inp[1]=""'),Button([0,0],[128,128],'game','0')]+[Button([root.get_width()//2-256,(i+1)*128],[root.get_width()//2+256,(i+2)*128],'main-player',f'''
pl.world=worlds[{i}]
pl.locate="game"''') for i in range(len(worlds))]
	while 1:
		if pl.world==0:
			if pl.locate.startswith('main'):
				if plus[0]<0:
					plus
					locs[locate][-1][2]=images[f'{he}{count}']	
				else:
					locs[locate][-1][2]=p.transform.flip(images[f'{he}{count}'],1,0)
				if locs[locate][-1][1]+plus[1]>root.get_height():
					plus=[-randint(10,15),randint(10,15)]
					plus[1]=-plus[1]
				if locs[locate][-1][0]+plus[0]>root.get_width():
					plus=[randint(10,15),randint(10,15)]
					plus[0]=-plus[0]
					locs[locate][-1][2]=images[f'{he}{count}']
				if locs[locate][-1][0]+plus[0]<0:
					plus=[randint(10,15),randint(10,15)]
					locs[locate][-1][2]=p.transform.flip(images[f'{he}{count}'],1,0)
				if locs[locate][-1][1]+plus[1]<0:
					plus=[-plus[0],randint(10,15)]
					
				locs[locate][-1][0]=locs[locate][-1][0]+plus[0]
				locs[locate][-1][1]=locs[locate][-1][1]+plus[1]
				if count:
					count=0
				else:
					count=1
			for ev in p.event.get():
					#print(ev)
				
					if ev.type==QUIT:
						p.quit()
						quit()
					if ev.type==KEYUP and inp[0]:
						if ev.key==8:
							locs['main-create-world'][-1][2]=shrift(30).render(locs['main-create-world'][-1][3][:-1],(25,255,255))
							locs['main-create-world'][-1][3]=locs['main-create-world'][-1][3][:-1]
							inp[1]=locs['main-create-world'][-1][3][:-1]
					if ev.type==TEXTINPUT and inp[0]:
						locs['main-create-world'][-1][3]+=ev.text
						if not game:
							locs['main-create-world'][-1][2]=shrift(30).render(locs["main-create-world"][-1][3],(25,255,255))
							inp[1]=locs["main-create-world"][-1][3]
					if ev.type==MOUSEBUTTONDOWN:
						for button in [i for i in buttons if i.loc==pl.locate]:
							if button.collide(ev.pos):
								button.result()
		else:
			for button in [i for i in buttons if i.loc==pl.locate]:
				if button.collide(p.mouse.get_pos()):
					button.result()
			[root.blit(images[pl.world.map[i][j].name],(i*128-(player(pl.name).x), root.get_height()-(j*128-player(pl.name).y)))
    for i in range(player(pl.name).x//128-root.get_width()//128-2,player(pl.name).x//128+root.get_width()//128+2) 
    for j in range(player(pl.name).y//128-root.get_height()//128-2,player(pl.name).y//128+root.get_height()//128+2)]
#
			[root.blit(player(pl.name).anim,(root.get_width()//2-32,root.get_height()//2)) for i in pl.world.players ]
			[root.blit(shrift(25).render(pl.world.players[i].name,(25,255,255)),(root.get_width()//2,root.get_height()//2-30)) for i in pl.world.players]
			[root.blit(images[pl.world.builds[i][2].name],(pl.world.builds[i][0]+pl.world.builds[i][2].place['x']-player(pl.name).x,root.get_height()-(pl.world.builds[i][1]-player(pl.name).y))) for i in range(len(pl.world.builds))]
			j.draw(root)
			for i in pygame.event.get():
				j.on_touch(i)
			player(pl.name).x-=round(-(j.stick_x-j.x)/j.r*20*pl.world.map[player(pl.name).x//128][player(pl.name).y//128].speed)
			player(pl.name).y-=round((j.stick_y-j.y)/j.r*20*pl.world.map[player(pl.name).x//128][player(pl.name).y//128].speed)
	
			if round((j.stick_x-j.x)/j.r)!=0 or round(-(j.stick_y-j.y)/j.r)!=0:
			
				player(pl.name).counter+=1
				if (j.stick_x-j.x)/j.r>0:
					player(pl.name).anim=p.transform.flip(images[he+str(player(pl.name).counter%2)],1,0)
				else:
					player(pl.name).anim=images[he+str(player(pl.name).counter%2)]
			#print(round((j.stick_y-j.y)/j.r*20))к
		[root.blit(locs[pl.locate][i][2],locs[pl.locate][i][:2]) for i in range(0,len(locs[pl.locate]))]
		
		p.display.flip()
def main2():
	global root
	try:
		main()
	except Exception as e:
		print(e.with_traceback(e.__traceback__))
		root=p.display.set_mode(((2000,700)))
		main2()
main2()