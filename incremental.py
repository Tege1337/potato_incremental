import pygame
import sys
import requests
from io import BytesIO

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
UPGRADE_COLOR = (200, 0, 0)
FONT_COLOR = (255, 255, 255)

# Function to download an image
def download_image(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for request errors
        return pygame.image.load(BytesIO(response.content))
    except Exception as e:
        print(f"Error downloading the image: {e}")
        return None

# Icon URLs
menu_icon_url = "https://img.icons8.com/ios-filled/50/000000/menu.png"
farmers_icon_url = "https://img.icons8.com/ios-filled/50/000000/farmer.png"

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Potato Clicker")

# Load icons
menu_icon = download_image(menu_icon_url)
farmers_icon = download_image(farmers_icon_url)

# Scale the icons
menu_icon = pygame.transform.scale(menu_icon, (40, 40)) if menu_icon else None
farmers_icon = pygame.transform.scale(farmers_icon, (40, 40)) if farmers_icon else None

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Game variables
potatoes = 0  # Renamed from score to potatoes
click_value = 1
upgrade_cost = 10
farmers = 0
farmer_costs = [50, 100, 200]  # Cost for each type of farmer
farmer_incomes = [1, 2, 3]  # Income per second from each type of farmer
button_pressed = False
upgrade_button_pressed = False
menu_open = False
farmers_menu_open = False

# Function to draw the main game screen
def draw_game_screen():
    screen.fill(WHITE)

    # Draw title
    title_text = font.render("Potato Clicker", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

    # Draw stats texts
    potatoes_text = small_font.render(f'Potatoes: {potatoes}', True, BLACK)
    click_text = small_font.render(f'Click Value: {click_value}', True, BLACK)

    # Position for statistics
    stat_x = 30
    stat_y = 100
    spacing = 50  # Vertical spacing between statistics

    screen.blit(potatoes_text, (stat_x, stat_y))
    screen.blit(click_text, (stat_x, stat_y + spacing))

    # Draw the click button
    button_rect = pygame.Rect(300, 350, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
    button_text = font.render('Click!', True, FONT_COLOR)
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2, button_rect.y + (button_rect.height - button_text.get_height()) // 2))

    # Draw the upgrade button
    upgrade_button_rect = pygame.Rect(300, 475, 200, 100)
    pygame.draw.rect(screen, UPGRADE_COLOR, upgrade_button_rect, border_radius=10)
    upgrade_button_text = font.render('Upgrade', True, FONT_COLOR)
    screen.blit(upgrade_button_text, (upgrade_button_rect.x + (upgrade_button_rect.width - upgrade_button_text.get_width()) // 2, upgrade_button_rect.y + (upgrade_button_rect.height - upgrade_button_text.get_height()) // 2))

    # Draw the upgrade cost next to the button
    upgrade_cost_text = small_font.render(f'Cost: {upgrade_cost}', True, BLACK)
    screen.blit(upgrade_cost_text, (upgrade_button_rect.x + upgrade_button_rect.width + 10, upgrade_button_rect.y + (upgrade_button_rect.height - upgrade_cost_text.get_height()) // 2))

    # Draw menu button
    menu_button_center = (WIDTH - 50, 50)
    pygame.draw.circle(screen, BUTTON_COLOR, menu_button_center, 30)
    if menu_icon:
        screen.blit(menu_icon, menu_icon.get_rect(center=menu_button_center))

    # Draw farmers button
    farmers_button_center = (WIDTH - 50, 120)
    pygame.draw.circle(screen, BUTTON_COLOR, farmers_button_center, 30)
    if farmers_icon:
        screen.blit(farmers_icon, farmers_icon.get_rect(center=farmers_button_center))

    pygame.display.flip()

# Function to draw the farmers menu screen
def draw_farmers_menu_screen():
    screen.fill(WHITE)

    # Draw menu title
    farmers_menu_title_text = font.render("Farmers", True, BLACK)
    screen.blit(farmers_menu_title_text, (WIDTH // 2 - farmers_menu_title_text.get_width() // 2, 20))

    # Draw farmer information and buy buttons
    for i in range(3):
        farmer_text = small_font.render(f'Farmer {i + 1}', True, BLACK)
        cost_text = small_font.render(f'Cost: {farmer_costs[i]}', True, BLACK)
        income_text = small_font.render(f'Income: {farmer_incomes[i]}', True, BLACK)
        buy_button_rect = pygame.Rect(450, 200 + i * 120, 100, 40)  # Smaller button

        # Draw texts with more spacing
        screen.blit(farmer_text, (50, 200 + i * 120))
        screen.blit(cost_text, (200, 200 + i * 120))
        screen.blit(income_text, (320, 200 + i * 120))

        # Draw buy button
        pygame.draw.rect(screen, BUTTON_COLOR, buy_button_rect, border_radius=10)
        buy_button_text = small_font.render('Buy', True, FONT_COLOR)
        screen.blit(buy_button_text, (buy_button_rect.x + (buy_button_rect.width - buy_button_text.get_width()) // 2, buy_button_rect.y + (buy_button_rect.height - buy_button_text.get_height()) // 2))

    # Draw back button
    back_button_rect = pygame.Rect(300, 475, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect, border_radius=10)
    back_button_text = font.render('Back', True, FONT_COLOR)
    screen.blit(back_button_text, (back_button_rect.x + (back_button_rect.width - back_button_text.get_width()) // 2, back_button_rect.y + (back_button_rect.height - back_button_text.get_height()) // 2))

    pygame.display.flip()

# Function to draw the menu screen
def draw_menu_screen():
    screen.fill(WHITE)

    # Draw menu title
    menu_title_text = font.render("Menu", True, BLACK)
    screen.blit(menu_title_text, (WIDTH // 2 - menu_title_text.get_width() // 2, 20))

    # Draw statistics
    stats_title_text = small_font.render("Statistics", True, BLACK)
    potatoes_text = small_font.render(f'Potatoes: {potatoes}', True, BLACK)
    click_value_text = small_font.render(f'Click Value: {click_value}', True, BLACK)

    screen.blit(stats_title_text, (30, 100))
    screen.blit(potatoes_text, (30, 150))
    screen.blit(click_value_text, (30, 200))

    # Draw achievements
    achievements_title_text = small_font.render("Achievements", True, BLACK)
    achievement1_text = small_font.render("Achieved 10 Clicks", True, BLACK) if potatoes >= 10 else small_font.render("Achieved 10 Clicks", True, (150, 150, 150))
    achievement2_text = small_font.render("Bought 1 Farmer", True, BLACK) if farmers >= 1 else small_font.render("Bought 1 Farmer", True, (150, 150, 150))

    screen.blit(achievements_title_text, (30, 300))
    screen.blit(achievement1_text, (30, 350))
    screen.blit(achievement2_text, (30, 400))

    # Draw return button
    return_button_rect = pygame.Rect(300, 475, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, return_button_rect, border_radius=10)
    return_button_text = font.render('Return', True, FONT_COLOR)
    screen.blit(return_button_text, (return_button_rect.x + (return_button_rect.width - return_button_text.get_width()) // 2, return_button_rect.y + (return_button_rect.height - return_button_text.get_height()) // 2))

    pygame.display.flip()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Check if click on the "Click!" button
            if not menu_open and not farmers_menu_open and 300 <= mouse_x <= 500 and 350 <= mouse_y <= 450:
                potatoes += click_value

            # Check if click on the "Upgrade" button
            if not menu_open and not farmers_menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                upgrade_button_pressed = True
                if potatoes >= upgrade_cost:
                    potatoes -= upgrade_cost
                    click_value += 1
                    upgrade_cost *= 2  # Double the upgrade cost

            # Check if click on the menu button
            if not farmers_menu_open and (WIDTH - 80 <= mouse_x <= WIDTH - 20) and (20 <= mouse_y <= 80):
                menu_open = True

            # Check if click on the farmers button
            if not menu_open and (WIDTH - 80 <= mouse_x <= WIDTH - 20) and (90 <= mouse_y <= 150):
                farmers_menu_open = True

            # Check if click on the buy buttons in the farmers menu
            if farmers_menu_open:
                for i in range(3):
                    buy_button_rect = pygame.Rect(450, 200 + i * 120, 100, 40)  # Smaller button
                    if buy_button_rect.collidepoint(mouse_x, mouse_y):
                        if potatoes >= farmer_costs[i]:
                            potatoes -= farmer_costs[i]
                            farmers += 1  # Increment farmer count

            # Check if click on the back button in farmers menu
            if farmers_menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                farmers_menu_open = False

            # Check if click on the return button in menu
            if menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                menu_open = False

    # Update the screen based on the current menu state
    if menu_open:
        draw_menu_screen()
    elif farmers_menu_open:
        draw_farmers_menu_screen()
    else:
        draw_game_screen()

    # Control frame rate
    pygame.time.Clock().tick(60)
