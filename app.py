import customtkinter as ctk

class ScrollingText(ctk.CTkFrame):
    """แถบตัวหนังสือวิ่งสีสดใส"""
    def __init__(self, master, text, color, **kwargs):
        super().__init__(master, fg_color=color, height=35, **kwargs)
        self.text = f" {text}          " * 10
        self.label = ctk.CTkLabel(self, text=self.text, font=("Arial", 14, "bold"), text_color="white")
        self.label.place(x=0, y=5)
        self.x_pos = 0
        self.animate()

    def animate(self):
        self.x_pos -= 2
        if self.x_pos < -500: self.x_pos = 0
        self.label.place(x=self.x_pos, y=5)
        self.after(30, self.animate)

class VideoCard(ctk.CTkFrame):
    """จอวิดีโอ + แผงควบคุมจัดเต็ม"""
    def __init__(self, master, platform, **kwargs):
        super().__init__(master, **kwargs)
        
        # หัวข้อ
        ctk.CTkLabel(self, text=f"แผงควบคุม {platform}", font=("Arial", 18, "bold")).pack(pady=5)

        # 1. ช่องใส่ลิงก์ + ปุ่มโหลด (เพิ่มลูกเล่น)
        input_frame = ctk.CTkFrame(self, fg_color="transparent")
        input_frame.pack(pady=5, fill="x", padx=10)
        self.url_entry = ctk.CTkEntry(input_frame, placeholder_text=f"วางลิงก์ {platform} ตรงนี้...", width=250)
        self.url_entry.pack(side="left", padx=5)
        ctk.CTkButton(input_frame, text="โหลด", width=60, fg_color="gray").pack(side="left")

        # 2. จอวิดีโอจำลอง
        self.screen = ctk.CTkFrame(self, width=450, height=250, fg_color="black", border_width=2, border_color="#333")
        self.screen.pack(pady=10, padx=10)
        ctk.CTkLabel(self.screen, text="[ SCREEN ]", text_color="#555", font=("Arial", 20)).place(relx=0.5, rely=0.5, anchor="center")

        # 3. ปุ่มควบคุมเครื่องเล่น (Media Controls)
        control_btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        control_btn_frame.pack(pady=5)
        ctk.CTkButton(control_btn_frame, text="◀◀", width=40).pack(side="left", padx=2)
        ctk.CTkButton(control_btn_frame, text="PLAY", width=60, fg_color="green").pack(side="left", padx=2)
        ctk.CTkButton(control_btn_frame, text="PAUSE", width=60, fg_color="orange").pack(side="left", padx=2)
        ctk.CTkButton(control_btn_frame, text="STOP", width=60, fg_color="red").pack(side="left", padx=2)
        ctk.CTkButton(control_btn_frame, text="▶▶", width=40).pack(side="left", padx=2)

        # 4. แผง EQ 5 ปุ่ม (ต่ำ -> สูง)
        eq_label_frame = ctk.CTkFrame(self, fg_color="#222")
        eq_label_frame.pack(pady=10, padx=10, fill="x")
        
        self.sliders = []
        bands = [".ต่ำ.", "ต่ำกลาง", ".กลาง.", "สูงกลาง", ".สูง."]
        for b in bands:
            unit = ctk.CTkFrame(eq_label_frame, fg_color="transparent")
            unit.pack(side="left", expand=True, pady=10)
            s = ctk.CTkSlider(unit, orientation="vertical", width=20, height=100)
            s.set(0)
            s.pack()
            self.sliders.append(s)
            ctk.CTkLabel(unit, text=b, font=("Arial", 10)).pack()

        # 5. ปุ่มทางลัดเสียง (Presets)
        preset_frame = ctk.CTkFrame(self, fg_color="transparent")
        preset_frame.pack(pady=5)
        ctk.CTkButton(preset_frame, text="Bass Boost", size=(80, 25), command=self.set_bass).pack(side="left", padx=5)
        ctk.CTkButton(preset_frame, text="Rock", size=(80, 25), command=self.set_rock).pack(side="left", padx=5)
        ctk.CTkButton(preset_frame, text="Reset", size=(80, 25), fg_color="gray", command=self.reset_eq).pack(side="left", padx=5)

    def set_bass(self):
        vals = [80, 40, 0, -20, -40]
        for s, v in zip(self.sliders, vals): s.set(v)

    def set_rock(self):
        vals = [60, -20, 40, -20, 60]
        for s, v in zip(self.sliders, vals): s.set(v)

    def reset_eq(self):
        for s in self.sliders: s.set(0)

class FullApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Super Media Equalizer - จัดเต็มลูกเล่น")
        self.geometry("580x900")

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.pack(fill="both", expand=True, padx=5, pady=5)

        # รายการคั่นด้วยตัวหนังสือวิ่ง
        configs = [
            ("YOUTUBE", "red", "● LIVE FROM YOUTUBE CHANNEL ●"),
            ("TIKTOK", "black", "● LATEST TIKTOK FEED ●"),
            ("FACEBOOK", "blue", "● FACEBOOK VIDEO POSTS ●"),
            ("LINE VOOM", "green", "● LINE VOOM CONTENT ●")
        ]

        for platform, color, msg in configs:
            ScrollingText(self.scroll, text=msg, color=color).pack(fill="x", pady=(15, 0))
            VideoCard(self.scroll, platform=platform, border_width=1, border_color="#555").pack(pady=(0, 20), padx=5, fill="x")

if __name__ == "__main__":
    app = FullApp()
    app.mainloop()
