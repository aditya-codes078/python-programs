import math
import random
import tkinter as tk


class CyberVisualizer:

    def __init__(self, root):
        self.root = root
        self.root.title("Cyber Space Particle Visualizer")

        # Window Screen Dimensions
        self.width = 900
        self.height = 650
        self.canvas = tk.Canvas(
            root, width=self.width, height=self.height, bg="#050505"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Glowing Neon Colors
        self.colors = [
            "#00ff66",
            "#00ffff",
            "#ff00ff",
            "#ffff00",
            "#ff0055",
            "#0099ff",
        ]

        # Particles Setup
        self.num_particles = 1200
        self.particles = []
        self.init_particles()

        # Dynamic Overlay Text List
        self.texts = [
            "SYSTEM OVERRIDE DIGITAL...",
            "CALCULATING INFINITE PROBABILITIES...",
            "IGNITING ENERGY REACTOR...",
            "OMNISCIENCE ACHIEVED.",
        ]
        self.text_index = 0

        # UI Text Element
        self.text_id = self.canvas.create_text(
            self.width // 2,
            self.height // 2,
            text=self.texts[0],
            fill="#00ff66",
            font=("Courier", 16, "bold"),
        )

        # Animation parameters
        self.angle_x = 0
        self.angle_y = 0
        self.time = 0

        # Start Loops
        self.update_text()
        self.animate()

    def init_particles(self):
        # Generate 3D Spherical Swarm
        for _ in range(self.num_particles):
            u = random.random()
            v = random.random()
            theta = u * 2.0 * math.pi
            phi = math.acos(2.0 * v - 1.0)
            r = (random.random() ** (1 / 3)) * 220

            x = r * math.sin(phi) * math.cos(theta)
            y = r * math.sin(phi) * math.sin(theta)
            z = r * math.cos(phi)

            color = random.choice(self.colors)
            self.particles.append([x, y, z, color])

    def update_text(self):
        # Change text every 3 seconds
        self.text_index = (self.text_index + 1) % len(self.texts)
        self.canvas.itemconfig(
            self.text_id,
            text=self.texts[self.text_index],
            fill=random.choice(self.colors),
        )
        self.root.after(3000, self.update_text)

    def animate(self):
        self.canvas.delete("particle")  # Clear previous frame particles

        self.time += 0.04
        self.angle_x += 0.015
        self.angle_y += 0.025

        # Pulse Effect
        pulse = 1 + 0.15 * math.sin(self.time * 2)

        cx, cy = self.width // 2, self.height // 2
        fov = 400  # Field of view for 3D projection

        for p in self.particles:
            # Fixed the variable assignment here:
            p_x, p_y, p_z, color = p
            x, y, z = p_x * pulse, p_y * pulse, p_z * pulse

            # 3D Rotation (Y-axis)
            x1 = x * math.cos(self.angle_y) + z * math.sin(self.angle_y)
            z1 = -x * math.sin(self.angle_y) + z * math.cos(self.angle_y)

            # 3D Rotation (X-axis)
            y1 = y * math.cos(self.angle_x) - z1 * math.sin(self.angle_x)
            z2 = y * math.sin(self.angle_x) + z1 * math.cos(self.angle_x)

            # Perspective Projection (3D to 2D)
            distance = fov + z2
            if distance > 1:
                screen_x = cx + (x1 * fov) / distance
                screen_y = cy + (y1 * fov) / distance

                # Dynamic Size based on depth
                size = max(1, (fov / distance) * 1.5)

                self.canvas.create_oval(
                    screen_x - size,
                    screen_y - size,
                    screen_x + size,
                    screen_y + size,
                    fill=color,
                    outline="",
                    tags="particle",
                )

        # Keep text always on top
        self.canvas.tag_raise(self.text_id)

        # Frame rate ~30 FPS
        self.root.after(30, self.animate)


# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = CyberVisualizer(root)
    root.mainloop()
