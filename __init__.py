import customtkinter as ctk
from PIL import Image, ImageTk
import fitz  # PyMuPDF
class PDFViewer:
    def __init__(self, root, pdf_path):
        self.pdf_document = fitz.open(pdf_path)
        self.total_pages = self.pdf_document.page_count
        self.current_page = 0

        self.root = root
        self.root.geometry("700x900")
        self.root.title("PDF Viewer")
        self.width = None
        self.root.minsize(width=600,height=700)
        # Widget'ları oluşturma
        self.create_widgets()
        # Pencere genişliğiyle görseli eşitler ve görseli pencereye göre ölçeklendirir
        self.root.after(1000, lambda : self.show_page(0,breaker=True)) # 4 sn sonra ilk sayfayı göster

    def create_widgets(self):
        # Ana Frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill=ctk.BOTH, expand=True)

        # Scrollable Frame içinde görseli göstermek için
        self.scrollable_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.scrollable_frame.place(y=0, x=0, relheight=0.95, relwidth=1)

        self.image_frame = ctk.CTkFrame(self.scrollable_frame)
        self.image_frame.pack(fill=ctk.BOTH, expand=True)

        # Butonlar ve etiketler için bir frame oluşturma
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.place(rely=0.95, relx=0, relheight=0.05, relwidth=1)

        self.page_number_label = ctk.CTkLabel(self.controls_frame, text=f"Page 1 of {self.total_pages}")
        self.page_number_label.place(relx=0.5,rely=0.05,relwidth=0.27)

 
        self.prev_button = ctk.CTkButton(self.controls_frame, text="◀", command=self.prev_page,fg_color="black",border_color="white",border_width=1)
        self.prev_button.place(relx=0.01,rely=0.05,relwidth=0.1)

        self.next_button = ctk.CTkButton(self.controls_frame, text="▶", command=self.next_page,fg_color="black",border_color="white",border_width=1)
        self.next_button.place(relx=0.89,rely=0.05,relwidth=0.1)

        # İstenen sayfaya gitmek için entry ve buton

        self.page_entry = ctk.CTkEntry(self.controls_frame,fg_color="black",border_color="white",border_width=1)
        self.page_entry.place(relx=0.25,rely=0.05,relwidth=0.1)

        self.go_button = ctk.CTkButton(self.controls_frame, text="Go", command=self.go_to_page,fg_color="black",border_color="white",border_width=1)
        self.go_button.place(relx=0.37,rely=0.05,relwidth=0.1)

        # Frame boyutu değiştiğinde sayfayı yeniden göster
        self.image_frame.bind("<Configure>", lambda event: self.show_page())

    def show_page(self, page_num=None,breaker=False):
        if page_num is None:
            page_num=self.current_page
        if self.root.winfo_width() != self.width or self.current_page!=page_num or breaker:
            self.current_page = page_num
            self.width = self.root.winfo_width()
            self.root.maxsize(width=self.root.winfo_screenwidth(), height=int(self.width * 1.75))
            self.display_page()

    def go_to_page(self):
        page_num = int(self.page_entry.get()) - 1
        if 0 <= page_num < self.total_pages:
            self.show_page(page_num)

    def prev_page(self):
        if self.current_page > 0:
            self.show_page(self.current_page - 1)

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.show_page(self.current_page + 1)

    def display_page(self):
        page = self.pdf_document.load_page(self.current_page)
        zoom_factor = 5 # Artırılmış çözünürlük için zoom faktörü
        zoom_matrix = fitz.Matrix(zoom_factor, zoom_factor)
        pix = page.get_pixmap(matrix=zoom_matrix)

        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img.save("current_page.png",format="PNG")
        # Frame genişliğini al
        frame_width = self.scrollable_frame.winfo_width()

        # Görselin yeni genişliğini ve uzunluğunu hesapla
        img_width, img_height = img.size
        scale_factor = frame_width / img_width
        new_img_width = frame_width
        new_img_height = int(img_height * scale_factor)

        # Görseli yeniden boyutlandır
        img = img.resize((new_img_width, new_img_height), Image.LANCZOS)
        self.img_tk = ImageTk.PhotoImage(img)

        # Eski görsel varsa, üzerine yeni görsel ekle
        if hasattr(self, 'image_label'):
            self.image_label.configure(image=self.img_tk)
        else:
            # Yeni bir label oluşturup ekleyin
            self.image_label = ctk.CTkLabel(self.image_frame, image=self.img_tk)
            self.image_label.pack(fill=ctk.BOTH, expand=True)

        # Sayfa numarasını güncelle
        self.page_number_label.configure(text=f"Page {self.current_page + 1} of {self.total_pages}")

        # Görselin scroll region'ını ayarla
        self.scrollable_frame.update_idletasks()



if __name__ == "__main__":
    root = ctk.CTk()
    pdf_path = r"yourfile.pdf"
    viewer = PDFViewer(root, pdf_path)
    root.mainloop()
