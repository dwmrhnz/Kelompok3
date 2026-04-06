# ==========================================================
# Sistem Antrian Restoran + File TXT
# ==========================================================
nama_file_menu = "Kelompok3/menu_restoran.txt"
nama_file_antrean = "Kelompok3/antrean_restoran.txt"

# Node Linked List
class Node:
    def __init__(self,no,nama,pesanan,total_harga):
        self.no = no
        self.nama = nama
        self.pesanan = pesanan
        self.total_harga = total_harga
        self.next = None

# Queue Linked List
class queueRestoran:
    def __init__(self):
        self.front = None
        self.rear = None
    
    def is_empty(self):
        return self.front is None
    
    def enqueue(self,no,nama,pesanan,total_harga, save=True):
        nodeBaru = Node(no,nama,pesanan,total_harga)

        if self.is_empty():
            self.front = nodeBaru
            self.rear = nodeBaru
        else:
            self.rear.next = nodeBaru
            self.rear = nodeBaru 

        # AUTO SAVE (hanya kalau save=True)
        if save:
            with open(nama_file_antrean, "a") as file:
                file.write(f"{no},{nama},{pesanan},{total_harga}\n")

    def dequeue(self):
        if self.is_empty():
            print("Antrian Kosong")
            return None
        
        node_dilayani = self.front
        self.front = self.front.next

        if self.front is None:
            self.rear = None

        return node_dilayani
    
    def tampilkan(self):
        if self.is_empty():
            print("Antrian Kosong")
            return
        
        print("Daftar Antrian:")
        current = self.front
        no = 1
        while current:
            print(f"{no}. {current.no} - {current.nama} - {current.pesanan} - Rp{current.total_harga}")
            current = current.next
            no += 1

    # ==========================
    # LOAD DARI FILE
    # ==========================
    def load_dari_file(self, nama_file_antrean):
        try:
            with open(nama_file_antrean, "r") as file:
                for baris in file:
                    no, nama, pesanan, total = baris.strip().split(",")
                    
                    # ⛔ jangan simpan lagi ke file
                    self.enqueue(int(no), nama, pesanan, int(total), save=False)

            print("Data antrean berhasil dimuat dari file!")
        except FileNotFoundError:
            print("File antrean tidak ditemukan, mulai dari kosong.")


# ==========================
# MENU RESTORAN (TXT)
# ==========================
def tampilkan_menu():
    try:
        with open(nama_file_menu, "r") as file:
            print("\n===== MENU RESTORAN =====")
            no = 1
            for baris in file:
                baris = baris.strip()
                
                # Split berdasarkan koma
                nama_menu, harga = baris.split(",")

                print(f"{no}. {nama_menu} - Rp{harga}")
                no += 1

    except FileNotFoundError:
        print("File menu tidak ditemukan!")

def tambah_menu():
    try:
        nama_menu = input("Masukkan nama menu: ").strip()
        harga = int(input("Masukkan harga: ").strip())

        # Simpan langsung ke file (append)
        with open(nama_file_menu, "a") as file:
            file.write(f"{nama_menu},{harga}\n")

        print("Menu berhasil ditambahkan!\n")

        # Langsung tampilkan menu terbaru
        tampilkan_menu()

    except ValueError:
        print("Harga harus berupa angka!")

def ambil_menu():
    daftar_menu = []
    try:
        with open(nama_file_menu, "r") as file:
            for baris in file:
                nama, harga = baris.strip().split(",")
                daftar_menu.append((nama, int(harga)))
    except FileNotFoundError:
        print("File menu tidak ditemukan!")
    
    return daftar_menu