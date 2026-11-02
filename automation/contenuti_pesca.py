import io, json, os, re, glob
# GUIDA-SVILUPPO: contenuti di pescaecommerce (home, chi siamo, articoli IT+EN), toglie Servizi e gli esempi del template.
# Uso dalla radice:  python automation/contenuti_pesca.py   poi  python automation/permalink_articoli.py --apply  e  python automation/allinea_hash.py en
def rd(p): return json.load(io.open(p, encoding='utf-8'))
def wj(p, d): io.open(p, 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2))
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
def card(title, items=None, text=None, n=None):
    s = '<div class="gc-pl%s">' % (' ent-pl' if items else '')
    if n: s += '<span class="n">%s</span>' % n
    s += '<b>%s</b>' % title
    if items: s += '<ul>' + ''.join('<li>%s</li>' % i for i in items) + '</ul>'
    if text: s += '<p>%s</p>' % text
    return s + '</div>'
def lin_card(i, title, items):
    return '<article class="lin-card lin-c%d"><i class="lin-dot" aria-hidden="true"></i><h3>%s</h3><ul>%s</ul></article>' % (i + 1, title, ''.join('<li>%s</li>' % x for x in items))
LIN_JS = '<script>(function(){if(!window.matchMedia||!matchMedia("(hover:hover)").matches)return;document.querySelectorAll(".lin-card").forEach(function(c){c.addEventListener("pointermove",function(e){var r=c.getBoundingClientRect();c.style.setProperty("--mx",e.clientX-r.left+"px");c.style.setProperty("--my",e.clientY-r.top+"px")})})})();</script>'
def home(L):
    t = L
    hero = ('<div class="gc"><section class="ent-hero"><div class="gc-wrap gc-hero-in"><div><p class="gc-eyebrow">%s</p><h1 class="gc-h1">%s</h1><p class="gc-lead">%s</p>'
      '<div class="gc-act"><a class="gc-btn gc-btn-a" href="__BASEURL__%s">%s</a><a class="gc-btn gc-btn-o" href="#linee">%s</a></div></div><div class="ent-cycle">%s</div></div></section></div>'
      % (t['eb'], t['h1'], t['lead'], t['shop'], t['b1'], t['b2'], ''.join('<div><b>%s</b><span>%s</span></div>' % x for x in t['cyc'])))
    linee = ('<div class="gc"><section class="gc-sec lin" id="linee"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><div class="lin-grid">%s</div>'
      '<p class="lin-all"><a class="gc-link" href="__BASEURL__%s">%s</a></p></div></section></div>'
      % (t['l_eb'], t['l_h2'], ''.join(lin_card(i, a, b) for i, (a, b) in enumerate(t['linee'])), t['shop'], t['l_all'])) + LIN_JS
    perchi = ('<div class="gc"><section class="gc-sec" id="perchi"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><div class="gc-plat ent-4">%s</div></div></section></div>'
      % (t['p_eb'], t['p_h2'], ''.join(card(a, items=b) for a, b in t['perchi'])))
    metodo = ('<div class="gc"><section class="gc-sec gc-soft" id="metodo"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><div class="gc-plat ent-4">%s</div></div></section></div>'
      % (t['m_eb'], t['m_h2'], ''.join(card(a, text=b, n='0%d' % (i + 1)) for i, (a, b) in enumerate(t['metodo']))))
    avvisi = ('<div class="gc"><section class="gc-sec" id="avvisi"><div class="gc-wrap gc-2c"><div><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><a class="gc-btn gc-btn-k" href="__BASEURL__%s">%s</a></div>%s</div></section></div>'
      % (t['a_eb'], t['a_h2'], t['a_lead'], t['blog'], t['a_btn'], card(t['a_t'], text=t['a_p'], n=t['a_n'])))
    cont = ('<div class="gc"><section class="gc-sec gc-dark" id="contatti"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><a class="gc-btn" href="__BASEURL__%s">%s</a></div></section></div>'
      % (t['c_eb'], t['c_h2'], t['c_lead'], t['contatti'], t['c_btn']))
    return {'hero': hero, 'servizi': linee, 'perchi': perchi, 'metodo': metodo, 'avvisi': avvisi, 'contatti': cont}
