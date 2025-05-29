class Tile:

	def __init__(self, image, pos, rect = None):
		
		self.tile_image = image
		self.pos = pos
		self.tile_rect = rect
	

	def get_info(self):
		print(f'img = {self.tile_image}, pos = {self.pos}, rect = {self.tile_rect}')