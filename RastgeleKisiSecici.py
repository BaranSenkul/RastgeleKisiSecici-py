## Rastgele Satır Seçici
## BaranSenkul tarafından hazırlandı
## Ver. 0.2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk  
import random
import time

class RandomPickerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Rastgele Kişi Seçici")
        self.geometry("340x360") 
        self.selected_file = ""
        self.random_picker_list = []

        self.create_widgets()

    def create_widgets(self):
        
        self.title("Rastgele Kişi Seçici")
        self.geometry("340x360")  

       
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 370
        window_height = 350
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        self.geometry(f"340x360+{x_coordinate}+{y_coordinate}")

  
        self.select_file_button = tk.Button(self, text="Dosya Seç", command=self.select_file)
        self.select_file_button.grid(row=0, column=0, pady=10, padx=10, sticky="w")

        self.pick_random_button = tk.Button(self, text="Seçimi Yap", command=self.pick_random)
        self.pick_random_button.grid(row=0, column=1, pady=10, padx=10)

        self.remove_from_list_button = tk.Button(self, text="Listeden sil", command=self.remove_from_list)
        self.remove_from_list_button.grid(row=0, column=2, pady=10, padx=10)

        self.about_button = tk.Button(self, text="Hakkında", command=self.about_window)
        self.about_button.grid(row=0, column=3, pady=10, padx=10)

        self.list_frame = tk.Frame(self)
        self.list_frame.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        self.random_label = tk.Label(self.list_frame, text="Seçilecekler Listesi")
        self.random_label.pack()

        self.random_listbox = tk.Listbox(self.list_frame, width=50, height=15)
        self.random_listbox.pack(side="left", fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.list_frame, orient="vertical")
        self.scrollbar.config(command=self.random_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.random_listbox.config(yscrollcommand=self.scrollbar.set)


        version_label = tk.Label(self, text="Ver. 0.2 - Build: 08/03/24 - BaranSenkul", anchor="e")
        version_label.grid(row=2, column=0, columnspan=4, pady=(0, 10), padx=10, sticky="e")

    def select_file(self):
        self.selected_file = filedialog.askopenfilename(filetypes=[("Metin Dosyaları", "*.txt")])
        if self.selected_file:
            self.load_random_picker_list()

    def load_random_picker_list(self):
        with open(self.selected_file, 'r', encoding='utf-8') as file:
            self.random_picker_list = [line.strip() for line in file if not line.startswith('#')]
        
        self.update_random_listbox()

    def update_random_listbox(self):
        self.random_listbox.delete(0, tk.END)
        for item in self.random_picker_list:
            self.random_listbox.insert(tk.END, item)

    def pick_random(self):
        if not self.random_picker_list:
            messagebox.showerror("Seçim - Hata", "Seçilecek kimse yok veya kalmadı\nLütfen bir dosya seçin. ")
            return

        self.loading_window = tk.Toplevel(self)
        self.loading_window.title("Bekleyin...")
        self.loading_window.geometry(f"300x100+{self.winfo_screenwidth() // 2 - 150}+{self.winfo_screenheight() // 2 - 50}")
        self.loading_window.attributes("-topmost", True)

        progress_label = tk.Label(self.loading_window, text="Seçiliyor")
        progress_label.pack(pady=10)
        progress_bar = ttk.Progressbar(self.loading_window, length=200, mode="determinate")  
        progress_bar.pack(pady=5)


        steps = 100
        duration = 2000 

      
        step_size = 100 / steps

        def update_progress(i):
            progress_bar["value"] = step_size * i

        for i in range(steps + 1):
            self.loading_window.after(int(duration / steps * i), update_progress, i)
            self.loading_window.update_idletasks()

      
        self.after(duration, self.close_loading_window)

    def close_loading_window(self):
        self.loading_window.destroy()
        if self.random_picker_list:
            random_item = random.choice(self.random_picker_list)
            selected_item_window = tk.Toplevel(self)
            selected_item_window.title("Seçilen Kişi")
            selected_item_window.geometry(f"300x150+{self.winfo_screenwidth() // 2 - 150}+{self.winfo_screenheight() // 2 - 75}")
            selected_item_window.attributes("-topmost", True)

            item_label = tk.Label(selected_item_window, text="Seçilen kişi:")
            item_label.pack(pady=5)

            selected_label = tk.Label(selected_item_window, text=random_item, font=("Arial", 14, "bold"))  
            selected_label.pack(pady=5)

            close_button = tk.Button(selected_item_window, text="Pencereyi Kapat", command=selected_item_window.destroy)
            close_button.pack(pady=5)

            remove_button = tk.Button(selected_item_window, text="Seçilecekler Listesinden Kaldır", command=lambda: self.remove_item_from_list(random_item, selected_item_window))
            remove_button.pack(pady=5)

    def remove_item_from_list(self, item, window):
        if item in self.random_picker_list:
            self.random_picker_list.remove(item)
            self.update_random_listbox()
            window.destroy()

    def remove_from_list(self):
        if not self.random_picker_list:
            messagebox.showwarning("Uyarı", "Listede kimse olmadığı için kimseyi silemezsiniz\nLütfen bir dosya seçin.")
            return

        selection_window = tk.Toplevel(self)
        selection_window.title("Kişi Sil")
        selection_window.geometry(f"300x260+{self.winfo_screenwidth() // 2 - 200 }+{self.winfo_screenheight() // 2 - 200 }")
        selection_window.attributes("-topmost", False)

        label = tk.Label(selection_window, text="Silinecek kişiyi seçin\nNot: Silinen kişi dosya tekrar açılmadan geri gelemez")
        label.pack(pady=10)

        selection_listbox = tk.Listbox(selection_window, width=50, height=10)
        selection_listbox.pack()

        scrollbar = tk.Scrollbar(selection_window, orient="vertical")
        scrollbar.config(command=selection_listbox.yview)
        scrollbar.pack(side="right", fill="y")

        selection_listbox.config(yscrollcommand=scrollbar.set)

        for item in self.random_picker_list:
            selection_listbox.insert(tk.END, item)

        remove_button = tk.Button(selection_window, text="Kişiyi Sil", command=lambda: self.remove_selected_item(selection_listbox, selection_window))
        remove_button.pack(pady=10)

    def remove_selected_item(self, selection_listbox, window):
        selected_index = selection_listbox.curselection()
        if selected_index:
            item = selection_listbox.get(selected_index)
            self.random_picker_list.remove(item)
            self.update_random_listbox()
            window.destroy()
        else:
            messagebox.showwarning("Uyarı", "Kimse seçilmedi.\nBirini silmek istemiyorsanız Kişiyi Sil penceresini kapatın.\n\nKimse seçilmediği için kimse silinmedi.")

    def about_window(self):
        about_text = """Rastgele Kişi Seçici Ver. 0.2\n\n--HAKKINDA--\n    Linux, Windows, Android ve macOS uyumlu, sınıf ortamında kullanılması için tasarlanmış MIT Lisansı altında açık kaynaklı, Python dili ve Tkinter kütüphanesi kullanılarak yazılmış, bir .txt dosyasından rastgele satır seçen ve hoş (hoş olup olmadığı tartışılır) bir kulanıcı arayüzüne sahip bir program.\n\n--LİSTE DOSYASI HAZIRLAMA--\n    Liste dosyaları .txt formatında kaydedilmelidir, her satıra farklı biri gelecek şekilde yazılmalıdır. # ile başlayan satırlar not olarak kabul edildiği için program tarafından okunmayacaktır. örnek için programla aynı dizinde bulunan örnek.txt incelenebilir. \n\n --GENEL KULLANIM--\nAna pencerede "Dosya seç" butonı ile bir dosya seçilir,\n silinmesi gereken kişiler varsa "Listeden sil" menüsü altından silinir, \n"Seçimi Yap" butonuna basılarak listeden rastgele biri seçilir,\n son olarak sonuç penceresinden kullanıcının isteği ile kişi listeden kaldırılır.\n\n--ULAŞIM--\nKaynak kodu: --github--\nMail: baransenkul@protonmail.com\nGuilded: guilded.gg/u/BaranSenkul\n\n BaranSenkul tarafından hazırlanmıştır."""

        messagebox.showinfo("Program Hakkında Bilgilendirme", about_text)

if __name__ == "__main__":
    app = RandomPickerApp()
    app.mainloop()