IT = dict(eb='Articoli da pesca online', h1='Tutto per la tua <em>prossima uscita.</em>',
  lead='Canne, mulinelli, lenze, ami, esche e accessori per la pesca in mare, lago e fiume. Scegli, ordina e preparati.',
  shop='/negozio/', b1='Vai al negozio', b2='Scopri le linee',
  cyc=[('Canne e mulinelli','Per spinning, surfcasting e galleggiante'),('Lenze e terminali','Nylon, trecciato, fluorocarbon, ami e girelle'),('Esche e artificiali','Cucchiaini, minnow e siliconici'),('Accessori','Guadini, pinze, borse e portaccessori')],
  l_eb='Il catalogo', l_h2='Le nostre linee', l_all='Vedi tutto il negozio',
  linee=[('Canne',['Spinning e telescopiche','Surfcasting','Bolognese']),('Mulinelli',['Spinning e frizione frontale','Surfcasting']),('Lenze e fili',['Nylon monofilo','Trecciato','Fluorocarbon']),('Ami e terminali',['Ami, girelle e moschettoni','Piombi e galleggianti']),('Esche e artificiali',['Cucchiaini rotanti e minnow','Siliconici e pasturatori']),('Accessori',['Guadino e pinze','Borse e scatole portaccessori'])],
  p_eb='Per chi è', p_h2='Chi si trova bene con noi',
  perchi=[('Chi comincia',['Attrezzatura di base per iniziare','Articoli semplici da usare']),('Pesca in mare',['Surfcasting e spinning','Lenze e terminali']),('Lago e fiume',['Galleggiante e telescopiche','Esche e artificiali']),('Idee regalo',['Accessori e portaccessori','Per ogni appassionato'])],
  m_eb='Come funziona', m_h2='Ordinare è semplice',
  metodo=[('Scegli','Sfoglia le linee e trova ciò che ti serve.'),('Ordina','Aggiungi al carrello e completa l\'ordine.'),('Ricevi','Spediamo il tuo ordine all\'indirizzo indicato.'),('Pesca','Controlla sempre le regole locali prima di uscire.')],
  a_eb='Dal blog', a_h2='Idee e consigli', a_lead='Guide brevi per scegliere l\'attrezzatura, scritte in modo semplice.', blog='/blog/', a_btn='Vai al blog',
  a_t='Come scegliere la prima canna da pesca', a_p='Pochi criteri per orientarti tra spinning, telescopica e surfcasting.', a_n='ULTIMO ARTICOLO',
  c_eb='Contatti', c_h2='Scriviamoci', c_lead='Domande su un prodotto o su un ordine? Scrivici, ti rispondiamo appena possibile.', contatti='/contatti/', c_btn='Scrivici')
EN = dict(eb='Fishing gear online', h1='Everything for your <em>next trip.</em>',
  lead='Rods, reels, lines, hooks, baits and accessories for sea, lake and river fishing. Choose, order and get ready.',
  shop='/en/shop/', b1='Go to the shop', b2='Discover our ranges',
  cyc=[('Rods and reels','For spinning, surfcasting and float fishing'),('Lines and terminal tackle','Nylon, braid, fluorocarbon, hooks and swivels'),('Baits and lures','Spinners, minnows and soft baits'),('Accessories','Landing nets, pliers, bags and tackle boxes')],
  l_eb='The catalog', l_h2='Our ranges', l_all='See the whole shop',
  linee=[('Rods',['Spinning and telescopic','Surfcasting','Float rods']),('Reels',['Spinning and front drag','Surfcasting']),('Lines and braids',['Nylon monofilament','Braided line','Fluorocarbon']),('Hooks and terminal tackle',['Hooks, swivels and snaps','Sinkers and floats']),('Baits and lures',['Spinners and minnows','Soft baits and feeders']),('Accessories',['Landing net and pliers','Bags and tackle boxes'])],
  p_eb='Who it is for', p_h2='Who gets on well with us',
  perchi=[('Beginners',['Basic gear to get started','Easy-to-use items']),('Sea fishing',['Surfcasting and spinning','Lines and terminal tackle']),('Lake and river',['Float and telescopic rods','Baits and lures']),('Gift ideas',['Accessories and tackle boxes','For every angler'])],
  m_eb='How it works', m_h2='Ordering is simple',
  metodo=[('Choose','Browse the ranges and find what you need.'),('Order','Add to the cart and complete the order.'),('Receive','We ship your order to the address you give.'),('Fish','Always check local rules before heading out.')],
  a_eb='From the blog', a_h2='Ideas and tips', a_lead='Short guides to choosing your gear, written simply.', blog='/en/blog/', a_btn='Go to the blog',
  a_t='How to choose your first fishing rod', a_p='A few criteria to find your way among spinning, telescopic and surfcasting rods.', a_n='LATEST ARTICLE',
  c_eb='Contact', c_h2='Get in touch', c_lead='Questions about a product or an order? Write to us, we will reply as soon as possible.', contatti='/en/contact/', c_btn='Write to us')
