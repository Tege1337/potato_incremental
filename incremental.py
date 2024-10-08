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
farmer_names = ["John Doe", "Jesus Christ", "Adolf Hitler"]


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
prestige_icon_url = "https://img.icons8.com/ios-filled/50/000000/up-arrow.png"  # Arrow icon for prestige

# Initialize Pygame
pygame.init()

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Potato Clicker")

# Load icons
menu_icon = download_image(menu_icon_url)
farmers_icon = download_image(farmers_icon_url)
prestige_icon = download_image(prestige_icon_url)  # Load the prestige icon

# Scale the icons
menu_icon = pygame.transform.scale(menu_icon, (40, 40)) if menu_icon else None
farmers_icon = pygame.transform.scale(farmers_icon, (40, 40)) if farmers_icon else None
prestige_icon = pygame.transform.scale(prestige_icon, (40, 40)) if prestige_icon else None  # Scale the prestige icon

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
prestige_requirement = 500
prestige_multiplier = 1.0  # Multiplier for potatoes based on prestige
achievement_multiplier = 1.0  # Multiplier for potatoes based on achievements
pps_accumulator = 0.0  # Accumulator for PPS
pps_interval = 0.1  # Time interval for PPS update

# Prestige upgrades
prestige_upgrades = {
    'Click Value Boost': {'cost': 1, 'effect': lambda: increase_click_value(1), 'purchased': False},
    'Farmer Efficiency': {'cost': 2, 'effect': lambda: increase_farmer_income(1), 'purchased': False}
}


# Achievements
def check_achievements():
    global achievement_multiplier
    if potatoes >= 10 and "10 Potatoes" not in achievements:
        achievements.append("10 Potatoes")
        achievement_multiplier += 0.02
    if potatoes >= 50 and "50 Potatoes" not in achievements:
        achievements.append("50 Potatoes")
        achievement_multiplier += 0.02
    if farmers >= 1 and "Bought 1 Farmer" not in achievements:
        achievements.append("Bought 1 Farmer")
        achievement_multiplier += 0.02
    if farmers >= 3 and "Bought 3 Farmers" not in achievements:
        achievements.append("Bought 3 Farmers")
        achievement_multiplier += 0.02
    if click_value >= 10 and "Click Value 10" not in achievements:
        achievements.append("Click Value 10")
        achievement_multiplier += 0.02
    if click_value >= 100 and "Click Value 100" not in achievements:
        achievements.append("Click Value 100")
        achievement_multiplier += 0.02
    if prestige_count >= 1 and "First Prestige" not in achievements:
        achievements.append("First Prestige")
        achievement_multiplier += 0.02
    if prestige_count >= 5 and "5 Prestiges" not in achievements:
        achievements.append("5 Prestiges")
        achievement_multiplier += 0.02
    if prestige_count >= 10 and "10 Prestiges" not in achievements:
        achievements.append("10 Prestiges")
        achievement_multiplier += 0.02
    if potatoes >= 100 and "100 Potatoes" not in achievements:
        achievements.append("100 Potatoes")
        achievement_multiplier += 0.02
    if potatoes >= 500 and "500 Potatoes" not in achievements:
        achievements.append("500 Potatoes")
        achievement_multiplier += 0.02
    if farmers >= 5 and "Bought 5 Farmers" not in achievements:
        achievements.append("Bought 5 Farmers")
        achievement_multiplier += 0.02
    if farmers >= 10 and "Bought 10 Farmers" not in achievements:
        achievements.append("Bought 10 Farmers")
        achievement_multiplier += 0.02
    if click_value >= 20 and "Click Value 20" not in achievements:
        achievements.append("Click Value 20")
        achievement_multiplier += 0.02
    if potatoes >= 1000 and "1000 Potatoes" not in achievements:
        achievements.append("1000 Potatoes")
        achievement_multiplier += 0.02
    if potatoes >= 10000 and "10000 Potatoes" not in achievements:
        achievements.append("10000 Potatoes")
        achievement_multiplier += 0.02
    if farmers >= 2 and "Bought 2 Farmers" not in achievements:
        achievements.append("Bought 2 Farmers")
        achievement_multiplier += 0.02
    if farmers >= 5 and "Bought 5 Farmers" not in achievements:
        achievements.append("Bought 5 Farmers")
        achievement_multiplier += 0.02
    if farmers >= 10 and "Bought 10 Farmers" not in achievements:
        achievements.append("Bought 10 Farmers")
        achievement_multiplier += 0.02
    if potatoes >= 1000 and "1000 Potatoes" not in achievements:
        achievements.append("1000 Potatoes")
        achievement_multiplier += 0.02
    if prestige_count >= 3 and "Prestiged 3 Times" not in achievements:
        achievements.append("Prestiged 3 Times")
        achievement_multiplier += 0.02
    if potatoes >= 5000 and "5000 Potatoes" not in achievements:
        achievements.append("5000 Potatoes")
        achievement_multiplier += 0.02
    if farmers >= 20 and "Bought 20 Farmers" not in achievements:
        achievements.append("Bought 20 Farmers")
        achievement_multiplier += 0.02
    if click_value >= 50 and "Click Value 50" not in achievements:
        achievements.append("Click Value 50")
        achievement_multiplier += 0.02
    if potatoes >= 10000 and "10000 Potatoes" not in achievements:
        achievements.append("10000 Potatoes")
        achievement_multiplier += 0.02
    if farmers >= 50 and "Bought 50 Farmers" not in achievements:
        achievements.append("Bought 50 Farmers")
        achievement_multiplier += 0.02


