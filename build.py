import json, html, os
BASE = "https://creamodul.com"
ROOT = os.path.dirname(os.path.abspath(__file__))
MODS = json.load(open(os.path.join(ROOT, "assets", "catalog.json")))
E = html.escape

def fmt(n): return f"{n:,}".replace(",", ".") + " TL"
def price_line(p):
    a = []
    if p.get("setup"): a.append(fmt(p["setup"]) + (" kurulum" if p.get("monthly") or p.get("yearly") else ""))
    if p.get("monthly"): a.append(fmt(p["monthly"]) + " / ay")
    if p.get("yearly"): a.append(fmt(p["yearly"]) + " / yıl bakım")
    return " + ".join(a)
def start_price(m):
    p = min(m["packages"], key=lambda p: p.get("setup") or p.get("monthly") or 0)
    if p.get("setup") and p.get("monthly"): return fmt(p["setup"]), "kurulum + " + fmt(p["monthly"]) + " / ay"
    if p.get("setup"): return fmt(p["setup"]), "tek seferlik"
    return fmt(p["monthly"]), "aylık"
def title_of(m): return m["name"].split(":", 1)[-1].strip()
def sector_of(m): return m["name"].split(":")[0]

LOGO = '<i aria-hidden="true"><b></b><b></b><b></b><b></b></i>creamodul'
def page(path, title, desc, body, extra_head="", noindex=False, scripts=""):
    url = BASE + path
    out = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">{'<meta name="robots" content="noindex,nofollow">' if noindex else ''}
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/assets/img/og.jpg"><meta property="og:locale" content="tr_TR">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#F7F8FA">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700&family=Unbounded:wght@500;600&display=swap">
<link rel="stylesheet" href="/assets/style.css?v=6">{extra_head}</head><body>
<header class="top"><div class="w"><a class="logo" href="/" aria-label="Creamodul ana sayfa">{LOGO}</a>
<nav class="mn" aria-label="Ana menü"><a class="hm" href="/yapabildiklerimiz/">Yapabildiklerimiz</a><a class="hm" href="/#moduller">Modüller</a><a class="hm" href="/#surec">Süreç</a><a class="hm" href="/#sss">Sorular</a><a class="btn sm" href="/siparis/">Sipariş ver</a></nav></div></header>
<main>{body}</main>
<footer><div class="w"><div><a class="logo" href="/">{LOGO}</a><p>İşletmelere hazır dijital modüller. Paketinizi seçin, bilgilerinizi verin; 4–5 iş gününde kurup teslim edelim.</p></div>
<div><b>Modüller</b>{''.join(f'<a href="/moduller/{m["slug"]}/">{E(title_of(m))}</a>' for m in MODS)}</div>
<div><b>İletişim</b><a href="https://www.instagram.com/creamodul/" rel="noopener">Instagram: @creamodul</a><a href="/siparis/?modul=ozel">Özel modül talebi</a><a href="/kvkk/">KVKK aydınlatma metni</a></div>
<div class="cp">© 2026 Creamodul</div></div></footer>{scripts}</body></html>"""
    if path.endswith(".html"):
        open(os.path.join(ROOT, path.strip("/")), "w").write(out); return
    d = os.path.join(ROOT, path.strip("/")); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)

def jsonld(o): return f'<script type="application/ld+json">{json.dumps(o, ensure_ascii=False)}</script>'
ORG = {"@context": "https://schema.org", "@type": "Organization", "name": "Creamodul", "url": BASE, "logo": BASE + "/assets/img/og.jpg",
       "sameAs": ["https://www.instagram.com/creamodul/"], "description": "İşletmeler için hazır dijital modüller: ürün oluşturucu, buket oluşturucu, Google yorum kartı, 3D anatomi videoları."}

TILE_IMG = {"kafe": "burger.jpg", "cicek": "foto-cicek.jpg", "yorum": "yorum.jpg", "anatomi": "anatomi.jpg"}
rack = "".join(f'<a class="tile {m["id"]}{" photo" if m["id"]=="cicek" else ""}" href="/moduller/{m["slug"]}/"><span>{E(title_of(m))}</span><img src="/assets/img/{TILE_IMG[m["id"]]}" alt=""></a>' for m in MODS)
rows = ""
for m in MODS:
    if m["id"] == "kafe": continue
    pr, suf = start_price(m)
    demo = f'<a class="btn gh sm" href="{m["demos"][0][1]}" target="_blank" rel="noopener">Demoyu aç</a>' if m["demos"] else ""
    rows += f"""<div class="row-m"><div class="sw {m['id']}"><img src="/assets/img/{TILE_IMG[m['id']]}" alt=""></div>
