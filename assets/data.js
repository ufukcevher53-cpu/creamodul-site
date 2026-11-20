// Creamodul modül ve paket kataloğu. Fiyatlar KDV hariç, TL.
window.CM = {
  modules: [
    {
      id: "kafe", slug: "kafe-restoran-qr-siparis",
      name: "Kafe & Restoran: Ürün Oluşturucu",
      short: "Müşteri burgerini, waffle'ını ya da bowl'unu masadaki QR'dan kendisi oluşturur; sipariş anında kasaya düşer.",
      img: "burger.jpg",
      demos: [["Waffle demosu", "/demo/waffle/?masa=B1"], ["Burger demosu", "https://burger.creamodul.com"]],
      packages: [
        { id: "kafe-aylik", name: "Aylık Plan", setup: 6000, monthly: 1200, hl: true,
          features: ["Kendi ürünlerinize göre oluşturucu (burger, waffle, pizza, bowl…)", "Masa QR'ları ve masaya özel sipariş", "Kasa / mutfak ekranı, sesli uyarı", "Menü ekleme-çıkarma ve fiyat değişiklikleri bizden", "İlk ay ücretsiz"] },
        { id: "kafe-tek", name: "Tek Seferlik", setup: 18000, yearly: 3000,
          features: ["Aylık plandaki her şey", "Menüyü kendiniz yöneteceğiniz yönetici paneli", "Günlük stok / ürün açma-kapama", "İlk yıl bakım dahil, sonrası yıllık bakım"] }
      ],
      extras: [
        { id: "garson", name: "Garson çağır & hesap iste butonları", price: 1000 },
        { id: "gorsel", name: "Gerçekçi ürün görselleri (10 ürüne kadar)", price: 2500 },
        { id: "qrbaski", name: "Masa QR baskı tasarımı (10 masa)", price: 750 },
        { id: "yorum", name: "Sipariş sonrası Google yorum yönlendirmesi", price: 500 },
        { id: "alanadi", name: "Kendi alan adınıza bağlama", price: 750 }
      ],
      fields: [
        { id: "urun", label: "Hangi ürün için oluşturucu istiyorsunuz?", ph: "Örn. burger, waffle, pizza, bowl", req: true },
        { id: "masa", label: "Masa sayısı", type: "number", ph: "Örn. 12" },
        { id: "menu", label: "Menünüz", type: "textarea", ph: "Menü linkiniz ya da ürün listesi (ürün, fiyat)" }
      ]
    },
    {
      id: "cicek", slug: "cicekci-buket-olusturucu",
      name: "Çiçekçi: Buket Oluşturucu",
      short: "Müşteri çiçeklerini, yeşilliğini ve ambalajını seçer; buket ekranda oluşur, fiyat anında hesaplanır.",
      img: "cicek.jpg",
      demos: [],
      packages: [
        { id: "cicek-aylik", name: "Aylık Plan", setup: 6000, monthly: 1200, hl: true,
          features: ["Kendi çiçek ve ambalaj seçenekleriniz", "Anlık fiyat hesaplama", "Siparişler size anında düşer", "Ürün ve fiyat güncellemeleri bizden", "İlk ay ücretsiz"] },
        { id: "cicek-tek", name: "Tek Seferlik", setup: 18000, yearly: 3000,
          features: ["Aylık plandaki her şey", "Ürünleri kendiniz yöneteceğiniz panel", "İlk yıl bakım dahil"] }
      ],
      extras: [
        { id: "gorsel", name: "Gerçekçi çiçek görselleri (15 çeşide kadar)", price: 2500 },
        { id: "alanadi", name: "Kendi alan adınıza bağlama", price: 750 },
        { id: "not", name: "Kart notu ve teslim saati seçimi", price: 750 }
      ],
      fields: [
        { id: "cesit", label: "Satılan çiçek çeşitleri", type: "textarea", ph: "Örn. gül, lale, papatya, orkide… (fiyatlarıyla)" },
        { id: "teslim", label: "Teslimat yapıyor musunuz?", ph: "Örn. Evet, ilçe içi" }
      ]
    },
    {
      id: "yorum", slug: "google-yorum-karti",
      name: "Google Yorum QR Kartı",
      short: "Kasaya ya da masaya koyduğunuz kart, müşteriyi tek okutmayla doğrudan sizin Google yorum ekranınıza götürür.",
      img: "yorum.jpg",
      demos: [],
      packages: [
        { id: "yorum-dijital", name: "Dijital", setup: 750,
          features: ["Markanıza özel kart tasarımı", "Doğrudan yorum ekranını açan QR", "Baskıya hazır dosya (PDF)", "Kart, masa standı ve sticker boyutları"] },
        { id: "yorum-baskili", name: "Baskılı", setup: 1500, hl: true,
          features: ["Dijital paketteki her şey", "20 adet baskılı kart", "Kargo dahil"] }
      ],
      extras: [
        { id: "ekkart", name: "+20 baskılı kart", price: 600 },
        { id: "stand", name: "Masa standı tasarımı + 5 baskı", price: 750 }
      ],
      fields: [
        { id: "glink", label: "Google işletme profilinizin linki ya da tam adı", ph: "Google Haritalar'daki adınız", req: true },
        { id: "adres", label: "Baskılı paket için teslimat adresi", type: "textarea", ph: "Sadece baskılı pakette gerekli" }
      ]
    },
    {
      id: "anatomi", slug: "3d-anatomi-klinik",
      name: "3D Anatomi: Klinikler İçin Video",
      short: "Hastalıkların vücutta nasıl geliştiğini gösteren, kliniğinizin logolu 3D videoları. Instagram ve hasta bilgilendirme için.",
      img: "anatomi.jpg",
      demos: [["3D anatomi demosu", "https://anatomi.creamodul.com"]],
      packages: [
        { id: "anatomi-video", name: "Tek Video", setup: 1500,
          features: ["20–30 saniyelik dikey 3D video", "Kliniğinizin logosu ve renkleri", "Listedeki hastalıklardan biri", "Instagram / TikTok formatında"] },
        { id: "anatomi-aylik", name: "Aylık 4 Video", monthly: 5000, hl: true,
          features: ["Her ay 4 logolu 3D video", "Hastalık seçimini siz yaparsınız", "Gönderi metinleri dahil", "İstediğiniz zaman bırakın"] },
        { id: "anatomi-sayfa", name: "Kliniğe Özel Anatomi Sayfası", setup: 5000, monthly: 750,
          features: ["Logolu, kliniğinize özel 3D anatomi sayfası", "Hastaya QR / link ile gönderme", "Uzmanlığınıza göre hastalık seçkisi", "Ayda 1 yeni hastalık ekleme"] }
      ],
      extras: [
        { id: "yeni", name: "Listede olmayan hastalık / işlem animasyonu", price: 3000 },
        { id: "ses", name: "Türkçe seslendirme (video başına)", price: 750 }
      ],
      fields: [
        { id: "uzmanlik", label: "Uzmanlık alanı", ph: "Örn. ortopedi, kardiyoloji, diş", req: true },
        { id: "hastalik", label: "Hangi hastalıklar / işlemler?", type: "textarea", ph: "Örn. bel fıtığı, menisküs yırtığı" }
      ]
    }
  ],
  fmt(n) { return n.toLocaleString("tr-TR") + " TL"; }
};