def save_progress():
    data = {
        'potatoes': potatoes,
        'click_value': click_value,
        'farmers': farmers,
        'farmer_counts': farmer_counts,
        'achievements': achievements,
        'prestige_count': prestige_count,
        'prestige_multiplier': prestige_multiplier,
        'achievement_multiplier': achievement_multiplier,
        'upgrade_cost': upgrade_cost,  # Include upgrade cost
        'farmer_costs': farmer_costs,  # Include farmer costs
        'farmer_incomes': farmer_incomes,  # Include farmer incomes
    }
    with open('save_data.json', 'w') as f:
        json.dump(data, f)


# Load progress from a file
def load_progress():
    global potatoes, click_value, farmers, farmer_counts, achievements
    global prestige_count, prestige_multiplier, achievement_multiplier
    global upgrade_cost, farmer_costs, farmer_incomes  # Add the new variables

    try:
        with open('save_data.json', 'r') as f:
            data = json.load(f)
            potatoes = data['potatoes']
            click_value = data['click_value']
            farmers = data['farmers']
            farmer_counts = data['farmer_counts']
            achievements = data['achievements']
            prestige_count = data.get('prestige_count', 0)
            prestige_multiplier = data.get('prestige_multiplier', 1.0)
            achievement_multiplier = data.get('achievement_multiplier', 1.0)
            upgrade_cost = data.get('upgrade_cost', 10.0)  # Load upgrade cost
            farmer_costs = data.get('farmer_costs', [50, 250, 500])  # Load farmer costs
            farmer_incomes = data.get('farmer_incomes', [1, 2, 3])  # Load farmer incomes
    except FileNotFoundError:
        pass


# Function to increase click value
def increase_click_value(amount):
    global click_value
    click_value += amount

def calculate_potatoes_per_second():
    return sum(farmer_counts[i] * farmer_incomes[i] for i in range(len(farmer_counts)))

# Function to increase farmer income
def increase_farmer_income(amount):
    global farmer_incomes
    for i in range(len(farmer_incomes)):
        farmer_incomes[i] += amount


# Function to handle prestige
def handle_prestige():
    global potatoes, click_value, prestige_count, prestige_requirement, farmers, farmer_counts, upgrade_cost, prestige_multiplier

    if potatoes >= prestige_requirement:
        # Reset game variables except prestige_count and prestige_multiplier
        potatoes = 0
        click_value = 1.0  # Reset click value to its initial state
        farmers = 0  # Reset the number of farmers
        farmer_counts = [0, 0, 0]  # Reset farmer counts
        upgrade_cost = 10.0  # Reset upgrade cost
        prestige_count += 1
        prestige_multiplier *= 1.3  # Increase potato gain by 1.3x
        prestige_requirement = int(prestige_requirement * 1.7)


