# comic_creator_complete.py
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import urllib.request
import os

# --- 主要應用程式類別 ---
class ComicCreatorApp:
    def __init__(self, root):
        """
        初始化應用程式
        :param root: tkinter 的主視窗
        """
        self.root = root
        self.root.title("🎨 數位四格漫畫創作器")
        self.root.geometry("700x750")        # 設定視窗背景色和字體
        self.root.config(bg="#2c3e50") # 深藍灰色背景

        # --- 漫畫資料 ---
        # 每一頁都是一個字典，包含本地圖片檔案與文字
        self.pages = [
            {
                "image": "1.png",
                "text": "從前從前，有一隻勇敢的小貓，他夢想著成為一名太空探險家。"
            },
            {
                "image": "2.png",
                "text": "他用紙箱和瓶子，日以繼夜地打造自己的太空船。"
            },
            {
                "image": "3.png",
                "text": "終於，在一個星光燦爛的夜晚，他啟動了引擎，向著月亮飛去！"
            },
            {
                "image": "4.png",
                "text": "雖然他只飛到了院子裡的蘋果樹上，但對他來說，這已經是宇宙的邊際了。 (完)"
            }
        ]
        self.current_page_index = 0
        self.tk_image = None # 用來儲存 tkinter 可以顯示的圖片物件

        # --- 建立 GUI 元件 ---

        # 1. 圖片顯示區 (使用 Frame 作為容器)
        self.image_frame = tk.Frame(root, bg="#34495e", pady=15, padx=15)
        self.image_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.image_label = tk.Label(self.image_frame, bg="#ffffff", relief="solid", bd=2)
        self.image_label.pack(expand=True)

        # 2. 文字顯示區 (使用 Frame 作為容器)
        self.text_frame = tk.Frame(root, bg="#2c3e50", pady=10)
        self.text_frame.pack(fill="x", padx=20, pady=5)
        
        self.text_label = tk.Label(self.text_frame, 
                                text="", 
                                font=("Microsoft JhengHei", 16, "bold"), 
                                wraplength=600, 
                                justify="center",
                                fg="#ecf0f1",  # 淺灰色文字
                                bg="#2c3e50",   # 與背景同色
                                padx=10,
                                pady=10)
        self.text_label.pack()
        
        # 4. 按鈕控制區 (使用 Frame 包裝按鈕)
        self.button_frame = tk.Frame(root, bg="#2c3e50", pady=10)
        self.button_frame.pack(fill="x")

        # 設定 ttk 樣式，近似圓角效果
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Rounded.TButton',
                        font=('Microsoft JhengHei', 12, 'bold'),
                        padding=10,
                        background='#3498db',
                        foreground='white',
                        borderwidth=0,
                        relief='flat')
        style.map('Rounded.TButton',
                  background=[('active', '#2980b9'), ('!active', '#3498db')],
                  foreground=[('active', 'white'), ('!active', 'white')])
        # 上一頁按鈕
        self.prev_button = ttk.Button(self.button_frame,
                                   text="⬅️ 上一頁",
                                   command=self.prev_page,
                                   state="disabled",  # 初始狀態禁用
                                   style='Rounded.TButton')
        self.prev_button.pack(side="left", padx=10, pady=5)

        # 下一頁按鈕
        self.next_button = ttk.Button(self.button_frame,
                                   text="下一頁 ➡️",
                                   command=self.next_page,
                                   style='Rounded.TButton')
        self.next_button.pack(side="right", padx=10, pady=5)
        
        # 頁碼標籤
        self.page_indicator_label = ttk.Label(
            self.button_frame,
            text=f"第 1 / {len(self.pages)} 頁",
            style='TLabel',
            foreground='white',
            background='#2c3e50'
        )
        self.page_indicator_label.pack(side='top', pady=5)
        
        # 初始載入第一頁
        self.load_page(self.current_page_index)

    def create_colored_image(self, color, width=600, height=400):
        """創建一個彩色方塊圖片"""
        from PIL import ImageDraw, ImageFont
        
        # 創建一個新的圖片
        image = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(image)
        
        # 添加文字標籤
        try:
            # 嘗試使用系統字體
            font_size = 24
            font = ImageFont.truetype("Arial", font_size)
        except IOError:
            # 如果找不到字體，使用預設字體
            font = ImageFont.load_default()
        
        # 繪製文字
        text = f"第 {self.current_page_index + 1} 格"
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # 計算文字位置（置中）
        x = (width - text_width) / 2
        y = (height - text_height) / 2
        
        # 繪製文字
        draw.text((x, y), text, fill="black", font=font)
        
        return image

    def load_page(self, page_index):
        """
        載入指定頁面的圖片和文字
        """
        if not 0 <= page_index < len(self.pages):
            return
            
        self.current_page_index = page_index
        page_data = self.pages[page_index]
        
        try:
            # 載入本地圖片
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, page_data["image"])
            print(f"[DEBUG] 嘗試載入圖片路徑: {image_path}")
            
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"找不到圖片檔案: {image_path}")
                
            img = Image.open(image_path)
            
            # 調整圖片大小
            max_size = (400, 400)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # 轉換為 Tkinter 可用的格式
            self.tk_image = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.tk_image)
            self.image_label.image = self.tk_image  # 強制保留引用
            
            # 更新文字
            self.text_label.config(text=page_data["text"])
            
        except Exception as e:
            print(f"[DEBUG] 載入圖片時發生錯誤: {e}")
            # 創建一個錯誤提示圖片
            error_img = Image.new('RGB', (500, 150), color=(44, 62, 80))  # 深藍灰色背景
            draw = ImageDraw.Draw(error_img)
            try:
                font = ImageFont.truetype("Microsoft JhengHei", 16)
            except:
                font = ImageFont.load_default()
            # 添加錯誤標題
            draw.text((20, 30), "❌ 圖片載入失敗", fill="#e74c3c", font=font, stroke_width=2)
            # 添加錯誤詳情
            draw.text((40, 70), f"錯誤: {str(e)[:50]}...", fill="#ecf0f1", font=font)
            # 添加解決方案提示
            draw.text((40, 100), "請確認圖片檔案是否存在於正確位置", fill="#bdc3c7", font=font)
            self.tk_image = ImageTk.PhotoImage(error_img)
            self.image_label.config(image=self.tk_image)
            self.image_label.image = self.tk_image

        self.text_label.config(text=page_data["text"])
        
        # 更新頁碼
        self.page_indicator_label.config(text=f"第 {page_index + 1} / {len(self.pages)} 頁")
        
        # 更新按鈕狀態 ---
        # 如果是第一頁，禁用「上一頁」按鈕
        self.prev_button.config(state="disabled" if page_index == 0 else "normal")
        # 如果是最後一頁，禁用「下一頁」按鈕
        self.next_button.config(state="disabled" if page_index == len(self.pages) - 1 else "normal")

    def next_page(self):
        """
        切換到下一頁
        """
        if self.current_page_index < len(self.pages) - 1:
            self.current_page_index += 1
            self.load_page(self.current_page_index)

    def prev_page(self):
        """
        切換到上一頁
        """
        if self.current_page_index > 0:
            self.current_page_index -= 1
            self.load_page(self.current_page_index)


# --- 主程式進入點 ---
if __name__ == "__main__":
    # 建立 tkinter 主視窗
    root = tk.Tk()
    # 建立應用程式實體
    app = ComicCreatorApp(root)
    # 進入主迴圈，等待使用者操作
    root.mainloop()

