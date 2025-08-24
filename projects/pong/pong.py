import pygame
import sys
import random

# 1. 初始化 Pygame
pygame.init()

# 2. 設定螢幕尺寸和顏色
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
BG_COLOR = pygame.Color('#008000')      # 桌球綠
PADDLE_COLOR = pygame.Color('#FFFFFF')  # 白色
BALL_COLOR = pygame.Color('#FF8C00')    # 暗橘色
LINE_COLOR = pygame.Color('#FFFFFF')    # 白色
TEXT_COLOR = pygame.Color('#FFFFFF')    # 白色

# 3. 建立字體物件
title_font = pygame.font.Font(None, 64)
game_font = pygame.font.Font(None, 48)
prompt_font = pygame.font.Font(None, 32)

# 4. 建立遊戲視窗和時脈
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

# 球拍尺寸
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100

# 球尺寸
BALL_SIZE = 15

# 為遊戲物件建立 Rect
paddle_1 = pygame.Rect(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_2 = pygame.Rect(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# 球的速度
ball_speed_x = 0
ball_speed_y = 0

# 分數
player_1_score = 0
player_2_score = 0

# 遊戲狀態
game_active = False
ball_moving = False
game_over = False
winner_text = ""

# 5. 主遊戲迴圈
running = True
while running:
    # --- 事件處理 ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_active:
                game_active = True
            
            if not ball_moving and game_active and not game_over:
                ball_moving = True
                ball_speed_x = 7 * random.choice((1, -1))
                ball_speed_y = 7 * random.choice((1, -1))

            if game_over:
                game_over = False
                winner_text = ""
                player_1_score = 0
                player_2_score = 0
                ball_moving = False
                ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    # --- 繪圖與邏輯 ---
    screen.fill(BG_COLOR)

    if game_active and not game_over:
        # --- 遊戲邏輯 (只有球在動的時候才更新) ---
        if ball_moving:
            ball.x += ball_speed_x
            ball.y += ball_speed_y

            if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
                ball_speed_y *= -1
            if ball.colliderect(paddle_1) or ball.colliderect(paddle_2):
                ball_speed_x *= -1

            if ball.left <= 0:
                player_2_score += 1
                if player_2_score >= 10:
                    winner_text = "Player 2 Wins!"
                    game_over = True
                ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                ball_moving = False

            if ball.right >= SCREEN_WIDTH:
                player_1_score += 1
                if player_1_score >= 10:
                    winner_text = "Player 1 Wins!"
                    game_over = True
                ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                ball_moving = False
        
        # --- 玩家移動 (隨時都可以) ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: paddle_1.y -= 7
        if keys[pygame.K_s]: paddle_1.y += 7
        if keys[pygame.K_UP]: paddle_2.y -= 7
        if keys[pygame.K_DOWN]: paddle_2.y += 7

        if paddle_1.top <= 0: paddle_1.top = 0
        if paddle_1.bottom >= SCREEN_HEIGHT: paddle_1.bottom = SCREEN_HEIGHT
        if paddle_2.top <= 0: paddle_2.top = 0
        if paddle_2.bottom >= SCREEN_HEIGHT: paddle_2.bottom = SCREEN_HEIGHT
        
        # --- 遊戲中繪圖 ---
        pygame.draw.rect(screen, PADDLE_COLOR, paddle_1)
        pygame.draw.rect(screen, PADDLE_COLOR, paddle_2)
        pygame.draw.ellipse(screen, BALL_COLOR, ball)
        pygame.draw.aaline(screen, LINE_COLOR, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        
        player_1_text = game_font.render(f"{player_1_score}", True, TEXT_COLOR)
        screen.blit(player_1_text, (SCREEN_WIDTH // 2 - 60, 20))
        player_2_text = game_font.render(f"{player_2_score}", True, TEXT_COLOR)
        screen.blit(player_2_text, (SCREEN_WIDTH // 2 + 40, 20))

        if not ball_moving:
            prompt_surface = prompt_font.render("Press Space to Serve", True, TEXT_COLOR)
            prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
            screen.blit(prompt_surface, prompt_rect)

    elif game_over:
        win_text_surface = game_font.render(winner_text, True, TEXT_COLOR)
        win_text_rect = win_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(win_text_surface, win_text_rect)
        
        restart_text_surface = prompt_font.render("Press Space to Restart", True, TEXT_COLOR)
        restart_text_rect = restart_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(restart_text_surface, restart_text_rect)
    
    else: # 如果遊戲未啟動且未結束 -> 開始畫面
        title_surface = title_font.render("Pong Game", True, TEXT_COLOR)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        
        prompt_surface = prompt_font.render("Press Space to Start", True, TEXT_COLOR)
        prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        screen.blit(title_surface, title_rect)
        screen.blit(prompt_surface, prompt_rect)


    # --- 更新螢幕 ---
    pygame.display.flip()

    # --- 將幀率限制在 60 FPS ---
    clock.tick(60)

# 6. 退出 Pygame
pygame.quit()
sys.exit()