import pygame

from package.entities.inimigo import Inimigo
from package.entities.grupo import Grupo
from package.core.tile import Tile
from package.entities.moeda import Moeda


class World:

	def __init__(self, screen, data: dict, pos_inicial: tuple, tile_size = 50):
		
		self.tile_list = []
		self.tile_size = tile_size
		self.data = data
		self.screen = screen
		self.pos_inical = pos_inicial
		self.obstaculos = []
		self.inimigos = []
		self.moedas = []

	
	# carregar imagem dos tiles
	def load_tile_image(self):
		tile0_img = pygame.image.load('package/assets/tileset/tile0.png').convert_alpha()
		tile1_img = pygame.image.load('package/assets/tileset/tile1.png').convert_alpha()
		tile2_img = pygame.image.load('package/assets/tileset/tile2.png').convert_alpha()
		tile3_img = pygame.image.load('package/assets/tileset/tile3.png').convert_alpha()

		return (tile0_img, tile1_img, tile2_img, tile3_img)


	# carregar o tilemap
	def load_world(self):

		tiles_images = self.load_tile_image()
		
		lista = []
		linha_index = 0
		for linha in self.data['tilemap']:
			col_index = 0
			for tile in linha:
				
				if tile == 0:
					img = tiles_images[0]
					img_rect = img.get_rect()

					img_rect.x = col_index * self.tile_size + self.pos_inical[0]
					img_rect.y = linha_index * self.tile_size + self.pos_inical[1]
					pos = (img_rect.x, img_rect.y)

					tile = Tile(img, pos, img_rect)
					self.obstaculos.append(img_rect)

				elif tile == 1:
					img = tiles_images[1]

					img_x = col_index * self.tile_size + self.pos_inical[0]
					img_y = linha_index * self.tile_size + self.pos_inical[1]
					pos = (img_x, img_y)


					tile = Tile(img, pos)

				elif tile == 2:
					img = tiles_images[2]
					
					img_x = col_index * self.tile_size + self.pos_inical[0]
					img_y = linha_index * self.tile_size + self.pos_inical[1]
					pos = (img_x, img_y)

					tile = Tile(img, pos)

				elif tile == 3:
					img = tiles_images[3]

					img_x = col_index * self.tile_size + self.pos_inical[0]
					img_y = linha_index * self.tile_size + self.pos_inical[1]
					pos = (img_x, img_y)

					tile = Tile(img, pos, img_rect)
				
				elif tile == 4:
					img = tiles_images[3]
					img_rect = img.get_rect()

					img_rect.x = col_index * self.tile_size + self.pos_inical[0]
					img_rect.y = linha_index * self.tile_size + self.pos_inical[1]
					pos = (img_rect.x, img_rect.y)

					tile = Tile(img, pos, img_rect)	
				
				lista.append(tile)
				col_index += 1

			self.tile_list.append(lista)
			linha_index += 1
			lista = []
	

	def draw_world(self):
		if not self.tile_list:
			self.load_world()
		

		for linha in self.tile_list:
			for tile in linha:
				self.screen.blit(tile.tile_image, (tile.pos[0], tile.pos[1]))

				# mostrar hitbox
				#pygame.draw.rect(self.screen, 'white', (tile.pos[0], tile.pos[1], self.tile_size, self.tile_size), 2)
	

	def desenhar_linha_em_volta(self):
		tamanho_tile = self.tile_size

		for y, linha in enumerate(self.data['tilemap']):
			for x, tile in enumerate(linha):

				#ignorar caso for background
				if tile == 0:
					continue

				tile_x = x * tamanho_tile + self.pos_inical[0]
				tile_y = y * tamanho_tile + self.pos_inical[1]

				# Cima
				if (y > 0 and self.data['tilemap'][y - 1][x] == 0) or y == 0:
					pygame.draw.line(self.screen, (0, 0, 0), (tile_x, tile_y-1), (tile_x + tamanho_tile-1, tile_y-1), 5)

				# Baixo
				if (y < len(self.data['tilemap']) - 1 and self.data['tilemap'][y + 1][x] == 0) or y == len(self.data['tilemap']) - 1:
				#if mapa[y + 1][x] == 0:
					pygame.draw.line(self.screen, (0, 0, 0), (tile_x, tile_y + tamanho_tile+1), (tile_x + tamanho_tile, tile_y + tamanho_tile+1), 5)

				# Esquerda
				if (x > 0 and self.data['tilemap'][y][x - 1] == 0) or x == 0:
					#tava 2
					pygame.draw.line(self.screen, (0, 0, 0), (tile_x-2, tile_y), (tile_x-2, tile_y + tamanho_tile), 5)

				# Direita
				if (x < len(self.data['tilemap'][0]) - 1 and self.data['tilemap'][y][x + 1] == 0) or x == len(self.data['tilemap'][0]) - 1:
					pygame.draw.line(self.screen, (0, 0, 0), (tile_x + tamanho_tile+1, tile_y), (tile_x + tamanho_tile+1, tile_y + tamanho_tile), 5)


	def get_info(self) -> tuple:
		#return (len(self.data[0]) * 50, len(self.data) * 50) retorna só tamanho da matriz ex: 900x300
		return (self.pos_inical[0] + len(self.data['tilemap'][0]) * 50, self.pos_inical[1] + len(self.data['tilemap']) * 50)
	

	def load_inimigos(self):
		
		for inimigo in self.data['inimigos']:	
				
				# pos no centro do tile
				x = inimigo['pos'][0] * self.tile_size + self.pos_inical[0] + self.tile_size // 2
				y = inimigo['pos'][1] * self.tile_size + self.pos_inical[1] + self.tile_size // 2

				pos_inicial = (x, y)
				sentido = inimigo['sentido']
				variante = inimigo['variante']
				fator = inimigo['fator']

				inimigo = Inimigo(pos_inicial, sentido, variante, fator)
				self.inimigos.append(inimigo)


	def load_moedas(self):

		if self.data['moedas_qtd']:
			for moeda in self.data['moedas_pos']:
				
				x = moeda['pos'][0] * self.tile_size + self.pos_inical[0] + self.tile_size // 2 + moeda['var'][0]
				y = moeda['pos'][1] * self.tile_size + self.pos_inical[1] + self.tile_size // 2 + moeda['var'][1]

				pos_inical = (x, y)

				moeda = Moeda(pos_inical)
				self.moedas.append(moeda)


	def criar_grupo(self):
		self.load_inimigos()
		self.load_moedas()

		if self.inimigos:
			self.grupo_inimigo = Grupo(self.screen, self.inimigos, tipo='inimigo')

		if self.moedas:
			self.grupo_moedas = Grupo(self.screen, self.moedas, tipo='moeda')


	def update(self, player):
		self.draw_world()
		self.desenhar_linha_em_volta()

		if self.inimigos:
			self.grupo_inimigo.update(player, self)

		if self.moedas:
			self.grupo_moedas.update(player, self)