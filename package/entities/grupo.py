class Grupo:

	def __init__(self, screen, grupo, tipo: str):
		self.grupo = grupo
		self.screen = screen
		self.tipo = tipo
	

	def desenhar(self):
		if self.tipo == 'inimigo':
			for inimigo in self.grupo:
				self.screen.blit(inimigo.surface, inimigo.rect)

		elif self.tipo == 'moeda':
			for moeda in self.grupo:
				self.screen.blit(moeda.surface, moeda.rect)
	

	def update(self, player, world):
		self.desenhar()

		if self.tipo == 'inimigo':
			for inimigo in self.grupo:
				inimigo.colisao_player(player, world)
				inimigo.update(world)
		
		elif self.tipo == 'moeda':
			for moeda in self.grupo:
				moeda.check_colision(player)
				moeda.update(self.screen)