<div><h3><a href="/moduller/{m['slug']}/" style="text-decoration:none">{E(title_of(m))}</a></h3><p>{E(m['short'])}</p></div>
<div class="price"><small>başlangıç</small><b>{pr}</b><small>{suf}</small></div>
<div class="acts">{demo}<a class="btn sm" href="/moduller/{m['slug']}/">Paketler</a></div></div>"""
rows += """<div class="row-m"><div class="sw ozel"></div><div><h3>Sektörünüze özel modül</h3><p>Aklınızdaki fikri yazın. İşletmenize özel modülü tasarlayıp kuralım.</p></div>
<div class="price"><small>fiyat</small><b>Teklif</b></div><div class="acts"><a class="btn sm" href="/siparis/?modul=ozel">Talep gönder</a></div></div>"""
KAFE = next(m for m in MODS if m["id"] == "kafe")
KDEMO = KAFE["demos"][0][1] if KAFE["demos"] else "/moduller/" + KAFE["slug"] + "/"
faq = [("Teslim ne kadar sürer?", "Ödeme onayından sonra 4–5 iş günü içinde kurulumu tamamlayıp linklerinizi ve QR'larınızı teslim ediyoruz."),
       ("Kurulum için yanınıza gelmeniz gerekiyor mu?", "Hayır. Her şey uzaktan kuruluyor. Size linkler, QR dosyaları ve kısa bir kullanım anlatımı gönderiyoruz."),
       ("Sipariş verdikten sonra ne oluyor?", "Siparişiniz bize düşer ve size bir sipariş numarası verilir. 1 iş günü içinde sizi arayıp detayları netleştiririz, ödeme bilgilerini paylaşırız. Ödemeden sonra kurulum başlar."),
       ("Ödeme nasıl yapılıyor?", "Havale veya EFT ile, faturalı. Aylık planlarda ilk ay ücretsizdir."),
       ("Teknik bilgim yok, kullanabilir miyim?", "Evet. Müşteriniz QR'ı okutur, sipariş ekranınıza düşer. Aylık planlarda menü ve fiyat değişikliklerini biz yapıyoruz."),
       ("İşletmeme özel bir şey istiyorum.", "Sipariş sayfasında “Sektörüme özel modül”ü seçip fikrinizi yazın, size özel teklif hazırlayalım.")]
FAQLD = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
CHIPS = "".join(f'<span class="cx"><i class="dot {c}"></i>{E(t)}</span>' for t, c in [("Ürün oluşturucu ile sipariş","kafe"),("QR menü","kafe"),("Alerjen ve kalori bilgili menü","kafe"),("Tezgâh ekranı, garson çağırma","kafe"),("Google yorum kartı","yorum"),("İşletme web sitesi","yorum"),("Reklam filmi","cicek"),("Gerçekçi ürün görselleri","cicek"),("Sosyal medya gönderileri","cicek"),("Size özel modül","anatomi")])
body = f"""<section class="hero kh"><div class="w"><div>
<p class="eyebrow">Kafe, burgerci ve tatlıcılar için sipariş modülü</p>
<h1>Siparişi müşteri kendisi oluştursun.</h1>
<p class="lead">Müşteri waffle'ını, burgerini ya da tatlısını masadaki telefondan adım adım kendisi oluşturur; sipariş yazıldığı gibi tezgâha düşer. Yanlış sipariş biter, hesap büyür.</p>
<div class="cta"><a class="btn br" href="/siparis/?modul=kafe">Kafem için başvur</a><a class="btn gh" href="#video">Videoyu izle</a></div>
<ul class="facts"><li>4–5 iş gününde kurulum</li><li>İlk ay ücretsiz</li><li>Menünüzü biz giriyoruz</li></ul></div>
<div class="phones"><div class="phone p2"><img src="/assets/img/burger.jpg" alt="Burger oluşturucu ekranı" loading="lazy"></div><div class="phone"><video src="/assets/vid/olusturucu.mp4" poster="/assets/vid/olusturucu.jpg" autoplay muted loop playsinline aria-label="Müşterinin waffle'ını adım adım oluşturduğu ekran"></video></div></div></div></section>
<section id="video" class="alt"><div class="w split"><div class="vid"><video src="/assets/vid/reklam.mp4" poster="/assets/vid/reklam.jpg" controls playsinline preload="none"></video></div>
<div><h2>“Çilek olmasın” dedin. Duyan olmadı.</h2><p class="lead">Her kafede her gün yaşanıyor. Sebebi garson değil, sipariş yolunun kendisi:</p>
<ol class="why"><li><b>Gürültü ve acele.</b> Kalabalık saatte sipariş yarım duyulur.</li><li><b>Kâğıttaki kısaltmalar.</b> “Wfl çkl çlk-” mutfakta herkes aynı okumaz.</li><li><b>Ekstralar ve değişiklikler.</b> “Sosu ayrı, fıstık bol” fişe sığmaz, akılda kalmaz.</li></ol>
<p class="lead" style="margin-top:18px"><b style="color:var(--ink)">Çözüm:</b> sipariş müşteriden doğrudan ekrana. Arada kulak, kâğıt, hafıza yok.</p></div></div></section>
<section id="nasil"><div class="w"><div class="sh"><h2>Nasıl çalışır?</h2><p>Müşteriniz hiçbir uygulama indirmez. Masadaki kodu okutur, gerisi ekranda. Oluşturucu sizin ürünlerinize göre kurulur.</p></div>
<div class="how"><figure><img src="/assets/img/burger_sec.jpg" alt="Burger oluşturucuda et seçimi" loading="lazy"><figcaption><b>1. Seçer</b>Et, malzeme, sos; hamur, çikolata, meyve. Ne istemiyorsa seçmez.</figcaption></figure>
<figure><img src="/assets/img/waffle4.jpg" alt="Çikolata ve meyve eklenmiş waffle" loading="lazy"><figcaption><b>2. Görür</b>Her seçimde ürün ekranda gözünün önünde oluşur, fiyat anında hesaplanır.</figcaption></figure>
<figure><img src="/assets/img/siparis_kart.jpg" alt="Tezgâh ekranına düşen sipariş" loading="lazy"><figcaption><b>3. Sipariş verir</b>Sipariş masa numarasıyla tezgâh ekranına düşer; yazıldığı gibi.</figcaption></figure></div>
<div class="prods"><h3>Hangi ürün olursa olsun</h3><div class="pr-row">
<a class="prc" href="/demo/waffle/?masa=B1" target="_blank" rel="noopener"><img src="/assets/img/waffle6.jpg" alt="Waffle" loading="lazy"><span><b>Waffle &amp; tatlı</b>Demoyu dene</span></a>
<a class="prc" href="https://burger.creamodul.com" target="_blank" rel="noopener"><img src="/assets/img/burger_kare.jpg" alt="Burger" loading="lazy"><span><b>Burger</b>Demoyu dene</span></a>
<a class="prc ph" href="/siparis/?modul=kafe"><div class="ic">+</div><span><b>Sizin ürününüz</b>Bowl, pizza, krep, kahve, dürüm…</span></a></div></div>
<div class="kpk"><div><h3>Kafe &amp; Restoran paketi</h3><p>Kendi ürünlerinize göre oluşturucu, masa kodları, tezgâh ekranı, garson çağırma ve hesap isteme. Menü değişikliklerini biz yaparız.</p></div>
<div class="kp"><small>kurulum</small><b>6.000 TL</b><small>+ 1.200 TL / ay · ilk ay ücretsiz · KDV hariç</small></div>
<div class="acts"><a class="btn br" href="/moduller/{KAFE['slug']}/">Paketleri gör</a></div></div></div></section>
<section id="yap"><div class="w"><div class="sh"><h2>Sadece sipariş değil</h2><p>QR menüden reklam filmine, işletmenizin dijital tarafını tek elden kuruyoruz.</p></div><div class="chipsx">{CHIPS}</div><div style="margin-top:22px"><a class="btn br" href="/yapabildiklerimiz/">Yapabildiklerimizin hepsi</a></div></div></section>
<section id="moduller" class="alt"><div class="w"><div class="sh"><h2>Diğer sektörler</h2><p>Aynı yaklaşım başka işletmeler için de hazır.</p></div><div class="cat">{rows}</div></div></section>
<section id="surec"><div class="w"><div class="sh"><h2>Siparişten teslime</h2><p>Kurulum için yanınıza gelmemiz gerekmiyor; her adım uzaktan ilerliyor.</p></div>
<div class="steps"><div class="st"><h3>Paketi seçin</h3><p>Demoyu deneyin, paketinizi ve ekstralarınızı seçin.</p></div>
<div class="st"><h3>Formu doldurun</h3><p>İşletme bilgileriniz ve menünüz ya da ürünleriniz. Sipariş numaranız oluşur.</p></div>
<div class="st"><h3>Görüşme ve ödeme</h3><p>1 iş günü içinde sizi arar, detayları netleştiririz. Ödeme havale / EFT ile.</p></div>
<div class="st"><h3>Kurulum ve teslim</h3><p>4–5 iş gününde linkleriniz, QR'larınız ve kullanım anlatımı hazır.</p></div></div></div></section>
<section id="sss" class="alt"><div class="w" style="max-width:840px"><div class="sh"><h2>Sık sorulan sorular</h2></div>
{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q,a in faq)}
<div style="display:flex;gap:12px;margin-top:32px;flex-wrap:wrap"><a class="btn br" href="/siparis/">Sipariş ver</a><a class="btn gh" href="https://www.instagram.com/creamodul/" rel="noopener">Instagram'dan yazın</a></div></div></section>"""
page("/", "Creamodul | Kafe ve tatlıcılar için sipariş modülü: müşteri ürününü kendisi oluşturur",
     "Müşteri waffle'ını, burgerini, tatlısını masadaki telefondan kendisi oluşturur; sipariş yazıldığı gibi tezgâha düşer. Yanlış sipariş biter. 4–5 iş gününde uzaktan kurulum, ilk ay ücretsiz.",
     body, jsonld(ORG) + jsonld(FAQLD))

