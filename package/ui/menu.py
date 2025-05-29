import pygame
import sys

from package.ui.button import Button


BG = (183, 180, 254)

class Menu:
    
	def __init__(self, screen, game):
		self.screen = screen
		self.game = game


	def get_font(self, size): # Returns Press-Start-2P in the desired size
		return pygame.font.Font('package/assets/menu/font.ttf', size)


	def controls(self):

		while True:
			CONTROLS_MOUSE_POS = pygame.mouse.get_pos()

			self.screen.fill("white")


			# text da setinha
			CONTROLS_TEXT = self.get_font(40).render("Setinhas :)", True, "Black") # "#b68f40"
			CONTROLS_RECT = CONTROLS_TEXT.get_rect(center=(610, 150))

			self.screen.blit(CONTROLS_TEXT, CONTROLS_RECT)


			# imagem da setinha
			img = pygame.image.load('package/assets/menu/controles2.png')
			img = pygame.transform.scale_by(img, 0.8)
			self.screen.blit(img, (170, 220))


			# botao pra voltar
			CONTROLS_BACK = Button(image=None, pos=(610, 700),  # 640, 460
								text_input="BACK", font=self.get_font(75), base_color="Black", hovering_color="Green")

			CONTROLS_BACK.changeColor(CONTROLS_MOUSE_POS)
			CONTROLS_BACK.update(self.screen)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if CONTROLS_BACK.checkForInput(CONTROLS_MOUSE_POS):
						self.main_menu()

			pygame.display.update()


	def main_menu(self):

		while True:
			self.screen.fill('black')

			MENU_MOUSE_POS = pygame.mouse.get_pos()

			MENU_TEXT = self.get_font(55).render("WORLD'S EASIEST GAME", True, "forestgreen") # "#b68f40" firebrick3
			MENU_RECT = MENU_TEXT.get_rect(center=(605, 150)) # 640, 100

			PLAY_BUTTON = Button(image=pygame.image.load("package/assets/menu/button_rect.png"), pos=(630, 350),  # X = 640
								text_input="PLAY", font=self.get_font(75), base_color="#d7fcd4", hovering_color="chartreuse3") #"#d7fcd4"
			CONTROLS_BUTTON = Button(image=pygame.image.load("package/assets/menu/button_rect.png"), pos=(630, 500), 
								text_input="CONTROLS", font=self.get_font(70), base_color="#d7fcd4", hovering_color="cyan3")
			QUIT_BUTTON = Button(image=pygame.image.load("package/assets/menu/button_rect.png"), pos=(630, 650), 
								text_input="QUIT", font=self.get_font(75), base_color="#d7fcd4", hovering_color="darkred")

			self.screen.blit(MENU_TEXT, MENU_RECT)

			for button in [PLAY_BUTTON, CONTROLS_BUTTON, QUIT_BUTTON]:
				button.changeColor(MENU_MOUSE_POS)
				button.update(self.screen)
			
			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.MOUSEBUTTONDOWN:

					if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
						self.game.main_game()

					if CONTROLS_BUTTON.checkForInput(MENU_MOUSE_POS):
						self.controls()

					if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
						pygame.quit()
						sys.exit()

			pygame.display.update()