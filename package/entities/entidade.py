import pygame

from abc import ABC, abstractmethod
from package.entities.imagemMixin import ImagemMixin


class Entidade(ABC, ImagemMixin):

	def __init__(self, pos_inicial: list):
		caminho, escala = self.definir_sprite()

		self.pos_inicial = pos_inicial
		self.surface = self.carregar_imagem(caminho, escala)
		self.rect = self.surface.get_rect(topleft=pos_inicial)
		self.mask = pygame.mask.from_surface(self.surface)


	@abstractmethod
	def update(self):
		pass


	@abstractmethod
	def check_colision(self):
		pass


	@abstractmethod
	def definir_sprite(self) -> tuple[str, float]:
		"""Subclasses devem retornar o caminho da imagem e a escala."""
		pass