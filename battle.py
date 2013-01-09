# Author: Christopher Reid
#
# Date: Original: 06/01/2013
#       Latest: 08/01/2013
#
# Name: Battle Processing Test v1.3
#
# Description: My attempt to create a simple text-based, rpg-esque battle processing system.

import sys
import random

# initialise global variables
encounter_no = 1

# player related variables
player_level = 1
player_health = 1000
player_strength = 30
player_vitality = 1000
player_gold = 0
player_exp = 0
total_player_exp = 0

level_target = 50

small_potions = 0
potions = 0
large_potions = 0

# enemy related variables
monster_type = ""
monster_health = 0
monster_vitality = 0
enemy_strength = 0
enemy_atk_limit = 0

dmg_received = 0

is_defending = False

# if this were part of a larger game, say an rpg, this is where you would start battle processing
def determine_monster():
	global monster_type, monster_health, monster_vitality, enemy_strength, enemy_atk_limit, dmg_received, player_level
	
	dmg_received = 0
	
	rand_no = 0
	rand_no = random.randrange(0, 1000, 2)
	
	if rand_no >= 995:
		# make sure a low level player doesn't encounter high level monsters
		if encounter_no < 40:
			determine_monster()
		# set the enemy the player will face
		monster_type = "Dragon"
		monster_health = 1500
		enemy_strength = 250
		enemy_atk_limit = 250
		
	elif (rand_no >= (976 - player_level)) and (rand_no < 994):
		if encounter_no < 18:
			determine_monster()
			
		monster_type = "Wyvern"
		monster_health = 1000
		enemy_strength = 140
		enemy_atk_limit = 60
		
	elif (rand_no >= 750) and (rand_no < (975 - player_level)):
		monster_type = "Rat"
		monster_health = 150
		enemy_strength = 20
		enemy_atk_limit = 50
		
	elif (rand_no >=525) and (rand_no < 749):
		monster_type = "Goblin"
		monster_health = 350
		enemy_strength = 30
		enemy_atk_limit = 40
		
	elif (rand_no >= (501 - player_level)) and (rand_no < 524):
		if encounter_no < 14:
			determine_monster()
			
		monster_type = "Wraith"
		monster_health = 750
		enemy_strength = 40
		enemy_atk_limit = 100
		
	elif (rand_no >= 275) and (rand_no < (500 - player_level)):
		monster_type = "Bandit"
		monster_health = 250
		enemy_strength = 40
		enemy_atk_limit = 30
		
	elif (rand_no >= 250) and (rand_no < 274):
		if encounter_no < 14:
			determine_monster()
			
		monster_type = "Centaur"
		monster_health = 850
		enemy_strength = 100
		enemy_atk_limit = 40
		
	elif (rand_no >= (24 + player_level)) and (rand_no < 249):
		monster_type = "Skeleton"
		monster_health = 300
		enemy_strength = 50
		enemy_atk_limit = 20
		
	elif (rand_no >= 5) and (rand_no < (23 + player_level)):
		if encounter_no < 18:
			determine_monster()
			
		monster_type = "Lich"
		monster_health = 950
		enemy_strength = 60
		enemy_atk_limit = 140
		
	else:
		if encounter_no < 30:
			determine_monster()
			
		monster_type = "Cerberus"
		monster_health = 2000
		enemy_strength = 150
		enemy_atk_limit = 250
		
	# for displaying the enemy's max health
	monster_vitality = monster_health
	
	print """
\n+---------------------+
  Enemy encounter: %s
+---------------------+\n
A %s appears before you.

	""" % (encounter_no, monster_type)
	
	menu_msg()
	
def menu_msg():
	# game menu
	print """+---------------------------------------------------------------------------------+
  Menu
+---------------------------------------------------------------------------------+
  1 -> Attack   2 -> Defend   3 -> Item  \t<< Player health -> %s/%s >>
                                         \t<< %s's health -> %s/%s >>
 
  << To next level -> %s >>  << Level -> %s >>
  << Total Exp -> %s >>  << Gold -> %s >>  << Strength -> %s >>
+---------------------------------------------------------------------------------+
	""" % (player_health, player_vitality, monster_type, monster_health, monster_vitality, (level_target - player_exp), 
	player_level, total_player_exp, player_gold, player_strength)
	
	game_logic()
	