DESC = {
 "kafe": ("Kafe ve restoranlar için ürün oluşturucu | Creamodul", "Müşteriniz burgerini, waffle'ını masadaki QR'dan kendisi oluştursun; sipariş anında kasaya düşsün. Aylık 1.200 TL'den başlayan paketler, 4–5 günde kurulum.",
          ["Müşteri ürününü adım adım kendisi oluşturur; ürün ekranda gözünün önünde hazırlanır.", "Fiyat seçtikçe anında hesaplanır, yanlış sipariş ve uzun açıklamalar biter.", "Her masanın kendi QR'ı var; sipariş masa numarasıyla kasaya ya da mutfağa düşer.", "Kasada sesli uyarı: onay bekleyen sipariş varken susmaz.", "Boş masadan gelen ilk sipariş onaya düşer; dışarıdan QR fotoğrafıyla sipariş verilemez.", "Menü Google'da çıkmaz, sadece masadaki QR ile açılır."], ["burger.jpg","waffle.jpg"]),
 "cicek": ("Çiçekçiler için buket oluşturucu | Creamodul", "Müşteriniz buketini çiçek çiçek kendisi oluştursun; fiyat anında hesaplansın, sipariş size düşsün. Çiçekçilere özel dijital modül.",
          ["Müşteri çiçeklerini, yeşilliğini, ambalajını ve kurdelesini seçer.", "Buket ekranda oluşur, fiyat seçtikçe hesaplanır.", "“Şundan üç tane, bundan iki tane” mesajlaşması biter; sipariş net gelir.", "Aynı yapı pastane, çikolatacı ve hediye kutusu için de kurulabilir."], ["cicek.jpg"]),
 "yorum": ("Google yorum QR kartı: daha çok Google yorumu alın | Creamodul", "Kasaya veya masaya koyduğunuz markalı QR kart, müşteriyi tek okutmayla Google yorum ekranınıza götürür. 750 TL'den başlayan fiyatlarla.",
          ["Müşteri kamerasıyla okutur; doğrudan sizin yorum ekranınız açılır.", "Arama, sayfa bulma, buton arama adımları ortadan kalkar.", "Markanıza özel tasarım; kart, masa standı ve sticker boyutları.", "Ödül ya da indirim karşılığı değil; Google kurallarına uygun."], ["yorum.jpg"]),
 "anatomi": ("Klinikler için 3D anatomi videoları ve hasta bilgilendirme | Creamodul", "Hastalıkların vücutta nasıl geliştiğini gösteren, kliniğinizin logolu 3D videoları. Instagram içeriği ve hasta bilgilendirme için. Tek video 1.500 TL.",
          ["Hastalığın sağlıklı halden adım adım nasıl geliştiği 3D olarak gösterilir.", "Kliniğinizin logosu ve renkleriyle, Instagram / TikTok formatında.", "Kalp, akciğer, beyin, karın organları ve omurgada 25+ hastalık hazır.", "Hastaya QR veya link ile gönderebileceğiniz kliniğe özel anatomi sayfası.", "Bilgilendirme amaçlıdır; tanı veya tedavi önerisi içermez."], ["anatomi.jpg","anatomi2.jpg"]),
}
for m in MODS:
    t, d, feats, imgs = DESC[m["id"]]
    pk = ""
    for p in m["packages"]:
        big = fmt(p.get("setup") or p.get("monthly")); suf = "" if p.get("setup") else "<small> / ay</small>"
        pk += f"""<div class="pc{' hl' if p.get('hl') else ''}">{'<span class="tag">En çok tercih edilen</span>' if p.get('hl') and len(m['packages'])>1 else ''}<h3>{E(p['name'])}</h3>
<div class="pr">{big}{suf}</div><div class="pr2">{E(price_line(p))} · KDV hariç</div>
<ul>{''.join(f'<li>{E(f)}</li>' for f in p['features'])}</ul><a class="btn{' br' if p.get('hl') else ''}" href="/siparis/?paket={p['id']}">Bu paketle sipariş ver</a></div>"""
    ex = "".join(f'<div class="ex"><span>{E(e["name"])}</span><b>+{fmt(e["price"])}</b></div>' for e in m["extras"])
    demos = "".join(f'<a class="btn gh" href="{u}" target="_blank" rel="noopener">{E(n)}</a>' for n, u in m["demos"])
    stage = "".join(f'<img src="/assets/img/{i}" alt="{E(title_of(m))} ekran görüntüsü">' for i in imgs[:2])
    body = f"""<section class="hero mhero"><div class="w"><div><div class="crumb"><a href="/">Ana sayfa</a> / <a href="/#moduller">Modüller</a> / {E(sector_of(m))}</div>
<h1>{E(title_of(m))}</h1><p class="lead">{E(m['short'])}</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:28px"><a class="btn br" href="#paketler">Paketleri gör</a>{demos}</div></div>
<div class="stage {m['id']}">{stage}</div></div></section>
<section class="alt"><div class="w"><div class="sh"><h2>Neler sunuyor?</h2></div><ul class="feat">{''.join(f'<li>{E(f)}</li>' for f in feats)}</ul></div></section>
<section id="paketler"><div class="w"><div class="sh"><h2>Paketler</h2><p>Fiyatlara KDV dahil değildir. Ödeme onayından sonra 4–5 iş gününde teslim.</p></div><div class="pk">{pk}</div>
<h3 style="margin-top:48px">İsteğe bağlı ekstralar</h3><p class="mute sm">Sipariş formunda seçebilirsiniz.</p><div class="extras">{ex}</div></div></section>"""
    offers = [{"@type": "Offer", "name": p["name"], "price": p.get("setup") or p.get("monthly"), "priceCurrency": "TRY"} for p in m["packages"]]
    ld = {"@context": "https://schema.org", "@type": "Service", "name": m["name"], "description": d, "provider": {"@type": "Organization", "name": "Creamodul", "url": BASE}, "areaServed": "TR", "offers": offers}
    page(f"/moduller/{m['slug']}/", t, d, body, jsonld(ld))

