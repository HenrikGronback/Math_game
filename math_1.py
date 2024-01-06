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
question_font = pygame.font.Font(None, 65)
correct_font = pygame.font.Font(None, 64)  # Bigger font for "Correct!"

# Confetti parameters
confetti_particles = []

# Game variables
score = 0
clock = pygame.time.Clock()
questions_per_round = 10

# Operation symbols for generating questions
operation_symbols = {
    'addition': '+',
    'subtraction': '-',
    'multiplication': '*',
    'division': '/',
    'mixed mode': None  # No specific symbol for mixed mode
}

# Define a dictionary to store the fastest times for each operation
fastest_times = {
    'addition': float('inf'),
    'subtraction': float('inf'),
    'multiplication': float('inf'),
    'division': float('inf'),
    'mixed mode': float('inf')
}

def generate_question(operation=None):
    num1 = random.randint(-10, 10)
    num2 = random.randint(1, 10)  # Ensure non-zero denominator for division
    operator = operation if operation else random.choice(['+', '-', '*', '/'])

    if operator == '/':
        # Adjust the numerator to ensure a whole number result
        num1 = num2 * random.randint(1, 10)
    
    question = f"{num1} {operator} {num2} ="
    answer = eval(f"{num1} {operator} {num2}")
    return question, answer

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def spawn_confetti():
    for _ in range(100):
        # Increase the values here for faster confetti
        confetti_particles.append([
            random.randint(0, WIDTH),
            HEIGHT,
            random.uniform(-2, 2),  # Faster horizontal movement
            random.uniform(-24, -8),  # Faster vertical movement
            random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255)])
        ])

def draw_confetti():
    for particle in confetti_particles:
        pygame.draw.circle(screen, particle[4], (int(particle[0]), int(particle[1])), 5)

def update_confetti():
    for particle in confetti_particles:
        particle[0] += particle[2]
        particle[1] += particle[3]

