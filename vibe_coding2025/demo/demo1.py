# meme_generator_complete.py
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

# --- 主要應用程式類別 ---
class MemeGeneratorApp:
    def __init__(self, root):
        """
        初始化應用程式
        :param root: tkinter 的主視窗
        """
        self.root = root
        self.root.title("😂 簡單迷因產生器")
        self.root.geometry("800x700") # 設定視窗大小

        # 儲存圖片路徑和 PIL 圖片物件
        self.image_path = None
        self.original_image = None
        self.generated_image = None
        self.tk_image = None

        # --- 建立 GUI 元件 ---
        
        # 1. 頂部框架 (放置按鈕和輸入框)
        top_frame = tk.Frame(root, pady=10)
        top_frame.pack(fill="x")

        # 2. 選擇圖片按鈕
        self.btn_select = tk.Button(top_frame, text="1. 選擇圖片", command=self.select_image)
        self.btn_select.pack(pady=5)

        # 3. 頂部文字輸入框
        tk.Label(top_frame, text="頂部文字:").pack()
        self.entry_top_text = tk.Entry(top_frame, width=50)
        self.entry_top_text.pack(pady=2)

        # 4. 底部文字輸入框
        tk.Label(top_frame, text="底部文字:").pack()
        self.entry_bottom_text = tk.Entry(top_frame, width=50)
        self.entry_bottom_text.pack(pady=2)
        
        # 5. 產生迷因按鈕
        self.btn_generate = tk.Button(top_frame, text="2. 產生迷因", command=self.generate_meme)
        self.btn_generate.pack(pady=10)
        
        # 6. 圖片顯示區 (使用 Label 來顯示圖片)
        self.image_label = tk.Label(root)
        self.image_label.pack(expand=True, fill="both", padx=10, pady=10)

        # 7. 底部框架 (放置儲存按鈕)
        bottom_frame = tk.Frame(root, pady=10)
        bottom_frame.pack(fill="x")
        
        # 8. 儲存迷因按鈕
        self.btn_save = tk.Button(bottom_frame, text="3. 儲存迷因", command=self.save_meme)
        self.btn_save.pack(pady=5)


    def select_image(self):
        """
        開啟檔案選擇對話框，讓使用者選擇一張圖片，並顯示在畫面上。
        """
        # 使用 filedialog 開啟檔案選擇視窗，並篩選圖片格式
        self.image_path = filedialog.askopenfilename(
            title="請選擇一張圖片",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")]
        )
        # 如果使用者沒有選擇任何檔案，就結束這個函式
        if not self.image_path:
            return

        # 使用 Pillow 的 Image.open() 開啟圖片檔案
        self.original_image = Image.open(self.image_path)
        
        # 調整圖片大小，使其最大寬高不超過700x500，以適應視窗
        self.original_image.thumbnail((700, 500))
        
        # 將 Pillow 圖片物件轉換為 tkinter 可以顯示的 PhotoImage 物件
        self.tk_image = ImageTk.PhotoImage(self.original_image)
        
        # 更新 Label 元件的圖片
        self.image_label.config(image=self.tk_image)
        
        print(f"圖片已載入: {self.image_path}")


    def generate_meme(self):
        """
        核心功能：在圖片上加上文字，產生迷因並更新畫面。
        """
        # 檢查使用者是否已經選擇了圖片
        if self.original_image is None:
            messagebox.showwarning("錯誤", "請先選擇一張圖片！")
            return

        # 複製原始圖片，這樣才不會更動到原圖
        self.generated_image = self.original_image.copy()
        
        # 建立一個可以在圖片上繪圖的 Draw 物件
        draw = ImageDraw.Draw(self.generated_image)

        # 從輸入框取得使用者輸入的文字
        top_text = self.entry_top_text.get()
        bottom_text = self.entry_bottom_text.get()

        # 取得圖片的寬度和高度
        width, height = self.generated_image.size

        # 設定字體。這裡會嘗試使用常見的黑體字，如果找不到則使用預設字體
        try:
            # 判斷作業系統來選擇不同的字體路徑
            font_path = "msjhbd.ttc" if self.root.tk.call('tk', 'windowingsystem') == 'win32' else "/System/Library/Fonts/PingFang.ttc"
            # 字體大小設定為圖片高度的十分之一，讓它能隨圖片大小縮放
            font_size = int(height / 10)
            font = ImageFont.truetype(font_path, size=font_size)
        except IOError:
            print("警告：找不到預設字體，使用內建字體。")
            font = ImageFont.load_default()

        # 使用 textbbox 方法計算文字的邊界框，以利置中
        top_left, top_right, top_bottom = draw.textbbox((0, 0), top_text, font=font)[:3]
        top_text_width = top_right - top_left
        
        bottom_bbox = draw.textbbox((0, 0), bottom_text, font=font)
        bottom_text_width = bottom_bbox[2] - bottom_bbox[0]
        bottom_text_height = bottom_bbox[3] - bottom_bbox[1]
        
        # 計算文字置中的 x 座標
        top_x = (width - top_text_width) / 2
        bottom_x = (width - bottom_text_width) / 2
        
        # 計算底部文字的 y 座標 (離底部保留10個像素的距離)
        bottom_y = height - bottom_text_height - 10

        # 在圖片上繪製文字，並加上黑色的邊框讓文字更清晰
        draw.text((top_x, 10), top_text, font=font, fill="white", stroke_width=2, stroke_fill="black")
        draw.text((bottom_x, bottom_y), bottom_text, font=font, fill="white", stroke_width=2, stroke_fill="black")

        # 將產生好的新圖片轉換成 tkinter 格式並更新到畫面上
        self.tk_image = ImageTk.PhotoImage(self.generated_image)
        self.image_label.config(image=self.tk_image)

        print("迷因已產生！")

    def save_meme(self):
        """
        將產生的迷因圖片儲存到檔案。
        """
        # 檢查是否已經產生了迷因圖片
        if self.generated_image is None:
            messagebox.showwarning("錯誤", "請先產生迷因圖片！")
            return
        
        # 開啟「另存新檔」對話框，讓使用者選擇儲存路徑和檔名
        file_path = filedialog.asksaveasfilename(
            title="請選擇儲存位置",
            defaultextension=".png",
            filetypes=[("PNG file", "*.png"), ("JPEG file", "*.jpg")]
        )
        
        # 如果使用者取消儲存，就結束函式
        if not file_path:
            return
            
        # 使用 Pillow 的 save 方法儲存圖片
        self.generated_image.save(file_path)
        messagebox.showinfo("成功", f"迷因已儲存至：\n{file_path}")
        print(f"迷因已儲存至: {file_path}")


# --- 主程式進入點 ---
if __name__ == "__main__":
    # 建立 tkinter 主視窗
    root = tk.Tk()
    # 建立應用程式實體
    app = MemeGeneratorApp(root)
    # 進入主迴圈，等待使用者操作
    root.mainloop()

