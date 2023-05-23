""" This module control all the functionality related to player spirte used in this game,
	If any additions or modifications need to be made to the player sprite,
	they should be done within this module.
	
	Fetures:-
	-Control all the inputs, update, postion, collisiondetection, physics
	-Control all the animations etc..

	For use this module, ensure that the player asserts are loaded properly in the following
	format: `dict[str: list[pyimage]]`.Once the assets are ready, you can use the provided methods
	of the module.

	Some of the methods of this module:
	-`blit`: Takes `display_surf` and `delta_time` as arguments and can be used to blit the player image
			onto the screen.

"""
import pygame

# importing in-built module
from .math import Math
from .support import *
from .animationplayer import AnimationPlayer
import os

"CONSTANTS"
PLAYERIMGPATH = "LEVELS/Source/Player"
LEFT = pygame.K_LEFT
A = pygame.K_a
RIGHT = pygame.K_RIGHT
D = pygame.K_d
UP = pygame.K_UP
W = pygame.K_w
SPACE = pygame.K_SPACE

"Variables"
vec = pygame.math.Vector2
# in-built class set-up
math = Math()
		
def convertToAnimationData(path: str, key: str=None, alpha: bool= True) -> dict:
	""" This function converts the data from the specified image directory into a format used to create an AnimationPlayer object.

	    The directory structure should be as follows:
		root-|
			 |-run(dir)->[images of the run animation](inside dir)
			 ....
		
		Note: Only provide the path up to the root directory. The function will automatically handle subdirectories.
	    This function is suitable for frame-based images and does not support loading sprite sheet images.

		:param path: path of the image directory.
		:param key: Optional specific key required.
		:param alpha: Determines how the pygame object will convert the image. If True,
			 it calls pygame.image.convert_alpha(); otherwise, it does not.
		:return: Dictionary format: `dict[str: list[pyimages]]`
	"""
	dirs_list = getFilesWithExt(path, ext=("DIR", ))
	player_img_dict = {}

	for dirname in dirs_list:
		player_img_dict[dirname] = loadPyImgInList(os.path.join(path, dirname), alpha, ext=("png",))

	return player_img_dict