def show_menu():
    selected_option = 0
    operation_options = ['Addition', 'Subtraction', 'Multiplication', 'Division', 'Mixed Mode']

    while True:
        screen.fill(BACKGROUND_COLOR)

        title_text = title_font.render("Math Game", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        menu_text = menu_font.render("Select Operation:", True, WHITE)
        screen.blit(menu_text, (WIDTH // 2 - menu_text.get_width() // 2, HEIGHT // 2 - 150))

        for i, option in enumerate(operation_options):
            text_color = WHITE if i != selected_option else GREEN
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
                    return operation_options[selected_option]  # Return the selected operation as is
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.clear()  # Clear events to prevent capturing Escape in the main loop
                    return None  # Return None when Escape is pressed

        clock.tick(30)

def game_overs(start_time, operation, correct_answer, user_answer, question):
    screen.fill(BACKGROUND_COLOR)

    # Display "Game Over" title
    title_text = title_font.render("Game Over", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 100))

    # Display the question
    question_text = text_font.render(f"{question}", True, WHITE)
    screen.blit(question_text, (WIDTH // 2 - question_text.get_width() // 2, 200))

    # Display the correct answer
    correct_answer_text = text_font.render(f"Correct Answer: {correct_answer}", True, GREEN)
    screen.blit(correct_answer_text, (WIDTH // 2 - correct_answer_text.get_width() // 2, 300))

    # Display the user's answer
    user_answer_text = text_font.render(f"Your Answer: {user_answer}", True, RED)
    screen.blit(user_answer_text, (WIDTH // 2 - user_answer_text.get_width() // 2, 400))

    pygame.display.flip()
    pygame.time.wait(3000)

def draw_progress_bar(current, total, bar_width=600, bar_height=20):
    progress = current / total
    fill_width = progress * bar_width

    bar_x = (WIDTH - bar_width) // 2
    bar_y = HEIGHT - 50  # Positioning the bar at the bottom

    pygame.draw.rect(screen, WHITE, [bar_x, bar_y, bar_width, bar_height], 2)  # Border of the bar
    pygame.draw.rect(screen, GREEN, [bar_x, bar_y, fill_width, bar_height])  # Filled part of the bar




def winning_screen(start_time, operation):
    screen.fill(BACKGROUND_COLOR)
    
    title_text = title_font.render("Good job!", True, GREEN)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 150))

    # Display elapsed time in seconds
    elapsed_time = time.time() - start_time
    elapsed_time_text = text_font.render(f"Time: {elapsed_time:.2f} seconds", True, WHITE)
    screen.blit(elapsed_time_text, (WIDTH // 2 - elapsed_time_text.get_width() // 2, HEIGHT // 2 + 50))

    # Display the fastest time for the current operation in seconds (convert to lowercase)
    fastest_time = fastest_times.get(operation.lower())
    if fastest_time is not None and fastest_time != float('inf'):
        fastest_time_text = text_font.render(f"Fastest time: {fastest_time:.2f} seconds", True, WHITE)
    else:
        fastest_time_text = text_font.render("Fastest time: N/A", True, WHITE)

    screen.blit(fastest_time_text, (WIDTH // 2 - fastest_time_text.get_width() // 2, HEIGHT // 2 + 100))

    pygame.display.flip()
    pygame.time.wait(3000)

def main():
    while True:
        operation = show_menu()

        if operation is None:
            continue  # Go back to the main menu if operation is None

        game_continues = True
        current_question_number = 0

        start_time = time.time()  # Start the timer at the beginning of the round
        fastest_time_for_operation = fastest_times.get(operation.lower(), float('inf'))  # Get the fastest time for the current operation

        for _ in range(questions_per_round):
            current_question_number += 1
            if not game_continues:
                break  # Exit the questions loop if Escape is pressed

            if operation.lower() == 'mixed mode':
                question, correct_answer = generate_question()  # For mixed mode
            else:
                operation_symbol = operation_symbols[operation.lower()]
                question, correct_answer = generate_question(operation_symbol)  # For single operation mode

            user_answer = ""
            answer_submitted = False
            correct_message_displayed = False

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
                        elif event.key == pygame.K_RETURN:
                            answer_submitted = True
                        elif event.key == pygame.K_ESCAPE:
                            game_continues = False
                            break

                if not game_continues:
                    break  # Break the inner loop to go back to the main menu

                screen.fill(BACKGROUND_COLOR)

                # Draw the timer and fastest time for the current operation
                draw_text(f"Time: {time.time() - start_time:.2f}s", text_font, WHITE, 120, 30)

# Fastest time for the operation on the top right
                if fastest_time_for_operation == float("inf"):
                    fastest_time_text = f"Fastest time: None"
                else:
                    fastest_time_text = f"Fastest time: {fastest_time_for_operation:.2f}s"

                draw_text(fastest_time_text, text_font, WHITE, WIDTH + 110 - text_font.size(fastest_time_text)[0], 30)

                combined_text = f"{question} {user_answer}"
                draw_text(combined_text, question_font, WHITE, WIDTH // 2, HEIGHT // 2)

                if answer_submitted:
                    if user_answer.replace('-', '').isdigit() and int(user_answer) == correct_answer:
                        correct_message_displayed = True
                        spawn_confetti()  # Spawn confetti

                        for _ in range(50):  # Confetti animation loop
                            update_confetti()  # Update confetti positions
                            screen.fill(BACKGROUND_COLOR)

                            draw_text(f"Time: {time.time() - start_time:.2f}s", text_font, WHITE, 120, 30)

# Fastest time for the operation on the top right
                            if fastest_time_for_operation == float("inf"):
                                fastest_time_text = f"Fastest time: None"
                            else:
                                fastest_time_text = f"Fastest time: {fastest_time_for_operation:.2f}s"
                            draw_text(fastest_time_text, text_font, WHITE, WIDTH + 110 - text_font.size(fastest_time_text)[0], 30)

                            combined_text = f"{question} {user_answer}"
                            draw_text(combined_text, question_font, WHITE, WIDTH // 2, HEIGHT // 2)

                            if correct_message_displayed:
                                draw_text("Correct!", correct_font, GREEN, WIDTH // 2, HEIGHT // 6)

                            draw_progress_bar(current_question_number, questions_per_round)

                            draw_confetti()  # Draw confetti
                            pygame.display.flip()
                            pygame.time.delay(20)  # Short delay for each frame of confetti animation

                        break
                    else:
                        game_overs(start_time, operation, correct_answer, user_answer, question)
                        game_continues = False
                        break

                draw_progress_bar(current_question_number - 1, questions_per_round)

                pygame.display.flip()

            if not game_continues:
                break

        if not game_continues:
            continue

        # Update the fastest time for the current operation
        if time.time() - start_time < fastest_time_for_operation:
            fastest_time_for_operation = time.time() - start_time
            fastest_times[operation.lower()] = fastest_time_for_operation

        winning_screen(start_time, operation)

        # Reset the timer for the next round
        start_time = 0

if __name__ == "__main__":
    main()
