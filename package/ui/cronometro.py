import pygame


class Cronometro:

    def __init__(self, total_time=0, fases_time=None):
        self.total_time = total_time  # acumulado em milissegundos, para exibição
        self.fases_time = fases_time or {str(i): 0 for i in range(1, 11)} # tempos individuais por fase
        self.current_fase = "1"
        self.running = True

        self.start_ticks_global = pygame.time.get_ticks() # ponto de partida para o tempo total
        self.start_ticks_fase = pygame.time.get_ticks()   # ponto de partida para a fase atual
        self.paused_at_global = 0  # tempo total acumulado antes de pausar
        self.paused_at_fase = 0    # tempo da fase atual acumulado antes de pausar


    def update(self, screen, fonte):
        if self.running:
            # calcula o tempo decorrido desde o último 'start_ticks_global' ou 'resume' para o tempo total
            current_elapsed_time_global = pygame.time.get_ticks() - self.start_ticks_global
            self.total_time = self.paused_at_global + current_elapsed_time_global

            # calcula o tempo decorrido para a fase atual
            current_elapsed_time_fase = pygame.time.get_ticks() - self.start_ticks_fase
            self.fases_time[self.current_fase] = self.paused_at_fase + current_elapsed_time_fase
        
        milis = self.total_time % 1000
        seconds = int(self.total_time / 1000) % 60
        minutes = int(self.total_time / 60000)

        out = fonte.render(f'{minutes:0>2}:{seconds:0>2}:{milis:0>3}', True, 'black')
        screen.blit(out, (100, 850))

        if not self.running:
            cheater = fonte.render('Cheater', True, 'orangered2')
            screen.blit(cheater, (300, 850))

            mickey = pygame.image.load('package/assets/menu/mickey.png')
            screen.blit(mickey, (450, 810))


    def set_fase(self, fase):
        # salva o tempo da fase atual antes de mudar
        if self.running:
            self.paused_at_fase = self.fases_time[self.current_fase]
            self.start_ticks_fase = pygame.time.get_ticks() - self.paused_at_fase # reseta o 'start_ticks_fase' para a nova fase

        self.current_fase = str(fase)
        if self.current_fase not in self.fases_time:
            self.fases_time[self.current_fase] = 0
        
        # define o ponto de partida para a nova fase
        self.paused_at_fase = self.fases_time[self.current_fase]
        self.start_ticks_fase = pygame.time.get_ticks() - self.paused_at_fase


    def pause(self):
        if self.running:
            self.paused_at_global = self.total_time  # salva o tempo total antes de pausar
            self.paused_at_fase = self.fases_time[self.current_fase] # salva o tempo da fase atual antes de pausar
            self.running = False


    def resume(self):
        if not self.running:
            # ajusta o start_ticks para o tempo total
            self.start_ticks_global = pygame.time.get_ticks() - (self.total_time - self.paused_at_global)

            # ajusta o start_ticks para a fase atual
            self.start_ticks_fase = pygame.time.get_ticks() - (self.fases_time[self.current_fase] - self.paused_at_fase)
            self.running = True


    def reset(self):
        self.total_time = 0
        self.fases_time = {str(i): 0 for i in range(1, 11)}
        self.current_fase = "1"
        self.running = True
        self.start_ticks_global = pygame.time.get_ticks()
        self.start_ticks_fase = pygame.time.get_ticks()
        self.paused_at_global = 0
        self.paused_at_fase = 0


    def to_dict(self):
        return {
            "total_time": self.total_time,
            "fases_time": self.fases_time,
            "current_fase": self.current_fase # adiciona a fase atual para ser salva
        }


    @classmethod
    def from_dict(cls, data):
        total_time = data.get('total_time', 0)
        fases_time = data.get('fases_time', {})
        current_fase = data.get('current_fase', '1')

        if not total_time and not fases_time:
            fases_time = {str(i): 0 for i in range(1, 11)}

        instance = cls(total_time, fases_time)
        instance.current_fase = current_fase
        instance.paused_at_global = total_time
        instance.paused_at_fase = fases_time.get(current_fase, 0) # carrega o tempo da fase atual
        instance.running = False 
        return instance