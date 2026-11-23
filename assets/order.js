(function () {
  const SB_URL = "https://hvdmodrcagrbpxiwjdtq.supabase.co";
  const SB_KEY = "sb_publishable_1y98p0cOvJN7kEL1kwKNbw_o6GieAKm";
  const M = window.CM.modules, fmt = window.CM.fmt;
  const $ = s => document.querySelector(s);
  const q = new URLSearchParams(location.search);
  let mod = q.get("modul") === "ozel" ? "ozel" : (M.find(m => m.id === q.get("modul")) || null);
  let pkg = null;
  if (q.get("paket")) { for (const m of M) { const p = m.packages.find(p => p.id === q.get("paket")); if (p) { mod = m; pkg = p; } } }
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function priceLine(p) {
    const a = [];
    if (p.setup) a.push(fmt(p.setup) + (p.monthly || p.yearly ? " kurulum" : ""));
    if (p.monthly) a.push(fmt(p.monthly) + " / ay");
    if (p.yearly) a.push(fmt(p.yearly) + " / yıl bakım (2. yıldan itibaren)");
    return a.join(" + ");
  }

  function renderMods() {
    $("#mods").innerHTML = M.map(m => `<label class="opt"><input type="radio" name="mod" value="${m.id}" ${mod && mod.id === m.id ? "checked" : ""}><span class="t"><b>${esc(m.name)}</b><small>${esc(m.short)}</small></span></label>`).join("")
      + `<label class="opt"><input type="radio" name="mod" value="ozel" ${mod === "ozel" ? "checked" : ""}><span class="t"><b>Sektörüme özel modül</b><small>Aklınızdaki fikri yazın, size özel teklif hazırlayalım.</small></span></label>`;
    document.querySelectorAll('input[name=mod]').forEach(r => r.onchange = () => { mod = r.value === "ozel" ? "ozel" : M.find(m => m.id === r.value); pkg = null; renderRest(); });
  }

  function renderRest() {
    const isO = mod === "ozel";
    $("#bPkg").classList.toggle("hidden", !mod || isO);
    $("#bExt").classList.toggle("hidden", !mod || isO || !mod.extras.length);
    $("#bDet").classList.toggle("hidden", !mod);
    if (!mod) { sum(); return; }
    if (!isO) {
      if (!pkg) pkg = mod.packages.find(p => p.hl) || mod.packages[0];
      $("#pkgs").innerHTML = mod.packages.map(p => `<label class="opt"><input type="radio" name="pkg" value="${p.id}" ${pkg.id === p.id ? "checked" : ""}><span class="t"><b>${esc(p.name)}</b><small>${esc(p.features.slice(0, 3).join(" · "))}</small></span><span class="p">${esc(priceLine(p))}</span></label>`).join("");
      document.querySelectorAll('input[name=pkg]').forEach(r => r.onchange = () => { pkg = mod.packages.find(p => p.id === r.value); sum(); });
      $("#exts").innerHTML = mod.extras.map(e => `<label class="opt"><input type="checkbox" name="ext" value="${e.id}"><span class="t"><b>${esc(e.name)}</b></span><span class="p">+${fmt(e.price)}</span></label>`).join("");
      document.querySelectorAll('input[name=ext]').forEach(c => c.onchange = sum);
      $("#dets").innerHTML = mod.fields.map(f => `<label class="f" for="d_${f.id}">${esc(f.label)}${f.req ? " *" : ""}</label>` + (f.type === "textarea"
        ? `<textarea class="i" id="d_${f.id}" data-k="${f.id}" placeholder="${esc(f.ph || "")}" ${f.req ? "required" : ""}></textarea>`
        : `<input class="i" id="d_${f.id}" data-k="${f.id}" type="${f.type || "text"}" placeholder="${esc(f.ph || "")}" ${f.req ? "required" : ""}>`)).join("");
    } else {
      pkg = null;
      $("#dets").innerHTML = `<label class="f" for="d_fikir">Nasıl bir modül istiyorsunuz? *</label><textarea class="i" id="d_fikir" data-k="fikir" required placeholder="Sektörünüz, müşterinizin ekranda ne yapacağı, siparişin nereye düşeceği…"></textarea>`;
    }
    sum();
  }

  function chosenExtras() { return mod && mod !== "ozel" ? [...document.querySelectorAll('input[name=ext]:checked')].map(c => mod.extras.find(e => e.id === c.value)) : []; }

  function sum() {
    const el = $("#sumBody");
    if (!mod) { el.innerHTML = `<p class="mute sm">Seçtiğiniz modül ve paket burada görünür.</p>`; return; }
    if (mod === "ozel") { el.innerHTML = `<div class="row"><span>Sektörünüze özel modül</span><b>Teklif</b></div><p class="note">Talebinizi aldıktan sonra kapsam ve fiyatı birlikte netleştiririz.</p>`; return; }
    const ex = chosenExtras();
    const once = (pkg.setup || 0) + ex.reduce((a, e) => a + e.price, 0);
    let h = `<div class="row"><span>${esc(mod.name)}</span></div><div class="row"><span>${esc(pkg.name)}</span><b>${pkg.setup ? fmt(pkg.setup) : "—"}</b></div>`;
    ex.forEach(e => h += `<div class="row"><span>${esc(e.name)}</span><b>+${fmt(e.price)}</b></div>`);
    h += `<div class="row tot"><span>Tek seferlik</span><span>${fmt(once)}</span></div>`;
    if (pkg.monthly) h += `<div class="row"><span>Aylık</span><b>${fmt(pkg.monthly)} / ay</b></div>`;
    if (pkg.yearly) h += `<div class="row"><span>Yıllık bakım (2. yıldan)</span><b>${fmt(pkg.yearly)} / yıl</b></div>`;
    h += `<p class="note">Fiyatlara KDV dahil değildir. Ödeme, sipariş onaylandıktan sonra havale / EFT ile alınır. Teslim: 4–5 iş günü.</p>`;
    el.innerHTML = h;
  }

  async function submit(e) {
    e.preventDefault();
    const err = $("#err"); err.style.display = "none";
    const f = $("#frm");
    if (!mod) { err.textContent = "Lütfen bir modül seçin."; err.style.display = "block"; return; }
    if (!f.reportValidity()) return;
    if (!$("#kvkk").checked) { err.textContent = "Devam etmek için aydınlatma metnini onaylayın."; err.style.display = "block"; return; }
    if (!$("#soz").checked) { err.textContent = "Devam etmek için hizmet sözleşmesini onaylayın."; err.style.display = "block"; return; }
    const details = {}; document.querySelectorAll("#dets [data-k]").forEach(i => details[i.dataset.k] = i.value.trim()); details.sozlesme_onay = "v1 · 23 Kasım 2026 · " + new Date().toISOString();
    const ex = chosenExtras();
    const body = {
      module: mod === "ozel" ? "ozel" : mod.id,
      package: pkg ? pkg.id : null,
      package_name: pkg ? pkg.name : "Özel teklif",
      extras: ex.map(e => ({ id: e.id, name: e.name, price: e.price })),
      total_once: pkg ? (pkg.setup || 0) + ex.reduce((a, x) => a + x.price, 0) : 0,
      monthly: pkg && pkg.monthly || 0, yearly: pkg && pkg.yearly || 0,
      business: $("#o_bus").value.trim(), contact: $("#o_name").value.trim(), phone: $("#o_tel").value.trim(),
      email: $("#o_mail").value.trim(), city: $("#o_city").value.trim(), note: $("#o_note").value.trim(),
      details, hp: $("#o_web").value
    };
    const btn = $("#send"); btn.disabled = true; btn.textContent = "Gönderiliyor…";
    try {
      const r = await fetch(SB_URL + "/rest/v1/rpc/cm_create_order", { method: "POST", headers: { apikey: SB_KEY, Authorization: "Bearer " + SB_KEY, "Content-Type": "application/json" }, body: JSON.stringify({ p: body }) });
      const j = await r.json();
      if (!r.ok || !j || !j.code) throw new Error(j && j.message || "Hata");
      $("#formWrap").classList.add("hidden"); $("#done").classList.remove("hidden");
      $("#code").textContent = j.code; window.scrollTo(0, 0);
      const msg = `Merhaba, creamodul.com üzerinden sipariş oluşturdum. Sipariş numaram: ${j.code} (${body.business}).`;
      $("#cpBtn").onclick = async () => { try { await navigator.clipboard.writeText(msg); $("#cpBtn").textContent = "Kopyalandı"; } catch (e) { prompt("Mesajı kopyalayın:", msg); } };
      $("#igBtn").onclick = () => { try { navigator.clipboard.writeText(msg); } catch (e) {} };
    } catch (x) {
      err.textContent = "Sipariş gönderilemedi. Bağlantınızı kontrol edip tekrar deneyin; sorun sürerse Instagram'dan @creamodul hesabına yazın."; err.style.display = "block";
      btn.disabled = false; btn.textContent = "Siparişi oluştur";
    }
  }

  renderMods(); renderRest();
  $("#frm").addEventListener("submit", submit);
})();
