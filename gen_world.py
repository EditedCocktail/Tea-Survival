def new_world(seed,il=[256,128,64,32,16,8,4,2]):
	from perlin import SimplexNoise
	import sys
	seed=str(seed)
	seed=sum([ord(i) for i in seed])
	print(seed)
	rgb=[]
	for l in il :
		for i in range(l):
			if len(rgb)<i+1:
				rgb.append([])
			for j in range(l):
				if len(rgb[i])<j+1:
					rgb[i].append([0,0,0])
				color=[random.randint(0,i+j)%256,0,0]
				for m in range(1,il[0]//l+1):
					for k in range(1,il[0]//l+1):
						try:
							rgb[i*m][j*k][0]+=color[0]
						except:
								print(i,j,m,k*m,j*k,l,len(rgb),len(rgb[i*m]))
								sys.exit()
								
							
	for i in rgb:
		i[j][0]//=len(il)
	for i in rgb:
		for j in range(len(rgb[0])):
			if i[j][0]*255%256<200:
				i[j]='grass'
			elif i[j][0]*255%256<256:
				i[j]='water'
			
	return rgb

from math import sqrt
import random
def new_world2(il=[32]):
	from random import randint
	map=[['grass' for i in range(il[0])] for j in range(il[0])]
	
	for i in range(random.randint(0,len(map[0])**2//128)):
		x,y=random.randint(0,len(map[0])),random.randint(0,len(map[0]))
		size=10
		if x+size>len(map[0])-1 or y+size>len(map[0])-1:
			continue
		middle=(x+(size//2),y+(size//2))
		for i in range(size):
			for j in range(size):
				map[i+x][j+y]='water'
		for i in range(3):
			can=[[i+x,j+y] for i in range(size) for j in range(size) if map[i+x+1][j+y]!="water" or map[i+x-1][j+y]!="water" or map[i+x][j+y+1]!="water" or map[i+x][j+y-1]!="water"]
			for i in can:
				if random.randint(1,100)<50:
					map[i[0]][i[1]]='grass'
	return map
		
if __name__=='__main__':
	print(new_world2(il=[256]))
	#print(random.gauss(1,1))
	