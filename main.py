import os
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from modules.linkedlist_menu import LinkedListMenu
from modules.queue_antrean import QueuePesanan

console = Console()

def bersihkan_layar():
    """ Fungsi helper buat clear screen terminal. """
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # inisialisasi object list & queue
    daftar_menu = LinkedListMenu()
    antrean_kasir = QueuePesanan()

    # error handling kalo folder data belum ada
    if not os.path.exists('data'):
        os.makedirs('data')

    # load data menu awal dari txt ke memori (linked list)
    lokasi_file_txt = "data/menu.txt"
    daftar_menu.muat_dari_txt(lokasi_file_txt)

    while True: # main loop aplikasi
        bersihkan_layar()
        
        # render UI panel judul pake library rich
        judul = Panel(
            Align.center("[bold yellow]SELAMAT DATANG DI RESTORAN SARIAWAM[/bold yellow]\n[italic white]Fardhan - Hirzi - Dawam[/italic white]"),
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
            while True: # nested loop buat sub-menu menu
                bersihkan_layar()
                daftar_menu.tampilkan_menu()
                
                console.print("\n[bold cyan]-- Opsi Menu --[/bold cyan]")
                console.print("[1] Cari Hidangan (Ketik Nama)")
                console.print("[2] Urutkan Harga Termahal - Termurah")
                console.print("[3] Urutkan Harga Termurah - Termahal")
                console.print("[4] Kembali ke Layanan Utama")
                
                opsi_menu = input(">> Pilih opsi: ").strip()
                
                if opsi_menu == '1':
                    kata = input("Masukkan kata kunci pencarian: ").strip()
                    hasil = daftar_menu.cari_menu_sebagian(kata)
                    console.print(f"\n[bold green]Hasil Pencarian untuk '{kata}':[/bold green]")
                    if hasil:
                        for h in hasil:
                            # format value integer ke string IDR
                            harga_format = f"Rp{h.harga:,}".replace(",", ".")
                            console.print(f"- {h.nama} ([yellow]{harga_format}[/yellow])")
                    else:
                        console.print("[red]Menu tidak ditemukan.[/red]")
                    input("\nTekan Enter untuk melanjutkan...")
                    
                elif opsi_menu == '2':
                    daftar_menu.urutkan_harga(ascending=False) # sort desc (termahal)
                    console.print("[green]Menu telah diurutkan dari yang termahal.[/green]")
                    input("Tekan Enter untuk melihat...")
                    
                elif opsi_menu == '3':
                    daftar_menu.urutkan_harga(ascending=True) # sort asc (termurah)
                    console.print("[green]Menu telah diurutkan dari yang termurah.[/green]")
                    input("Tekan Enter untuk melihat...")
                    
                elif opsi_menu == '4':
                    break # exit sub-menu
                    
        elif pilihan == '2':
            bersihkan_layar()
            console.print("[bold cyan]--- AMBIL NOMOR ANTREAN ---[/bold cyan]")
            nama = input("Masukkan Nama Anda: ").strip()
            if nama:
                console.print("Pilih Tipe: [1] Dine-in  [2] Takeaway")
                tipe_input = input("Pilihan (1/2): ").strip()
                # set default string pake ternary operator
                tipe = "Takeaway" if tipe_input == '2' else "Dine-in"
                antrean_kasir.ambil_antrean(nama, tipe) # hit function enqueue
            input("\nTekan Enter kembali...")

        elif pilihan == '3':
            bersihkan_layar()
            antrean_kasir.tampilkan_antrean()
            input("\nTekan Enter kembali...")

        elif pilihan == '4':
            bersihkan_layar()
            antrean_kasir.layani_pelanggan(daftar_menu) # hit function dequeue
            input("\nTekan Enter kembali...")

        elif pilihan == '5':
            bersihkan_layar()
            console.print("[bold green]Terima kasih telah berkunjung ke Sariawam. Sampai jumpa![/bold green]")
            break

        # secret code buat masuk backdoor admin
        elif pilihan == '67':
            while True: # nested loop buat menu admin (CRUD)
                bersihkan_layar()
                admin_panel = Panel(Align.center("[bold red]*** MODE ADMIN SARIAWAM ***[/bold red]"), width=65)
                console.print(admin_panel)
                console.print("[1] Tambah Menu Baru (Create)")
                console.print("[2] Ubah Harga/Stok Menu (Update)")
                console.print("[3] Hapus Menu (Delete)")
                console.print("[4] Keluar ke Menu Utama\n")
                
                admin_pilihan = input(">> Pilih aksi admin: ").strip()

                if admin_pilihan == '1': # CREATE
                    jenis = input("Jenis (Makanan Utama/Kopi/dll): ")
                    nama_menu = input("Nama Menu: ")
                    try:
                        # validasi input pake try-except biar ga crash kalo diinput huruf
                        harga = int(input("Harga: "))
                        stok = int(input("Stok: "))
                        daftar_menu.tambah_di_akhir(jenis, nama_menu, harga, stok)
                        antrean_kasir.simpan_data_ke_txt(daftar_menu, lokasi_file_txt)
                        console.print("[green]Berhasil ditambah![/green]")
                    except ValueError:
                        console.print("[red]Harga/Stok harus angka![/red]")
                    input("Tekan Enter...")
                
                elif admin_pilihan == '2': # UPDATE
                    nama_ubah = input("Masukkan nama menu yang ingin diubah: ").strip()
                    node = daftar_menu.cari_menu(nama_ubah)
                    if node: # ngecek kalo nodenya beneran ada
                        console.print(f"Data saat ini -> Harga: {node.harga}, Stok: {node.stok}")
                        try:
                            hrg_baru = input("Harga baru (kosongkan jika tidak ingin diubah): ")
                            stk_baru = input("Stok baru (kosongkan jika tidak ingin diubah): ")
                            # update value node kalo input ga kosong
                            if hrg_baru: node.harga = int(hrg_baru)
                            if stk_baru: node.stok = int(stk_baru)
                            
                            antrean_kasir.simpan_data_ke_txt(daftar_menu, lokasi_file_txt)
                            harga_skrg = f"Rp{node.harga:,}".replace(",", ".")
                            console.print("[green]Berhasil diubah![/green]")
                            console.print(f"Data saat ini -> Harga: [yellow]{harga_skrg}[/yellow], Stok: {node.stok}")
                        except ValueError:
                            console.print("[red]Input harus angka![/red]")
                    else:
                        console.print("[red]Menu tidak ditemukan![/red]")
                    input("Tekan Enter...")
                
                elif admin_pilihan == '3': # DELETE
                    nama_hapus = input("Masukkan nama menu yang ingin dihapus: ").strip()
                    
                    # manual traversal buat delete node
                    current = daftar_menu.head
                    prev = None
                    ditemukan = False
                    
                    while current:
                        if current.nama.lower() == nama_hapus.lower():
                            ditemukan = True
                            if prev: # target ada di tengah/belakang list
                                prev.next = current.next # bypass / unlink node
                            else: # target itu head-nya sendiri
                                daftar_menu.head = current.next
                            break
                        prev = current
                        current = current.next
                        
                    if ditemukan:
                        # write ulang ke txt kalo berhasil kehapus
                        antrean_kasir.simpan_data_ke_txt(daftar_menu, lokasi_file_txt)
                        console.print(f"[green]Menu '{nama_hapus}' berhasil dihapus![/green]")
                    else:
                        console.print("[red]Menu tidak ditemukan![/red]")
                    input("Tekan Enter...")

                elif admin_pilihan == '4':
                    break # exit backdoor
        else:
            console.print("\n[red]Pilihan tidak valid.[/red]")
            input("Tekan Enter...")

if __name__ == "__main__":
    main()