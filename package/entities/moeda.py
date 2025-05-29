from package.entities.entidade import Entidade


class Moeda(Entidade):

	def __init__(self, pos_inicial: tuple):
		super().__init__(pos_inicial)

		self.rect.center = self.pos_inicial
		self.coletada = False


	def definir_sprite(self):
		caminho = f'package/assets/moeda/moeda.png'
		scale = 0.4
		return (caminho, scale)

	def update(self, screen):
		if not self.coletada:
			screen.blit(self.surface, self.rect)

	
	def check_colision(self, player):
		if self.mask.overlap(player.mask, (player.rect.x - self.rect.x, player.rect.y - self.rect.y)):
				player.moedas += 1
				self.coletada = True
				self.rect.topleft = (0, 0) # muda o rect da moeda de lugar para evitar bugs
				self.surface.set_alpha(0) # coloca transparencia


	def reset(self):
		self.coletada = False
		self.rect.center = self.pos_inicial
		self.surface.set_alpha(255)