body = """<section style="padding-top:48px"><div class="w"><div id="formWrap"><div class="sh"><h1 style="font-size:clamp(32px,4.4vw,48px)">Siparişinizi oluşturun</h1><p>Paketinizi ve ekstralarınızı seçin, bilgilerinizi verin. Sipariş oluşturmak ödeme yapmak değildir; önce sizi arayıp detayları netleştiririz.</p></div>
<form id="frm" class="ord" novalidate><div>
<div class="box"><h3><i>1</i>Modül</h3><div class="opts" id="mods"></div></div>
<div class="box hidden" id="bPkg"><h3><i>2</i>Paket</h3><div class="opts" id="pkgs"></div></div>
<div class="box hidden" id="bExt"><h3><i>3</i>Ekstralar <span class="mute sm" style="font-family:var(--body);font-weight:400">isteğe bağlı</span></h3><div class="opts" id="exts"></div></div>
<div class="box hidden" id="bDet"><h3><i>4</i>İşletmenizle ilgili</h3><div id="dets"></div></div>
<div class="box"><h3><i>5</i>İletişim bilgileri</h3>
<label class="f" for="o_bus">İşletme adı *</label><input class="i" id="o_bus" required autocomplete="organization">
<label class="f" for="o_name">Adınız soyadınız *</label><input class="i" id="o_name" required autocomplete="name">
<label class="f" for="o_tel">Telefon *</label><input class="i" id="o_tel" type="tel" required autocomplete="tel" placeholder="05xx xxx xx xx">
<label class="f" for="o_mail">E-posta</label><input class="i" id="o_mail" type="email" autocomplete="email">
<label class="f" for="o_city">Şehir / ilçe</label><input class="i" id="o_city" autocomplete="address-level2">
<label class="f" for="o_note">Eklemek istedikleriniz</label><textarea class="i" id="o_note"></textarea>
<input id="o_web" name="website" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
<label class="chk"><input type="checkbox" id="kvkk"><span><a href="/kvkk/" target="_blank">KVKK aydınlatma metnini</a> okudum; siparişim için benimle iletişime geçilmesini kabul ediyorum.</span></label>
</div></div>
<aside class="box sum"><h3>Özet</h3><div id="sumBody"></div><button class="btn br" id="send" type="submit" style="width:100%;margin-top:18px">Siparişi oluştur</button><div class="err" id="err" role="alert"></div>
<h3 style="margin-top:28px;font-size:16px">Sonra ne olacak?</h3><ol class="next"><li><b>Sipariş numaranız oluşur</b><span>Siparişiniz anında bize ulaşır.</span></li><li><b>1 iş günü içinde ararız</b><span>Detayları netleştirip ödeme bilgisini paylaşırız.</span></li><li><b>4–5 iş gününde teslim</b><span>Ödemeden sonra kurulum başlar.</span></li></ol></aside></form></div>
<div id="done" class="done hidden"><div class="box" style="padding:36px"><h2>Siparişiniz alındı</h2><p class="mute">Sipariş numaranız</p><div class="code" id="code"></div>
<ol class="next"><li class="ok"><b>Sipariş alındı</b><span>Bilgileriniz bize ulaştı.</span></li>
<li><b>1 iş günü içinde sizi arayacağız</b><span>Detayları netleştirip ödeme bilgisini (havale / EFT) paylaşacağız.</span></li>
<li><b>Kurulum</b><span>Ödeme onayından sonra 4–5 iş gününde kurup linklerinizi ve QR dosyalarınızı göndereceğiz.</span></li>
<li><b>Teslim ve kısa eğitim</b><span>Nasıl kullanacağınızı birlikte gözden geçireceğiz.</span></li></ol>
<p class="sm mute" style="margin-top:8px">Daha hızlı ilerlemek isterseniz sipariş numaranızla bize Instagram'dan yazabilirsiniz.</p>
<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:12px"><a class="btn br" id="igBtn" href="https://ig.me/m/creamodul" target="_blank" rel="noopener">Instagram'dan yaz</a><button class="btn gh" id="cpBtn" type="button">Mesajı kopyala</button><a class="btn gh" href="/">Ana sayfa</a></div></div></div></div></section>"""
page("/siparis/", "Sipariş ver | Creamodul", "Creamodul modülünüzü seçin, paket ve ekstraları belirleyin, bilgilerinizi verin. Siparişiniz oluşsun, 4–5 iş gününde teslim edelim.",
     body, scripts='<script src="/assets/data.js?v=2"></script><script src="/assets/order.js?v=2"></script>')

