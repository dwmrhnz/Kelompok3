import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from modules.linkedlist_menu import LinkedListMenu
from modules.queue_antrean import QueuePesanan

console = Console()

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    daftar_menu = LinkedListMenu()
    antrean_kasir = QueuePesanan()

    if not os.path.exists('data'):
        os.makedirs('data')

    lokasi_file_txt = "data/menu.txt"
    daftar_menu.muat_dari_txt(lokasi_file_txt)
    
    input("\nTekan Enter untuk masuk ke aplikasi Sariawam...")

    while True:
        bersihkan_layar()
        # Panel Judul menggunakan rich
        judul = Panel(
            Align.center("[bold yellow]SELAMAT DATANG DI RESTORAN SARIAWAM[/bold yellow]\n[italic white]Fardhan BianSA - HiRzI HAidi - DaWAM[/italic white]"),
            style="bold cyan",
            width=65
        )
        console.print(judul)
        
        console.print("\n[bold cyan]-- Silakan Pilih Layanan --[/bold cyan]")
        console.print("[1] Tampilkan Menu & Cari")
        console.print("[2] Ambil Nomor Antrean")
        console.print("[3] Tampilkan Antrean Saat Ini")
        console.print("[4] Menuju Kasir (Melayani Pelanggan)")
        console.print("[5] Keluar\n")

        pilihan = input(">> Masukkan pilihan Anda: ").strip()

        if pilihan == '1':
            while True: # Sub-menu untuk Tampilkan Menu
                bersihkan_layar()
                daftar_menu.tampilkan_menu()
                
                console.print("\n[bold cyan]-- Opsi Menu --[/bold cyan]")
                console.print("[1] Cari Hidangan (Ketik Nama)")
                console.print("[2] Urutkan Harga Termahal - Termurah")
                console.print("[3] Urutkan Harga Termurah - Termahal")
                console.print("[0] Kembali ke Layanan Utama")
                
                opsi_menu = input(">> Pilih opsi: ").strip()
                
                if opsi_menu == '1':
                    kata = input("Masukkan kata kunci pencarian: ").strip()
                    hasil = daftar_menu.cari_menu_sebagian(kata)
                    console.print(f"\n[bold green]Hasil Pencarian untuk '{kata}':[/bold green]")
                    if hasil:
                        for h in hasil:
                            console.print(f"- {h.nama} ([yellow]Rp{h.harga}[/yellow])")
                    else:
                        console.print("[red]Menu tidak ditemukan.[/red]")
                    input("\nTekan Enter untuk melanjutkan...")
                    
                elif opsi_menu == '2':
                    daftar_menu.urutkan_harga(ascending=False) # Termahal
                    console.print("[green]Menu telah diurutkan dari yang termahal.[/green]")
                    input("Tekan Enter untuk melihat...")
                    
                elif opsi_menu == '3':
                    daftar_menu.urutkan_harga(ascending=True) # Termurah
                    console.print("[green]Menu telah diurutkan dari yang termurah.[/green]")
                    input("Tekan Enter untuk melihat...")
                    
                elif opsi_menu == '0':
                    break # Kembali ke while True utama
                    
        elif pilihan == '2':
            bersihkan_layar()
            console.print("[bold cyan]--- AMBIL NOMOR ANTREAN ---[/bold cyan]")
            nama = input("Masukkan Nama Anda: ").strip()
            if nama:
                console.print("Pilih Tipe: [1] Dine-in  [2] Takeaway")
                tipe_input = input("Pilihan (1/2): ").strip()
                tipe = "Takeaway" if tipe_input == '2' else "Dine-in"
                antrean_kasir.ambil_antrean(nama, tipe)
            input("\nTekan Enter kembali...")

        elif pilihan == '3':
            bersihkan_layar()
            antrean_kasir.tampilkan_antrean()
            input("Tekan Enter kembali...")

        elif pilihan == '4':
            bersihkan_layar()
            antrean_kasir.layani_pelanggan(daftar_menu)
            input("\nTekan Enter kembali...")

        elif pilihan == '5':
            bersihkan_layar()
            console.print("[bold green]Terima kasih telah berkunjung ke Sariawam. Sampai jumpa![/bold green]")
            break

        # KODE ADMIN BARU
        elif pilihan == '67':
            while True:
                bersihkan_layar()
                admin_panel = Panel(Align.center("[bold red]*** MODE ADMIN SARIAWAM ***[/bold red]"), width=65)
                console.print(admin_panel)
                console.print("[1] Tambah Menu Baru (Create)")
                console.print("[2] Ubah Harga/Stok Menu (Update)")
                console.print("[3] Hapus Menu (Delete)")
                console.print("[0] Keluar ke Menu Utama\n")
                
                admin_pilihan = input(">> Pilih aksi admin: ").strip()

                if admin_pilihan == '1':
                    jenis = input("Jenis (Makanan Utama/Kopi/dll): ")
                    nama_menu = input("Nama Menu: ")
                    try:
                        harga = int(input("Harga: "))
                        stok = int(input("Stok: "))
                        daftar_menu.tambah_di_akhir(jenis, nama_menu, harga, stok)
                        antrean_kasir.simpan_data_ke_txt(daftar_menu, lokasi_file_txt)
                        console.print("[green]Berhasil ditambah![/green]")
                    except ValueError:
                        console.print("[red]Harga/Stok harus angka![/red]")
                    input("Tekan Enter...")
                
                elif admin_pilihan == '2': # FITUR UPDATE
                    nama_ubah = input("Masukkan nama menu yang ingin diubah: ").strip()
                    node = daftar_menu.cari_menu(nama_ubah)
                    if node:
                        console.print(f"Data saat ini -> Harga: {node.harga}, Stok: {node.stok}")
                        try:
                            hrg_baru = input("Harga baru (kosongkan jika tidak ingin diubah): ")
                            stk_baru = input("Stok baru (kosongkan jika tidak ingin diubah): ")
                            if hrg_baru: node.harga = int(hrg_baru)
                            if stk_baru: node.stok = int(stk_baru)
                            antrean_kasir.simpan_data_ke_txt(daftar_menu, lokasi_file_txt)
                            console.print("[green]Berhasil diubah![/green]")
                        except ValueError:
                            console.print("[red]Input harus angka![/red]")
                    else:
                        console.print("[red]Menu tidak ditemukan![/red]")
                    input("Tekan Enter...")
                
                elif admin_pilihan == '3': # FITUR DELETE
                    nama_hapus = input("Masukkan nama menu yang ingin dihapus: ").strip()
                    
                    # Logika Delete Linked List (Langsung di main atau oper ke Fardhan)
                    # Karena Fardhan belum buat, kita handle bypass di sini:
                    current = daftar_menu.head
                    prev = None
                    ditemukan = False
                    
                    while current:
                        if current.nama.lower() == nama_hapus.lower():
                            ditemukan = True
                            if prev: # Jika ada di tengah/akhir
                                prev.next = current.next
                            else: # Jika head yang dihapus
                                daftar_menu.head = current.next
                            break
                        prev = current
                        current = current.next
                        
                    if ditemukan:
                        antrean_kasir.simpan_data_ke_txt(daftar_menu, lokasi_file_txt)
                        console.print(f"[green]Menu '{nama_hapus}' berhasil dihapus![/green]")
                    else:
                        console.print("[red]Menu tidak ditemukan![/red]")
                    input("Tekan Enter...")

                elif admin_pilihan == '0':
                    break
        else:
            console.print("\n[red]Pilihan tidak valid.[/red]")
            input("Tekan Enter...")

if __name__ == "__main__":
    main()