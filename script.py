#!/usr/bin/env python3
"""
Terminal Dinosaur Game - A Chrome dinosaur game clone for the terminal
Press SPACE to jump and avoid obstacles
"""

import curses
import random
import time
import sys
from threading import Thread

class DinoGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.height, self.width = stdscr.getmaxyx()
        
        # Game settings
        self.ground_y = self.height - 3
        self.dino_x = 5
        self.dino_y = self.ground_y
        
        # Game state
        self.score = 0
        self.game_over = False
        self.jump_velocity = 0
        self.jump_active = False
        self.gravity = 0.6
        self.is_jumping = False
        self.obstacles = []
        self.obstacle_spawn_rate = 50
        self.base_speed = 3
        self.current_speed = self.base_speed
        self.max_score = 0
        
        # Setup colors
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        
        self.stdscr.nodelay(True)
        self.stdscr.timeout(0)
        
        self.frame_count = 0
        self.input_thread = Thread(target=self.handle_input, daemon=True)
        self.input_thread.start()
    
    def handle_input(self):
        """Handle keyboard input in a separate thread"""
        while not self.game_over:
            try:
                key = self.stdscr.getch()
                if key == ord(' '):
                    if not self.is_jumping:
                        self.is_jumping = True
                        self.jump_velocity = -15
                elif key == ord('q'):
                    self.game_over = True
            except:
                pass
            time.sleep(0.01)
    
    def update_jump(self):
        """Update jump physics"""
        if self.is_jumping:
            self.jump_velocity += self.gravity
            self.dino_y += self.jump_velocity
            
            # Land on ground
            if self.dino_y >= self.ground_y:
                self.dino_y = self.ground_y
                self.is_jumping = False
                self.jump_velocity = 0
    
    def spawn_obstacle(self):
        """Spawn a new obstacle randomly"""
        if random.randint(1, self.obstacle_spawn_rate) == 1:
            self.obstacles.append({
                'x': self.width,
                'y': self.ground_y,
                'type': 'spike'
            })
    
    def update_obstacles(self):
        """Update obstacle positions and remove off-screen ones"""
        for obstacle in self.obstacles[:]:
            obstacle['x'] -= self.current_speed
            if obstacle['x'] < 0:
                self.obstacles.remove(obstacle)
                self.score += 10
    
    def check_collision(self):
        """Check collision between dinosaur and obstacles"""
        dino_width = 3
        dino_height = 2
        obstacle_width = 2
        obstacle_height = 2
        
        for obstacle in self.obstacles:
            if (self.dino_x + dino_width > obstacle['x'] and
                self.dino_x < obstacle['x'] + obstacle_width and
                self.dino_y + dino_height > obstacle['y'] and
                self.dino_y < obstacle['y'] + obstacle_height):
                return True
        return False
    
    def increase_difficulty(self):
        """Increase game difficulty based on score"""
        # Increase speed gradually
        self.current_speed = self.base_speed + (self.score // 100) * 0.5
        self.current_speed = min(self.current_speed, 8)
        
        # Decrease spawn rate (more obstacles)
        self.obstacle_spawn_rate = max(20, 50 - (self.score // 150))
    
    def draw_dino(self):
        """Draw dinosaur character"""
        dino = [
            "  ^^",
            " /--\\",
            "/    \\",
        ]
        
        for i, line in enumerate(dino):
            if self.dino_y + i < self.height - 1:
                if self.dino_x + len(line) < self.width:
                    self.stdscr.addstr(int(self.dino_y + i), self.dino_x, 
                                      line, curses.color_pair(2))
    
    def draw_obstacles(self):
        """Draw obstacles"""
        for obstacle in self.obstacles:
            if 0 <= obstacle['x'] < self.width and 0 <= obstacle['y'] < self.height:
                if obstacle['x'] + 1 < self.width:
                    self.stdscr.addstr(obstacle['y'], int(obstacle['x']), 
                                      "/\\", curses.color_pair(3))
    
    def draw_ground(self):
        """Draw ground line"""
        ground_line = "=" * self.width
        self.stdscr.addstr(self.height - 2, 0, ground_line, curses.color_pair(1))
    
    def draw_hud(self):
        """Draw heads-up display (score, speed)"""
        score_text = f"Score: {self.score}  Speed: {self.current_speed:.1f}x  High: {self.max_score}"
        if len(score_text) < self.width:
            self.stdscr.addstr(0, 0, score_text, curses.color_pair(4))
    
    def draw_game_over(self):
        """Draw game over screen"""
        game_over_text = "GAME OVER!"
        restart_text = "Press SPACE to restart or Q to quit"
        
        center_y = self.height // 2
        center_x = (self.width - len(game_over_text)) // 2
        
        self.stdscr.addstr(center_y, center_x, game_over_text, 
                          curses.color_pair(3) | curses.A_BOLD)
        
        score_text = f"Final Score: {self.score}"
        center_x_score = (self.width - len(score_text)) // 2
        self.stdscr.addstr(center_y + 2, center_x_score, score_text, 
                          curses.color_pair(4))
        
        restart_x = (self.width - len(restart_text)) // 2
        self.stdscr.addstr(center_y + 4, restart_x, restart_text, 
                          curses.color_pair(1))
    
    def render(self):
        """Render the game"""
        self.stdscr.clear()
        self.draw_ground()
        self.draw_dino()
        self.draw_obstacles()
        self.draw_hud()
        
        if self.game_over:
            self.draw_game_over()
        
        self.stdscr.refresh()
    
    def reset_game(self):
        """Reset game state"""
        self.dino_y = self.ground_y
        self.score = 0
        self.obstacles = []
        self.is_jumping = False
        self.jump_velocity = 0
        self.current_speed = self.base_speed
        self.obstacle_spawn_rate = 50
        self.frame_count = 0
    
    def update(self):
        """Update game state"""
        self.frame_count += 1
        
        self.update_jump()
        self.spawn_obstacle()
        self.update_obstacles()
        self.increase_difficulty()
        
        if self.check_collision():
            if self.score > self.max_score:
                self.max_score = self.score
            self.game_over = True
    
    def handle_restart(self):
        """Handle restart input"""
        try:
            key = self.stdscr.getch()
            if key == ord(' '):
                self.game_over = False
                self.reset_game()
            elif key == ord('q'):
                return False
        except:
            pass
        return True
    
    def run(self):
        """Main game loop"""
        last_time = time.time()
        frame_delay = 1 / 60  # 60 FPS target
        
        while True:
            current_time = time.time()
            delta_time = current_time - last_time
            
            if delta_time >= frame_delay:
                if not self.game_over:
                    self.update()
                else:
                    if not self.handle_restart():
                        break
                
                self.render()
                last_time = current_time
            else:
                time.sleep(0.001)


def main(stdscr):
    """Main function to run the game"""
    # Clear screen
    stdscr.clear()
    
    # Display welcome message
    height, width = stdscr.getmaxyx()
    
    # Check minimum terminal size
    if height < 20 or width < 50:
        stdscr.addstr(0, 0, "Terminal terlalu kecil! Minimal 20x50")
        stdscr.refresh()
        stdscr.getch()
        return
    
    game = DinoGame(stdscr)
    game.run()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
        print("Game selesai! Terima kasih telah bermain.")
    except KeyboardInterrupt:
        print("\nGame dihentikan.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
