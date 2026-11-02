import io, json, os
# GUIDA-SVILUPPO: popola lo shop pescaecommerce (categorie + prodotti IT+EN), toglie gli esempi del template. Idempotente. Poi: python automation/allinea_hash.py en
C = [
("canne","Canne da pesca","🎣","Fishing rods","fishing-rods"),
("mulinelli","Mulinelli","⚙️","Reels","reels"),
("lenze-fili","Lenze e fili","🧵","Lines and braids","lines-and-braids"),
("ami-terminali","Ami e terminali","🪝","Hooks and terminal tackle","hooks-and-terminal-tackle"),
("esche-artificiali","Esche e artificiali","🐟","Baits and lures","baits-and-lures"),
("accessori","Accessori","🧰","Accessories","accessories"),
]
# id, nome IT, nome EN, categoria, centesimi, icona, uso IT, uso EN
P = [
("canna-spinning","Canna da spinning","Spinning rod","canne",3990,"🎣","Per la pesca con artificiali da riva o da barca.","For lure fishing from shore or boat."),
("canna-telescopica","Canna telescopica","Telescopic rod","canne",2490,"🎣","Compatta da trasportare, comoda per lago e fiume.","Compact to carry, handy for lake and river."),
("canna-surfcasting","Canna da surfcasting","Surfcasting rod","canne",5990,"🎣","Per lanci lunghi dalla spiaggia.","For long casts from the beach."),
("canna-bolognese","Canna bolognese","Float rod","canne",3490,"🎣","Per la pesca a galleggiante in acque ferme e correnti lente.","For float fishing in still water and slow currents."),
("mulinello-spinning","Mulinello da spinning","Spinning reel","mulinelli",2990,"⚙️","Per canne da spinning e pesca leggera.","For spinning rods and light fishing."),
("mulinello-surf","Mulinello da surfcasting","Surfcasting reel","mulinelli",4990,"⚙️","Bobina capiente per lanci lunghi.","Large spool for long casts."),
("mulinello-frontale","Mulinello a frizione frontale","Front drag reel","mulinelli",3490,"⚙️","Frizione regolabile sul lato anteriore della bobina.","Adjustable drag on the front of the spool."),
("monofilo-nylon","Filo in nylon monofilo","Nylon monofilament line","lenze-fili",990,"🧵","Per montature, terminali e pesca generale.","For rigs, leaders and general fishing."),
("trecciato","Filo trecciato","Braided line","lenze-fili",1990,"🧵","Per spinning e pesca con poca elasticità del filo.","For spinning and fishing with low line stretch."),
("fluorocarbon","Filo in fluorocarbon","Fluorocarbon line","lenze-fili",1490,"🧵","Per terminali poco visibili in acqua.","For leaders that are hard to see in water."),
("ami-assortiti","Assortimento di ami","Assorted hooks","ami-terminali",590,"🪝","Misure diverse per tipi di pesca diversi.","Different sizes for different kinds of fishing."),
("girelle-moschettoni","Girelle e moschettoni","Swivels and snaps","ami-terminali",490,"🪝","Per collegare filo, terminali e artificiali.","To connect line, leaders and lures."),
("piombi-assortiti","Piombi assortiti","Assorted sinkers","ami-terminali",690,"⚫","Pesi diversi per adattare la montatura.","Different weights to adjust the rig."),
("galleggianti","Set di galleggianti","Float set","ami-terminali",590,"🔴","Per la pesca a galleggiante.","For float fishing."),
("cucchiaino-rotante","Cucchiaino rotante","Spinner","esche-artificiali",490,"✨","Artificiale classico per spinning in acque dolci.","Classic spinning lure for fresh water."),
("minnow","Pesciolino artificiale (minnow)","Minnow lure","esche-artificiali",690,"🐟","Imita un piccolo pesce per la pesca con artificiali.","Imitates a small fish for lure fishing."),
("siliconici","Esche siliconiche assortite","Assorted soft baits","esche-artificiali",790,"🐛","Per la pesca a spinning leggero.","For light spinning."),
("pasturatore","Pasturatore","Bait feeder","esche-artificiali",390,"🥣","Per distribuire pastura vicino alla lenza.","To spread groundbait near the line."),
("guadino","Guadino pieghevole","Folding landing net","accessori",1990,"🥅","Per recuperare il pesce in sicurezza.","To land the fish safely."),
("pinza-sganciaami","Pinza e sganciaami","Pliers and hook remover","accessori",1290,"🔧","Per slamare il pesce e tagliare il filo.","To unhook the fish and cut the line."),
("borsa-pesca","Borsa per attrezzatura","Tackle bag","accessori",2990,"👜","Per tenere ordinati ami, artificiali e accessori.","To keep hooks, lures and accessories tidy."),
("scatola-assortimenti","Scatola portaccessori","Tackle box","accessori",1490,"🧰","Scomparti per ami, girelle e piombi.","Compartments for hooks, swivels and sinkers."),
("treppiede-canne","Appoggiacanne","Rod rest","accessori",1790,"📐","Per appoggiare la canna durante l'attesa.","To rest the rod while waiting."),
("cappello-pesca","Cappello da pesca","Fishing hat","accessori",1290,"🧢","Per ripararsi dal sole durante la giornata.","To shade you from the sun during the day."),
]
def wr(p, s): io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
for f in ['_negozio/categoria-esempio.md','_negozio/prodotto-esempio.md','en/negozio/prodotto-esempio.md','en/negozio/categoria/esempio.md']:
    if os.path.exists(f): os.remove(f)