for path, L in (('_data/blocks_home.json', IT), ('_data/i18n/en/blocks_home.json', EN)):
    d = rd(path); new = home(L)
    for b in d:
        if b['id'] == 'contesto': b['enabled'] = False
        if b['id'] in new: b['html'] = new[b['id']]
        if b['id'] == 'servizi': b['nome'] = 'Le linee' if L is IT else 'Ranges'
    wj(path, d)
def az(p, h2, lead, par, pr):
    d = rd(p)
    for b in d:
        if b['id'] == 'chi': b['html'] = '<div class="gc"><section class="gc-sec" id="chi"><div class="gc-wrap"><p class="gc-eyebrow">%s</p><h2 class="gc-h2">%s</h2><p class="gc-lead">%s</p><p>%s</p></div></section></div>' % (pr[0], h2, lead, par)
        if b['id'] == 'principi': b['html'] = '<div class="gc"><section class="gc-sec gc-soft" id="principi"><div class="gc-wrap"><h2 class="gc-h2">%s</h2><div class="gc-plat">%s</div></div></section></div>' % (pr[1], ''.join(card(a, text=t, n=str(i + 1)) for i, (a, t) in enumerate(pr[2])))
    wj(p, d)
az('_data/blocks_azienda.json', 'Attrezzatura da pesca, scelta con cura', 'Pesca Ecommerce propone canne, mulinelli, lenze, ami, esche e accessori per chi pesca in mare, lago e fiume.', 'Il catalogo è pensato per essere semplice da consultare: poche linee chiare, descrizioni dirette e prezzi visibili. Se hai un dubbio su un prodotto o su un ordine, scrivici.',
   ('Chi siamo', 'Come ci comportiamo', [('Chiarezza', 'Descrizioni semplici, senza promesse che non possiamo verificare.'), ('Praticità', 'Un catalogo ordinato per trovare subito ciò che serve.'), ('Assistenza', 'Ci scrivi, ti rispondiamo: prima e dopo l\'acquisto.')]))
az('_data/i18n/en/blocks_azienda.json', 'Fishing gear, chosen with care', 'Pesca Ecommerce offers rods, reels, lines, hooks, baits and accessories for sea, lake and river anglers.', 'The catalog is meant to be easy to browse: a few clear ranges, direct descriptions and visible prices. If you have a question about a product or an order, write to us.',
   ('About us', 'How we behave', [('Clarity', 'Simple descriptions, with no promises we cannot verify.'), ('Practicality', 'A tidy catalog to find what you need quickly.'), ('Support', 'You write, we reply: before and after your purchase.')]))
for p, pat in (('_data/navigation.yml', r'  - title: "Servizi"\r?\n    url: /servizi/\r?\n'), ('_data/i18n/en/navigation.yml', r'  - title: "Services"\r?\n    url: /en/services/\r?\n')):
    s = io.open(p, encoding='utf-8').read(); io.open(p, 'w', encoding='utf-8', newline='').write(re.sub(pat, '', s))
for f in ['_pages/servizi.md', 'en/servizi.md'] + glob.glob('redirect/*.html') + glob.glob('_posts/*.md') + glob.glob('en/_posts/*.md'):
    if os.path.exists(f): os.remove(f)
def post(path, ref, title, date, exc, cat, body, en=False):
    wr(path, '---\nlayout: single\nref: %s\ntitle: "%s"\ndate: %s\nexcerpt: "%s"\ncategories:\n  - %s\n%s---\n\n%s\n' % (ref, title, date, exc, cat, 'tr: tradotto\n' if en else '', body))
