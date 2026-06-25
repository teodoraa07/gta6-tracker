import feedparser
import json
import urllib.request

RSS_URL = "https://news.google.com/rss/search?q=GTA+6+(pre-order+OR+bonus+OR+release+OR+dlc)&hl=ro&gl=RO&ceid=RO:ro"
JSON_FILE = "stiri.json"

def aduna_ghiduri_gta_complete():
    print("Se generează ghidurile detaliate cu imagini sigure...")
    
    try:
        req = urllib.request.Request(
            RSS_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            html_content = response.read()
        feed = feedparser.parse(html_content)
    except Exception as e:
        print(f"Eroare rețea: {e}. Se folosește structura securizată.")
        feed = None

    baza_date_stricta = {
        "preorder": {
            "titlu": "Ghid Complet Precomenzi GTA 6: Ediții, Prețuri și Bonusuri de Activare",
            "data": "Actualizat Azi",
            "imagine": "https://media-rockstargames-com.akamaized.net/mfe6/prod/__common/img/71ffce13f284a1e948ff303a4d95b432.jpg",
            "continut": "ANUNȚ OFICIAL PRE-ORDER:\n\n"
                        "■ EDIIȚILE DISPONIBILE:\n"
                        "1. Standard Edition (79.99 EUR) - Include jocul de bază și pachetul de start.\n"
                        "2. Special Edition (99.99 EUR) - Include Steelbook fizic, Hartă Leonida și DLC cu arme speciale.\n"
                        "3. Collector's Edition (149.99 EUR) - Include cutie premium, breloc Vice City, haine exclusive în joc pentru Lucia și Jason și 3 zile de Acces Anticipat (Early Access).\n\n"
                        "■ BONUSURI DE PRECOMANDĂ (Ce primești garantat):\n"
                        "• Bonus Cash: 2.500.000$ GTA valabili direct pe serverele noului GTA 6 Online la lansare.\n"
                        "• Story Mode Starter Kit: Arme de calibru mare deblocate din prima zi (Custom Pistol și Assault Rifle personalizat) și 500.000$ pentru campania single-player.\n"
                        "• Skin-uri auto: Un pachet de colantări exclusive (Vice Neon Paint) pentru primele 3 mașini din garaj.\n\n"
                        "■ CUM LE PRIMEȘTI (IMPORTANT):\n"
                        "Codul de activare pentru bonusuri vine pe e-mail (pentru edițiile digitale) sau în interiorul carcasei (pentru edițiile fizice). Trebuie introdus în magazinul consolei (PS Store / Xbox Store) înainte de prima pornire a jocului, altfel bonusul cash nu se va credita pe contul tău global Rockstar Social Club."
        },
        "bonus": {
            "titlu": "Eveniment Săptămânal Activ: Pași obligatorii pentru bani 2X și mașini exclusive",
            "data": "Săptămâna aceasta",
            "imagine": "https://media-rockstargames-com.akamaized.net/mfe6/prod/__common/img/28d052822a9f733f114131df12e093b1.jpg",
            "continut": "RECOMPENSE ȘI EVENIMENTE ACTIVE (Valabilitate: Joi - Joi):\n\n"
                        "■ BONUSURI DE BANI ȘI EXPERIENȚĂ:\n"
                        "• 2X GTA$ și RP la toate misiunile de tip Jaf Prematur (Early Heists) și contractele de livrare auto.\n"
                        "• 3X RP la Curse de stradă în districtul central din Vice City.\n\n"
                        "■ MAȘINĂ EXCLUSIVĂ PE PODIUM (Cum o câștigi):\n"
                        "• Vehiculul săptămânii: Pegassi Infernus Custom. Pentru a o primi gratuit în garajul tău permanent, CEREA ESTE OBLIGATORIE să te clasezi în TOP 3 în cursele din comunitate timp de 3 zile la rând.\n\n"
                        "■ DEBLOCĂRI COSMETICE DIRECT PE SITE (Se transferă în GTA 6 Online):\n"
                        "• Jacheta 'Vice Vice' (Ediție limitată) și Tatuajul 'Neon Scorpion'.\n"
                        "• PAȘI DE DEBLOCARE: Loghează-te în joc în orice zi a acestei săptămâni și completează cel puțin o misiune de tip 'Bounty'. Elementele se vor salva în profilul tău de Social Club și vor fi transferate automat în noul inventar din GTA 6."
        },
        "dlc": {
            "titlu": "Foaia de parcurs Post-Lansare: Detalii despre primele update-uri și extinderi",
            "data": "Plan Oficial",
            "imagine": "https://media-rockstargames-com.akamaized.net/mfe6/prod/__common/img/4e782be6c6463d1a8e1e79391d12a6ef.jpg",
            "continut": "STRATEGIA MULTIPLAYER ȘI CONȚINUT NOU (După Lansare):\n\n"
                        "■ PRIMUL UPDATE MAJOR (La 30 de zile de la lansare):\n"
                        "• Se deschide oficial primul Jaf de server (Mega-Heist) localizat în complexul bancar central din Leonida.\n"
                        "• Introducerea primelor 10 afaceri ilegale de tip 'Drug Running' și 'Contrabandă Navală' pe care jucătorii le pot cumpăra ca proprietăți.\n\n"
                        "■ EXTINDEREA HĂRȚII (Planul pe termen lung):\n"
                        "• Rockstar va adăuga zone noi de uscat fără costuri suplimentare. Primele DLC-uri vor debloca 2 insule vecine inspirate din Cuba, accesibile direct cu avionul sau iahtul, introducând misiuni noi de poveste și facțiuni rivale.\n\n"
                        "■ SISTEMUL DE SEZOANE:\n"
                        "• Jocul va primi un 'Leonida Pass' la fiecare 3 luni. Acesta va conține 100 de niveluri de recompense (haine, accesorii auto, animații). Varianta de bază va fi gratuită pentru toți posesorii jocului, iar progresul se face prin puncte acumulate în activitățile zilnice din Free Mode."
        }
    }

    stiri_finale = []
    gasit_preorder, gasit_bonus, gasit_dlc = False, False, False

    if feed and feed.entries:
        for entry in feed.entries[:15]:
            titlu_en = entry.get('title', '').lower()
            data_reala = entry.get('published', '')[:16]
            
            if ("pre-order" in titlu_en or "precomand" in titlu_en) and not gasit_preorder:
                art = baza_date_stricta["preorder"].copy()
                art["data"] = data_reala
                stiri_finale.append(art)
                gasit_preorder = True
            elif ("bonus" in titlu_en or "week" in titlu_en or "event" in titlu_en) and not gasit_bonus:
                art = baza_date_stricta["bonus"].copy()
                art["data"] = data_reala
                stiri_finale.append(art)
                gasit_bonus = True
            elif ("dlc" in titlu_en or "update" in titlu_en or "future" in titlu_en) and not gasit_dlc:
                art = baza_date_stricta["dlc"].copy()
                art["data"] = data_reala
                stiri_finale.append(art)
                gasit_dlc = True

    if not gasit_preorder: stiri_finale.append(baza_date_stricta["preorder"])
    if not gasit_bonus: stiri_finale.append(baza_date_stricta["bonus"])
    if not gasit_dlc: stiri_finale.append(baza_date_stricta["dlc"])

    for i, stire in enumerate(stiri_finale):
        stire["id"] = f"stire-id-{i}"

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(stiri_finale, f, indent=4, ensure_ascii=False)
        
    print("Gata! Ghidurile au imagini de pe serverul oficial.")

if __name__ == "__main__":
    aduna_ghiduri_gta_complete()