class SpiderMan(pygame.sprite.Sprite):
	"""This class is controls the player in the game,
	Any improvement relate to player needs to modify this class.

	Features and Responsibilities:-
	-This class control the input, animations, updates, collisionsdetection,
	-physics based movement, position, bliting etc.

	To create this class:-
	:param pos: Provide a position where to spawn the player
	"""
	def __init__(self, pos: tuple, *args):
		super().__init__()
		self.pos = vec(pos) # track position (speed_x, speed_y)
		self.PLAYERIMG = convertToAnimationData(PLAYERIMGPATH)

		# initializing in-build classes
		self.playeranimation = AnimationPlayer(self.PLAYERIMG)
		self.width, self.height = (32, 32)

		self.image = pygame.Surface((self.width, self.height))
		# self.image.fill(pygame.Color("Green"))
		self.rect = pygame.Rect((0, 0), self.image.get_size())
		self.rect.center = self.pos

		self.vel = vec() # velocity of the game.
		self.acc = 200 # used for implimenting acceleration.
		self.deacc = 1200 # used for deaccelated the speed.
		self.flip_deacc = 3000 # used for deaccelated during fliping the image.
		self.max_vel = 200 # used for limiting speed.
		self.dir = 1  # used for tracking direction (left/right) not the player direction.
		
		# used to track the player facing toward direction (False for right/True for Left).
		self.player_current_facing_dir = False
		self.player_previous_facing_dir = self.player_current_facing_dir
		self.keypressed_run = False # track the key is pressed or not for run

		self.INITIAL_JUMP_SPEED = -200 # negetive means upward direction
		self.test_gravity = 300
		self.jump_speed = 2000
		self.max_jump_height = 30
		self.ground_level = 480//2 # keep track of ground_level
		self.gravity = 950
		self.is_jump = False
		self.is_flip = True # keep track of the wether the player should be flip or not
		self.is_on_ground = True

		# Variables Related to animating the player
		self.running_animation_speed = 0.2
		self.jumping_animation_speed = 0.2

		# set the threshold Value used for speed up certain things accroding to speed up of
		math = Math()
		# player velocity, (eg:- running animation, etc..)
		math.setThresholdValue(self.vel.x, self.max_vel)

		
	def update(self, *args):
		"""This method is used to update the player's input, position, movement,
		and animations

		Note: The method does not require any specific parameters to be called,
			but one important parameter, `delta_time`, should be passed. `delta_time`
			is crucial for achieving smooth updates and ensuring frame-independent movement.

	    :param delta_time: The time elapsed since the last update. It is used for smooth,
		    frame-independent updates.It should be specified in seconds.
		"""
		delta_time = args[0]

		# Implimenting Run Mechanics
		if self.keypressed_run:
			self.vel.x += self.acc * self.dir * delta_time
		else:
			self.vel.x = math.deacclerate(self.max_vel, self.vel.x, self.deacc, delta_time)

		# # Implimenting Jump Mechanics
		# if self.is_jump: # limiting the jump height
		# 	if self.rect.centery <= (self.ground_level - self.max_jump_height):
		# 		self.is_jump = False
				
		# if self.is_jump: # accelerating the jump while the button is pressed
		# 	self.vel.y -= self.jump_speed * delta_time
		self.vel.y += (self.test_gravity * delta_time)

		if self.is_jump and self.rect.centery < self.ground_level:
			self.is_jump = False
		elif not self.is_jump and self.rect.centery >= self.ground_level:
			self.vel.y = min(0, self.vel.y)
			self.is_flip = True
			self.is_on_ground = True

		# # checking the ground level is crossed or not
		# if self.rect.centery > self.ground_level:
		# 	self.vel.y = min(0, self.vel.y)
		# 	self.is_flip = True
		# 	self.is_on_ground = True
		# else:
		# 	self.vel.y += (self.test_gravity * delta_time)

		print(self.vel.y, self.test_gravity * delta_time, self.rect.centery)
		
		self.vel.x = pygame.math.clamp(self.vel.x, -self.max_vel, self.max_vel)
		self.rect.centerx += self.vel.x * delta_time
		self.rect.centery += self.vel.y * delta_time
		self.pos = self.rect.center

	def blit(self, display_surf, delta_time):
		"""
		    This method is used to blit the player onto the screen. It is recommended to use
		    this method instead of other methods to ensure the correct order of operations and
		    updates for the player and its display on the screen.

		    :param display_surf: The pygame surface object where the player image should be displayed.
		    :param delta_time: The elapsed time (in seconds) required for independent updates. `delta_time`
			    represents the time gap between two frames and can be obtained using `pygame.Clock.tick()`.
		"""
		self.input()
		self.update(*[delta_time,])
		self.playerAnimation(delta_time)
		display_surf.blit(self.image, self.pos)

	def playerAnimation(self, delta_time):
		# Implimating animation logic
		if self.is_on_ground: # if player touches the ground he could able to run
			if self.keypressed_run:
				# deciding how long it's takes to go to next frame
				# more the value rate of change of frame took longer
				self.running_animation_speed = round(pygame.math.lerp(0.2, 0.1, abs(self.vel.x)/self.max_vel), 2)

				animation_image = self.playeranimation.playAnimationWithDeltaTime("Run", self.running_animation_speed,
																	 None, delta_time)
			else:
				animation_image = self.playeranimation.playAnimationWithDeltaTime("Idle", None, None, delta_time)

			# returs: Player only could flip when he is on top of ground
			# and Facing `Left` is True is the pygame.transform.flip() so that this statement return True
			# when fliping.
			# Note:- This is opposite to general convention that facing right is True
			# because the True value could flip the image in pygame.transform.flip()
			# that's why it used.
			if self.is_flip:
				self.player_current_facing_dir = isFlipCondition(self.dir)

			# This statement here is written here because of applying deaccleration during the time of fliping image,
			# other wise player get slipped further towards facing direction before fliping.
			if self.player_current_facing_dir != self.player_previous_facing_dir:
				self.player_previous_facing_dir = self.player_current_facing_dir
				self.vel.x = math.deacclerate(self.max_vel, self.vel.x, self.flip_deacc, delta_time)
		else:
			if self.vel.y < 0:
				# self.jumping_animation_speed = 0.2
				# self.jumping_animation_speed = round(self.jumping_animation_speed - abs(self.vel.y)/self.max_jump_height, 2)

				# if self.jumping_animation_speed < 0.1:
				# 	self.jumping_animation_speed = 0.1

				# easing out the animation while going upward
				weight = abs(self.rect.centery)/abs(self.ground_level-self.max_jump_height)
				# print(weight)
				# self.jumping_animation_speed = round(pygame.math.lerp(0.1, 0.2, weight), 2)

				# print(self.jumping_animation_speed)
				animation_image = self.playeranimation.playAnimationWithDeltaTime("Jump_Ascend", self.jumping_animation_speed,
																			None, delta_time, isloop=False)
			else:
				self.jumping_animation_speed = 0.2
				animation_image = self.playeranimation.playAnimationWithDeltaTime("Jump_Descend", self.jumping_animation_speed, 
																		None, delta_time, isloop=False)

		self.image = pygame.transform.flip(animation_image, self.player_current_facing_dir, False)

	def input(self):
		"""This method handle all the inputs needed to control the player sprite
		   
		  Inputs:
		    - Keyboard inputs:
		        - Left Arrow/A: Run Left
		        - Right Arrow/D: Run Right
		        - Up Arrow/W: Jump
		        - SpaceBar: Swing


	    The method is responsible for updating the player sprite based on the input 
	    received and triggering the corresponding actions such as running, jumping,
	    or swinging.
		"""
		key = pygame.key.get_pressed()
		
		# Controling Run Inputs
		if key[LEFT] or key[A]:
			# left key mechanics
			self.dir = -1
			self.keypressed_run = True
		elif key[RIGHT] or key[D]:
			# right key mechanics
			self.dir = 1
			self.keypressed_run = True
		else:
			self.keypressed_run = False

		# Controlling Jump Inputs
		if (key[UP] or key[W]) and self.is_on_ground:
			self.is_jump = True
			self.is_flip = False
			self.is_on_ground = False
			self.vel.y = self.INITIAL_JUMP_SPEED
						
		if key[SPACE] == True:
			# swing mechanics
			print("Swing")

def isFlipCondition(direction: int) -> bool:
	"""docstirng for isFlipCondition (Based on pygame)"""
	if direction < 0:
		return True
	return False