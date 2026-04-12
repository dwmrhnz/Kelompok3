import os
from rich.console import Console

class QueuePesanan:
    """
    Class untuk mengelola antrean pesanan restoran menggunakan struktur data Queue (FIFO).
    Dibuat menggunakan List bawaan Python.
    """
    
    def __init__(self):
        # Menggunakan list untuk simulasi antrean
        self.antrian = []
        # Menyimpan nomor urut terakhir agar nomor antrean selalu bertambah
        self.nomor_terakhir = 0

    def ambil_antrean(self, nama_pelanggan, tipe_pesanan):
        """
        Fitur Enqueue: Memasukkan pelanggan ke dalam antrean.
        
        Args:
            nama_pelanggan (str): Nama pelanggan yang memesan.
            tipe_pesanan (str): Tipe pesanan (contoh: "Dine-in" atau "Takeaway").
            
        Untuk Dawam: Panggil fungsi ini saat user di menu utama memilih "Tambah Antrean".
        """
        self.nomor_terakhir += 1
        data_pelanggan = {
            "nomor": self.nomor_terakhir,
            "nama": nama_pelanggan,
            "tipe": tipe_pesanan
        }
        self.antrian.append(data_pelanggan)
        print(f"\n[SUKSES] {nama_pelanggan} berhasil masuk antrean dengan nomor {self.nomor_terakhir} ({tipe_pesanan}).")

    def tampilkan_antrean(self):
        """
        Menampilkan status antrean saat ini (Antrean terdepan, berikutnya, dan total).
        
        Untuk Dawam: Panggil ini di menu utama jika user ingin melihat daftar tunggu.
        """
        print("\n=== STATUS ANTREAN ===")
        total_antrean = len(self.antrian)
        
        if total_antrean == 0:
            print("Antrean saat ini kosong.")
            return

        # Menampilkan antrean terdepan (index 0)
        sedang_dilayani = self.antrian[0]
        print(f"Sedang Dilayani : Nomor {sedang_dilayani['nomor']} - {sedang_dilayani['nama']} ({sedang_dilayani['tipe']})")

        # Menampilkan antrean berikutnya (index 1) jika ada
        if total_antrean > 1:
            berikutnya = self.antrian[1]
            print(f"Antrean Next    : Nomor {berikutnya['nomor']} - {berikutnya['nama']}")
        else:
            print("Antrean Next    : - (Tidak ada)")
            
        print(f"Total orang dalam antrean: {total_antrean}")
        print("======================\n")

    def layani_pelanggan(self, menu_list):
        console = Console()
        if len(self.antrian) == 0:
            console.print("\n[bold yellow][INFO] Tidak ada pelanggan dalam antrean untuk dilayani.[/bold yellow]")
            return

        pelanggan = self.antrian[0] # Jangan di-pop dulu, pop jika sudah konfirmasi 'y'
        
        # Tampilkan menu sebelum melayani
        menu_list.tampilkan_menu()
        
        console.print(f"\n[bold green]>>> MELAYANI PELANGGAN NOMOR: {pelanggan['nomor']} ({pelanggan['nama']} - {pelanggan['tipe']})[/bold green]")
        console.print("[italic cyan]*PENTING: Ketik nama menu sesuai dengan yang ada di daftar. Tekan ENTER kosong jika sudah selesai memesan.*[/italic cyan]\n")
        
        while True: # Loop Utama Transaksi
            keranjang = []
            total_belanja = 0
            # Salinan stok sementara untuk transaksi ini (mencegah stok habis kalau user batal)
            stok_sementara = {} 

            while True: # Loop Pemesanan Item
                pesanan = input("Kasir: 'Ingin pesan apa kak?' (Tekan ENTER untuk selesai): ").strip()
                
                if pesanan == '': # Selesai memesan
                    break
                    
                hasil_pencarian = menu_list.cari_menu(pesanan)
                if hasil_pencarian is None:
                    console.print(f"[bold red][GAGAL] Maaf, menu '{pesanan}' tidak ditemukan. Cek ejaanmu![/bold red]")
                    continue
                    
                # Ambil stok dari stok_sementara jika ada, jika tidak ambil dari database
                stok_saat_ini = stok_sementara.get(pesanan, hasil_pencarian.stok)
                harga_menu = hasil_pencarian.harga
                
                if stok_saat_ini <= 0:
                    console.print(f"[bold red][GAGAL] Maaf, stok untuk '{pesanan}' sedang habis.[/bold red]")
                    continue
                    
                try:
                    jumlah_pesan = int(input(f"Berapa porsi {pesanan}? (Tersedia: {stok_saat_ini}): "))
                except ValueError:
                    console.print("[bold red][ERROR] Masukkan harus angka![/bold red]")
                    continue
                    
                if jumlah_pesan <= 0 or jumlah_pesan > stok_saat_ini:
                    console.print(f"[bold red][GAGAL] Jumlah tidak valid atau melebihi stok.[/bold red]")
                    continue
                    
                # Masukkan ke keranjang
                stok_sementara[pesanan] = stok_saat_ini - jumlah_pesan
                subtotal = harga_menu * jumlah_pesan
                total_belanja += subtotal
                
                keranjang.append({
                    "menu": hasil_pencarian.nama, # Simpan nama asli
                    "jumlah": jumlah_pesan,
                    "harga_satuan": harga_menu,
                    "subtotal": subtotal
                })
                console.print(f"[bold green] + Berhasil menambah {jumlah_pesan}x {hasil_pencarian.nama}[/bold green]\n")

            # --- FASE KONFIRMASI ---
            if not keranjang:
                console.print("[yellow][INFO] Pelanggan tidak memesan apa pun.[/yellow]")
                self.antrian.pop(0) # Buang dari antrean
                break

            console.print("\n[bold cyan]--- REVIEW PESANAN ---[/bold cyan]")
            for item in keranjang:
                console.print(f"- {item['menu']} (x{item['jumlah']}) : Rp{item['subtotal']}")
            console.print(f"[bold yellow]TOTAL BAYAR: Rp{total_belanja}[/bold yellow]")
            
            yakin = input("\nApakah pesanan sudah benar? (y/n): ").strip().lower()
            if yakin == 'y':
                # Potong stok beneran di Linked List
                for item in keranjang:
                    menu_list.kurangi_stok(item['menu'], item['jumlah'])
                
                self.antrian.pop(0) # Selesai, buang dari antrean
                self._cetak_struk(pelanggan, keranjang, total_belanja)
                self.simpan_data_ke_txt(menu_list)
                break
            else:
                console.print("[bold yellow]Baik, mari kita ulang pesanannya dari awal...[/bold yellow]\n")
                # Loop utama akan berulang, keranjang reset.
    
    def _cetak_struk(self, pelanggan, keranjang, total_belanja):
        """Fungsi internal untuk mencetak struk (dipisah agar rapi)"""
        console = Console()
        console.print("\n[bold white on black]          STRUK PEMBELIAN SARIAWAM          [/bold white on black]")
        console.print(f"Pelanggan: {pelanggan['nama']} ({pelanggan['tipe']})")
        console.print("-" * 44)
        for item in keranjang:
            console.print(f"{item['menu']} (x{item['jumlah']})")
            console.print(f"  @ Rp{item['harga_satuan']:<15} Rp{item['subtotal']}")
        console.print("-" * 44)
        console.print(f"[bold green]TOTAL BAYAR: Rp{total_belanja}[/bold green]")
        console.print("-" * 44)
        console.print("       Terima kasih telah berkunjung!       \n")

    def simpan_data_ke_txt(self, menu_list, nama_file="menu.txt"):
        """
        Fitur File Handling: Menyimpan perubahan stok ke file .txt.
        
        Args:
            menu_list (object): Objek Linked List berisi daftar menu.
            nama_file (str): Nama file tempat menyimpan data. Default 'menu.txt'.
            
        Untuk Dawam:
        Pastikan Linked List milikmu memiliki fungsi ambil_semua_data() yang 
        mengembalikan list of dictionary dengan key: 'jenis', 'nama', 'harga', 'stok'.
        """
        try:
            # Ambil semua data terupdate dari Linked List
            data_menu_terupdate = menu_list.ambil_semua_data()
            
            # Rewrite file text dengan data baru
            with open(nama_file, 'w', encoding='utf-8') as file:
                for item in data_menu_terupdate:
                    file.write(item + "\n")
                    
            print(f"[SISTEM] Data stok terbaru berhasil disimpan ke dalam file '{nama_file}'.")
            
        except Exception as e:
            print(f"[SISTEM ERROR] Terjadi kesalahan saat menyimpan file: {e}")