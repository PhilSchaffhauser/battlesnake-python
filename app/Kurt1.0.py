import bottle
import os
import random


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

SNAKE = 1
FOOD = 3
directions = ['up', 'down', 'left', 'right']

def checkUp(kurt, grid, data):
	head = kurt['coords'][0]
	body = kurt['coords']
	print(body)
	futureMove = [head[0], head[1]-1]
	for coord in body:
		if futureMove == coord:
			return False
	for snake in data['snakes']:
		for coord in snake['coords']:
			if futureMove == coord:
				return false
			if futureMove ==wall:
				return false
	if futureMove[1] < 0:
		return False
	return True

def checkLeft(kurt, grid, data):
	head = kurt['coords'][0]
	body = kurt['coords']
	futureMove = [head[0]-1, head[1]]
	for coord in body:
		if futureMove == coord:
			return False
	for snake in data['snakes']:
		for coord in snake['coords']:
			if futureMove == coord:
				return false
			if futureMove ==wall:
				return false
	if futureMove[0] < 0:
		return False
	return True

def checkRight(kurt, grid, data):
	head = kurt['coords'][0]
	body = kurt['coords']
	futureMove = [head[0]+1, head[1]]
	for coord in body:
		if futureMove == coord:
			return False
	for snake in data['snakes']:
		for coord in snake['coords']:
			if futureMove == coord:
				return false
			if futureMove ==wall:
				return false

	if futureMove[0] > 14:
		return False
	return True

def checkDown(kurt, grid, data):
	head = kurt['coords'][0]
	body = kurt['coords']
	futureMove = [head[0], head[1]+1]
	for coord in body:
		if futureMove == coord:
			return False
		if futureMove ==wall:
				return false
	for snake in data['snakes']:
		for coord in snake['coords']:
			if futureMove == coord:
				return false

	if futureMove[1] > 14:
		return False
	return True

def noKill(kurt, grid, data):
	legal = []
	if checkUp(kurt, grid, data):
		legal.append('up')
	if checkLeft(kurt, grid, data):
		legal.append('left')
	if checkRight(kurt, grid, data):
		legal.append('right')
	if checkDown(kurt, grid, data):
		legal.append('down')
	print(legal)
	if legal:
		return legal
	return 'down'

def closestFood(kurt, data):
	head = kurt['coords'][0]
	foodList = []
	minDist = 10000
	minCoord = None
	for food in data['food']:
		print(food)
		print(head)
		kurtDistance = abs(food[0]-head[0]) + abs(food[1] - head[1])
		if kurtDistance < minDist:
			minDist = kurtDistance
			minCoord = food
	return minCoord 	

def goForFood(kurt, data):
	head = kurt['coords'][0]
	food = closestFood(kurt, data)
	kurtDistance = abs(food[0]-head[0]) + abs(food[1] - head[1])
	for otherSnake in data['snakes']:
		enemyHead = otherSnake['coords'][0]
		distance = abs(food[0]-enemyHead[0]) + abs(food[1] - enemyHead[1])
		if distance < kurtDistance:
			return False
			print(False)
	return True, food

def eat(kurt, data, legalMoves, foodCoords):
	head = kurt['coords'][0]
	dx = foodCoords[0] - head[0]
	dy = foodCoords[1] - head[1]
	print(dx)
	print(dy)
	if dx > 0:
		ourMove = 'right'
	elif dx < 0: 
		ourMove = 'left'
	elif dy > 0:
		ourMove = 'down'
	elif dy < 0:
		ourMove = 'up'
	else:
		ourmove = randbom.choice(legalMoves)
	if ourMove not in legalMoves:
		ourMove = random.choice(legalMoves)	
	return ourMove

def init(data):
    grid = [[0 for col in xrange(data['height'])] for row in xrange(data['width'])]
    ourID = data['you']
    for snek in data['snakes']:
        if snek['id'] == ourID:
            kurt = snek
        for coord in snek['coords']:
            grid[coord[0]][coord[1]] = SNAKE

    for f in data['food']:
        grid[f[0]][f[1]] = FOOD

    return kurt, grid

@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data['game_id']
    board_width = data['width']
    board_height = data['height']
    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )

    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url,
        'name': 'battlesnake-python'
    }


@bottle.post('/move')
def move():
    taunts = ['According to all know laws of aviation, there is no way a bee should be able to fly.'] 
    data = bottle.request.json
    kurt, grid = init(data)
    legalMoves = noKill(kurt, grid, data)
    ourMove = random.choice(legalMoves)
    getFood, foodCoords = goForFood(kurt, data)
    if getFood:
	ourMove = eat(kurt, data, legalMoves, foodCoords)
    # TODO: Do things with data
    return {
        'move': ourMove,
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()
if __name__ == '__main__':
    bottle.run(application, host=os.getenv('IP', '0.0.0.0'), port=os.getenv('PORT', '8080'))


