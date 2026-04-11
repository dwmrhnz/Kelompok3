import os

# Import class dari folder modules buatan Fardhan dan Hirzi
from modules.linkedlist_menu import LinkedListMenu
from modules.queue_antrean import QueuePesanan

def bersihkan_layar():
    """Fungsi untuk membersihkan layar terminal agar tampilan rapi."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # 1. INISIALISASI OBJEK
    daftar_menu = LinkedListMenu()
    antrean_kasir = QueuePesanan()

    # Memastikan folder data ada (mencegah error jika folder belum dibuat)
    if not os.path.exists('data'):
        os.makedirs('data')

    # Memuat data dari file txt ke dalam Linked List saat aplikasi pertama dibuka
    lokasi_file_txt = "data/menu.txt"
    daftar_menu.muat_dari_txt(lokasi_file_txt)
    
    input("\nTekan Enter untuk masuk ke aplikasi...")

    # 2. MENU UTAMA (CUSTOMER VIEW)
    while True:
        bersihkan_layar()
        print("=========================================")
        print("       SELAMAT DATANG DI McDawam")
        print("=========================================")
        print("-- Silakan Pilih Layanan --")
        print("1. Tampilkan Menu Utama")
        print("2. Ambil Nomor Antrean")
        print("3. Tampilkan Antrean Saat Ini")
        print("4. Menuju Kasir (Panggil Antrean)")
        print("5. Keluar")
        print("=========================================")

        pilihan = input(">> Masukkan pilihan Anda: ").strip()

        if pilihan == '1':
            bersihkan_layar()
            print("--- TAMPILKAN MENU ---")
            urutkan = input("Apakah Anda ingin mengurutkan menu berdasarkan harga termurah? (y/n): ").strip().lower()
            
            if urutkan == 'y':
                daftar_menu.urutkan_harga(ascending=True)
                print("\n[INFO] Menu telah diurutkan dari termurah ke termahal.\n")
            
            # Panggil fungsi Read buatan Fardhan
            daftar_menu.tampilkan_menu()
            input("\nTekan Enter untuk kembali ke Menu Utama...")

        elif pilihan == '2':
            bersihkan_layar()
            print("--- AMBIL NOMOR ANTREAN ---")
            nama = input("Masukkan Nama Anda: ").strip()
            
            if not nama:
                print("[ERROR] Nama tidak boleh kosong!")
            else:
                print("\nPilih Tipe Pesanan:")
                print("1. Dine-in (Makan di tempat)")
                print("2. Takeaway (Bawa pulang)")
                tipe_input = input("Pilihan (1/2): ").strip()
                
                # Validasi tipe pesanan
                if tipe_input == '1':
                    tipe = "Dine-in"
                elif tipe_input == '2':
                    tipe = "Takeaway"
                else:
                    tipe = "Dine-in" # Default jika input ngawur
                    print("[WARNING] Pilihan tidak valid, otomatis diset ke 'Dine-in'.")
                
                # Panggil fungsi Enqueue buatan Hirzi
                antrean_kasir.ambil_antrean(nama, tipe)
                
            input("\nTekan Enter untuk kembali ke Menu Utama...")

        elif pilihan == '3':
            bersihkan_layar()
            # Panggil fungsi lihat Queue buatan Hirzi
            antrean_kasir.tampilkan_antrean()
            input("Tekan Enter untuk kembali ke Menu Utama...")

        elif pilihan == '4':
            bersihkan_layar()
            # Panggil fungsi Dequeue dan transaksi buatan Hirzi
            # Parameter daftar_menu dilempar agar Hirzi bisa memotong stok
            antrean_kasir.layani_pelanggan(daftar_menu)
            
            # Karena di layani_pelanggan path file default Hirzi mungkin 'menu.txt', 
            # kita force save di sini agar aman dan rapi masuk folder data/
            antrean_kasir.simpan_data_ke_txt(daftar_menu, lokasi_file_txt)
            input("\nTekan Enter untuk kembali ke Menu Utama...")

        elif pilihan == '5':
            bersihkan_layar()
            print("Terima kasih telah berkunjung ke McDawam. Sampai jumpa!")
            break

        # 3. MODE ADMIN TERSEMBUNYI (CRUD)
        elif pilihan == '99':
            while True:
                bersihkan_layar()
                print("=========================================")
                print("           *** MODE ADMIN *** ")
                print("=========================================")
                print("1. Tambah Menu Baru")
                print("2. Keluar ke Menu Utama")
                print("=========================================")
                
                admin_pilihan = input(">> Pilih aksi admin: ").strip()

                if admin_pilihan == '1':
                    bersihkan_layar()
                    print("--- TAMBAH MENU BARU ---")
                    jenis = input("Masukkan Jenis (Contoh: Makanan/Minuman/Dessert): ").strip()
                    nama_menu = input("Masukkan Nama Menu: ").strip()
                    
                    # 4. ATURAN PENGAMANAN (Try-Except untuk angka)
                    try:
                        harga = int(input("Masukkan Harga (angka): ").strip())
                        stok = int(input("Masukkan Stok Awal (angka): ").strip())
                        
                        # Panggil fungsi Create buatan Fardhan
                        daftar_menu.tambah_di_akhir(jenis, nama_menu, harga, stok)
                        print(f"\n[SUKSES] Menu '{nama_menu}' berhasil ditambahkan!")
                        
                        # Simpan pembaruan ke TXT menggunakan fungsi Hirzi
                        antrean_kasir.simpan_data_ke_txt(daftar_menu, lokasi_file_txt)
                        
                    except ValueError:
                        print("\n[ERROR] Harga dan Stok harus berupa angka! Penambahan dibatalkan.")
                    
                    input("\nTekan Enter untuk kembali ke Menu Admin...")
                    
                elif admin_pilihan == '2':
                    break # Keluar dari loop admin, kembali ke menu utama
                else:
                    print("\n[ERROR] Pilihan admin tidak valid!")
                    input("Tekan Enter untuk mengulangi...")

        else:
            print("\n[ERROR] Pilihan tidak valid. Silakan masukkan angka 1-5.")
            input("Tekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()