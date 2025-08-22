import pygame
import random
from particle import Particle
from readings import I_CHING_READINGS

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("I Ching Particle Simulation")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game variables
particles = []
explosion_center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
is_exploding = False
explosion_duration = 200
frame_count = 0
final_reading = None
start_screen = True

# Create the 6 sections for the I Ching hexagram
section_height = SCREEN_HEIGHT // 6
sections = []
for i in range(6):
    sections.append(pygame.Rect(0, i * section_height, SCREEN_WIDTH, section_height))

# Fonts
font_title = pygame.font.Font(None, 40)
font_desc = pygame.font.Font(None, 24)
font_instruction = pygame.font.Font(None, 24)

def generate_explosion():
    """Populates the particles list for a new explosion."""
    global is_exploding, frame_count
    particles.clear()
    for _ in range(2000):
        particle_type = random.randint(1, 8)
        particles.append(Particle(explosion_center[0], explosion_center[1], particle_type))
    is_exploding = True
    frame_count = 0

def get_hexagram_from_sections():
    """Determines the hexagram based on particle counts in each section."""
    particle_counts = [0] * 6
    for particle in particles:
        for i, section in enumerate(sections):
            if section.collidepoint(particle.x, particle.y):
                # Count all particle types
                particle_counts[i] += 1
                break
    
    # Odd counts for Yang (1), even for Yin (0)
    hexagram_lines = []
    for count in particle_counts:
        hexagram_lines.append('1' if count % 2 != 0 else '0')
    
    hexagram_lines.reverse()
    return "".join(hexagram_lines)

def draw_sections():
    """Draws the dividing lines for the 6 hexagram sections."""
    for i in range(6):
        pygame.draw.line(screen, WHITE, (0, i * section_height), (SCREEN_WIDTH, i * section_height))

def draw_text_wrapped(surface, text, font, color, rect, alignment="left"):
    """Draws text wrapped to fit within a rect."""
    words = text.split(' ')
    lines = []
    current_line = ''
    for word in words:
        test_line = current_line + ' ' + word if current_line else word
        test_surface = font.render(test_line, True, color)
        if test_surface.get_width() <= rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    y_offset = rect.y
    for line in lines:
        text_surface = font.render(line, True, color)
        text_rect = text_surface.get_rect()
        if alignment == "center":
            text_rect.centerx = rect.centerx
        else:
            text_rect.x = rect.x
        text_rect.y = y_offset
        surface.blit(text_surface, text_rect)
        y_offset += font.get_height()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                generate_explosion()
                final_reading = None
                start_screen = False

    screen.fill(BLACK)

    if start_screen:
        draw_text_wrapped(screen, "Press SPACE to start the nuclear divination", font_instruction, WHITE, pygame.Rect(50, SCREEN_HEIGHT // 2 - 20, SCREEN_WIDTH - 100, 100), "center")
    else:
        if is_exploding:
            for particle in particles:
                particle.update()
            
            frame_count += 1
            if frame_count > explosion_duration:
                is_exploding = False
                
        for particle in particles:
            particle.draw(screen)
        draw_sections()

        if not is_exploding and final_reading is None:
            hexagram_binary = get_hexagram_from_sections()
            final_reading = I_CHING_READINGS.get(hexagram_binary, {
                'title': 'Unknown Reading',
                'description': 'This reading is not in the database. A true quantum anomaly.'
            })
            
        if final_reading:
            # Title
            title_rect = pygame.Rect(0, 50, SCREEN_WIDTH, 50)
            draw_text_wrapped(screen, final_reading['title'], font_title, WHITE, title_rect, "center")

            # Description
            desc_rect = pygame.Rect(50, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150)
            draw_text_wrapped(screen, final_reading['description'], font_desc, WHITE, desc_rect, "left")

            # Instructions
            instruction_rect = pygame.Rect(50, SCREEN_HEIGHT - 50, SCREEN_WIDTH - 100, 50)
            draw_text_wrapped(screen, "Press SPACE for another reading", font_instruction, WHITE, instruction_rect, "center")
    
    pygame.display.flip()

pygame.quit()