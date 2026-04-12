from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

class NodeMenu:
    """
    Class ini merepresentasikan satu entitas (node) menu di dalam Linked List.
    Menyimpan atribut jenis, nama, harga, stok, dan pointer/referensi ke node berikutnya.
    """
    def __init__(self, jenis, nama, harga, stok):
        self.jenis = jenis
        self.nama = nama
        self.harga = int(harga)  # Memastikan tipe data integer
        self.stok = int(stok)    # Memastikan tipe data integer
        self.next = None         # Pointer ke node berikutnya


class LinkedListMenu:
    """
    Class ini mengelola struktur data Single Linked List untuk semua daftar menu.
    Berisi kumpulan fungsi/method (CRUD dan Sorting) untuk diakses oleh modul lain.
    """
    def __init__(self):
        self.head = None  # Titik awal dari Linked List

    def tambah_di_akhir(self, jenis, nama, harga, stok):
        """
        Membuat node baru dan menambahkannya ke posisi paling belakang (tail) di Linked List.
        """
        node_baru = NodeMenu(jenis, nama, harga, stok)
        
        # Jika linked list masih kosong, jadikan node baru sebagai head
        if not self.head:
            self.head = node_baru
            return
        
        # Jika tidak kosong, telusuri (traverse) sampai ke node terakhir
        current = self.head
        while current.next:
            current = current.next
        
        # Sambungkan node terakhir ke node baru
        current.next = node_baru

    def muat_dari_txt(self, nama_file="menu.txt"):
        """
        Membaca data dari file .txt dan memuatnya ke dalam Linked List.
        """
        try:
            with open(nama_file, 'r') as file:
                for line in file:
                    # Menghilangkan whitespace/newline di awal dan akhir
                    line = line.strip()
                    if not line:
                        continue  # Abaikan baris kosong
                    
                    # Memisahkan data berdasarkan koma (CSV format)
                    parts = line.split(',')
                    if len(parts) == 4:
                        jenis, nama, harga, stok = parts
                        self.tambah_di_akhir(jenis.strip(), nama.strip(), harga, stok)
            print(f"[INFO] Data menu berhasil dimuat dari {nama_file}.")
        except FileNotFoundError:
            print(f"[ERROR] File {nama_file} tidak ditemukan!")

    def tampilkan_menu(self):
        """Mencetak daftar menu dengan library rich (4 Kolom)"""
        console = Console()
        if not self.head:
            console.print("[bold red]Daftar menu masih kosong.[/bold red]")
            return

        kategori_menu = {}
        current = self.head
        while current:
            if current.jenis not in kategori_menu:
                kategori_menu[current.jenis] = []
            kategori_menu[current.jenis].append(current)
            current = current.next

        # Membuat tabel utama (tanpa garis luar)
        table = Table(show_header=False, box=box.SIMPLE, expand=True)
        for _ in range(4): # 4 Kolom sesuai permintaan
            table.add_column(justify="left", ratio=1)

        nama_kategori = list(kategori_menu.keys())
        
        # Memecah kategori menjadi per 4 kolom
        for i in range(0, len(nama_kategori), 4):
            chunk = nama_kategori[i:i+4]
            
            # Baris untuk Judul Kategori
            judul_cols = [f"[bold cyan]-- {k.upper()} --[/bold cyan]" for k in chunk]
            # Menambah padding kosong jika kategori kurang dari 4 di baris terakhir
            while len(judul_cols) < 4:
                judul_cols.append("")
            table.add_row(*judul_cols)
            
            # Baris untuk Isi Menu
            isi_cols = []
            for k in chunk:
                teks_menu = ""
                for item in kategori_menu[k]:
                    # Menggunakan :, untuk ribuan dan replace untuk mengubah koma ke titik
                    harga_format = f"Rp{item.harga:,}".replace(",", ".")
                    teks_menu += f"[white]{item.nama}[/white]\n[yellow]{harga_format}[/yellow]\n\n"
                isi_cols.append(teks_menu.strip())
            
            while len(isi_cols) < 4:
                isi_cols.append("")
            table.add_row(*isi_cols)
            table.add_row("", "", "", "") # Spasi antar baris kategori

        panel = Panel(table, title="[bold magenta] DAFTAR MENU SARIAWAM [/bold magenta]", border_style="magenta")
        console.print(panel)

    def cari_menu(self, nama_menu):
        """
        Mencari menu berdasarkan nama (case-insensitive).
        Return: Object NodeMenu jika ditemukan, atau None jika tidak ditemukan.
        """
        current = self.head
        while current:
            # Menggunakan .lower() agar pencarian tidak sensitif terhadap huruf besar/kecil
            if current.nama.lower() == nama_menu.lower():
                return current
            current = current.next
        return None

    def cari_menu_sebagian(self, keyword):
        """Mencari menu yang mengandung kata kunci (partial match)"""
        hasil = []
        current = self.head
        while current:
            if keyword.lower() in current.nama.lower():
                hasil.append(current)
            current = current.next
        return hasil

    def urutkan_harga(self, ascending=True):
        """
        Mengurutkan menu di dalam Linked List berdasarkan harga.
        Menggunakan algoritma Bubble Sort pada nilai (value) dari node.
        """
        if not self.head or not self.head.next:
            return  # Tidak perlu diurutkan jika kosong atau hanya 1 elemen

        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current.next:
                # Tentukan kondisi pertukaran berdasarkan parameter ascending
                if ascending:
                    kondisi_tukar = current.harga > current.next.harga
                else:
                    kondisi_tukar = current.harga < current.next.harga

                # Jika kondisi terpenuhi, tukar (swap) isi data nodenya
                if kondisi_tukar:
                    # Menukar jenis
                    current.jenis, current.next.jenis = current.next.jenis, current.jenis
                    # Menukar nama
                    current.nama, current.next.nama = current.next.nama, current.nama
                    # Menukar harga
                    current.harga, current.next.harga = current.next.harga, current.harga
                    # Menukar stok
                    current.stok, current.next.stok = current.next.stok, current.stok
                    
                    swapped = True
                
                current = current.next

    def kurangi_stok(self, nama_menu, jumlah):
        """
        Mengurangi stok dari suatu menu ketika dipesan.
        Akan dipanggil oleh modul antrean / kasir.
        Return: True jika berhasil, False jika stok kurang atau menu tidak ada.
        """
        node = self.cari_menu(nama_menu)
        if node:
            if node.stok >= jumlah:
                node.stok -= jumlah
                return True
            else:
                print(f"[Peringatan] Stok {node.nama} tidak mencukupi! Sisa stok: {node.stok}")
                return False
        else:
            print(f"[Peringatan] Menu '{nama_menu}' tidak ditemukan di database.")
            return False

    def ambil_semua_data(self):
        """
        Mengambil seluruh data pada Linked List dan mengemasnya menjadi list of string.
        Format pengembalian (Return): ["jenis,nama,harga,stok", "jenis,nama,harga,stok", ...]
        Berguna untuk di-rewrite kembali ke file menu.txt oleh teman setim.
        """
        list_data = []
        current = self.head
        while current:
            # Memformat atribut sesuai format awal file txt
            baris_data = f"{current.jenis},{current.nama},{current.harga},{current.stok}"
            list_data.append(baris_data)
            current = current.next
        
        return list_data
