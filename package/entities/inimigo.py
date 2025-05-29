from package.entities.entidade import Entidade


class Inimigo(Entidade):

	def __init__(self, pos_inicial: tuple, sentido, variante = 1, fator = 2):
		self.variante = variante
		super().__init__(pos_inicial)

		# coloca no centro do tile
		self.rect.center = self.pos_inicial

		# movimentacao
		self.fator = fator
		sentido_mov = sentido # 0 - direita, 1 - esquerda, 2 - baixo, 3 - cima
		tipo_mov = {0: [self.fator, 0], 1: [self.fator*-1, 0], 2: [0, self.fator], 3: [0, self.fator*-1]}
		self.movement = tipo_mov[sentido_mov]
	

	def definir_sprite(self):
		caminho = f'package/assets/inimigo/modelo_inimigo{self.variante}.png'
		scale = 0.4
		return (caminho, scale)


	def update(self, world):
		self.rect = self.check_colision(self.rect, self.movement, world)


	def obstaculo_list(self, world):

		# calcula a pos do inimigo na grade
		pos_inimigo = ((int((self.rect.x - world.pos_inical[0]) / 50)), (int((self.rect.y - world.pos_inical[1]) / 50)))
		px, py = pos_inimigo

				#        cima          d - cima          direita        d - baixo         baixo         e - baixo         esquerda       e - cima
		directions = [[px, py - 1], [px + 1, py - 1], [px + 1, py], [px + 1, py + 1], [px, py + 1], [px - 1 , py + 1], [px - 1, py], [px - 1, py - 1],
		[px, py]]


		hit_list = []
		world_data = world.data['tilemap']

		for direction in directions:
			x, y = direction

			if world_data[y][x] == 0:
				tile = world.tile_list[y][x]

				if self.rect.colliderect(tile.tile_rect):
					hit_list.append(tile.tile_rect)

		return hit_list


	def check_colision(self, rect, movement, world):

		if movement[0]:
			rect.x += movement[0]
			hit_list = self.obstaculo_list(world)
			for tile in hit_list:

				#direita
				if movement[0] > 0:
					rect.right = tile.left
					movement[0] *= -1
				
				#esquerda
				elif movement[0] < 0:
					rect.left = tile.right
					movement[0] *= -1

		if movement[1]:
			rect.y += movement[1]
			hit_list = self.obstaculo_list(world)
			for tile in hit_list:
				
				#baixo
				if movement[1] > 0:
					rect.bottom = tile.top
					movement[1] *= -1
				
				#topo
				elif movement[1] < 0:
					rect.top = tile.bottom
					movement[1] *= -1

		return rect
	

	def colisao_player(self, player, world):
		if self.mask.overlap(player.mask, (player.rect.x - self.rect.x, player.rect.y - self.rect.y)):
			player.reset_pos(world)
			player.mortes += 1