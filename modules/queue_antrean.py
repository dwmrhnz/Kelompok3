import os
from rich.console import Console
from rich.panel import Panel

class QueuePesanan:
    """ Class buat urus antrean FIFO (First In First Out) pakai list Python. """
    
    def __init__(self):
        self.antrian = []  # list buat nampung antrean
        self.nomor_terakhir = 0  # nyimpen nomor terakhir biar auto-increment

    def ambil_antrean(self, nama_pelanggan, tipe_pesanan):
        """ Enqueue: masukin pelanggan baru ke antrean. """
        console = Console(highlight=False)
        self.nomor_terakhir += 1
        data_pelanggan = {
            "nomor": self.nomor_terakhir,
            "nama": nama_pelanggan,
            "tipe": tipe_pesanan
        }
        self.antrian.append(data_pelanggan)
        console.print(f"\n[[green]SUKSES[/green]] {nama_pelanggan} berhasil masuk antrean dengan nomor {self.nomor_terakhir} ({tipe_pesanan}).")

    def tampilkan_antrean(self):
        """ Intip isi antrean (siapa yang lagi dilayani, next siapa, total antrean). """
        console = Console(highlight=False)
        console.print("[bold cyan]--- STATUS ANTREAN ---[/bold cyan]")
        total_antrean = len(self.antrian)
        
        if total_antrean == 0:
            print("Antrean saat ini kosong.")
            return

        # ambil data index 0 (paling depan)
        sedang_dilayani = self.antrian[0]
        print(f"Sedang Dilayani : Nomor {sedang_dilayani['nomor']} - {sedang_dilayani['nama']} ({sedang_dilayani['tipe']})")

        # cek kalo masih ada antrean di belakangnya (index 1)
        if total_antrean > 1:
            berikutnya = self.antrian[1]
            print(f"Antrean Next    : Nomor {berikutnya['nomor']} - {berikutnya['nama']}")
        else:
            print("Antrean Next    : - (Tidak ada)")
            
        print(f"Total orang dalam antrean: {total_antrean}")

    def layani_pelanggan(self, menu_list):
        """ Dequeue & Transaksi: panggil pelanggan pertama terus proses orderannya. """
        console = Console(highlight=False)
        if len(self.antrian) == 0:
            console.print("\n[bold yellow][INFO] Tidak ada pelanggan dalam antrean untuk dilayani.[/bold yellow]")
            return

        # tahan index 0 (jangan di-pop dulu, ntar aja kalo udah fix bayar)
        pelanggan = self.antrian[0] 
        
        # tampilin menu UI dari object linked list
        menu_list.tampilkan_menu()
        
        console.print(f"\n[bold green]>>> MELAYANI PELANGGAN NOMOR: {pelanggan['nomor']} ({pelanggan['nama']} - {pelanggan['tipe']})[/bold green]")
        console.print("[italic cyan]*PENTING: Ketik nama menu sesuai dengan yang ada di daftar. Tekan ENTER kosong jika sudah selesai memesan.*[/italic cyan]\n")
        
        while True: # main loop buat 1 transaksi
            keranjang = []
            total_belanja = 0
            # dict buat track stok sementara biar kalo cancel, stok asli tetep aman
            stok_sementara = {} 

            while True: # loop pesen item per item
                pesanan = input("Kasir: 'Ingin pesan apa kak?' (Tekan ENTER untuk selesai): ").strip()
                
                if pesanan == '': # kalo user cuma teken enter brarti beres milih
                    break
                    
                hasil_pencarian = menu_list.cari_menu(pesanan)
                if hasil_pencarian is None:
                    console.print(f"[bold red][GAGAL] Maaf, menu '{pesanan}' tidak ditemukan. Cek ejaanmu![/bold red]")
                    continue
                    
                # cek stok sementara, kalo kosong ambil dari master data (database node)
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
                    
                # update keranjang & stok sementara
                stok_sementara[pesanan] = stok_saat_ini - jumlah_pesan
                subtotal = harga_menu * jumlah_pesan
                total_belanja += subtotal
                
                keranjang.append({
                    "menu": hasil_pencarian.nama,
                    "jumlah": jumlah_pesan,
                    "harga_satuan": harga_menu,
                    "subtotal": subtotal
                })
                console.print(f"[bold green] + Berhasil menambah {jumlah_pesan}x {hasil_pencarian.nama}[/bold green]\n")

            # --- FASE KONFIRMASI ---
            if not keranjang:
                console.print("[yellow][INFO] Pelanggan tidak memesan apa pun.[/yellow]")
                self.antrian.pop(0) # pop & buang pelanggan dari antrean
                break

            console.print("\n[bold cyan]--- REVIEW PESANAN ---[/bold cyan]")
            for item in keranjang:
                subtotal_format = f"Rp{item['subtotal']:,}".replace(",", ".")
                total_format = f"Rp{total_belanja:,}".replace(",", ".")
                console.print(f"- {item['menu']} (x{item['jumlah']}) : [yellow]{subtotal_format}[/yellow]")
            console.print(f"[bold yellow]TOTAL BAYAR: {total_format}[/bold yellow]")
            
            yakin = input("\nApakah pesanan sudah benar? (y/n): ").strip().lower()
            if yakin == 'y':
                # potong stok real di Linked List
                for item in keranjang:
                    menu_list.kurangi_stok(item['menu'], item['jumlah'])
                
                self.antrian.pop(0) # pesanan fix, buang dari list antrean
                self._cetak_struk(pelanggan, keranjang, total_belanja)
                self.simpan_data_ke_txt(menu_list)
                break
            else:
                console.print("[bold yellow]Baik, mari kita ulang pesanannya dari awal...[/bold yellow]\n")

    def _cetak_struk(self, pelanggan, keranjang, total_belanja):
        """ Pisah logic print struk biar kodingan lebih rapi & modular. """
        console = Console(highlight=False)
        
        # 1. Kumpulkan semua baris teks ke dalam satu variabel string (isi_struk)
        isi_struk = f"Pelanggan: {pelanggan['nama']} ({pelanggan['tipe']})\n"
        isi_struk += "-" * 44 + "\n"
        
        for item in keranjang:
            # format duit ke IDR
            h_satuan = f"Rp{item['harga_satuan']:,}".replace(",", ".")
            s_total = f"Rp{item['subtotal']:,}".replace(",", ".")
            isi_struk += f"{item['menu']} (x{item['jumlah']})\n"
            isi_struk += f"  @ {h_satuan:<15} {s_total}\n"
            
        isi_struk += "-" * 44 + "\n"
        total_format = f"Rp{total_belanja:,}".replace(",", ".")
        isi_struk += f"[bold green]TOTAL BAYAR: {total_format}[/bold green]\n"
        isi_struk += "-" * 44 + "\n"
        isi_struk += "       Terima kasih telah berkunjung!       "

        # 2. Bungkus string tadi ke dalam Panel berwarna putih
        struk_panel = Panel(
            isi_struk,
            title="[bold white] STRUK PEMBELIAN SARIAWAM [/bold white]",
            border_style="white", # Ubah warna garis panel jadi putih
            expand=False # Biar lebar panelnya pas ngikutin teks, ngga full layar terminal
        )
        
        # 3. Print panelnya ke layar
        console.print() # Print enter kosong biar ada jarak
        console.print(struk_panel)
        console.print()

    def simpan_data_ke_txt(self, menu_list, nama_file="data/menu.txt"):
        """ Rewrite database txt tiap kali beres transaksi. """
        console = Console(highlight=False)
        try:
            # narik semua string data terbaru dari method Linked List
            data_menu_terupdate = menu_list.ambil_semua_data()
            
            # overwrite isi file txt-nya (w flag)
            with open(nama_file, 'w', encoding='utf-8') as file:
                for item in data_menu_terupdate:
                    file.write(item + "\n")
                    
        except Exception as e:
            console.print(f"[[red]SISTEM ERROR[/red]] Terjadi kesalahan saat menyimpan file: {e}")