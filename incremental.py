import pygame
import sys
import requests
from io import BytesIO
import time

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 200, 0)
UPGRADE_COLOR = (200, 0, 0)
FONT_COLOR = (255, 255, 255)
BUTTON_HOVER_COLOR = (0, 255, 0)
UPGRADE_HOVER_COLOR = (255, 0, 0)
BUTTON_PRESS_COLOR = (0, 150, 0)
UPGRADE_PRESS_COLOR = (150, 0, 0)


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
menu_icon = pygame.transform.scale(menu_icon, (30, 30)) if menu_icon else None
farmers_icon = pygame.transform.scale(farmers_icon, (30, 30)) if farmers_icon else None

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Game variables
score = 0
click_value = 1
upgrade_cost = 10
upgrades = 0
farmers = 0
farmer_cost = 50
farmer_income = 1  # Income per second from one farmer
last_update_time = time.time()  # For automatic income calculation
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
    score_text = small_font.render(f'Score: {score}', True, BLACK)
    click_text = small_font.render(f'Click Value: {click_value}', True, BLACK)
    upgrade_text = small_font.render(f'Upgrade Cost: {upgrade_cost}', True, BLACK)
    upgrades_text = small_font.render(f'Upgrades: {upgrades}', True, BLACK)
    farmers_text = small_font.render(f'Farmers: {farmers}', True, BLACK)

    screen.blit(score_text, (30, 100))
    screen.blit(click_text, (30, 150))
    screen.blit(upgrade_text, (30, 200))
    screen.blit(upgrades_text, (30, 250))
    screen.blit(farmers_text, (30, 300))

    # Draw the click button with hover and press effect
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(300, 350, 200, 100)
    if button_rect.collidepoint(mouse_x, mouse_y):
        button_color = BUTTON_HOVER_COLOR if not button_pressed else BUTTON_PRESS_COLOR
    else:
        button_color = BUTTON_COLOR

    # Draw button and border
    pygame.draw.rect(screen, button_color, button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, button_rect, 3, border_radius=10)  # Border
    button_text = font.render('Click!', True, FONT_COLOR)
    button_rect_center = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_rect_center)

    # Draw the upgrade button with hover and press effect
    upgrade_button_rect = pygame.Rect(300, 475, 200, 100)
    if upgrade_button_rect.collidepoint(mouse_x, mouse_y):
        upgrade_button_color = UPGRADE_HOVER_COLOR if not upgrade_button_pressed else UPGRADE_PRESS_COLOR
    else:
        upgrade_button_color = UPGRADE_COLOR

    # Draw button and border
    pygame.draw.rect(screen, upgrade_button_color, upgrade_button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, upgrade_button_rect, 3, border_radius=10)  # Border
    upgrade_button_text = font.render('Upgrade', True, FONT_COLOR)
    upgrade_button_rect_center = upgrade_button_text.get_rect(center=upgrade_button_rect.center)
    screen.blit(upgrade_button_text, upgrade_button_rect_center)

    # Draw rounded menu button
    menu_button_center = (WIDTH - 50, 50)
    menu_button_radius = 30
    pygame.draw.circle(screen, BUTTON_COLOR, menu_button_center, menu_button_radius)
    pygame.draw.circle(screen, BLACK, menu_button_center, menu_button_radius, 3)  # Border
    if menu_icon:
        icon_rect = menu_icon.get_rect(center=menu_button_center)
        screen.blit(menu_icon, icon_rect)

    # Draw rounded farmers button with added padding
    farmers_button_center = (WIDTH - 50, 120)  # Increased vertical position for padding
    pygame.draw.circle(screen, BUTTON_COLOR, farmers_button_center, menu_button_radius)
    pygame.draw.circle(screen, BLACK, farmers_button_center, menu_button_radius, 3)  # Border
    if farmers_icon:
        farmers_icon_rect = farmers_icon.get_rect(center=farmers_button_center)
        screen.blit(farmers_icon, farmers_icon_rect)

    pygame.display.flip()


# Function to draw the farmers menu screen
def draw_farmers_menu_screen():
    screen.fill(WHITE)

    # Draw menu title
    farmers_menu_title_text = font.render("Farmers", True, BLACK)
    screen.blit(farmers_menu_title_text, (WIDTH // 2 - farmers_menu_title_text.get_width() // 2, 20))

    # Draw stats
    farmers_text = small_font.render(f'Farmers: {farmers}', True, BLACK)
    farmers_cost_text = small_font.render(f'Farmer Cost: {farmer_cost}', True, BLACK)
    screen.blit(farmers_text, (30, 100))
    screen.blit(farmers_cost_text, (30, 150))

    # Draw buy farmer button
    buy_farmer_button_rect = pygame.Rect(300, 350, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, buy_farmer_button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, buy_farmer_button_rect, 3, border_radius=10)  # Border
    buy_farmer_button_text = font.render('Buy Farmer', True, FONT_COLOR)
    buy_farmer_button_rect_center = buy_farmer_button_text.get_rect(center=buy_farmer_button_rect.center)
    screen.blit(buy_farmer_button_text, buy_farmer_button_rect_center)

    # Draw back button
    back_button_rect = pygame.Rect(300, 475, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect, border_radius=10)
    pygame.draw.rect(screen, BLACK, back_button_rect, 3, border_radius=10)  # Border
    back_button_text = font.render('Back', True, FONT_COLOR)
    back_button_rect_center = back_button_text.get_rect(center=back_button_rect.center)
    screen.blit(back_button_text, back_button_rect_center)

    pygame.display.flip()


# Main game loop
while True:
    current_time = time.time()

    # Generate potatoes from farmers every second
    if current_time - last_update_time >= 1:
        score += farmers * farmer_income
        last_update_time = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # Check if click on the "Click!" button
            if not menu_open and not farmers_menu_open and 300 <= mouse_x <= 500 and 350 <= mouse_y <= 450:
                button_pressed = True
                score += click_value

            # Check if click on the "Upgrade" button
            if not menu_open and not farmers_menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                upgrade_button_pressed = True
                if score >= upgrade_cost:
                    score -= upgrade_cost
                    upgrades += 1
                    click_value += 1  # Increase the value of each click
                    upgrade_cost = int(upgrade_cost * 1.5)  # Increase the cost of the next upgrade

            # Check if click on the "Menu" button
            if not menu_open and not farmers_menu_open:
                if (mouse_x - (WIDTH - 50)) ** 2 + (mouse_y - 50) ** 2 <= 30 ** 2:  # Circular collision
                    menu_open = True

            # Check if click on the "Farmers" button
            if not menu_open and not farmers_menu_open:
                if (mouse_x - (WIDTH - 50)) ** 2 + (mouse_y - 120) ** 2 <= 30 ** 2:  # Circular collision
                    farmers_menu_open = True

            # Check if click on the "Buy Farmer" button in the farmers menu
            if farmers_menu_open and 300 <= mouse_x <= 500 and 350 <= mouse_y <= 450:
                if score >= farmer_cost:
                    score -= farmer_cost
                    farmers += 1
                    farmer_cost = int(farmer_cost * 1.5)  # Increase cost for the next farmer

            # Check if click on the "Back" button in the farmers menu
            if farmers_menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                farmers_menu_open = False

        if event.type == pygame.MOUSEBUTTONUP:
            button_pressed = False
            upgrade_button_pressed = False

    if farmers_menu_open:
        draw_farmers_menu_screen()
    elif menu_open:
        draw_menu_screen()
    else:
        draw_game_screen()
