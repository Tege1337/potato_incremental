import pygame
import sys
import requests
from io import BytesIO
import time
import json

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
        response.raise_for_status()
        return pygame.image.load(BytesIO(response.content))
    except Exception as e:
        print(f"Error downloading the image: {e}")
        return None

# Icon URLs
menu_icon_url = "https://img.icons8.com/ios-filled/50/000000/menu.png"
farmers_icon_url = "https://img.icons8.com/ios-filled/50/000000/user.png"
user_icon_url = "https://img.icons8.com/ios-filled/50/000000/user.png"

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Potato Clicker")

# Load icons
menu_icon = download_image(menu_icon_url)
farmers_icon = download_image(farmers_icon_url)
user_icon = download_image(user_icon_url)

# Scale the icons
menu_icon = pygame.transform.scale(menu_icon, (40, 40)) if menu_icon else None
farmers_icon = pygame.transform.scale(farmers_icon, (40, 40)) if farmers_icon else None
user_icon = pygame.transform.scale(user_icon, (40, 40)) if user_icon else None

# Fonts
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Game variables
potatoes = 0.0
click_value = 1.0
upgrade_cost = 10.0
farmers = 0
farmer_costs = [50, 250, 500]
farmer_incomes = [1, 2, 3]
farmer_counts = [0, 0, 0]
achievements = []
menu_open = False
farmers_menu_open = False
prestige_menu_open = False
last_farmer_update = time.time()
farmer_generation_interval = 1
prestige_count = 0
prestige_requirement = 100

# Achievements
def check_achievements():
    if potatoes >= 10 and "10 Potatoes" not in achievements:
        achievements.append("10 Potatoes")
    if potatoes >= 50 and "50 Potatoes" not in achievements:
        achievements.append("50 Potatoes")
    if farmers >= 1 and "Bought 1 Farmer" not in achievements:
        achievements.append("Bought 1 Farmer")
    if farmers >= 3 and "Bought 3 Farmers" not in achievements:
        achievements.append("Bought 3 Farmers")
    if click_value >= 10 and "Click Value 10" not in achievements:
        achievements.append("Click Value 10")

# Save progress to a file
def save_progress():
    data = {
        'potatoes': potatoes,
        'click_value': click_value,
        'farmers': farmers,
        'farmer_counts': farmer_counts,
        'achievements': achievements,
        'prestige_count': prestige_count
    }
    with open('save_data.json', 'w') as f:
        json.dump(data, f)

# Load progress from a file
def load_progress():
    global potatoes, click_value, farmers, farmer_counts, achievements, prestige_count
    try:
        with open('save_data.json', 'r') as f:
            data = json.load(f)
            potatoes = data['potatoes']
            click_value = data['click_value']
            farmers = data['farmers']
            farmer_counts = data['farmer_counts']
            achievements = data['achievements']
            prestige_count = data.get('prestige_count', 0)
    except FileNotFoundError:
        pass

# Function to handle prestige
def handle_prestige():
    global potatoes, click_value, prestige_count, prestige_requirement
    if potatoes >= prestige_requirement:
        potatoes = 0
        click_value *= 1.3
        prestige_count += 1
        prestige_requirement = int(prestige_requirement * 1.7)