body = """<section style="padding-top:48px"><div class="w prose"><h1 style="font-size:40px">KVKK aydınlatma metni</h1>
<p class="mute">Son güncelleme: 15 Kasım 2026</p>
<p>Bu metin, 6698 sayılı Kişisel Verilerin Korunması Kanunu kapsamında, creamodul.com üzerindeki sipariş formu aracılığıyla toplanan kişisel verilere ilişkin olarak sizi bilgilendirmek amacıyla hazırlanmıştır.</p>
<h3>Hangi verileri topluyoruz?</h3><p>Ad soyad, işletme adı, telefon, e-posta, şehir/ilçe ve sipariş formuna yazdığınız işletme bilgileri.</p>
<h3>Neden topluyoruz?</h3><p>Siparişinizi oluşturmak, sizinle iletişime geçmek, siparişinizi hazırlayıp teslim etmek ve faturalandırmak için.</p>
<h3>Hukuki sebep</h3><p>Sözleşmenin kurulması ve ifası için gerekli olması ile açık rızanız.</p>
<h3>Kimlerle paylaşıyoruz?</h3><p>Verileriniz satılmaz ve pazarlama amacıyla üçüncü kişilerle paylaşılmaz. Verilerin saklanması için bulut altyapı hizmeti (Supabase) kullanılmaktadır.</p>
<h3>Ne kadar saklıyoruz?</h3><p>Sipariş ve yasal saklama yükümlülükleri süresince.</p>
<h3>Haklarınız</h3><p>KVKK'nın 11. maddesi kapsamında verilerinize erişme, düzeltilmesini veya silinmesini isteme haklarına sahipsiniz. Talepleriniz için Instagram üzerinden <a href="https://www.instagram.com/creamodul/">@creamodul</a> hesabına yazabilirsiniz.</p></div></section>"""
page("/kvkk/", "KVKK aydınlatma metni | Creamodul", "Creamodul sipariş formunda toplanan kişisel verilere ilişkin aydınlatma metni.", body)

