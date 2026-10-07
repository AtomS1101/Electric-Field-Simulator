from enum import Enum

import pygame


class MouseState(Enum):
	IDLE     = "idle"
	CLICKED  = "clicked"
	RELEASED = "released"
	DRAGGING = "dragging"

class Mouse:
	def __init__(self):
		self._event: pygame.event.Event
		self._center: tuple[int, int]
		self._radius: int
		self._isHolding: bool = False

	def _isClicked(self) -> bool:
		if self._event.type == pygame.MOUSEBUTTONDOWN and self._event.button == 1:
			x = (self._event.pos[0] - self._center[0]) ** 2
			y = (self._event.pos[1] - self._center[1]) ** 2
			if x + y <= (self._radius / 2) ** 2:
				self._isHolding = True
				return True
		return False

	def _isReleased(self) -> bool:
		if self._event.type == pygame.MOUSEBUTTONUP and self._event.button == 1:
			self._isHolding = False
			return True
		return False

	def _isDragging(self) -> bool:
		return self._event.type == pygame.MOUSEMOTION and self._isHolding

	def getScroll(self, event) -> tuple[int, int]:
		if event.type == pygame.MOUSEWHEEL:
			return event.x, event.y
		return 0, 0

	def isHolding(self) -> bool:
		return self._isHolding

	def getState(self, center: tuple[int, int], radius: int, event: pygame.event.Event) -> MouseState:
		self._center = center
		self._radius = radius
		self._event = event
		if self._isClicked():
			return MouseState.CLICKED
		elif self._isReleased():
			return MouseState.RELEASED
		elif self._isDragging():
			return MouseState.DRAGGING
		return MouseState.IDLE
