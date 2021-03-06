import libtcodpy as libtcod

from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from entity import Entity
from equipment_slots import EquipmentSlots
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder

def get_constants():
	WINDOW_TITLE = 'Roguelike Tutorial Revised'
	# screen dimensions
	SCREEN_WIDTH = 80
	SCREEN_HEIGHT = 50
	# hp panel dimensions
	BAR_WIDTH = 20
	PANEL_HEIGHT = 7
	PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
	# message panel dimensions
	MESSAGE_X = BAR_WIDTH + 2
	MESSAGE_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
	MESSAGE_HEIGHT = PANEL_HEIGHT - 1
	# map dimensions
	MAP_WIDTH = 80
	MAP_HEIGHT = 43
	# room dimensions and count
	ROOM_MAX_SIZE = 10
	ROOM_MIN_SIZE = 6
	MAX_ROOMS = 30
	# field of view settings
	FOV_ALGORITHM = 0
	FOV_LIGHT_WALLS = True
	FOV_RADIUS = 10
	# entity population settings
	MAX_MONSTERS_PER_ROOM = 3
	MAX_ITEMS_PER_ROOM = 2
	# define tile colors
	colors = {
		'dark_wall': libtcod.Color(0, 0, 100),
		'dark_ground': libtcod.Color(50, 50, 150),
		'light_wall': libtcod.Color(130, 110, 50),
		'light_ground': libtcod.Color(200, 180, 50)
	}
	
	constants = {
		'window_title': WINDOW_TITLE,
		'screen_width': SCREEN_WIDTH,
		'screen_height': SCREEN_HEIGHT,
		'bar_width': BAR_WIDTH,
		'panel_height': PANEL_HEIGHT,
		'panel_y': PANEL_Y,
		'message_x': MESSAGE_X,
		'message_width': MESSAGE_WIDTH,
		'message_height': MESSAGE_HEIGHT,
		'map_width': MAP_WIDTH,
		'map_height': MAP_HEIGHT,
		'room_max_size': ROOM_MAX_SIZE,
		'room_min_size': ROOM_MIN_SIZE,
		'max_rooms': MAX_ROOMS,
		'fov_algorithm': FOV_ALGORITHM,
		'fov_light_walls': FOV_LIGHT_WALLS,
		'fov_radius': FOV_RADIUS,
		'max_monsters_per_room': MAX_MONSTERS_PER_ROOM,
		'max_items_per_room': MAX_ITEMS_PER_ROOM,
		'colors': colors
	}
	
	return constants
	
def get_game_variables(constants):
	# create player
	fighter_component = Fighter(hp=100, defense=1, power=2)
	inventory_component = Inventory(26)
	level_component = Level()
	equipment_component = Equipment()
	player = Entity(0, 0, '@', libtcod.white ,'Player', blocks=True, render_order=RenderOrder.ACTOR,
					fighter=fighter_component, inventory=inventory_component, level=level_component,
					equipment=equipment_component)
	# create entity list
	entities = [player]
	
	equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
	dagger = Entity(0, 0, '-', libtcod.sky, 'Dagger', equippable=equippable_component)
	player.inventory.add_item(dagger)
	player.equipment.toggle_equip(dagger)
	# create game map
	game_map = GameMap(constants['map_width'], constants['map_height'])
	game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
						constants['map_width'], constants['map_height'], player, entities)
	# create message log
	message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])
	# create game state
	game_state = GameStates.PLAYERS_TURN
	
	return player, entities, game_map, message_log, game_state
	