body = """<section style="padding-top:48px"><div class="w"><h1 style="font-size:36px">Siparişler</h1>
<div id="login" class="box" style="max-width:420px"><label class="f" for="pin">Panel şifresi</label><input class="i" id="pin" type="password"><button class="btn br" id="go" style="margin-top:16px">Giriş</button><div class="err" id="perr"></div></div>
<div id="list" class="hidden"><div style="display:flex;gap:12px;margin:0 0 20px;flex-wrap:wrap"><button class="btn sm gh" id="ref">Yenile</button><select class="i" id="flt" style="width:auto"><option value="">Tümü</option><option>yeni</option><option>görüşüldü</option><option>hazırlanıyor</option><option>teslim edildi</option><option>iptal</option></select><span id="cnt" class="mute" style="align-self:center"></span></div><div id="rows"></div></div></div></section>"""
panel_js = """<script>
const SB="https://hvdmodrcagrbpxiwjdtq.supabase.co",K="sb_publishable_1y98p0cOvJN7kEL1kwKNbw_o6GieAKm";let PIN=sessionStorage.getItem("cmpin")||"";
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const rpc=(f,b)=>fetch(SB+"/rest/v1/rpc/"+f,{method:"POST",headers:{apikey:K,Authorization:"Bearer "+K,"Content-Type":"application/json"},body:JSON.stringify(b)}).then(async r=>{const j=await r.json();if(!r.ok)throw j;return j});
const ST=["yeni","görüşüldü","hazırlanıyor","teslim edildi","iptal"];let ALL=[];const seen=+localStorage.getItem("cmseen")||0;
const waNum=p=>{let d=String(p).replace(/\\D/g,"");if(d.startsWith("90"))d=d.slice(2);if(d.startsWith("0"))d=d.slice(1);return "90"+d};
async function load(){try{ALL=await rpc("cm_list_orders",{p_pin:PIN});sessionStorage.setItem("cmpin",PIN);document.getElementById("login").classList.add("hidden");document.getElementById("list").classList.remove("hidden");draw();
const nw=ALL.filter(r=>r.id>seen&&r.status==="yeni").length;document.title=(nw?`(${nw}) `:"")+"Siparişler | Creamodul";if(ALL[0])localStorage.setItem("cmseen",Math.max(seen,ALL[0].id))}catch(e){const p=document.getElementById("perr");p.textContent="Şifre hatalı.";p.style.display="block"}}
function draw(){const f=document.getElementById("flt").value;const rows=ALL.filter(r=>!f||r.status===f);document.getElementById("cnt").textContent=rows.length+" sipariş";
document.getElementById("rows").innerHTML=rows.length?rows.map(r=>`<div class="box"><div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap"><b style="font-family:var(--disp);color:var(--brand)">${esc(r.code)}${r.id>seen&&r.status==="yeni"?' <span style="background:var(--cicek);color:#fff;border-radius:6px;padding:2px 8px;font-size:12px;font-family:var(--body)">yeni</span>':''}</b><span class="mute sm">${new Date(r.created_at).toLocaleString("tr-TR")}</span></div>
<h3 style="margin-top:10px">${esc(r.business)} <span class="mute" style="font-family:var(--body);font-weight:500">· ${esc(r.contact)}</span></h3>
<p><a href="tel:${esc(r.phone)}">${esc(r.phone)}</a> ${r.email?"· "+esc(r.email):""} ${r.city?"· "+esc(r.city):""} · <a href="https://wa.me/${waNum(r.phone)}" target="_blank" rel="noopener">WhatsApp</a></p>
<p><b>${esc(r.module)}</b> · ${esc(r.package_name)} · Tek seferlik <b>${(r.total_once||0).toLocaleString("tr-TR")} TL</b>${r.monthly?` · ${r.monthly.toLocaleString("tr-TR")} TL/ay`:""}</p>
${(r.extras||[]).length?`<p class="mute sm">Ekstralar: ${r.extras.map(e=>esc(e.name)).join(", ")}</p>`:""}
${Object.entries(r.details||{}).filter(([k,v])=>v).map(([k,v])=>`<p class="sm"><b>${esc(k)}:</b> ${esc(v)}</p>`).join("")}
${r.note?`<p class="sm"><b>Not:</b> ${esc(r.note)}</p>`:""}
<select class="i" style="width:auto" data-id="${r.id}">${ST.map(s=>`<option ${s===r.status?"selected":""}>${s}</option>`).join("")}</select></div>`).join(""):'<p class="mute">Bu filtrede sipariş yok.</p>';
document.querySelectorAll("select[data-id]").forEach(s=>s.onchange=()=>rpc("cm_set_status",{p_pin:PIN,p_id:+s.dataset.id,p_status:s.value}).then(()=>{const r=ALL.find(x=>x.id==s.dataset.id);if(r)r.status=s.value}).catch(()=>alert("Durum kaydedilemedi, tekrar deneyin.")))}
document.getElementById("go").onclick=()=>{PIN=document.getElementById("pin").value;load()};document.getElementById("pin").onkeydown=e=>{if(e.key==="Enter"){PIN=e.target.value;load()}};
document.getElementById("ref").onclick=load;document.getElementById("flt").onchange=draw;if(PIN)load();setInterval(()=>{if(PIN&&!document.hidden)load()},60000);
</script>"""
page("/panel/", "Sipariş paneli | Creamodul", "Yönetim paneli", body, noindex=True, scripts=panel_js)