A1 = "Per scegliere la prima canna conta soprattutto dove e come vuoi pescare.\n\n## Spinning\n\nÈ adatta alla pesca con artificiali, da riva o da barca, ed è versatile per cominciare.\n\n## Telescopica\n\nSi chiude in poco spazio: comoda da portare in viaggio, per lago e fiume.\n\n## Surfcasting\n\nÈ pensata per lanci lunghi dalla spiaggia e richiede un mulinello adatto.\n\n## Prima di comprare\n\nPensa al tipo di pesca, al budget e alle regole locali. Se hai dubbi, scrivici."
A2 = "Una piccola scorta di terminali ti evita di interrompere la giornata di pesca.\n\n- **Ami** in più misure.\n- **Girelle e moschettoni** per cambiare in fretta l'artificiale.\n- **Piombi** di pesi diversi.\n- **Filo di scorta**, nylon o fluorocarbon.\n- **Una pinza** per slamare e tagliare il filo.\n\nTieni tutto in una scatola con scomparti, così ritrovi ogni cosa."
A3 = "È online Pesca Ecommerce: un negozio di articoli da pesca per mare, lago e fiume.\n\n## Cosa trovi\n\nSei linee: canne, mulinelli, lenze e fili, ami e terminali, esche e artificiali, accessori. Su ogni scheda trovi una descrizione chiara.\n\n## Cosa arriverà\n\nSul blog pubblichiamo guide per scegliere l'attrezzatura. Se hai una richiesta, scrivici dalla pagina Contatti."
B1 = "To choose your first rod, what matters most is where and how you want to fish.\n\n## Spinning\n\nIt suits lure fishing, from shore or boat, and is versatile for beginners.\n\n## Telescopic\n\nIt packs into little space: handy for travel, lake and river.\n\n## Surfcasting\n\nIt is made for long casts from the beach and needs a suitable reel.\n\n## Before buying\n\nThink about the kind of fishing, your budget and local rules. If in doubt, write to us."
B2 = "A small stock of terminal tackle saves you from cutting your fishing day short.\n\n- **Hooks** in several sizes.\n- **Swivels and snaps** to change lures quickly.\n- **Sinkers** of different weights.\n- **Spare line**, nylon or fluorocarbon.\n- **A pair of pliers** to unhook and cut line.\n\nKeep everything in a box with compartments so you can always find it."
B3 = "Pesca Ecommerce is online: a shop for fishing gear for sea, lake and river.\n\n## What you will find\n\nSix ranges: rods, reels, lines and braids, hooks and terminal tackle, baits and lures, accessories. Each page has a clear description.\n\n## What is coming\n\nOn the blog we publish guides to choosing your gear. If you have a request, write to us from the Contact page."
post('_posts/2026-11-02-come-scegliere-la-prima-canna.md', 'prima-canna', 'Come scegliere la prima canna da pesca', '2026-11-02', 'Pochi criteri per orientarti tra spinning, telescopica e surfcasting.', 'Guide', A1)
post('_posts/2026-11-02-terminali-da-tenere-sempre-con-te.md', 'terminali-scorta', 'I terminali da tenere sempre con te', '2026-11-02', 'Una piccola scorta per non interrompere la giornata di pesca.', 'Guide', A2)
post('_posts/2026-11-02-nasce-pesca-ecommerce.md', 'nasce-pesca', 'Nasce Pesca Ecommerce', '2026-11-02', 'Il nuovo negozio di articoli da pesca.', 'Novità', A3)
post('en/_posts/2026-11-02-how-to-choose-your-first-rod.md', 'prima-canna', 'How to choose your first fishing rod', '2026-11-02', 'A few criteria to find your way among spinning, telescopic and surfcasting rods.', 'Guides', B1, True)
post('en/_posts/2026-11-02-terminal-tackle-to-always-carry.md', 'terminali-scorta', 'Terminal tackle to always carry', '2026-11-02', 'A small stock so your fishing day is never cut short.', 'Guides', B2, True)
post('en/_posts/2026-11-02-pesca-ecommerce-is-born.md', 'nasce-pesca', 'Pesca Ecommerce is born', '2026-11-02', 'The new shop for fishing gear.', 'News', B3, True)
print('ok')
