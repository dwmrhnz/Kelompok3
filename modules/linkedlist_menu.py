from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

class NodeMenu:
    """ Blueprint buat tiap node menu di Linked List. """
    def __init__(self, jenis, nama, harga, stok):
        self.jenis = jenis
        self.nama = nama
        self.harga = int(harga)  # casting ke int biar aman buat dihitung
        self.stok = int(stok)    
        self.next = None         # pointer ke node selanjutnya


class LinkedListMenu:
    """ Class utama buat operasi Single Linked List (CRUD & Sorting). """
    def __init__(self):
        self.head = None  # head awal kosong

    def tambah_di_akhir(self, jenis, nama, harga, stok):
        """ Bikin node baru terus ditaruh di paling ujung (tail). """
        node_baru = NodeMenu(jenis, nama, harga, stok)
        
        # kalo list masih kosong, node baru langsung jadi head
        if not self.head:
            self.head = node_baru
            return
        
        # traverse sampe nemu ujungnya
        current = self.head
        while current.next:
            current = current.next
        
        # sambungin pointer node terakhir ke node baru
        current.next = node_baru

    def muat_dari_txt(self, nama_file="menu.txt"):
        """ Baca data dari file txt, terus masukin ke Linked List. """
        try:
            with open(nama_file, 'r') as file:
                for line in file:
                    line = line.strip() # bersihin enter/spasi berlebih
                    if not line:
                        continue # skip baris kosong
                    
                    # split string dari format CSV
                    parts = line.split(',')
                    if len(parts) == 4:
                        jenis, nama, harga, stok = parts
                        self.tambah_di_akhir(jenis.strip(), nama.strip(), harga, stok)
        except FileNotFoundError:
            print(f"[red][ERROR][/red] File {nama_file} nggak ketemu!")

    def tampilkan_menu(self):
        """ Print UI menu pakai library rich (dibuat 4 kolom). """
        console = Console(highlight=False)
        if not self.head:
            console.print("[bold red]Daftar menu masih kosong.[/bold red]")
            return

        # grouping menu ke dictionary biar gampang di-print per kategori
        kategori_menu = {}
        current = self.head
        while current:
            if current.jenis not in kategori_menu:
                kategori_menu[current.jenis] = []
            kategori_menu[current.jenis].append(current)
            current = current.next

        # setup tabel layout simple
        table = Table(show_header=False, box=box.SIMPLE, expand=True)
        for _ in range(4): 
            table.add_column(justify="left", ratio=1)

        nama_kategori = list(kategori_menu.keys())
        
        # pecah kategori jadi per 4 kolom
        for i in range(0, len(nama_kategori), 4):
            chunk = nama_kategori[i:i+4]
            
            judul_cols = [f"[bold cyan]-- {k.upper()} --[/bold cyan]" for k in chunk]
            while len(judul_cols) < 4:
                judul_cols.append("")
            table.add_row(*judul_cols)
            
            isi_cols = []
            for k in chunk:
                teks_menu = ""
                for item in kategori_menu[k]:
                    # convert integer ke string format rupiah
                    harga_format = f"Rp{item.harga:,}".replace(",", ".")
                    teks_menu += f"[white]{item.nama}[/white]\n[yellow]{harga_format}[/yellow]\n\n"
                isi_cols.append(teks_menu.strip())
            
            while len(isi_cols) < 4:
                isi_cols.append("")
            table.add_row(*isi_cols)
            table.add_row("", "", "", "")

        panel = Panel(table, title="[bold magenta] DAFTAR MENU SARIAWAM [/bold magenta]", border_style="magenta")
        console.print(panel)

    def cari_menu(self, nama_menu):
        """ Cari menu by nama exact. Return object Node kalo ketemu. """
        current = self.head
        while current:
            # di-lower() semua biar case-insensitive
            if current.nama.lower() == nama_menu.lower():
                return current
            current = current.next
        return None

    def cari_menu_sebagian(self, keyword):
        """ Fitur search pakai keyword (partial match). Return list of Nodes. """
        hasil = []
        current = self.head
        while current:
            if keyword.lower() in current.nama.lower():
                hasil.append(current)
            current = current.next
        return hasil

    def urutkan_harga(self, ascending=True):
        """ Sorting Linked List pakai Bubble Sort (cuma swap value/datanya). """
        if not self.head or not self.head.next:
            return  # skip kalo list kosong atau cuma 1 node

        swapped = True
        while swapped:
            swapped = False
            current = self.head
            while current.next:
                # cek kondisi asc / desc
                if ascending:
                    kondisi_tukar = current.harga > current.next.harga
                else:
                    kondisi_tukar = current.harga < current.next.harga

                # eksekusi swap data kalo kondisi terpenuhi
                if kondisi_tukar:
                    # swap jenis
                    current.jenis, current.next.jenis = current.next.jenis, current.jenis
                    # swap nama
                    current.nama, current.next.nama = current.next.nama, current.nama
                    # swap harga
                    current.harga, current.next.harga = current.next.harga, current.harga
                    # swap stok
                    current.stok, current.next.stok = current.next.stok, current.stok
                    
                    swapped = True
                
                current = current.next

    def kurangi_stok(self, nama_menu, jumlah):
        """ Update stok node waktu ada pesanan di kasir. """
        node = self.cari_menu(nama_menu)
        if node:
            if node.stok >= jumlah:
                node.stok -= jumlah
                return True
            else:
                print(f"[Peringatan] Stok {node.nama} kurang! Sisa: {node.stok}")
                return False
        else:
            print(f"[Peringatan] Menu '{nama_menu}' ga ketemu di database.")
            return False

    def ambil_semua_data(self):
        """ Ambil semua data list buat di-rewrite balik ke txt. """
        list_data = []
        current = self.head
        while current:
            # format ulang stringnya persis kayak format txt awal
            baris_data = f"{current.jenis},{current.nama},{current.harga},{current.stok}"
            list_data.append(baris_data)
            current = current.next
        
        return list_data