# ---------- Yapabildiklerimiz ----------
CAPS = [
 ("Sipariş ve menü", "kafe", [
   ("Ürün oluşturucu ile sipariş", "Müşteri waffle'ını, burgerini, bowl'unu adım adım kendisi oluşturur; ürün ekranda gözünün önünde değişir, fiyat anında hesaplanır.", "/demo/waffle/?masa=B1"),
   ("QR menü", "Sade, hızlı dijital menü. Fotoğraflı ürünler, kategoriler, fiyat güncellemesi. Basılı menü derdi biter.", None),
   ("Alerjen ve kalori bilgisi", "Menüde içerik, alerjen ve kalori bilgisini gösteririz; toplu tüketim yerleri için getirilen bilgilendirme zorunluluğuna uygun menü.", None),
   ("Masadan sipariş ve tezgâh ekranı", "Sipariş masa numarasıyla tezgâhtaki ekrana düşer; sesli uyarı, onay ve hazırlanıyor durumu.", None),
   ("Garson çağırma ve hesap isteme", "Müşteri tek dokunuşla garson çağırır ya da hesabı ister; bildirim tezgâha gelir.", None),
   ("Menü ve stok yönetimi", "Biten ürünü “bugün yok” yapın, fiyat değiştirin; menü anında güncellenir.", None)]),
 ("Görünürlük", "yorum", [
   ("Google yorum kartı ve standı", "Masaya ve kasaya markanıza özel kart; müşteri tek okutmayla yorum ekranınıza gider.", "/moduller/google-yorum-karti/"),
   ("Google işletme profili düzenleme", "Saatler, fotoğraflar, kategori ve menü linki; müşterinin sizi ilk gördüğü yer düzgün olsun.", None),
   ("İşletme web sitesi", "Hızlı, mobil uyumlu, alan adınızla; menü, konum, iletişim ve sipariş tek yerde.", None)]),
 ("İçerik ve reklam", "cicek", [
   ("Reklam filmleri", "Sosyal medya diline uygun, kancalı kısa reklam videoları. Instagram Reels ve TikTok formatında.", "#ornek"),
   ("Gerçekçi ürün görselleri", "Menünüz için stüdyo kalitesinde ürün ve malzeme görselleri; çekim yapmadan.", None),
   ("Sosyal medya gönderileri", "Kaydırmalı gönderi, tek görsel ve kısa video planı; paylaşım takvimiyle birlikte.", None)]),
 ("Sektöre özel", "anatomi", [
   ("Çiçekçiler için buket oluşturucu", "Müşteri çiçeğini, yeşilliğini, ambalajını seçer; buket ekranda oluşur.", "/moduller/cicekci-buket-olusturucu/"),
   ("Klinikler için 3D anatomi videoları", "Hastalığın vücutta nasıl ilerlediğini gösteren, kliniğinizin logolu 3D videoları.", "https://anatomi.creamodul.com"),
   ("Size özel modül", "Aklınızdaki fikri anlatın; işletmenize özel dijital aracı tasarlayıp kuralım.", "/siparis/?modul=ozel")]),
]
def caps_html(limit=None):
    out = ""
    for grp, col, items in CAPS:
        cards = ""
        for t, d, link in items[:limit] if limit else items:
            a = f'<a class="cl" href="{link}"{" target=_blank rel=noopener" if link.startswith("http") else ""}>Gör</a>' if link else ""
            cards += f'<div class="cap"><i class="dot {col}"></i><h3>{E(t)}</h3><p>{E(d)}</p>{a}</div>'
        out += f'<div class="capg"><h3 class="gt">{E(grp)}</h3><div class="caps">{cards}</div></div>'
    return out
