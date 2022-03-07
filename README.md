# Tugas 01 Pemrograman Jaringan 


Buatlah program klien server dengan spesifikasi sebagai berikut:
Klien:
- Meminta ke server untuk mengunduh salah satu file pada folder dataset (*.html, *.mp3, *.mp4, *.png, dan *.txt) dengan cara mengirim string: `unduh nama_file`. Ukuran file lebih dari 1 MB.
- Menerima isi file dari server
- Melakukan parsing message header. Message header tidak ikut ditulis ke dalam file
- Isi file yang telah diterima dari server, disimpan dalam sebuah file sesuai ekstensi filenya.

Server:
- Menerima pesan berupa `unduh nama_file`
- Membaca file yang diminta oleh klien
- Menambahkan message header yang diletakkan sebelum isi file dengan struktur sebagai berikut (contoh raw message header):
	file-name: contoh.html,\n
	
	file-size: 2048,\n
	
	\n\n
- Mengirim isi file yang telah dibaca ke klien
- Server dapat menangani banyak klien (gunakan modul select DAN serversocket pada Python).

Challenge:
- Membaca/menulis file dalam mode biner.
- Mengirim/menerima file yang ukurannya lebih besar daripada buffer pada socket (gunakan loop untuk send/recv).
- Menggunakan virtual box untuk simulasi dua host atau lebih.

Struktur folder:
- nrp1_nrp2
	- client
		- client_select.py
		- client_serversocket.py
	- server
		- server_select.py
		- server_serversocket.py
		- dataset