# Function to draw the main game screen
def draw_game_screen():
    screen.fill(WHITE)
    title_text = font.render("Potato Clicker", True, BLACK)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

    modified_click_value = click_value * prestige_multiplier * achievement_multiplier
    potatoes_text = small_font.render(f'Potatoes: {potatoes:.1f}', True, BLACK)
    click_text = small_font.render(f'Click Value: {modified_click_value:.2f}', True, BLACK)

    # Calculate potatoes per second
    pps = calculate_potatoes_per_second()
    pps_text = small_font.render(f'Potatoes per Second: {pps:.1f}', True, BLACK)

    stat_x = 30
    stat_y = 100
    spacing = 50

    screen.blit(potatoes_text, (stat_x, stat_y))
    screen.blit(click_text, (stat_x, stat_y + spacing))
    screen.blit(pps_text, (stat_x, stat_y + spacing * 2))  # Display PPS below click value

    button_rect = pygame.Rect(300, 350, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect, border_radius=10)
    button_text = font.render('Click!', True, FONT_COLOR)
    screen.blit(button_text, (button_rect.x + (button_rect.width - button_text.get_width()) // 2,
                              button_rect.y + (button_rect.height - button_text.get_height()) // 2))

    upgrade_button_rect = pygame.Rect(300, 475, 200, 100)
    pygame.draw.rect(screen, UPGRADE_COLOR, upgrade_button_rect, border_radius=10)
    upgrade_button_text = font.render('Upgrade', True, FONT_COLOR)
    screen.blit(upgrade_button_text,
                (upgrade_button_rect.x + (upgrade_button_rect.width - upgrade_button_text.get_width()) // 2,
                 upgrade_button_rect.y + (upgrade_button_rect.height - upgrade_button_text.get_height()) // 2))

    upgrade_cost_text = small_font.render(f'Cost: {upgrade_cost:.1f}', True, BLACK)
    screen.blit(upgrade_cost_text, (upgrade_button_rect.x + upgrade_button_rect.width + 10, upgrade_button_rect.y + (
            upgrade_button_rect.height - upgrade_cost_text.get_height()) // 2))

    # Draw menu buttons
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
    if prestige_icon:
        screen.blit(prestige_icon, prestige_icon.get_rect(center=prestige_button_center))

    achievements_text = small_font.render(f'Achievements: {len(achievements)}', True, BLACK)
    screen.blit(achievements_text, (30, HEIGHT - 50))

    pygame.display.flip()


# Function to draw the farmers menu screen
def draw_farmers_menu_screen():
    screen.fill(WHITE)
    farmers_menu_title_text = font.render("Farmers", True, BLACK)
    screen.blit(farmers_menu_title_text, (WIDTH // 2 - farmers_menu_title_text.get_width() // 2, 20))

    vertical_spacing = 80
    for i in range(3):
        farmer_text = small_font.render(f'{farmer_names[i]}: Cost: {farmer_costs[i]}, Income: {farmer_incomes[i]}', True, BLACK)
        screen.blit(farmer_text, (30, 100 + i * vertical_spacing))

        buy_button_rect = pygame.Rect(475, 100 + i * vertical_spacing, 100, 40)
        pygame.draw.rect(screen, BUTTON_COLOR, buy_button_rect, border_radius=10)
        buy_button_text = small_font.render('Buy', True, FONT_COLOR)
        screen.blit(buy_button_text, (buy_button_rect.x + (buy_button_rect.width - buy_button_text.get_width()) // 2,
                                       buy_button_rect.y + (buy_button_rect.height - buy_button_text.get_height()) // 2))

        upgrade_button_rect = pygame.Rect(595, 100 + i * vertical_spacing, 100, 40)
        pygame.draw.rect(screen, BUTTON_COLOR, upgrade_button_rect, border_radius=10)
        upgrade_button_text = small_font.render('Upgrade', True, FONT_COLOR)
        screen.blit(upgrade_button_text,
                    (upgrade_button_rect.x + (upgrade_button_rect.width - upgrade_button_text.get_width()) // 2,
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
    screen.blit(prestige_button_text,
                (prestige_button_rect.x + (prestige_button_rect.width - prestige_button_text.get_width()) // 2,
                 prestige_button_rect.y + (prestige_button_rect.height - prestige_button_text.get_height()) // 2))

    back_button_rect = pygame.Rect(300, 475, 200, 100)
    pygame.draw.rect(screen, BUTTON_COLOR, back_button_rect, border_radius=10)
    back_button_text = font.render('Back', True, FONT_COLOR)
    screen.blit(back_button_text, (back_button_rect.x + (back_button_rect.width - back_button_text.get_width()) // 2,
                                   back_button_rect.y + (back_button_rect.height - back_button_text.get_height()) // 2))

    # Draw prestige upgrades
    upgrade_y = 220
    for upgrade_name, upgrade in prestige_upgrades.items():
        upgrade_text = small_font.render(f'{upgrade_name}: Cost: {upgrade["cost"]}', True, BLACK)
        screen.blit(upgrade_text, (30, upgrade_y))
        if not upgrade['purchased']:
            upgrade_button_rect = pygame.Rect(475, upgrade_y, 100, 40)
            pygame.draw.rect(screen, BUTTON_COLOR, upgrade_button_rect, border_radius=10)
            upgrade_button_text = small_font.render('Buy', True, FONT_COLOR)
            screen.blit(upgrade_button_text,
                        (upgrade_button_rect.x + (upgrade_button_rect.width - upgrade_button_text.get_width()) // 2,
                         upgrade_button_rect.y + (upgrade_button_rect.height - upgrade_button_text.get_height()) // 2))
        upgrade_y += 50

    pygame.display.flip()


# Load progress at the start
load_progress()

# Main game loop
while True:
    current_time = time.time()
    last_update_time = time.time()  # Initialize last update time

    # Farmers generate potatoes over time
    if farmers > 0 and current_time - last_farmer_update >= farmer_generation_interval:
        potatoes += sum(
            farmer_counts[i] * farmer_incomes[i] * prestige_multiplier * achievement_multiplier for i in range(3))
        last_farmer_update = current_time

    # Calculate potatoes per second
    pps = calculate_potatoes_per_second()

    # Update the accumulator
    pps_accumulator += current_time - last_update_time

    # If 0.1 seconds have passed, give the player 10% of the PPS
    if pps_accumulator >= pps_interval:
        potatoes += pps * 0.1 * (pps_accumulator // pps_interval)
        pps_accumulator %= pps_interval  # Reset the accumulator for the remainder

    # Farmers generate potatoes over time
    if farmers > 0 and current_time - last_farmer_update >= farmer_generation_interval:
        potatoes += sum(
            farmer_counts[i] * farmer_incomes[i] * prestige_multiplier * achievement_multiplier for i in range(3))
        last_farmer_update = current_time

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_progress()
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if not menu_open and not farmers_menu_open and not prestige_menu_open and 300 <= mouse_x <= 500 and 350 <= mouse_y <= 450:
                potatoes += click_value * prestige_multiplier * achievement_multiplier

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
                vertical_spacing = 80  # Define vertical spacing for farmer buttons
                for i in range(3):
                    buy_button_rect = pygame.Rect(475, 100 + i * vertical_spacing, 100, 40)
                    if buy_button_rect.collidepoint(mouse_x, mouse_y):
                        if potatoes >= farmer_costs[i]:
                            potatoes -= farmer_costs[i]
                            farmer_counts[i] += 1  # Increase the number of farmers bought
                            farmers += 1  # Total farmers count
                            farmer_costs[i] = round(farmer_costs[i] * 1.4, 1)  # Increase cost for the next farmer

                    upgrade_button_rect = pygame.Rect(595, 100 + i * vertical_spacing, 100, 40)
                    if upgrade_button_rect.collidepoint(mouse_x, mouse_y):
                        if farmer_counts[i] > 0 and potatoes >= farmer_incomes[i] * 10:
                            potatoes -= farmer_incomes[i] * 10
                            farmer_incomes[i] = round(farmer_incomes[i] * 1.2, 1)  # Increase income by 20% on upgrade

            if farmers_menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                farmers_menu_open = False

            if prestige_menu_open and 300 <= mouse_x <= 500 and 350 <= mouse_y <= 450:
                handle_prestige()

            if prestige_menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                prestige_menu_open = False

            if menu_open and 300 <= mouse_x <= 500 and 475 <= mouse_y <= 575:
                menu_open = False

            # Handle prestige upgrades
            if prestige_menu_open:
                upgrade_y = 220
                for upgrade_name, upgrade in prestige_upgrades.items():
                    if not upgrade['purchased']:
                        upgrade_button_rect = pygame.Rect(475, upgrade_y, 100, 40)
                        if upgrade_button_rect.collidepoint(mouse_x, mouse_y):
                            if potatoes >= upgrade['cost']:
                                potatoes -= upgrade['cost']
                                upgrade['effect']()
                                upgrade['purchased'] = True
                                prestige_multiplier *= 1.1  # Example effect of the upgrade
                    upgrade_y += 50
            last_update_time = current_time  # Update the last update time

    if farmers_menu_open:
        draw_farmers_menu_screen()
    elif prestige_menu_open:
        draw_prestige_menu_screen()
    else:
        draw_game_screen()

    check_achievements()
