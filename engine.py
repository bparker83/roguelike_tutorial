import libtcodpy as libtcod

from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys
from render_functions import clear_all, render_all, RenderOrder
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
	# monster settings
	MAX_MONSTERS_PER_ROOM = 3
	# define tile colors
	colors = {
		'dark_wall': libtcod.Color(0, 0, 100),
		'dark_ground': libtcod.Color(50, 50, 150),
		'light_wall': libtcod.Color(130, 110, 50),
		'light_ground': libtcod.Color(200, 180, 50)
	}
	# create player
	fighter_component = Fighter(hp=30, defense=2, power=5)
	player = Entity(0, 0, '@', libtcod.white ,'Player', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component)
	# create entity list
	entities = [player]
	# set font
	libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
	# create screen
	libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'libtcod tutorial revised', False)
	# create console
	con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
	# create game map
	game_map = GameMap(MAP_WIDTH, MAP_HEIGHT)
	game_map.make_map(MAX_ROOMS, ROOM_MIN_SIZE, ROOM_MAX_SIZE, MAP_WIDTH, MAP_HEIGHT, player, entities, MAX_MONSTERS_PER_ROOM)
	# define field of view recompute trigger
	fov_recompute = True
	# create field of view map
	fov_map = initialize_fov(game_map)
	# create keybord input
	key = libtcod.Key()
	# create mouse input
	mouse = libtcod.Mouse()
	# create game state
	game_state = GameStates.PLAYERS_TURN
	# game loop
	while not libtcod.console_is_window_closed():
		# listen for events
		libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
		# recompute field of view
		if fov_recompute:
			recompute_fov(fov_map, player.x, player.y, FOV_RADIUS, FOV_LIGHT_WALLS, FOV_ALGORITHM)
		# render entities
		render_all(con, entities, player, game_map, fov_map, fov_recompute, SCREEN_WIDTH, SCREEN_HEIGHT, colors)
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
		# clear player results
		player_turn_results = []
		# handle dictionary value
		if move and game_state == GameStates.PLAYERS_TURN:
			dx, dy = move
			destination_x = player.x + dx
			destination_y = player.y + dy
			
			if not game_map.is_blocked(destination_x, destination_y):
				target = get_blocking_entities_at_location(entities, destination_x, destination_y)
				
				if target:
					attack_results = player.fighter.attack(target)
					player_turn_results.extend(attack_results)
				else:
					# move player
					player.move(dx, dy)
					# trigger field of view recompute
					fov_recompute = True
				
				game_state = GameStates.ENEMY_TURN
		if exit:
			return True
			
		if fullscreen:
			libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
			
		for player_turn_result in player_turn_results:
			message = player_turn_result.get('message')
			dead_entity = player_turn_result.get('dead')
			
			if message:
				print(message)
				
			if dead_entity:
				if dead_entity == player:
					message, game_state = kill_player(dead_entity)
				else:
					message = kill_monster(dead_entity)
					
				print(message)
			
		if game_state == GameStates.ENEMY_TURN:
			for entity in entities:
				if entity.ai:
					enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities)
					
					for enemy_turn_result in enemy_turn_results:
						message = enemy_turn_result.get('message')
						dead_entity = enemy_turn_result.get('dead')
						
						if message:
							print(message)
							
						if dead_entity:
							if dead_entity == player:
								message, game_state = kill_player(dead_entity)
							else:
								message = kill_monster(dead_entity)
							
							print(message)
						
							if game_state == GameStates.PLAYER_DEAD:
								break
							
					if game_state == GameStates.PLAYER_DEAD:
						break
			else:
				game_state = GameStates.PLAYERS_TURN
	
if __name__ == '__main__':
	main()
