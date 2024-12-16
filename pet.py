import tkinter as tk
from PIL import Image, ImageTk
import random
import time


class AnimatedPet:
    BASE_PATH = "cat_gifs\\"
    FRAME_SIZE = (128, 128)
    FRAME_DURATIONS = {
        "walk": 100,
        "idle": 300,
        "sleep": 500,
        "stretch": 300,
        "lick": 200,
        "clean": 250,
    }
    STATE_DURATIONS = {
        "walk": 3,
        "idle": 5,
        "sleep": 8,
        "stretch": 3,
        "lick": 4,
        "clean": 2,
    }

    def __init__(self, window, screen_width, screen_height):
        self.window = window
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = int((screen_width / 2) - (self.FRAME_SIZE[0] / 2))
        self.y = screen_height - self.FRAME_SIZE[1] - 48
        self.dx = 5
        self.direction = "right"
        self.current_state = "walk"
        self.state_start_time = time.time()
        self.last_direction_change = time.time()
        self.frames = self.load_all_frames()
        self.label = tk.Label(window, bd=0, bg="black")
        self.label.pack()
        self.update_position()

    def load_all_frames(self):
        frame_files = {
            "walk": "walk.gif",
            "idle": "idle.gif",
            "sleep": "sleep.gif",
            "stretch": "stretch.gif",
            "lick": "lick.gif",
            "clean": "clean.gif",
        }

        return {
            state: self.load_frames(self.BASE_PATH + file)
            for state, file in frame_files.items()
        }

    def load_frames(self, file_path):
        image = Image.open(file_path)
        frames_right = []
        frames_left = []

        for frame in range(image.n_frames):
            image.seek(frame)

            # Ensure transparency is preserved by converting to RGBA
            rgba_frame = image.convert("RGBA")
            resized_frame = rgba_frame.resize(self.FRAME_SIZE, Image.Resampling.LANCZOS)

            frames_right.append(ImageTk.PhotoImage(resized_frame))
            frames_left.append(
                ImageTk.PhotoImage(resized_frame.transpose(Image.FLIP_LEFT_RIGHT))
            )

        return {"right": frames_right, "left": frames_left}

    def change_state(self):
        current_time = time.time()
        if current_time - self.state_start_time > self.STATE_DURATIONS[self.current_state]:
            states = ["walk", "idle", "sleep", "stretch", "lick", "clean"]
            state_weights = {
                "walk": [1, 3, 1, 0, 1, 0],  # Bias towards idle
                "idle": [1, 1, 3, 0, 3, 0],  # Bias towards sleep or lick
                "sleep": [0, 0, 1, 4, 0, 0],  # Bias towards lick
                "stretch": [1, 1, 0, 0, 1, 0],  # Bias against sleep and stretch
                "lick": [0, 0, 0, 0, 0, 1],  # Clean
            }.get(self.current_state, [1, 1, 3, 0, 1, 0])  # Default bias towards sleep

            self.current_state = random.choices(states, weights=state_weights)[0]
            self.state_start_time = current_time

    def change_direction(self):
        current_time = time.time()
        if current_time - self.last_direction_change > 5:
            self.direction = "right" if random.random() < 0.5 else "left"
            self.dx = 5 if self.direction == "right" else -5
            self.last_direction_change = current_time

    def animate(self, frame_index=0):
        frames = self.frames[self.current_state][self.direction]
        frame = frames[min(frame_index, len(frames) - 1)]
        self.label.configure(image=frame, bg="black")

        if self.current_state == "walk":
            self.x += self.dx
            if self.x + self.FRAME_SIZE[0] >= self.screen_width or self.x <= 0:
                self.dx = -self.dx
                self.direction = "right" if self.dx > 0 else "left"

        self.update_position()
        self.change_state()
        self.change_direction()

        next_frame = (frame_index + 1) % len(frames)
        self.window.after(self.FRAME_DURATIONS[self.current_state], self.animate, next_frame)

    def update_position(self):
        self.window.geometry(f"+{self.x}+{self.y}")


def main():
    window = tk.Tk()
    window.config(highlightbackground="black")
    window.overrideredirect(True)
    window.wm_attributes("-transparentcolor", "black")
    window.wm_attributes("-topmost", True)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    pet = AnimatedPet(window, screen_width, screen_height)
    pet.animate()

    window.mainloop()


if __name__ == "__main__":
    main()
