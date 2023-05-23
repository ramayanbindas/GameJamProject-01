""" This module provide the methods to animate sprites and similar elements,
	Features:
	- Time duration-based animation: Allows for fast and slow animations based on the provided time.
	- Tracks time, frame, and duration: Provides functionality to keep track of time and animation frame details.
	- Duration modification: Enables the modification of animation durations.

	{"AnimationName":{{"PyImage": [FrameIndex, timeduration]}, {"PyImage": [1, timeduration]}, ...}}

    Some of the useful methods you can find in this module:
	- `class AnimationPlayer`: A class that provides animation-related functionality.
    - `playAnimationWithDeltaTime()`: Method for playing animations with a specified delta time.
    - `getFrameKeys()`: Method for retrieving the frame keys of an animation.

"""

import pygame

"CONSTANTS"
DEFAULTANIMATIONTIME = 0.3

class AnimationPlayer():
	"""
		This class provides functionality to creating an Animation Object to animate Sprite and similar elements
		-To create the Object, you need to provide a `dict` of format: `dict[str: list[pyimage]]`
		Example code:
		
		Note:- Time should be specified in second
	"""
	def __init__(self, imagedict: dict):
		self.current_time = float()
		self.previou_time  = float()
		self.current_frame = 0
		self.previou_frame = 0
		self.current_animationname = None
		self.previous_animationame = None

		# store suitable data for the AnimationPlayer Class
		self.animationdata = self.createAnimationData(imagedict)
		# used to store list of key and value of current frame
		self.framekeyvaluelist = []

	def playAnimationWithDeltaTime(self, animationname:str, time: float= None, addtional_time:float=None,
									frametimediff: float=None, isloop: bool=True) -> object:
		""" This method will update the animation by calculation the difference of two frame,
			which provide by the pygame Clock object(pygame.Clock.tick()) for additional information
			see the self.getTimePassed method.
			
			:param animationname: name of the given animation which should need to update(name
			should be same as the folder name that contain images).
			:param time: provide time duration to check how long it take to go next frame.
			:param additional_time: manupulate the default time which present in the animationdata.
			:param frametimediff: pass a frame gap between two frame or pygame Clock Object time
			:param isloop: True for looping the animation, and False for not. Default value is True.
			:return: Pygame Image based on frame number calculate by this method.
		"""
		self.current_animationname = animationname

		# If the animation changes, recalculate the data(data calculation is time consuming
		# so such action below this block)
		if self.current_animationname != self.previous_animationame:
			self.previous_animationame = self.current_animationname
			self.framekeyvaluelist = self.getFrameKeys(animationname)

		# Looping the animation
		if self.current_frame > len(self.framekeyvaluelist) - 1 and isloop:
			self.current_frame = 0
		elif self.current_frame > len(self.framekeyvaluelist) -1 and not isloop:
			# set back to the previous frame if frame increases, to make animation
			# look paused
			self.current_frame = len(self.framekeyvaluelist) - 1

		# Checking which time should be pass in the next calculation
		if time:
			time = time
		elif addtional_time:
			time = self.framekeyvaluelist[self.current_frame][1][1]
			time = abs(time + addtional_time)
		else:
			time = self.framekeyvaluelist[self.current_frame][1][1]
		
		# return a pygame image object based on current frame
		image = self.framekeyvaluelist[self.current_frame][0]
		
		# method for updating the current frame
		if self.getTimePassed(time=time, frametimediff=frametimediff):
			self.current_frame += 1

		return image

	def updateTime(self):
		"""docstring of update time"""
		pass

	def getTimePassed(self, time: float= DEFAULTANIMATIONTIME, frametimediff: float= None) -> bool:
		"""method checks weather the given time passed or not according to the frametimediff constantly
		   provided(e.g., from pygame.time.Clock()).

		   Note:- Time should be in second.

		   :param time: Time provided to check weather the time passes or not
		   :param frametimediff: pass a frame gap between two frame or pygame Clock Object time
		   :return: True/False if frame need to change return True otherwise False
		"""
		try:
			self.current_time += round(frametimediff, 3)
			if self.current_time >= round(time, 3):
				self.current_time = 0.0
				return True

			return False
		except TypeError as error:
			print("TypeError: Argument 1 and 2 must be pygame time (float)\n", error)

	# TODO: ONLY THIS METHON DOSN'T TESTED
	def updateAnimationDuration(self, animationname: str, durationlist: list):
		"""docstring for the updateAnimationDuration"""
		framekeylist = self.getFrameKeys(animationname)

		try:
			for index in enumerate(framekeylist):
				key = framekeylist[index][0]
				self.animationdata[animationname][index][key] = [index, durationlist[index]]
		
		except Exception as error:
			print(error)

	def getFrameKeys(self, animationname:str) -> list:
		"""method return the key-value paires for representing the animation data,
		   (eg. data like be: [[key, values], [pyimage, [frame_index, duration]],...])
		   key(pyimage object or image surface) and values([frame_index, duration])

		   :param animationname: Name of the animation of which key and value you needed
		"""
		# check the presence of the animaion_name in the animation_data
		if animationname not in self.getAnimationDataKeys():
			raise ValueError("Invalid animation name.")

		# return dict eg:-{{pyimg: [frame_index, duration]}, {..}, ..}
		animations = self.animationdata[animationname]
		return [[key, value] for key, value in animations.items()]

	def getAnimationDataKeys(self) -> list:
		"""method returns all the keys used in animation_data created by the AnimationPlayer Class"""
		return [key for key in self.animationdata.keys()]

	def getFrameDataWithIndex(self, animationname: str, frame_index: int) -> list:
		"""method return key-value pair of specific part from the animationdata based on
		   animation_name and the frame_index

		   Note: Frame Index should be positive
		   
		   :param animationname: key of the animation_data
		   :param frame_index: index of the frame the data you want
		   :return: key-value accroding to given index eg:-[pyimage, [frame_index, duration]]
		"""
		# return list of key-value pair eg:-[[pyimage, [frame_index, duration]], [..], ..]
		framekeyvaluelist = getFrameKeys(animationname)

		if frame_index > len(framekeyvaluelist):
			raise IndexError("frame_index out of range")

		return framekeyvaluelist[frame_index]
		
	@staticmethod
	def createAnimationData(imagedict: dict) -> dict:
		"""method create a reliable and useful data for the AnimationPlayer Class
		   Note:- Only specific data formate would be allow for this method

		   :param imagedict: data would be like eg:-{"key":[list of pyimage object]}
		   :return: return data would be like, 
		   eg:-{"key":{{pyimage:[frame_index, duration]}, {..}, ..}}
		"""
		final_animationdata = {}
		try:
			for animationname, animations in imagedict.items():
				data = {}
				for fram_index, frame in enumerate(animations):
					data[frame] = [fram_index, DEFAULTANIMATIONTIME]

				final_animationdata[animationname] = data
			
			return final_animationdata
		except KeyError as error:
			raise ValueError("Invalid image dictionary format") from error
		except Exception as error:
			raise RuntimeError("Failed to convert data to AnimationPlayer data") from error



	@staticmethod
	def flipImage(pyimg: pygame.Surface, flipdir: int) -> pygame.Surface:
		"""docstring for flipImage"""
		if flipdir < 0: return pygame.transform.flip(pyimg, True, False)
		else: return pyimg
