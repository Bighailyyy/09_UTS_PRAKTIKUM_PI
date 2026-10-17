"""Daftar stopword Bahasa Indonesia (+ sedikit Inggris) tanpa dependensi eksternal."""

STOPWORDS_ID = """
ada adalah adanya adapun agak agar akan akankah akhir akhirnya aku amat anda antar antara antaranya apa apaan apabila
apakah apalagi artinya asal asalkan atas atau ataukah ataupun awal awalnya bagai bagaikan bagaimana bagaimanakah
bagaimanapun bagi bagian bahkan bahwa bahwasanya banyak baik bapak baru bawah beberapa begini begitu begitulah bekerja
belakang belum belumlah benar benarkah berada berakhir berapa berarti berawal berbagai beri berikan berikut berikutnya
berjumlah berkata berlangsung bermacam bersama bersama-sama bertanya berupa besar betul biasa biasanya bila bisa
bisakah boleh bolehkah buat bukan bukankah bukanlah bukannya bulan bung cara caranya cukup cuma dahulu dalam dan dapat
dari daripada datang dekat demi demikian demikianlah dengan depan di dia diakhiri dialah diantara diantaranya diberi
diberikan dibuat dibuatnya didapat digunakan dijelaskan dikarenakan dikatakan dikerjakan diketahui dilakukan dilihat
dimaksud dimaksudkan diminta dimulai dini diperlukan dipunyai diri dirinya disampaikan disebut disebutkan ditambahkan
ditanya ditanyakan ditegaskan ditunjukkan diucapkan diungkapkan dong dua dulu empat enggak entah entahlah guna gunakan
hal hampir hanya hanyalah hari harus haruslah harusnya hendak hendaklah hendaknya hingga ia ialah ibarat ibu ikut ingat
ingin inginkah inginkan ini inikah inilah itu itukah itulah jadi jadilah jadinya jangan jangankan janganlah jauh jelas
jelaskan jelasnya jika jikalau juga jumlah jumlahnya justru kala kali kalian kalau kalaulah kalaupun kami kamilah kamu
kamulah kan kapan kapankah kapanpun karena karenanya kasus kata katakan katakanlah katanya ke keadaan kebetulan kecil
kedua keduanya keinginan kelima keluar kembali kemudian kemungkinan kenapa kepada kepadanya keseluruhan ketika khususnya
kini kira kira-kira kiranya kita kitalah kok kurang lagi lagian lah lain lainnya lalu lama lamanya lanjut lanjutnya
lebih lewat lima luar macam maka makanya makin malah malahan mampu mana manakala manalagi masa masalah masalahnya masih
masihkah masing masing-masing mau maupun melainkan melakukan melalui melihat melihatnya memang memastikan memberi
memberikan membuat memerlukan meminta mempergunakan memperkirakan mempersiapkan mempertanyakan mempunyai memulai
memungkinkan menambahkan menanyakan mendapat mendapatkan mendatang menegaskan mengakhiri mengapa mengatakan mengatakannya
mengenai mengerjakan mengetahui menggunakan menghendaki mengingat mengingatkan menginginkan mengira mengucapkan
mengungkapkan menjadi menjawab menjelaskan menuju menunjuk menunjukkan menurut menuturkan menyampaikan menyangkut
menyatakan menyebutkan menyeluruh menyiapkan merasa mereka merekalah merupakan meski meskipun meyakini minta mirip misal
misalkan misalnya mula mulai mulailah mulanya mungkin mungkinkah nah naik namun nanti nantinya nyaris nyatanya oleh
olehnya pada padahal padanya pak paling panjang pantas para pasti pastilah penting pentingnya per percuma perlu perlukah
perlunya pernah persoalan pertama pertama-tama pertanyaan pihak pihaknya pukul pula pun punya rasa rasanya rata rupanya
saat saatnya saja sajalah saling sama sama-sama sambil sampai sampai-sampai sampaikan sana sangat sangatlah satu saya
sayalah se sebab sebabnya sebagai sebagaimana sebagainya sebagian sebaik sebaiknya sebaliknya sebanyak sebegini sebegitu
sebelum sebelumnya sebenarnya seberapa sebesar sebetulnya sebisanya sebuah sebut sebutlah sebutnya secara secukupnya
sedang sedangkan sedemikian sedikit sedikitnya seenaknya segala segalanya segera seharusnya sehingga seingat sejak
sejauh sejenak sejumlah sekadar sekadarnya sekali sekali-kali sekalian sekaligus sekalipun sekarang sekitar sekitarnya
sekurang-kurangnya sekurangnya sela selain selaku selalu selama selama-lamanya selamanya selanjutnya seluruh seluruhnya
semacam semakin semampu semampunya semasa semasih semata semata-mata semaunya sementara semisal semisalnya sempat semua
semuanya semula sendiri sendirian sendirinya seolah seolah-olah seorang sepanjang sepantasnya seperlunya seperti
sepertinya sepihak sering seringnya serta serupa sesaat sesama sesampai sesegera sesekali seseorang sesuatu sesuatunya
sesudah sesudahnya setelah setempat setengah seterusnya setiap setiba setibanya setidak-tidaknya setidaknya setinggi
seusai sewaktu siap siapa siapakah siapapun sini sinilah soal soalnya suatu sudah sudahkah sudahlah supaya tadi tadinya
tahu tahun tak tambah tambahnya tampak tampaknya tandas tandasnya tanpa tanya tanyakan tanyanya tapi tegas tegasnya
telah tempat tengah tentang tentu tentulah tentunya tepat terakhir terasa terbanyak terdahulu terdapat terdiri terhadap
terhadapnya teringat terjadi terjadilah terjadinya terkira terlalu terlebih terlihat termasuk ternyata tersampaikan
tersebut tersebutlah tertentu tertuju terus terutama tetap tetapi tiap tiba tiba-tiba tidak tidakkah tidaklah tiga
tinggi toh tunjuk turut tutur tuturnya ucap ucapnya ujar ujarnya umum umumnya ungkap ungkapnya untuk usah usai waduh
wah wahai waktu waktunya walau walaupun wong yaitu yakin yakni yang
nya sih deh lho loh yah ya nih tuh
""".split()

STOPWORDS_EN = """
a an the and or of to in on at by for with from is are was were be been being this that these those it its as not no
""".split()

# Penanda sumber / boilerplate khas korpus berita (muncul di hampir semua dokumen)
STOPWORDS_CORPUS = """
com co id http https www html
""".split()

STOPWORDS = frozenset(STOPWORDS_ID) | frozenset(STOPWORDS_EN) | frozenset(STOPWORDS_CORPUS)
