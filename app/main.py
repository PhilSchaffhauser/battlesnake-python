from Astar import *
import bottle
import os
import random

#fuck the polic - phile

@bottle.route('/')
def static():
    return "the server is running"


@bottle.route('/static/<path:path>')
def static(path):
    return bottle.static_file(path, root='static/')

def init(data):
    grid = [[0 for col in xrange(data['height'])] for row in xrange(data['width'])]
    ourID = data['you']
    #food = []
    for snek in data['snakes']:
        if snek['id'] == ourID:
            kurt = snek
        for coord in snek['coords']:
            grid[coord[0]][coord[1]] = SNAKE

    for f in data['food']:
        grid[f[0]][f[1]] = FOOD
        #food.append((f[0],f[1]))


    return kurt, grid

def distance(p, q):
    dx = abs(p[0] - q[0])
    dy = abs(p[1] - q[1])
    return dx + dy;

def direction(from_cell, to_cell):
    dx = to_cell[0] - from_cell[0]
    dy = to_cell[1] - from_cell[1]

    if dx == 1:
        return 'left'
    elif dx == -1:
        return 'right'
    elif dy == -1:
        return 'down'
    elif dy == 1:
        return 'up'




@bottle.post('/start')
def start():
    data = bottle.request.json
    game_id = data.get('game_id')
    board_width = data.get('width')
    board_height = data.get('height')

    head_url = '%s://%s/static/head.png' % (
        bottle.request.urlparts.scheme,
        bottle.request.urlparts.netloc
    )


    # TODO: Do things with data

    return {
        'color': '#00FF00',
        'taunt': '{} ({}x{})'.format(game_id, board_width, board_height),
        'head_url': head_url
    }


@bottle.post('/move')
def move():
    data = bottle.request.json
    print("FUCK")
    kurt, grid = init(data)

    snek_head = kurt['coords'][0]
    snek_coords = kurt['coords']
    path = None

    foods = sorted(data['food'], key = lambda p: distance(p,snek_head))

    path = a_star(snek_head, food[0], grid, snek_coords)
    print(path)
    if not path:
        path = a_star(snek_head, snek_coords[-1], grid, snek_coords)
        

    # TODO: Do things with data
    
    return {
        'move': direction(path[0], path[1])
        'taunt': 'battlesnake-python!'
    }


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug = True)
