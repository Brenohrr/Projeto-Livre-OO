import pygame


class ImagemMixin:
	def carregar_imagem(self, caminho: str, scale: float):
		image = pygame.image.load(caminho).convert_alpha()
		return pygame.transform.scale_by(image, scale)