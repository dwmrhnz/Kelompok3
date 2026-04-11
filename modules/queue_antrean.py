import os

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
        """
        Fitur Dequeue: Memanggil dan melayani pelanggan antrean pertama.
        
        Args:
            menu_list (object): Objek Linked List yang berisi daftar menu.
            
        Untuk Dawam: 
        1. Pastikan objek Linked List milikmu dilempar ke dalam parameter fungsi ini.
        2. Pastikan objek Linked List milikmu memiliki fungsi:
           - cari_menu(nama_menu) -> return tuple/list (harga, stok) atau None jika tidak ketemu.
           - kurangi_stok(nama_menu, jumlah) -> tidak perlu return, hanya mengurangi stok di Linked List.
        """
        if len(self.antrian) == 0:
            print("\n[INFO] Tidak ada pelanggan dalam antrean untuk dilayani.")
            return

        # Dequeue: Mengambil dan menghapus pelanggan di urutan pertama (index 0)
        pelanggan = self.antrian.pop(0)
        
        print("\n" + "="*40)
        print(f"    MELAYANI PELANGGAN NOMOR: {pelanggan['nomor']}")
        print(f"    Nama: {pelanggan['nama']} | Tipe: {pelanggan['tipe']}")
        print("="*40)
        
        keranjang = []
        total_belanja = 0

        # Simulasi dialog kasir
        while True:
            pesanan = input("\nKasir: 'Ingin pesan apa kak? (Ketik 'selesai' jika sudah cukup): ' ").strip()
            
            if pesanan.lower() == 'selesai':
                break
                
            # Cek ke Linked List Dawam apakah menu ada
            hasil_pencarian = menu_list.cari_menu(pesanan)
            
            if hasil_pencarian is None:
                print(f"[GAGAL] Maaf, menu '{pesanan}' tidak ditemukan di sistem.")
                continue
                
            harga_menu = hasil_pencarian.harga
            stok_menu = hasil_pencarian.stok
            
            if stok_menu <= 0:
                print(f"[GAGAL] Maaf, stok untuk menu '{pesanan}' sedang habis/kosong.")
                continue
                
            # Validasi input jumlah menggunakan try-except
            try:
                jumlah_pesan = int(input(f"Kasir: 'Mau pesan {pesanan} berapa banyak? (Stok tersisa: {stok_menu}): ' "))
            except ValueError:
                print("[ERROR] Masukkan harus berupa angka! Silakan ulangi pesanan.")
                continue
                
            if jumlah_pesan <= 0:
                print("[ERROR] Jumlah pesanan minimal 1.")
                continue
                
            if jumlah_pesan > stok_menu:
                print(f"[GAGAL] Stok tidak mencukupi. Hanya bisa pesan maksimal {stok_menu}.")
                continue
                
            # Proses pesanan berhasil
            menu_list.kurangi_stok(pesanan, jumlah_pesan)
            subtotal = harga_menu * jumlah_pesan
            total_belanja += subtotal
            
            keranjang.append({
                "menu": pesanan,
                "jumlah": jumlah_pesan,
                "harga_satuan": harga_menu,
                "subtotal": subtotal
            })
            print(f"[SUKSES] Berhasil menambahkan {jumlah_pesan}x {pesanan} ke keranjang.")

        # Cetak Struk jika pelanggan jadi membeli sesuatu
        if keranjang:
            print("\n" + "-"*40)
            print("             STRUK PEMBELIAN")
            print("-"*40)
            print(f"Pelanggan: {pelanggan['nama']} ({pelanggan['tipe']})")
            print("-"*40)
            for item in keranjang:
                print(f"{item['menu']} (x{item['jumlah']})")
                print(f"  @ Rp{item['harga_satuan']} -> Rp{item['subtotal']}")
            print("-"*40)
            print(f"TOTAL BAYAR: Rp{total_belanja}")
            print("-"*40)
            print("Terima kasih telah berkunjung!\n")
            
            # Panggil fungsi simpan untuk mengupdate file txt setiap selesai transaksi
            self.simpan_data_ke_txt(menu_list)
        else:
            print(f"\n[INFO] Pelanggan {pelanggan['nama']} tidak jadi memesan apa pun.")

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