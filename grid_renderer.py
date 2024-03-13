import pygame
import sys
from math import ceil

class GridRenderer:
    def __init__(self, grid_size=5, cell_size=40, padding_size=2):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.padding_size = padding_size

        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.screen_width = (grid_size + 2 * padding_size) * cell_size
        self.screen_height = (grid_size + 2 * padding_size) * cell_size

    def draw_grid(self, traversal_array):
        screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        font = pygame.font.Font(pygame.font.get_default_font(), 20)
        screen.fill(self.black)
        for x in range(self.cell_size * self.padding_size - (self.cell_size // 3), self.screen_width - (self.cell_size * self.padding_size), self.cell_size):
            pygame.draw.rect(screen, self.black, (x, (self.cell_size / 2) * self.padding_size, (self.cell_size / 2), (self.cell_size / 2)))
            regressed_index = 0 if x == self.cell_size * self.padding_size - (self.cell_size // 3) else ceil((x - self.cell_size * self.padding_size - (self.cell_size // 3)) / self.cell_size)
            
            text_surface = font.render(str(regressed_index), True, self.white)
            
            rect_x = x
            rect_y = (self.cell_size / 2) * self.padding_size
            
            rect_width = (self.cell_size / 2)
            rect_height = (self.cell_size / 2)
            rect_center = (rect_x + rect_width // 2 - text_surface.get_width() // 2,
                           rect_y + rect_height // 2 - text_surface.get_height() // 2)
            
            screen.blit(text_surface, rect_center)
        
        for x in range(self.cell_size * self.padding_size, self.screen_width - (self.cell_size * self.padding_size) + 1, self.cell_size):
            pygame.draw.line(screen, self.white, (x, self.cell_size * self.padding_size), (x, self.screen_height - self.cell_size * self.padding_size))

        for y in range(self.cell_size * self.padding_size - (self.cell_size // 3), self.screen_height - (self.cell_size * self.padding_size), self.cell_size):
            pygame.draw.rect(screen, self.black, ((self.cell_size / 2) * self.padding_size, y, (self.cell_size / 2), (self.cell_size / 2)))
            regressed_index = 0 if y == self.cell_size * self.padding_size - (self.cell_size // 3) else ceil((y - self.cell_size * self.padding_size - (self.cell_size // 3)) / self.cell_size)
            
            text_surface = font.render(str(regressed_index), True, self.white)
            
            rect_x = (self.cell_size / 2) * self.padding_size
            rect_y = y
            
            rect_width = (self.cell_size / 2)
            rect_height = (self.cell_size / 2)

            rect_center = (rect_x + rect_width // 2 - text_surface.get_width() // 2,
                           rect_y + rect_height // 2 - text_surface.get_height() // 2)
            
            screen.blit(text_surface, rect_center)
        
        for y in range(self.cell_size * self.padding_size, self.screen_height - (self.cell_size * self.padding_size) + 1, self.cell_size):
            pygame.draw.line(screen, self.white, (self.cell_size * self.padding_size, y), (self.screen_width - self.cell_size * self.padding_size, y))
        
        for vertex in traversal_array:
            self.draw_circle(screen, vertex, self.red)

        pygame.display.flip()
        pygame.time.Clock().tick(10)

    def draw_circle(self, screen, pos, color):
        circle_radius = self.cell_size // 6
        circle_center = ((pos[0] + self.padding_size) * self.cell_size, (pos[1] + self.padding_size) * self.cell_size)
        pygame.draw.circle(screen, color, circle_center, circle_radius)

    def run(self, traversal_array):
        pygame.init()
        pygame.display.set_caption("A*")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_grid(traversal_array)

        pygame.quit()
        sys.exit()