def game_logic():
	global is_defending
	
	try:
		input = int( raw_input('  -> '))
		print ""
	
		if input == 1:
			print "You attack the %s!\n" % monster_type
			# goto attack logic
			attack_logic()
		elif input == 2:
			print "You hold your ground and brace for an attack.\n"
			# set defend to true
			is_defending = True
			# goto enemy turn
			enemy_turn()
		elif input == 3:
			# goto item and inventory handling
			inventory()
		# handles invalid input
		else:
			game_logic()
		
	except Exception:
		# print "Encountered an error: " + str(e) - debugging
		game_logic()
		
def attack_logic():
	global monster_health, encounter_no, player_level, player_exp, total_player_exp, player_strength, player_vitality, player_health, player_gold, level_target, dmg_received, small_potions, potions, large_potions	
	# determine damage variance and attack chance
	atk_range = 0
	atk_chance = 0
	
	atk_range = random.randrange(0, 200, 2)
	atk_chance = random.randrange(0, 10, 2)
	
	# determines the chance of finding item drops
	find_chance = 0
	
	find_chance = random.randrange(0, 100, 2)
	
	drop = 0
	
	if (find_chance > 5) and (find_chance < 10):
		drop = 1
	elif (find_chance > 40) and (find_chance < 60):
		drop = 2
	elif (find_chance > 70) and (find_chance < 80):
		drop = 3
				
	# calculate player damage based on player strength and variance
	atk_dmg = 0
	atk_dmg = player_strength + atk_range
	
	# determing a hit or a miss
	if atk_chance >= 2:
		print "%s received %s points of damage!\n" % (monster_type, atk_dmg)
		monster_health -= atk_dmg
		# if more attack methods are added in future, need to make the following code a function
		if monster_health <= 0:
			# calculate exp and gold so that the player always gets a return; this return increases with level
			player_gold += ((player_strength / 5) + (dmg_received / 4))
			player_exp += ((player_strength / 6) + (dmg_received / 3))
			total_player_exp += player_exp
			encounter_no += 1
			print "Enemy %s was defeated!\n" % monster_type
			print "Obtained %s gold and %s experience!\n" % (
			(player_strength / 5) + (dmg_received / 4), (player_strength / 6) + (dmg_received / 3))
			
			if drop == 1:
				print "%s dropped a large potion\n" % monster_type
				large_potions += 1
			elif drop == 2:
				print "%s dropped a small potion!\n" % monster_type
				small_potions += 1
			elif drop == 3:
				print "%s dropped a potion!\n" % monster_type
				potions += 1
				
			if player_exp >= level_target:
				player_level += 1
				player_exp = 0
				player_strength += (6 + (player_level * 2))
				player_vitality += (player_vitality / 10)
				player_health += (player_vitality / 5)
				
				if player_health > player_vitality:
					player_health = player_vitality
					
				level_target += (level_target / 2)
				
				print "You leveled up!\nLevel is now %s!" % player_level
				print "Health is now %s!\nStrength is now %s!\n" % (player_vitality, player_strength)
				# if this were part of a larger game, say an rpg, this is where you would exit battle processing
				determine_monster()
			else:
				determine_monster()
	else:
		print "Your attack missed!\n"
		
	enemy_turn()
	
def enemy_turn():
	global player_health, dmg_received, is_defending
	
	# determine damage variance and attack chance
	enemy_range = 0
	enemy_chance = 0
	
	enemy_range = random.randrange(4, enemy_atk_limit, 2)
	enemy_chance = random.randrange(0, 10, 2)
	
	# reduce enemy damage if player is defending
	if is_defending == True:
		enemy_dmg = (enemy_strength + enemy_range) / 2
	else:
		enemy_dmg = enemy_strength + enemy_range
		
	is_defending = False
	
	# determing a hit or a miss
	if enemy_chance <= 8:
		print "You received %s points of damage!\n" % enemy_dmg
		player_health -= enemy_dmg
		dmg_received += enemy_dmg
		
		if player_health <= 0:
			print "You were defeated!\n"
			game_over()
	else:
		print "The %s's attack missed!\n" % monster_type
	
	menu_msg()
		

