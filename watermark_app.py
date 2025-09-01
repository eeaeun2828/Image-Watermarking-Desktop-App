import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk, ImageDraw, ImageFont
import os
from typing import Tuple, Optional

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("이미지 워터마킹 앱")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # 변수 초기화
        self.original_image = None
        self.watermarked_image = None
        self.image_path = None
        self.watermark_text = tk.StringVar(value="www.yourwebsite.com")
        self.watermark_opacity = tk.DoubleVar(value=0.7)
        self.watermark_size = tk.IntVar(value=24)
        self.watermark_color = "#FFFFFF"
        self.watermark_position = tk.StringVar(value="bottom-right")
        
        self.setup_ui()
        
    def setup_ui(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 제목
        title_label = ttk.Label(main_frame, text="이미지 워터마킹 애플리케이션", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 이미지 업로드 섹션
        upload_frame = ttk.LabelFrame(main_frame, text="이미지 업로드", padding="10")
        upload_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(upload_frame, text="이미지 선택", 
                  command=self.select_image).grid(row=0, column=0, padx=(0, 10))
        
        self.image_label = ttk.Label(upload_frame, text="이미지를 선택해주세요")
        self.image_label.grid(row=0, column=1, sticky=tk.W)
        
        # 워터마크 설정 섹션
        settings_frame = ttk.LabelFrame(main_frame, text="워터마크 설정", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # 워터마크 텍스트
        ttk.Label(settings_frame, text="워터마크 텍스트:").grid(row=0, column=0, sticky=tk.W, pady=5)
        text_entry = ttk.Entry(settings_frame, textvariable=self.watermark_text, width=30)
        text_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 워터마크 크기
        ttk.Label(settings_frame, text="폰트 크기:").grid(row=1, column=0, sticky=tk.W, pady=5)
        size_scale = ttk.Scale(settings_frame, from_=12, to=72, variable=self.watermark_size, 
                              orient=tk.HORIZONTAL, length=200)
        size_scale.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 워터마크 투명도
        ttk.Label(settings_frame, text="투명도:").grid(row=2, column=0, sticky=tk.W, pady=5)
        opacity_scale = ttk.Scale(settings_frame, from_=0.1, to=1.0, variable=self.watermark_opacity, 
                                 orient=tk.HORIZONTAL, length=200)
        opacity_scale.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 워터마크 색상
        ttk.Label(settings_frame, text="색상:").grid(row=3, column=0, sticky=tk.W, pady=5)
        color_button = ttk.Button(settings_frame, text="색상 선택", command=self.choose_color)
        color_button.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 워터마크 위치
        ttk.Label(settings_frame, text="위치:").grid(row=4, column=0, sticky=tk.W, pady=5)
        position_combo = ttk.Combobox(settings_frame, textvariable=self.watermark_position, 
                                     values=["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                                     state="readonly", width=15)
        position_combo.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # 버튼들
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="워터마크 적용", 
                  command=self.apply_watermark).grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(button_frame, text="저장", 
                  command=self.save_image).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(button_frame, text="초기화", 
                  command=self.reset_image).grid(row=0, column=2)
        
        # 이미지 미리보기
        preview_frame = ttk.LabelFrame(main_frame, text="이미지 미리보기", padding="10")
        preview_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.preview_label = ttk.Label(preview_frame, text="이미지를 선택하면 여기에 미리보기가 표시됩니다")
        self.preview_label.grid(row=0, column=0)
        
        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
    def select_image(self):
        """이미지 파일을 선택합니다."""
        file_path = filedialog.askopenfilename(
            title="이미지 파일 선택",
            filetypes=[
                ("이미지 파일", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("모든 파일", "*.*")
            ]
        )
        
        if file_path:
            try:
                self.image_path = file_path
                self.original_image = Image.open(file_path)
                self.watermarked_image = self.original_image.copy()
                
                # 이미지 정보 표시
                filename = os.path.basename(file_path)
                self.image_label.config(text=f"선택됨: {filename}")
                
                # 미리보기 업데이트
                self.update_preview()
                
            except Exception as e:
                messagebox.showerror("오류", f"이미지를 불러올 수 없습니다: {str(e)}")
    
    def choose_color(self):
        """워터마크 색상을 선택합니다."""
        color = colorchooser.askcolor(title="워터마크 색상 선택")
        if color[1]:
            self.watermark_color = color[1]
    
    def get_position_coordinates(self, position: str, image_size: Tuple[int, int], 
                                watermark_size: Tuple[int, int]) -> Tuple[int, int]:
        """워터마크 위치에 따른 좌표를 반환합니다."""
        img_width, img_height = image_size
        wm_width, wm_height = watermark_size
        
        if position == "top-left":
            return (10, 10)
        elif position == "top-right":
            return (img_width - wm_width - 10, 10)
        elif position == "bottom-left":
            return (10, img_height - wm_height - 10)
        elif position == "bottom-right":
            return (img_width - wm_width - 10, img_height - wm_height - 10)
        elif position == "center":
            return ((img_width - wm_width) // 2, (img_height - wm_height) // 2)
        else:
            return (10, 10)
    
    def apply_watermark(self):
        """워터마크를 이미지에 적용합니다."""
        if self.original_image is None:
            messagebox.showwarning("경고", "먼저 이미지를 선택해주세요.")
            return
        
        try:
            # 원본 이미지 복사
            self.watermarked_image = self.original_image.copy()
            
            # 워터마크 텍스트 가져오기
            text = self.watermark_text.get()
            if not text.strip():
                messagebox.showwarning("경고", "워터마크 텍스트를 입력해주세요.")
                return
            
            # 이미지를 RGBA 모드로 변환 (투명도 지원)
            if self.watermarked_image.mode != 'RGBA':
                self.watermarked_image = self.watermarked_image.convert('RGBA')
            
            # 워터마크용 이미지 생성
            watermark_img = Image.new('RGBA', self.watermarked_image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark_img)
            
            # 폰트 설정 (기본 폰트 사용)
            try:
                font = ImageFont.truetype("arial.ttf", self.watermark_size.get())
            except:
                font = ImageFont.load_default()
            
            # 텍스트 크기 계산
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # 위치 계산
            position = self.get_position_coordinates(
                self.watermark_position.get(),
                self.watermarked_image.size,
                (text_width, text_height)
            )
            
            # 투명도 적용
            opacity = int(255 * self.watermark_opacity.get())
            color_with_opacity = (*self.hex_to_rgb(self.watermark_color), opacity)
            
            # 워터마크 그리기
            draw.text(position, text, font=font, fill=color_with_opacity)
            
            # 워터마크를 원본 이미지에 합성
            self.watermarked_image = Image.alpha_composite(self.watermarked_image, watermark_img)
            
            # 미리보기 업데이트
            self.update_preview()
            
            messagebox.showinfo("성공", "워터마크가 성공적으로 적용되었습니다!")
            
        except Exception as e:
            messagebox.showerror("오류", f"워터마크 적용 중 오류가 발생했습니다: {str(e)}")
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """16진수 색상을 RGB로 변환합니다."""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def update_preview(self):
        """이미지 미리보기를 업데이트합니다."""
        if self.watermarked_image:
            # 이미지 크기 조정 (미리보기용)
            preview_size = (300, 200)
            preview_img = self.watermarked_image.copy()
            preview_img.thumbnail(preview_size, Image.Resampling.LANCZOS)
            
            # PIL 이미지를 Tkinter용으로 변환
            photo = ImageTk.PhotoImage(preview_img)
            
            # 라벨 업데이트
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo  # 참조 유지
    
    def save_image(self):
        """워터마크가 적용된 이미지를 저장합니다."""
        if self.watermarked_image is None:
            messagebox.showwarning("경고", "저장할 이미지가 없습니다.")
            return
        
        # 저장 경로 선택
        file_path = filedialog.asksaveasfilename(
            title="이미지 저장",
            defaultextension=".png",
            filetypes=[
                ("PNG 파일", "*.png"),
                ("JPEG 파일", "*.jpg"),
                ("모든 파일", "*.*")
            ]
        )
        
        if file_path:
            try:
                # JPEG로 저장할 경우 RGB 모드로 변환
                if file_path.lower().endswith('.jpg') or file_path.lower().endswith('.jpeg'):
                    if self.watermarked_image.mode == 'RGBA':
                        rgb_image = Image.new('RGB', self.watermarked_image.size, (255, 255, 255))
                        rgb_image.paste(self.watermarked_image, mask=self.watermarked_image.split()[-1])
                        rgb_image.save(file_path, 'JPEG', quality=95)
                    else:
                        self.watermarked_image.save(file_path, 'JPEG', quality=95)
                else:
                    self.watermarked_image.save(file_path)
                
                messagebox.showinfo("성공", f"이미지가 성공적으로 저장되었습니다!\n경로: {file_path}")
                
            except Exception as e:
                messagebox.showerror("오류", f"이미지 저장 중 오류가 발생했습니다: {str(e)}")
    
    def reset_image(self):
        """이미지를 원본 상태로 되돌립니다."""
        if self.original_image:
            self.watermarked_image = self.original_image.copy()
            self.update_preview()
            messagebox.showinfo("초기화", "이미지가 원본 상태로 되돌아갔습니다.")

def main():
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
