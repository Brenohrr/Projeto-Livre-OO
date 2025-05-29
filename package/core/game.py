import pygame
import sys
import json
import traceback

from package.ui.menu import Menu
from package.core.world import World
from package.entities.player import Player
from package.ui.button import Button
from package.ui.cronometro import Cronometro


class Jogo:
	
	def __init__(self):
		pygame.init()

		# icone e nome
		self.icon = pygame.image.load('package/assets/player/player1.png')
		pygame.display.set_caption("World's Easiest Game")
		pygame.display.set_icon(self.icon)

		# altura e largura da janela
		self.altura = 900
		self.largura = 1200

		# informações
		self.screen = pygame.display.set_mode((self.largura, self.altura))
		self.background = (183, 180, 254)
		self.menu = Menu(self.screen, self)
		self.clock = pygame.time.Clock()
		self.fonte = pygame.font.Font('package/assets/menu/font.ttf', 20)
		self.players = []
		self.cronometro = []



	def run(self):
		try:
			self.carregar_save()

		except:
			print('explodiu')
			traceback.print_exc() # verificar de onde vem o erro
			pygame.quit()
			sys.exit()

		else:
			if not self.players:
				player = Player((250, 400))
				cronometro = Cronometro()
				self.players.append(player)
				self.cronometro.append(cronometro)
				self.salvar_jogo()

		self.menu.main_menu()
	

	def main_game(self):

		#carregamentos
		fases = self.carregar_fase()
		player = self.players[0]

		cronometro = self.cronometro[0]
		if not player.has_cheated:
			cronometro.resume()

		mapa = self.carregar_fase_do_jogador(player, fases)

		# main loop
		while True:

			self.clock.tick(60) # fps
			self.screen.fill(self.background)

			# atualiza o cronometro
			cronometro.update(self.screen, self.fonte)

			# hud
			menu_back, reset, mouse_pos = self.hud(player)

			# atualiza o mapa
			mapa.update(player)

			# atualiza o player
			player.update(self.screen, mapa)

			# verificar se passou de fase
			if player.check_level_completion(mapa):
				player, mapa = self.load_next_level(player, fases)
				cronometro.set_fase(player.fase)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.salvar_jogo()
					pygame.quit()
					sys.exit()

				elif event.type == pygame.MOUSEBUTTONDOWN:
					
					# botao do menu
					if menu_back.checkForInput(mouse_pos):
						cronometro.pause()
						self.salvar_jogo()
						self.menu.main_menu()
						return

					# botao de reset
					elif reset.checkForInput(mouse_pos):
						player.reset()

						cronometro.reset()
						cronometro.pause()

						self.salvar_jogo()
						self.menu.main_menu()
						return
				
				# funcionalidades
				elif event.type == pygame.KEYDOWN:

					# trocar skin
					if event.key == pygame.K_t:
						player.trocar_skin()

					# voltar pro menu pelo ESC
					elif event.key == pygame.K_ESCAPE:
						cronometro.pause()
						self.salvar_jogo()
						self.menu.main_menu()
						return


					# cheat pra testar o jogo

					# avancar fase
					elif event.key == pygame.K_n:
						player.fase += 1
						player, mapa = self.load_next_level(player, fases)
						player.has_cheated = 1
						cronometro.pause()

					# voltar fase
					elif event.key == pygame.K_m:
						player.fase -= 1
						if player.fase < 1:
							player.fase = 1
							
						player, mapa = self.load_next_level(player, fases)
						player.has_cheated = 1
						cronometro.pause()
				
			pygame.display.flip()


	def centralizar_mapa(self, fase_data):
		xstart = (self.largura - len(fase_data['tilemap'][0] * 50)) // 2
		ystart = (self.altura - len(fase_data['tilemap'] * 50)) // 2

		return xstart, ystart


	def carregar_fase_do_jogador(self, player, fases):

		fase_data = fases[f'fase{player.fase}']
		xstart, ystart = self.centralizar_mapa(fase_data)

		mapa = World(self.screen, fase_data, (xstart, ystart), 50)
		mapa.criar_grupo()

		player.pos_inicial = fase_data['pos_inicial']
		player.reset_pos(mapa)

		return mapa


	def load_next_level(self, player, fases):
		if player.fase == 11:

			times = self.cronometro[0].fases_time.copy()
			cheated = player.has_cheated
			mortes = player.mortes

			player.reset()

			self.cronometro[0].reset()
			self.cronometro[0].pause()

			self.salvar_jogo()
			self.tela_final(times, cheated, mortes)

		return player, self.carregar_fase_do_jogador(player, fases)


	def hud(self, player):
		pygame.draw.rect(self.screen, 'black', (0, 0, 1200, 80))

		# contador de mortes
		mortes = self.fonte.render(f'Mortes: {player.mortes}', True, 'white')
		self.screen.blit(mortes, (30, 32)) # o y é 40% do y do rect

		# fase
		fase = self.fonte.render(f'{player.fase}/10', True, 'white')
		self.screen.blit(fase, (560, 32))

		# botao de voltar pro menu
		mouse_pos = pygame.mouse.get_pos()
		menu_back = Button(image=None, pos=(1100, 42), text_input="MENU", font=self.fonte, base_color="White", hovering_color="Red")

		menu_back.changeColor(mouse_pos)
		menu_back.update(self.screen)

		# botao de reset
		reset = Button(image=None, pos=(950, 42), text_input="RESET", font=self.fonte, base_color='White', hovering_color="Red")
		reset.changeColor(mouse_pos)
		reset.update(self.screen)


		return (menu_back, reset, mouse_pos)
	

	def tela_final(self, times, cheated, mortes):
		while True:
			self.screen.fill('White')


			img = pygame.image.load('package/assets/menu/zerou.png')
			img = pygame.transform.scale_by(img, 0.8)
			self.screen.blit(img, (150, 300))


			mouse_pos = pygame.mouse.get_pos()

			fonte = pygame.font.Font('package/assets/menu/font.ttf', 60)
			menu_back = Button(image=None, pos=(600, 770), text_input="MENU", font=fonte, base_color="Black", hovering_color="forestgreen")

			menu_back.changeColor(mouse_pos)
			menu_back.update(self.screen)


			# tabela com os tempos
			if not cheated:
				soma = 0
				for fase, time in times.items():
					milis = time % 1000
					seconds = int(time / 1000) % 60
					minutes = int(time / 60000)

					text = self.fonte.render(f'{fase} - {minutes:0>2}:{seconds:0>2}:{milis:0>3}', True, 'Black')

					if int(fase) <= 5:
						self.screen.blit(text, (320, int(fase) * 50))
					else:
						self.screen.blit(text, (620, (int(fase) - 5) * 50))

					soma += time
				
				# colocar o tempo total do save aq
				milis = soma % 1000
				seconds = int(soma / 1000) % 60
				minutes = int(soma / 60000)

				# tempo total
				text = self.fonte.render(f'Total - {minutes:0>2}:{seconds:0>2}:{milis:0>3}', True, 'Black')
				self.screen.blit(text, (320, 300))

				# mortes
				deaths = self.fonte.render(f'Mortes: {mortes}', True, 'Black')
				self.screen.blit(deaths, (700, 300))
			

			else:
				text = self.fonte.render(f'Cheater', True, 'Black')
				self.screen.blit(text, (480, 200))

				mickey = pygame.image.load('package/assets/menu/mickey.png')
				self.screen.blit(mickey, (630, 170))


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:
					if menu_back.checkForInput(mouse_pos):
						self.menu.main_menu()
			
			pygame.display.update()


	def salvar_jogo(self):
		data = {'player': [player.to_dict() for player in self.players], 'timer': [cronometro.to_dict() for cronometro in self.cronometro]}

		try:
			with open('package/db/save.json', "w", encoding="utf-8") as fjson:
				json.dump(data, fjson, indent=4, ensure_ascii=False)

		except Exception as e:
			print(f"Erro ao salvar os dados: {e}")


	def carregar_save(self):
		try:

			with open('package/db/save.json', "r", encoding="utf-8") as fjson:
				try:
					data = json.load(fjson)
					self.players = [Player.from_dict(data_player) for data_player in data['player']]
					self.cronometro = [Cronometro.from_dict(data_timer) for data_timer in data['timer']]
				
				except json.JSONDecodeError:
					print('Arquivo existe, mas está vazio')
					self.players = []
					self.cronometro = []

		except FileNotFoundError:
			print(f"O arquivo não existe!")
			self.players = []
			self.cronometro = []

	
	def carregar_fase(self):
		try:
			with open('package/db/world_data.json', 'r', encoding='utf-8') as fjson:
				fases = json.load(fjson)
				return fases
		
		except FileNotFoundError:
			print('Arquivo não existe')