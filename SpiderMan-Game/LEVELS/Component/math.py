"""About the file"""
from pygame import math

class Math:
	def __init__(self, value: float=0.0):
		self.value = value
		self.threshold = 0

	def deacclerate(self, maximum_value: int, value: float, deacc: float, delta_time: float) -> float:
		"""Deaccelerate the value based on the given direction and deacceleration rate."""
		if type(value) == int: value = float(value)
		if type(deacc) == int: deacc = float(deacc)

		if value > 0.01:
			value -= deacc * delta_time
			value = math.clamp(value, 0, maximum_value)
		elif value < 0.01:
			value += deacc * delta_time
			value = math.clamp(value, -maximum_value, 0)

		return value

	def isTendingTowards(self, value: float, target: float, threshold: float=None) -> bool:
	    """
	    Check if a value is tending towards a target value within a threshold.

	    :param value: The value to check.
	    :param target: The desired target value.
	    :param threshold: The threshold within which the value is considered to be tending towards the target.
	    :return: True if the value is tending towards the target, False otherwise.
	    """
	    if threshold is None:
	    	self.setThresholdValue(value, target)

	    if abs(value - target) <= self.threshold:
	    	self.setThresholdValue(value, target)
	    	return True
	    else:
	    	self.setThresholdValue(value, target)
	    	return False

	def setThresholdValue(self, value: float, target: float):
		self.threshold = abs(value - target)

if __name__ == "__main__":
	math = Math()
	pass