d = json.load(io.open('_data/catalogo.json', encoding='utf-8'))
d['categorie'] = []; d['prodotti'] = []
for c in C:
    d['categorie'].append({"nome": c[1], "id": c[0], "icona": c[2], "tr": {"en": {"nome": c[3]}}})
    wr('_negozio/categoria-%s.md' % c[0], '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /negozio/categoria/%s/\ndescription: "%s"\nref: shop-cat-%s\n---\n' % (c[1], c[0], c[0], c[1], c[0]))
    wr('en/negozio/categoria/%s.md' % c[0], '---\nlayout: negozio-categoria\ntitle: "%s"\ncid: %s\npermalink: /en/shop/category/%s/\ndescription: "%s"\nlang: en\nlocale: en\nref: shop-cat-%s\ntr: tradotto\n---\n' % (c[3], c[0], c[4], c[3], c[0]))
for p in P:
    i, ni, ne, cat, pr, ic, ui, ue = p
    li = "%s: articolo da pesca per chi cerca praticità.\n\n## Come usarlo\n\n%s\n\n## Prima di acquistare\n\nControlla le caratteristiche indicate sulla confezione e scegli l'attrezzatura adatta al tipo di pesca e alle regole locali. Per dubbi su un prodotto scrivici." % (ni, ui)
    le = "%s: a fishing item for anglers who want practicality.\n\n## How to use it\n\n%s\n\n## Before buying\n\nCheck the features shown on the packaging and choose gear suited to your kind of fishing and to local rules. If you have a question about a product, write to us." % (ne, ue)
    d['prodotti'].append({"tipo":"fisico","id":i,"nome":ni,"categoria":cat,"prezzo_centesimi":pr,"descrizione":ui,"descrizione_completa":li,"immagine":"","icona":ic,"visibile":True,
      "tr":{"en":{"nome":ne,"descrizione":ue,"descrizione_completa":le}}})
    wr('_negozio/%s.md' % i, '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /negozio/%s/\ndescription: "%s"\nref: shop-prod-%s\n---\n' % (ni, i, i, ui, i))
    wr('en/negozio/%s.md' % i, '---\nlayout: negozio-prodotto\ntitle: "%s"\npid: %s\npermalink: /en/shop/%s/\ndescription: "%s"\nlang: en\nlocale: en\nref: shop-prod-%s\ntr: tradotto\n---\n' % (ne, i, i, ue, i))
io.open('_data/catalogo.json', 'w', encoding='utf-8').write(json.dumps(d, ensure_ascii=False, indent=2))
print('ok', len(d['categorie']), 'cat', len(d['prodotti']), 'prod')
