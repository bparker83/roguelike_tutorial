import libtcodpy as libtcod

from entity import Entity
from fov_functions import initialize_fov, recompute_fov
from input_handlers import handle_keys
from render_functions import clear_all, render_all
from map_objects.game_map import GameMap

def main():
	# screen dimensions
	SCREEN_WIDTH = 80
	SCREEN_HEIGHT = 50
	# map dimensions
	MAP_WIDTH = 80
	MAP_HEIGHT = 45
	# room dimensions and count
	ROOM_MAX_SIZE = 10
	ROOM_MIN_SIZE = 6
	MAX_ROOMS = 30
	# field of view settings
	FOV_ALGORITHM = 0
	FOV_LIGHT_WALLS = True
	FOV_RADIUS = 10
	# define tile colors
	colors = {
		'dark_wall': libtcod.Color(0, 0, 100),
		'dark_ground': libtcod.Color(50, 50, 150),
		'light_wall': libtcod.Color(130, 110, 50),
		'light_ground': libtcod.Color(200, 180, 50)
	}
	# create player
	player = Entity(int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2), '@', libtcod.white)
	# create npc
	npc = Entity(int(SCREEN_WIDTH / 2 - 5), int(SCREEN_HEIGHT / 2), '@', libtcod.yellow)
	# create entity list
	entities = [npc, player]
	# set font
	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	# create screen
	libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'libtcod tutorial revised', False)
	# create console
	con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
	# create game map
	game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
	game_map.make_map(MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAP_WIDTH, MAP_HEIGHT, player)
	# define field of view recompute trigger
	fov_recompute = True
	# create field of view map
	fov_map = initialize_fov(game_map)
	# create keybord input
	key = libtcod.Key()
	# create mouse input
	mouse = libtcod.Mouse()
	# game loop
	while not libtcod.console_is_window_closed():
		# listen for events
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
		# recompute field of view
		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGORITHM)
		# render entities
		render_all(con, entities, game_map, fov_map, fov_recompute, SCREEN_WIDTH, SCREEN_HEIGHT, colors)
		# reset field of view recompute trigger
		fov_recompute = False
		# update screen
		libtcod.console_flush()
		# clear entities
		clear_all(con, entities)
		# handle keyboard events
		action = handle_keys(key)
		# get dictionary value
		move = action.get('move')
		exit = action.get('exit')
		fullscreen = action.get('fullscreen')
		# handle dictionary value
		if move:
			dx, dy = move
			if not game_map.is_blocked(player.x + dx, player.y + dy):
				# move player
				player.move(dx, dy)
				# trigger field of view recompute
				fov_recompute = True
		if exit:
			return True
		if fullscreen:
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
	
if __name__ == '__main__':
	main()