cbody = f"""<section class="hero" style="padding-bottom:40px"><div class="w" style="display:block;max-width:900px">
<div class="crumb"><a href="/">Ana sayfa</a> / Yapabildiklerimiz</div>
<h1>Yapabildiklerimiz</h1>
<p class="lead">Sade bir QR menüden müşterinin kendi ürününü oluşturduğu sipariş sistemine, reklam filminden web sitesine kadar işletmenizin dijital tarafını tek elden kuruyoruz. Hepsi uzaktan, hepsi sizin markanızla.</p>
<div class="cta"><a class="btn br" href="/siparis/">Teklif / sipariş</a><a class="btn gh" href="https://www.instagram.com/creamodul/" rel="noopener">Instagram'dan yazın</a></div></div></section>
<section class="alt"><div class="w">{caps_html()}</div></section>
<section id="ornek"><div class="w split"><div class="vid"><video src="/assets/vid/reklam.mp4" poster="/assets/vid/reklam.jpg" controls playsinline preload="none"></video></div>
<div><h2>Örnek: kafe reklam filmi</h2><p class="lead">Kancası ilk 2 saniyede, altyazılı, müzikli; Reels ve TikTok için. Senaryodan kurguya biz hazırlıyoruz.</p>
<div class="cta"><a class="btn br" href="/siparis/?modul=ozel">Bize anlatın</a></div></div></div></section>"""
page("/yapabildiklerimiz/", "Yapabildiklerimiz | Creamodul: QR menü, ürün oluşturucu, reklam filmi, web sitesi",
     "QR menü, müşterinin kendi oluşturduğu sipariş sistemi, alerjen ve kalori bilgili menü, Google yorum kartı, web sitesi, reklam filmi ve ürün görselleri. Uzaktan kurulum.", cbody)

page("/404.html", "Sayfa bulunamadı | Creamodul", "Aradığınız sayfa bulunamadı.", """<section class="hero"><div class="w" style="display:block"><h1>Bu sayfa yok</h1><p class="lead">Adres değişmiş ya da yanlış yazılmış olabilir.</p><div class="cta"><a class="btn br" href="/">Ana sayfa</a><a class="btn gh" href="/#moduller">Modüller</a></div></div></section>""", noindex=True)
urls = ["/", "/yapabildiklerimiz/", "/siparis/", "/kvkk/"] + [f"/moduller/{m['slug']}/" for m in MODS]
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{BASE}{u}</loc><lastmod>2026-11-15</lastmod></url>" for u in urls) + "</urlset>\n")
open(os.path.join(ROOT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nDisallow: /panel/\nSitemap: {BASE}/sitemap.xml\n")
open(os.path.join(ROOT, "CNAME"), "w").write("creamodul.com\n")
open(os.path.join(ROOT, ".nojekyll"), "w").write("")
print("ok", len(urls))
