#import allows us to use the modules from the pygame framework
import pygame, sys
from pygame.locals import *

#Number of frames per second, we can change this to speed up or slow down the game
FPS = 200

#in the moveBall function instead of it moving its location by 1 your'e moving it by 5
#modified AI paddle so it wouldn't be too slow to hit the ball
INCREASESPEED = 5

#Global Variables used throughout the whole program
WINDOWWIDTH = 400
WINDOWHEIGHT = 300
LINETHICKNESS = 10
PADDLESIZE = 50
PADDLEOFFSET = 20

#Setting up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Draws Arena game is played on
def drawArena():
	DISPLAYSURF.fill((0, 0, 0))

	#Draw outline of arena
	#pygame.Rect(X-coord, Y-coord, Width of Rect, Length of Rect), (Linethickness)
	pygame.draw.rect(DISPLAYSURF, WHITE, ((0,0), (WINDOWWIDTH, WINDOWHEIGHT)),
		LINETHICKNESS*2)

	#Draw center line
	#pygame.draw.line(Starting coordinates, end coordinates)
	pygame.draw.line(DISPLAYSURF, WHITE, ((WINDOWWIDTH/2),0), ((WINDOWWIDTH/2),
		WINDOWHEIGHT), (LINETHICKNESS/4))

#Draws Paddle
def drawPaddle(paddle):
	#Stops paddle going too low
	if paddle.bottom > WINDOWHEIGHT - LINETHICKNESS:
		paddle.bottom = WINDOWHEIGHT - LINETHICKNESS

	#Stops paddle going too high
	elif paddle.top < LINETHICKNESS:
		paddle.top = LINETHICKNESS

	#Draw paddle
	pygame.draw.rect(DISPLAYSURF, WHITE, paddle)


#Draw the ball
def drawBall(ball):
	pygame.draw.rect(DISPLAYSURF, WHITE, ball)


#moves ball to new position
def moveBall(ball, ballDirX, ballDirY):
	ball.x += ballDirX
	ball.y += ballDirY
	return ball


#checks for collision with a wall and bounces off of it, returns new direction
def checkEdgeCollision(ball, ballDirX, ballDirY):
	if ball.top == (LINETHICKNESS) or ball.bottom == (WINDOWHEIGHT - LINETHICKNESS):
		ballDirY = ballDirY * -1

	if ball.left == (LINETHICKNESS) or ball.right == (WINDOWWIDTH - LINETHICKNESS):
		ballDirX = ballDirX * -1

	return ballDirX, ballDirY

#Checks if ball hit a paddle
def checkHitBall(ball, paddle1, paddle2, ballDirX):
	if ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
		return -1

	elif ballDirX == 1 and paddle2.left == ball.right and paddle2.top < ball.top and paddle2.bottom > ball.bottom:
		return -1

	else: return 1




#Computer Player
def artificialIntelligence(ball, ballDirX, paddle2):
	#if ball is moving away from paddle, center it
	if ballDirX == -1:
		if paddle2.centery < (WINDOWHEIGHT/2):
			paddle2.y += INCREASESPEED

		elif paddle2.centery > (WINDOWHEIGHT/2):
			paddle2.y -= INCREASESPEED

	#if ball is moving towards paddle, track it
	elif ballDirX == 1:
		if paddle2.centery < ball.centery:
			paddle2.y += INCREASESPEED
		else:
			paddle2.y -= INCREASESPEED

	return paddle2


#Score
def checkPointScored(paddle1, ball, score, ballDirX):
	#reset points if left wall is hit
	if ball.left == LINETHICKNESS:
		return 0
	#2 points for hitting the ball
	elif ballDirX == -1 and paddle1.right == ball.left and paddle1.top < ball.top and paddle1.bottom > ball.bottom:
		score += 2
		return score
	#5 points for beating paddle2
	elif ball.right == WINDOWWIDTH - LINETHICKNESS:
		score += 5
		return score
	#no points, return same score
	else: return score

def displayScore(score):
	resultSurf = BASICFONT.render('Score = %s' %(score), True, WHITE)
	resultRect = resultSurf.get_rect()
	resultRect.topleft = (WINDOWWIDTH - 125, 25)
	DISPLAYSURF.blit(resultSurf, resultRect)



#MAIN FUNCTION
def main():

	#needed to initialize the use of all the modules in pygame
	pygame.init()
	global DISPLAYSURF
	global BASICFONT, BASICFONTSIZE
	BASICFONTSIZE = 20
	BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

	#We want to set the frame rate ourselves rather than letting the program
	#run as fast as it wants
	FPSCLOCK = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	pygame.display.set_caption('Tuli\'s Pong')


	#Set starting positions
	ballX = WINDOWWIDTH/2 - LINETHICKNESS/2
	ballY = WINDOWHEIGHT/2 - LINETHICKNESS/2
	playerOnePosition = (WINDOWHEIGHT - PADDLESIZE)/2
	playerTwoPosition = (WINDOWHEIGHT - PADDLESIZE)/2
	score = 0

	#Tracks ball direction
	ballDirX = -1 ## -1 = left 1 = right
	ballDirY = -1 ## -1 = up 1 = down

	#create rectangles for ball and paddles
	#pygame.Rect(X-coord, Y-coord, Width of Rect, Length of Rect)
	paddle1 = pygame.Rect(PADDLEOFFSET, playerOnePosition, LINETHICKNESS, PADDLESIZE)
	paddle2 = pygame.Rect(WINDOWWIDTH - PADDLEOFFSET - LINETHICKNESS, 
		playerTwoPosition, LINETHICKNESS, PADDLESIZE)
	ball = pygame.Rect(ballX, ballY, LINETHICKNESS, LINETHICKNESS)

	#Draws starting position of the arena
	drawArena()
	drawPaddle(paddle1)
	drawPaddle(paddle2)
	drawBall(ball)

	#makes cursor invisible
	pygame.mouse.set_visible(0)
	#main game loop that'll keep running until the game is quit
	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()

			#mouse movement
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
				paddle1.y = mousey

		drawArena()
		drawPaddle(paddle1)
		drawPaddle(paddle2)
		drawBall(ball)

		ball = moveBall(ball, ballDirX, ballDirY)
		ballDirX, ballDirY = checkEdgeCollision(ball, ballDirX, ballDirY)
		score = checkPointScored(paddle1, ball, score, ballDirX)
		ballDirX = ballDirX * checkHitBall(ball, paddle1, paddle2, ballDirX)

		paddle2 = artificialIntelligence(ball, ballDirX, paddle2)

		displayScore(score)

		pygame.display.update()
		FPSCLOCK.tick(FPS)



if __name__=='__main__':
	main()


