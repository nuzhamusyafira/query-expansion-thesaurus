# Nama Kelompok
1. Nuzha Musyafira	05111640000014
2. Fadilla Sukma A.	05111640000024
3. Magdalena A. I.	05111640000112

# Judul Project
Aplikasi Pencarian Dokumen Referensi untuk Skripsi atau Tugas Akhir Berdasarkan Tesaurus 
Sinonim Kata Berbahasa Indonesia Guna Meningkatkan Kualitas dan Kuantitas Riset Nasional

# Petunjuk Manual Penggunaan dan Running Program
1. Install modul-modul atau library yang dibutuhkan, antara lain:
   - BeautifulSoup
   - urllib
   - Sastrawi
   - tqdm
   - sklearn
   - numpy
   - itertools
   - pandas
   - pickle
   - IPython

2. Untuk menjalankan source code pada folder Jupyter Notebook:
   a. Pastikan telah terinstall Jupyter Notebook dengan versi Python3.
   b. Terdapat 2 opsi pada folder Jupyter Notebook, yaitu: 
      - File main.ipynb berisi source code lengkap dengan pengambilan dan pengumpulan data
        untuk pencarian query.
      - Sedangkan pada file main-with-pickle.ipynb, pengguna tidak perlu mengumpulkan ulang 
        data karena data dapat langsung dimuat menggunakan library pickle.
   c. Untuk pemasukan keyword query, dapat dimodifikasi pada variable init_query yang telah
      disediakan.

3. Untuk menjalankan source code pada folder Python3:
   a. Pastikan versi yang digunakan merupakan Python3.
   b. Jalankan py get_documents.py untuk mengumpulkan dokumen. Input yang diminta adalah
      jumlah dokumen yang ingin di-scrap. Output dari proses ini yaitu file corpus dokumen 
      dalam format .xlsx dan .pkl.
   c. Jalankan py preprocess.py untuk melakukan praproses pada dokumen yang terkumpul   
      sebelumnya. Output dari proses ini yaitu file corpus dokumen hasil praproses dan 
      ekstraksi kata dalam format .xlsx dan .pkl.
   d. Jalankan py thesaurus.py untuk meng-generate thesaurus yang berdasarkan pada kata-  
      kata yang terdapat pada dokumen. Output dari proses ini yaitu file corpus thesaurus
      dalam format .xlsx dan .pkl.
   e. Jalankan py test_query untuk melakukan pengujian. Input yang diminta adalah keyword
      query. Output dari proses ini yaitu file corpus hasil pencarian baik dari query
      original mau pun query expansion dalam format .xlsx dan .pkl.