# Function to draw the main game screen
def draw_game_screen():
    screen.fill(WHITE)
    title_text = font.render("Potato Clicker", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

    potatoes_text = small_font.render(f'Potatoes: {potatoes:.1f}', True, BLACK)
    click_text = small_font.render(f'Click Value: {click_value:.1f}', True, BLACK)

    stat_x = 30
    stat_y = 100
    spacing = 50

    screen.blit(potatoes_text, (stat_x, stat_y))
    screen.blit(click_text, (stat_x, stat_y + spacing))

    button_rect = pygame.Rect(300, 350, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
    button_text = font.render('Click!', True, FONT_COLOR)
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                               button_rect.y + (button_rect.height - button_text.get_height()) // 2))

    upgrade_button_rect = pygame.Rect(300, 475, 200, 100)
    pygame.draw.rect(screen, UPGRADE_COLOR, upgrade_button_rect, border_radius=10)
    upgrade_button_text = font.render('Upgrade', True, FONT_COLOR)
    screen.blit(upgrade_button_text, (upgrade_button_rect.x + (upgrade_button_rect.width - upgrade_button_text.get_width()) // 2,
                                       upgrade_button_rect.y + (upgrade_button_rect.height - upgrade_button_text.get_height()) // 2))

    upgrade_cost_text = small_font.render(f'Cost: {upgrade_cost:.1f}', True, BLACK)
    screen.blit(upgrade_cost_text, (upgrade_button_rect.x + upgrade_button_rect.width + 10, upgrade_button_rect.y + (
        upgrade_button_rect.height - upgrade_cost_text.get_height()) // 2))

    menu_button_center = (WIDTH - 50, 50)
    pygame.draw.circle(screen, BUTTON_COLOR, menu_button_center, 30)
    if menu_icon:
        screen.blit(menu_icon, menu_icon.get_rect(center=menu_button_center))

    farmers_button_center = (WIDTH - 50, 120)
    pygame.draw.circle(screen, BUTTON_COLOR, farmers_button_center, 30)
    if farmers_icon:
        screen.blit(farmers_icon, farmers_icon.get_rect(center=farmers_button_center))

    prestige_button_center = (WIDTH - 50, 190)
    pygame.draw.circle(screen, BUTTON_COLOR, prestige_button_center, 30)
    prestige_text = small_font.render('P', True, FONT_COLOR)
    screen.blit(prestige_text, (prestige_button_center[0] - prestige_text.get_width() // 2,
                                 prestige_button_center[1] - prestige_text.get_height() // 2))

    if menu_open:
        # Draw the menu with stats and achievements
        menu_rect = pygame.Rect(100, 100, 600, 400)
        pygame.draw.rect(screen, WHITE, menu_rect)  # Background
        pygame.draw.rect(screen, BLACK, menu_rect, 5)  # Border

        menu_title = font.render("Menu", True, BLACK)
        screen.blit(menu_title, (menu_rect.x + 20, menu_rect.y + 20))

        # Display achievements
        for i, achievement in enumerate(achievements):
            achievement_text = small_font.render(achievement, True, BLACK)
            screen.blit(achievement_text, (menu_rect.x + 20, menu_rect.y + 70 + i * 30))

    pygame.display.flip()

# Function to draw the farmers menu screen
def draw_farmers_menu_screen():
    screen.fill(WHITE)
    farmers_menu_title_text = font.render("Farmers", True, BLACK)
    screen.blit(farmers_menu_title_text, (WIDTH // 2 - farmers_menu_title_text.get_width() // 2, 20))

    vertical_spacing = 100

    for i in range(3):
        farmer_text = small_font.render(f'Farmer {i + 1}', True, BLACK)
        cost_text = small_font.render(f'Cost: {farmer_costs[i]:.1f}', True, BLACK)
        income_text = small_font.render(f'Income: {farmer_incomes[i]:.1f}', True, BLACK)

        farmer_y_position = 200 + i * vertical_spacing
        screen.blit(farmer_text, (50, farmer_y_position))
        screen.blit(cost_text, (200, farmer_y_position))
        screen.blit(income_text, (350, farmer_y_position))

        buy_button_rect = pygame.Rect(475, farmer_y_position - 10, 100, 40)
        pygame.draw.rect(screen, BUTTON_COLOR, buy_button_rect, border_radius=10)
        buy_button_text = small_font.render('Buy', True, FONT_COLOR)
        screen.blit(buy_button_text, (buy_button_rect.x + (buy_button_rect.width - buy_button_text.get_width()) // 2,
                                       buy_button_rect.y + (buy_button_rect.height - buy_button_text.get_height()) // 2))

        upgrade_button_rect = pygame.Rect(595, farmer_y_position - 10, 100, 40)
        pygame.draw.rect(screen, BUTTON_COLOR, upgrade_button_rect, border_radius=10)
        upgrade_button_text = small_font.render('Upgrade', True, FONT_COLOR)
        screen.blit(upgrade_button_text, (upgrade_button_rect.x + (upgrade_button_rect.width - upgrade_button_text.get_width()) // 2,
                                           upgrade_button_rect.y + (upgrade_button_rect.height - upgrade_button_text.get_height()) // 2))

    back_button_rect = pygame.Rect(300, 475, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect, border_radius=10)
    back_button_text = font.render('Back', True, FONT_COLOR)
    screen.blit(back_button_text, (back_button_rect.x + (back_button_rect.width - back_button_text.get_width()) // 2,
                                   back_button_rect.y + (back_button_rect.height - back_button_text.get_height()) // 2))

    pygame.display.flip()

# Function to draw the prestige menu screen
def draw_prestige_menu_screen():
    screen.fill(WHITE)
    prestige_menu_title_text = font.render("Prestige", True, BLACK)
    screen.blit(prestige_menu_title_text, (WIDTH // 2 - prestige_menu_title_text.get_width() // 2, 20))

    prestige_text = small_font.render(f'Prestige Count: {prestige_count}', True, BLACK)
    screen.blit(prestige_text, (30, 100))

    requirement_text = small_font.render(f'Requirement for Next Prestige: {prestige_requirement}', True, BLACK)
    screen.blit(requirement_text, (30, 150))

    prestige_button_rect = pygame.Rect(300, 350, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, prestige_button_rect, border_radius=10)
    prestige_button_text = font.render('Prestige', True, FONT_COLOR)
    screen.blit(prestige_button_text, (prestige_button_rect.x + (prestige_button_rect.width - prestige_button_text.get_width()) // 2,
                                        prestige_button_rect.y + (prestige_button_rect.height - prestige_button_text.get_height()) // 2))

    back_button_rect = pygame.Rect(300, 475, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect, border_radius=10)
    back_button_text = font.render('Back', True, FONT_COLOR)
    screen.blit(back_button_text, (back_button_rect.x + (back_button_rect.width - back_button_text.get_width()) // 2,
                                   back_button_rect.y + (back_button_rect.height - back_button_text.get_height()) // 2))

    pygame.display.flip()

# Load progress at the start
load_progress()

# Main game loop
while True:
    current_time = time.time()

    # Farmers generate potatoes over time
    if farmers > 0 and current_time - last_farmer_update >= farmer_generation_interval:
        potatoes += sum(farmer_counts[i] * farmer_incomes[i] for i in range(3))
        last_farmer_update = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_progress()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if not menu_open and not farmers_menu_open and not prestige_menu_open and 300 <= mouse_x <= 500 and 350 <= mouse_y <= 450:
                potatoes += click_value

            if not menu_open and not farmers_menu_open and not prestige_menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                if potatoes >= upgrade_cost:
                    potatoes -= upgrade_cost
                    click_value += 1
                    upgrade_cost *= 1.3
                    upgrade_cost = round(upgrade_cost, 1)

            # Check for menu button click
            if (WIDTH - 80 <= mouse_x <= WIDTH - 20) and (20 <= mouse_y <= 80):
                menu_open = not menu_open  # Toggle menu open state

            # Check for farmers button click
            if (WIDTH - 80 <= mouse_x <= WIDTH - 20) and (90 <= mouse_y <= 150):
                farmers_menu_open = True

            # Check for prestige button click
            if (WIDTH - 80 <= mouse_x <= WIDTH - 20) and (160 <= mouse_y <= 220):
                prestige_menu_open = True

            if farmers_menu_open:
                for i in range(3):
                    buy_button_rect = pygame.Rect(475, 200 + i * 120, 100, 40)
                    if buy_button_rect.collidepoint(mouse_x, mouse_y):
                        if potatoes >= farmer_costs[i]:
                            potatoes -= farmer_costs[i]
                            farmer_counts[i] += 1
                            farmers += 1
                            farmer_costs[i] = round(farmer_costs[i] * 1.4, 1)

                    upgrade_button_rect = pygame.Rect(595, 200 + i * 120, 100, 40)
                    if upgrade_button_rect.collidepoint(mouse_x, mouse_y):
                        if farmer_counts[i] > 0 and potatoes >= farmer_incomes[i] * 10:
                            potatoes -= farmer_incomes[i] * 10
                            farmer_incomes[i] += 1

            if farmers_menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                farmers_menu_open = False

            if prestige_menu_open and 300 <= mouse_x <= 500 and 350 <= mouse_y <= 450:
                handle_prestige()

            if prestige_menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                prestige_menu_open = False

            if menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                menu_open = False

    check_achievements()
    if prestige_menu_open:
        draw_prestige_menu_screen()
    elif farmers_menu_open:
        draw_farmers_menu_screen()
    else:
        draw_game_screen()

    pygame.time.Clock().tick(60)
