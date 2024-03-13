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

    def draw_grid(self, traversal_array, blocked):
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
        

        for coord in blocked:
            if 0 <= coord[0] < self.grid_size and 0 <= coord[1] < self.grid_size:
                self.draw_rectangle(screen, coord)

        prev = None
        for coordinate_pair in traversal_array:
            if prev != None:
                prev_x = (prev[0] + self.padding_size) * self.cell_size
                prev_y = (prev[1] + self.padding_size) * self.cell_size
                coordinate_pair_x = (coordinate_pair[0] + self.padding_size) * self.cell_size
                coordinate_pair_y = (coordinate_pair[1] + self.padding_size) * self.cell_size
                pygame.draw.line(screen, self.red, (prev_x, prev_y), (coordinate_pair_x,coordinate_pair_y))
            prev = self.draw_circle(screen, coordinate_pair, self.red)

        pygame.display.flip()
        pygame.time.Clock().tick(10)

    def draw_rectangle(self, screen, pos):
        rect_x = (pos[0] + self.padding_size) * self.cell_size
        rect_y = (pos[1] + self.padding_size) * self.cell_size
        rect_width = self.cell_size
        rect_height = self.cell_size
        pygame.draw.rect(screen, self.white, (rect_x, rect_y, rect_width, rect_height))


    def draw_circle(self, screen, pos, color):
        circle_radius = self.cell_size // 6
        circle_center = ((pos[0] + self.padding_size) * self.cell_size, (pos[1] + self.padding_size) * self.cell_size)
        pygame.draw.circle(screen, color, circle_center, circle_radius)
        return pos
    
    def run(self, traversal_array, blocked=[]):
        pygame.init()
        pygame.display.set_caption("A*")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_grid(traversal_array, blocked)

        pygame.quit()
        sys.exit()


