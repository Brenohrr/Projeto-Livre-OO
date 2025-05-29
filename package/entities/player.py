import pygame

from package.entities.entidade import Entidade

class Player(Entidade):
	
	def __init__(self, pos_inicial: tuple, mortes = 0, fase = 1, skin = 1, has_cheated = 0):
		self.skin = skin
		super().__init__(pos_inicial)

		self.rect.topleft = self.pos_inicial

		# funcionalidades
		self.mortes = mortes
		self.fase = fase
		self.has_cheated = has_cheated # 0 para False e 1 para True
		self.moedas = 0



	def definir_sprite(self):
		caminho = f'package/assets/player/player{self.skin}.png'
		scale = 0.6
		return (caminho, scale)


	def trocar_skin(self):
		self.skin += 1
		if self.skin > 4:
			self.skin = 1

		caminho, escala = self.definir_sprite()
		self.surface = self.carregar_imagem(caminho, escala)


	def update(self, screen, world): # 1- guardar nova pos, 2- checar colisao no novo ponto, 3- mover o player 
		
		#variacao de movimento
		dx = 0
		dy = 0

		#inputs do jogador
		key = pygame.key.get_pressed()

		if key[pygame.K_UP] is True:
			dy -= 2
		if key[pygame.K_DOWN] is True:
			dy += 2
		if key[pygame.K_RIGHT] is True:
			dx += 2
		if key[pygame.K_LEFT] is True:
			dx -= 2

		#atualizar pos do player
		player_movement = (dx, dy)
		self.rect = self.check_colision(self.rect, player_movement, world)

		#desenha o player na tela
		screen.blit(self.surface, self.rect)
	

	def obstaculo_list(self, world):
		
		# calcula a pos do player na grade
		pos_player = ((int((self.rect.x - world.pos_inical[0]) / 50)), (int((self.rect.y - world.pos_inical[1]) / 50)))
		px, py = pos_player

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

		# se moveu no eixo X
		rect.x += movement[0]
		hit_list = self.obstaculo_list(world)
		for tile in hit_list:

			#direita
			if movement[0] > 0:
				rect.right = tile.left
			
			#esquerda
			elif movement[0] < 0:
				rect.left = tile.right
		
		# se moveu no eixo Y
		rect.y += movement[1]
		hit_list = self.obstaculo_list(world)
		for tile in hit_list:
			
			#baixo
			if movement[1] > 0:
				rect.bottom = tile.top
			
			#topo
			elif movement[1] < 0:
				rect.top = tile.bottom
	
		return rect


	def reset_pos(self, world):
		self.rect.topleft = self.pos_inicial
		self.moedas = 0

		for moeda in world.moedas:
			moeda.reset()
	

	def reset(self):
		self.fase = 1
		self.mortes = 0
		self.has_cheated = 0

	
	def check_level_completion(self, world):

		if self.moedas == world.data['moedas_qtd']:
			
			for tile in world.data['final']:

				# identificando os tiles no final do mapa
				pos = tile['pos']
				rect = world.tile_list[pos[1]][pos[0]].tile_rect

				if self.rect.colliderect(rect):
					self.fase += 1
					self.moedas = 0
					return True
		
		return False
	

	def to_dict(self):
		return {'pos_inicial': self.pos_inicial, 'mortes': self.mortes, 'fase': self.fase, 'skin': self.skin, "has_cheated": self.has_cheated}
	

	@classmethod
	def from_dict(cls, data):
		return cls(data['pos_inicial'], data['mortes'], data['fase'], data['skin'], data['has_cheated'])