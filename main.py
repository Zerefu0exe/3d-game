import pygame, map
from math import sin, cos, pi

pygame.init()

nScreenWidth, nScreenHeight = 640, 360
fPlayerX, fPlayerY, fPlayerA = 2.0, 2.0, 0.0
fViewingAngle, fDepth = pi / 3.0, 30.0
bRunGame = True

sc = pygame.display.set_mode((nScreenWidth, nScreenHeight))
pygame.display.set_caption('3D Game')

nTp1 = pygame.time.get_ticks()
nTp2 = pygame.time.get_ticks()

def timeClock():
  global nTp1, nTp2, fElapsedTime

  nTp2 = pygame.time.get_ticks()
  fElapsedTime = float(nTp2 - nTp1)
  nTp1 = nTp2
  print(fElapsedTime)

def exit():
  global bRunGame
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT: bRunGame = False

def normalize(i, size):
  if int(i) >= size: return size - 1
  elif int(i) <= 0: return 0
  else: return int(i)

def move():
  global fPlayerX, fPlayerY, fPlayerA, fElapsedTime
  
  keys = pygame.key.get_pressed()
  if keys[pygame.K_a]: fPlayerA -= 1.5 * fElapsedTime
  if keys[pygame.K_d]: fPlayerA += 1.5 * fElapsedTime
  if keys[pygame.K_w]:
    fPlayerX += sin(fPlayerA) * 5.0 * fElapsedTime
    fPlayerY += cos(fPlayerA) * 5.0 * fElapsedTime

    if map.aMap[normalize(fPlayerY, map.nMapHeight), normalize(fPlayerX, map.nMapWidth)] == '#':
      fPlayerX -= sin(fPlayerA) * 5.0 * fElapsedTime
      fPlayerY -= cos(fPlayerA) * 5.0 * fElapsedTime

def shadeWall(fDistanceToWall):
  global fDepth

  if fDistanceToWall <= fDepth / 3.0: return (255, 255, 255)
  elif fDistanceToWall < fDepth / 2.0: return (192, 192, 192)
  elif fDistanceToWall < fDepth / 1.5: return (128, 128, 128)
  elif fDistanceToWall < fDepth: return (64, 64, 64)
  else: return (0, 0, 0)

def shadeFloor(nY):
  global nScreenHeight

  fB = 1.0 - ((float(nY) - nScreenHeight / 2) / (nScreenHeight / 2))
  if fB < 0.25: return (254, 254, 254)
  elif fB < 0.5: return (191, 191, 191)
  elif fB < 0.75: return (127, 127, 127)
  elif fB < 0.9: return (63, 63, 63)
  else: return (0, 0, 0)

def drawPicture():
  global nScreenWidth, nScreenHeight
  global fViewingAngle, fDepth
  global fPlayerX, fPlayerY, fPlayerA
  
  sc.fill((0, 0, 0))
  
  for nX in range(nScreenWidth):
    fRayAngle = fPlayerA - fViewingAngle / 2.0 + (nX / nScreenWidth) * fViewingAngle
    fDistanceToWall = 0.0
    bHitWall = False

    fEyeX = sin(fRayAngle)
    fEyeY = cos(fRayAngle)

    while not bHitWall and fDistanceToWall < fDepth:
      fDistanceToWall += 0.1

      nTestX = int(fPlayerX + fEyeX * fDistanceToWall)
      nTestY = int(fPlayerY + fEyeY * fDistanceToWall)
      
      if nTestX < 0 or nTestX >= map.nMapWidth or nTestY < 0 or nTestY >= map.nMapHeight:
        bHitWall = True
        fDistanceToWall = fDepth
      elif map.aMap[nTestY, nTestX] == '#':
        bHitWall = True
    
    nCeiling = int(nScreenHeight / 2 - float(nScreenHeight) / fDistanceToWall)
    nFloor = nScreenHeight - nCeiling

    for nY in range(nScreenHeight):
      if nY <= nCeiling:
        pygame.draw.rect(sc, (0, 0, 0), (nX, nY, 1, 1))
      elif nY > nCeiling and nY <= nFloor:
        pygame.draw.rect(sc, shadeWall(fDistanceToWall), (nX, nY, 1, 1))
      else:
        pygame.draw.rect(sc, shadeFloor(nY), (nX, nY, 1, 1))
  
  pygame.display.update()

while bRunGame:
  timeClock()
  exit()  
  move()
  drawPicture()
  
pygame.quit()