def inventory():
	global small_potions, potions, large_potions, player_health, player_gold, player_vitality

	print """
Inventory - Press 1, 2 or 3 to use, 4, 5 or 6 to buy, 7 to return / Player Gold -> %s

  1/4 -> %s small potions  << 300 gold >>  << +250HP >>
  2/5 -> %s potions        << 600 gold >>  << +750HP >>
  3/6 -> %s large potions  << 1000 gold >>  << +1500HP >>
	""" % (player_gold, small_potions, potions, large_potions)
	
	try:
		inv_input = int( raw_input('  -> '))
		print ""
		
		if inv_input == 1:
			if small_potions >= 1:
				print "You drank a small potion, and recovered 250HP.\n"
				player_health += 250
				small_potions -= 1
				
				if player_health > player_vitality:
					player_health = player_vitality
					enemy_turn()
				else:
					enemy_turn()
					
			elif small_potions == 0:
				print "You don't have any small potions to use.\n"
				inventory()
				
		if inv_input == 2:
			if potions >= 1:
				print "You drank a potion, and recovered 750HP.\n"
				player_health += 750
				potions -= 1
				
				if player_health > player_vitality:
					player_health = player_vitality
					enemy_turn()
				else:
					enemy_turn()
					
			elif potions == 0:
				print "You don't have any potions to use.\n"
				inventory()
				
		if inv_input == 3:
			if large_potions >= 1:
				print "You drank a large potion, and recovered 1500HP.\n"
				player_health += 1500
				large_potions -= 1
				
				if player_health > player_vitality:
					player_health = player_vitality
					enemy_turn()
				else:
					enemy_turn()
			elif large_potions == 0:
				print "You don't have any large potions to use.\n"
				inventory()
				
		if inv_input == 4:
			if player_gold >= 300:
				print "You bought a small potion.\n"
				small_potions += 1
				player_gold -= 300
				inventory()
				
			elif player_gold < 300:
				print "You don't have enough gold.\n"
				inventory()
				
		if inv_input == 5:
			if player_gold >= 600:
				print "You bought a potion.\n"
				potions += 1
				player_gold -= 600
				inventory()
				
			elif player_gold < 600:
				print "You don't have enough gold.\n"
				inventory()
				
		if inv_input == 6:
			if player_gold >= 1000:
				print "You bought a large potion.\n"
				large_potions += 1
				player_gold -= 1000
				inventory()
				
			elif player_gold < 1000:
				print "You don't have enough gold.\n"
				inventory()
				
		if inv_input == 7:
			menu_msg()
			
	except Exception:
		# print "Encountered an error: " + str(e) - debugging
		inventory()

def game_over():
	global encounter_no, player_health, is_defending

	print "\n\nGAME OVER\n\nMonsters fought -> %s\n\nStart again?\n1\t-> Yes\nAny no. -> No\n" % encounter_no

	try:
		temp_in = int( raw_input('  -> '))
		print ""

		if temp_in == 1:
			# initialise global variables
			encounter_no = 1

			# player related variables
			player_level = 1
			player_health = 1000
			player_strength = 30
			player_vitality = 1000
			player_gold = 0
			player_exp = 0
			total_player_exp = 0

			level_target = 50

			small_potions = 0
			potions = 0
			large_potions = 0

			determine_monster()
			
		elif temp_in != 1:
			# exit game
			sys.exit()
			
	except Exception:
		# print "Encountered an error: " + str(e) - debugging
		game_over()
	
def start():
	print """
+-----------------------+
|   ARENA v1.3          |
|   by                  |
|   Christopher Reid    |
+-----------------------+

This is a small text-based arena game.
There may be some bugs.

All input is through the number keys.

Enter 1 to continue.
Any other key to quit.
	"""
	
	try:
		t_in = int( raw_input('  -> '))
		
		if t_in == 1:
			determine_monster()
		elif t_in != 1:
			sys.exit()
			
	except Exception:
		# print "Encountered an error: " + str(e) - debugging
		sys.exit()
		
start()