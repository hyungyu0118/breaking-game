import pygame
import sys
import random
import time

# 초기 설정
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("벽돌 깨기 게임")
clock = pygame.time.Clock()

# 색상 설정
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 패들 설정
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 10
paddle_x = WIDTH // 2 - PADDLE_WIDTH // 2
paddle_y = HEIGHT - 30
paddle_speed = 7

# 공 설정
BALL_SIZE = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 4 * random.choice((1, -1))  # 랜덤한 방향으로 시작
ball_speed_y = 4
ball_moving = False  # 공이 움직이는 상태 여부

# 벽돌 설정
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 20
bricks = []

# 벽돌 배열 만들기
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_x = col * BRICK_WIDTH
        brick_y = row * BRICK_HEIGHT + 30
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# 폰트 설정
font = pygame.font.SysFont('Arial', 24)

# 타이머 설정
start_time = pygame.time.get_ticks()  # 시작 시각

# 게임 루프
running = True
while running:
    screen.fill(BLACK)

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 키 입력 처리
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += paddle_speed

    # 3초 타이머 체크
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # 경과 시간 계산
    if elapsed_time < 3:
        # 화면 중앙에 타이머 표시
        timer_text = font.render(f"Game starts in: {3 - elapsed_time}", True, WHITE)
        screen.blit(timer_text, (WIDTH // 2 - timer_text.get_width() // 2, HEIGHT // 2 - timer_text.get_height() // 2))
    else:
        ball_moving = True  # 3초 이후에 공을 움직이도록 설정

    # 공 이동
    if ball_moving:
        ball_x += ball_speed_x
        ball_y += ball_speed_y

    # 벽에 부딪혀서 반사
    if ball_x <= 0 or ball_x >= WIDTH - BALL_SIZE:
        ball_speed_x = -ball_speed_x
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y
    if ball_y >= HEIGHT:
        running = False  # 공이 바닥에 닿으면 게임 종료

    # 패들에 부딪히면 반사
    paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    if paddle_rect.collidepoint(ball_x, ball_y + BALL_SIZE):
        ball_speed_y = -ball_speed_y

    # 벽돌에 부딪히면 반사 및 제거
    ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
    for brick in bricks[:]:
        if ball_rect.colliderect(brick):
            bricks.remove(brick)
            ball_speed_y = -ball_speed_y
            break

    # 벽돌, 패들, 공 그리기
    pygame.draw.rect(screen, WHITE, paddle_rect)
    pygame.draw.ellipse(screen, BLUE, ball_rect)
    for brick in bricks:
        pygame.draw.rect(screen, RED, brick)

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()