# clicker_hero_complete.py
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# --- 主要應用程式類別 ---
class ClickerHeroApp:
    def __init__(self, root):
        """
        初始化應用程式
        :param root: tkinter 的主視窗
        """
        self.root = root
        self.root.title("🎮 點擊英雄 (Clicker Hero)")
        self.root.geometry("500x600") # 設定視窗大小
        self.root.config(bg="#f0f0f0") # 設定背景顏色

        # --- 遊戲狀態變數 ---
        self.score = 0
        self.click_power = 1
        self.upgrade_cost = 10
        self.upgrade_power_increase = 1

        # --- 建立 GUI 元件 ---

        # 1. 頂部框架 (顯示遊戲狀態)
        stats_frame = tk.Frame(root, pady=10, bg="#d0d0d0")
        stats_frame.pack(fill="x", padx=10, pady=10)

        # 分數標籤
        self.score_label = tk.Label(stats_frame, text=f"金幣: {self.score}", font=("Arial", 20, "bold"), bg="#d0d0d0")
        self.score_label.pack()

        # 點擊力標籤
        self.power_label = tk.Label(stats_frame, text=f"點擊力: {self.click_power}", font=("Arial", 14), bg="#d0d0d0")
        self.power_label.pack()

        # 2. 主要遊戲區域
        game_frame = tk.Frame(root, pady=20, bg="#f0f0f0")
        game_frame.pack(expand=True)

        # 載入英雄圖片
        try:
            # 嘗試載入圖片 (使用絕對路徑)
            import os
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # 載入普通狀態圖片
            normal_img_path = os.path.join(script_dir, 'hero.png')
            self.hero_img = Image.open(normal_img_path)
            self.hero_img = self.hero_img.resize((200, 200), Image.Resampling.LANCZOS)
            self.hero_photo = ImageTk.PhotoImage(self.hero_img)
            
            # 載入點擊狀態圖片
            click_img_path = os.path.join(script_dir, 'hero_click.png')
            self.hero_click_img = Image.open(click_img_path)
            self.hero_click_img = self.hero_click_img.resize((200, 200), Image.Resampling.LANCZOS)
            self.hero_click_photo = ImageTk.PhotoImage(self.hero_click_img)
            
            # 創建圖片按鈕（注意：這裡不設置 command，因為我們使用 bind 來處理點擊）
            self.hero_button = tk.Button(game_frame, image=self.hero_photo, 
                                      bg="#a0e0a0", activebackground="#80c080", 
                                      relief="raised", bd=5)
            self.hero_button.image = self.hero_photo  # 保持圖片參考
            
            # 綁定滑鼠按鈕事件
            self.hero_button.bind('<ButtonPress-1>', self.on_hero_press)
            self.hero_button.bind('<ButtonRelease-1>', self.on_hero_release)
        except Exception as e:
            print(f"無法載入圖片: {e}")
            # 如果載入圖片失敗，使用預設的表情符號按鈕
            self.hero_button = tk.Button(game_frame, text="⚔️", font=("Arial", 100), 
                                      command=self.hero_click, bg="#a0e0a0", 
                                      activebackground="#80c080", relief="raised", bd=5)
        self.hero_button.pack()
        
        # 3. 底部升級區域
        upgrade_frame = tk.Frame(root, pady=20, bg="#d0d0d0")
        upgrade_frame.pack(fill="x", padx=10, pady=10)
        
        # 升級按鈕 (使用更生動的樣式)
        self.upgrade_button = tk.Button(
            upgrade_frame, 
            text=f"升級點擊力 (花費: {self.upgrade_cost} 金幣)", 
            font=("Arial", 14, "bold"), 
            command=self.upgrade_click,
            bg="#ffcc66",  # 淺橙色背景
            fg="#333333",   # 深灰色文字
            activebackground="#ffbb44",  # 按下的顏色
            activeforeground="#ffffff",  # 按下的文字顏色
            relief="raised",
            bd=3,
            padx=10,
            pady=5
        )
        self.upgrade_button.pack()


    def on_hero_press(self, event):
        """當滑鼠按鈕按下時觸發"""
        self.hero_button.config(image=self.hero_click_photo)
        self.hero_button.image = self.hero_click_photo
        
    def on_hero_release(self, event):
        """當滑鼠按鈕釋放時觸發"""
        self.hero_button.config(image=self.hero_photo)
        self.hero_button.image = self.hero_photo
        self.hero_click()
        
    def hero_click(self):
        """
        當英雄按鈕被點擊時觸發。
        增加分數並更新標籤。
        """
        # 根據目前的點擊力增加分數
        self.score += self.click_power
        # 更新顯示分數的標籤
        self.update_labels()
        

    def upgrade_click(self):
        """
        當升級按鈕被點擊時觸發。
        檢查分數是否足夠，如果足夠就進行升級。
        """
        # 檢查玩家的金幣是否足夠支付升級費用
        if self.score >= self.upgrade_cost:
            # 扣除升級費用
            self.score -= self.upgrade_cost
            # 提升點擊力
            self.click_power += self.upgrade_power_increase
            # 計算下一次升級的費用 (讓它變貴)
            self.upgrade_cost = int(self.upgrade_cost * 1.5)
            
            # 更新所有標籤的文字
            self.update_labels()
        else:
            # 如果金幣不夠，跳出提示視窗
            messagebox.showwarning("金幣不足", "你的金幣不夠，快去點擊英雄賺錢！")
            
            
    def update_labels(self):
        """
        一個統一更新所有標籤文字的函式。
        """
        self.score_label.config(text=f"金幣: {self.score}")
        self.power_label.config(text=f"點擊力: {self.click_power}")
        self.upgrade_button.config(text=f"升級點擊力 (花費: {self.upgrade_cost} 金幣)")


# --- 主程式進入點 ---
if __name__ == "__main__":
    # 建立 tkinter 主視窗
    root = tk.Tk()
    # 建立應用程式實體
    app = ClickerHeroApp(root)
    # 進入主迴圈，等待使用者操作
    root.mainloop()

