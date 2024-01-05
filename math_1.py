import pygame
import sys
import random
import time

pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BACKGROUND_COLOR = (38, 70, 83)  # Nice background color

# Fonts
title_font = pygame.font.Font(None, 72)
menu_font = pygame.font.Font(None, 36)
text_font = pygame.font.Font(None, 48)
correct_font = pygame.font.Font(None, 64)  # Bigger font for "Correct!"

# Confetti parameters
confetti_particles = []

# Game variables
score = 0
clock = pygame.time.Clock()
questions_per_round = 10
time_limit_per_question = 10  # in seconds

def generate_question(operation):
    num1 = random.randint(-10, 10)
    num2 = random.randint(1, 10)  # Ensure non-zero denominator for division
    if operation == '+':
        operator = '+'
    elif operation == '-':
        operator = '-'
    elif operation == '*':
        operator = '*'
    elif operation == '/':
        operator = '/'
        # Adjust the numerator to ensure a whole number result
        num1 = num2 * random.randint(1, 10)
    else:
        operator = '+'
    question = f"{num1} {operator} {num2} ="
    
    # Handle division by ensuring that the result is an integer
    if operator == '/' and num1 % num2 != 0:
        num1 = num1 * num2  # Adjust numerator to make the result an integer
    
    answer = eval(f"{num1} {operator} {num2}")
    return question, answer

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def spawn_confetti():
    for _ in range(100):
        confetti_particles.append([random.randint(0, WIDTH), HEIGHT, random.uniform(-1, 1), random.uniform(-4, -1), random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])])

def draw_confetti():
    for particle in confetti_particles:
        pygame.draw.circle(screen, particle[4], (int(particle[0]), int(particle[1])), 5)

def update_confetti():
    for particle in confetti_particles:
        particle[0] += particle[2]
        particle[1] += particle[3]

def show_menu():
    selected_option = 0

    operation_options = ['+', '-', '*', '/']

    while True:
        screen.fill(BACKGROUND_COLOR)

        title_text = title_font.render("Math Game", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        menu_text = menu_font.render("Select Operation:", True, WHITE)
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - 150))

        for i, option in enumerate(operation_options):
            text_color = WHITE if i != selected_option else RED
            draw_text(f"{i + 1}. {option}", menu_font, text_color, WIDTH // 2, HEIGHT // 2 - 50 + i * 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(operation_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(operation_options)
                elif event.key == pygame.K_RETURN:
                    return operation_options[selected_option].lower()  # Return lowercase for the selected operation
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.clear()  # Clear events to prevent capturing Escape in the main loop
                    return None  # Return None when Escape is pressed

        clock.tick(30)




def game_over():
    screen.fill(BACKGROUND_COLOR)
    
    title_text = title_font.render("Game Over", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 150))

    score_text = text_font.render(f"Your score: {score}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))

    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    global score

    while True:
        operation = show_menu()

        if operation is None:
            continue  # Go back to the main menu if operation is None

        start_time = time.time()

        for _ in range(questions_per_round):
            question, correct_answer = generate_question(operation)
            user_answer = ""
            correct_message_displayed = False
            confetti_spawned = False
            escape_pressed = False

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if pygame.K_0 <= event.key <= pygame.K_9 or event.key == pygame.K_MINUS:
                            user_answer += pygame.key.name(event.key)
                        elif event.key == pygame.K_BACKSPACE:
                            user_answer = user_answer[:-1]
                        elif event.key == pygame.K_ESCAPE:
                            escape_pressed = True

                if escape_pressed:
                    break  # Break the inner loop to go back to the main menu

                screen.fill(BACKGROUND_COLOR)

                combined_text = f"{question} {user_answer}"
                draw_text(combined_text, text_font, WHITE, WIDTH // 2, HEIGHT // 2)

                if user_answer.replace('-', '').isdigit() and int(user_answer) == correct_answer and not correct_message_displayed:
                    correct_message_displayed = True
                    draw_text("Correct!", correct_font, GREEN, WIDTH // 2, HEIGHT // 6)

                if correct_message_displayed and not confetti_spawned:
                    spawn_confetti()
                    confetti_spawned = True

                draw_confetti()
                update_confetti()

                pygame.display.flip()

                if user_answer.replace('-', '').isdigit() and int(user_answer) == correct_answer:
                    score += 1
                    pygame.time.wait(1000)
                    break

            elapsed_time = time.time() - start_time

            if escape_pressed or elapsed_time > time_limit_per_question * questions_per_round:
                break  # Break out of the main loop if Escape is pressed or time is up

        game_over()

if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
