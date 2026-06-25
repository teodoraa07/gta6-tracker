import feedparser
import json
import urllib.request
import re

RSS_URL = "https://news.google.com/rss/search?q=GTA+6+Rockstar+Games&hl=ro&gl=RO&ceid=RO:ro"
JSON_FILE = "stiri.json"

def curata_textul(text_html):
    # Șterge etichetele HTML și curăță spațiile
    text_curat = re.sub(r'<[^>]+>', '', text_html)
    # Elimină numele sursei de la final dacă apare în paranteze (ex: "(Playtech)")
    text_curat = re.sub(r'\s*\(.*?\)\s*$', '', text_curat)
    return text_curat.strip()

def aduna_stiri_detaliate_reale():
    print("Se adună știrile reale cu detalii importante...")
    try:
        req = urllib.request.Request(
            RSS_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            html_content = response.read()
        feed = feedparser.parse(html_content)
    except Exception as e:
        print(f"Eroare: {e}")
        return

    stiri_finale = []

    if feed and feed.entries:
        # Luăm cele mai recente 3 știri din presă
        for i, entry in enumerate(feed.entries[:3]):
            titlu_complet = entry.get('title', 'Actualizare GTA VI')
            data_reala = entry.get('published', 'Recent')[:16]
            link_real = entry.get('link', 'https://news.google.com')
            
            # Extragem rezumatul brut și îl curățăm
            rezumat_brut = entry.get('summary', '')
            detaliu_scurt = curata_textul(rezumat_brut)

            # Spargem titlul ca să aflăm publicația (Google News pune mereu "Titlu - Publicație")
            sursa = "Presa de Gaming"
            titlu_curat = titlu_complet
            if " - " in titlu_complet:
                parti = titlu_complet.rsplit(" - ", 1)
                titlu_curat = parti[0]
                sursa = parti[1]

            # Construim un bloc de detalii importante pe baza datelor reale transmise de flux
            continut_detaliat = (
                f"■ DETALII ACTUALE DIN PRESĂ:\n"
                f"• Subiect principal: {titlu_curat}\n"
                f"• Sumar informație: {detaliu_scurt}\n\n"
                f"■ SURSA ȘI CONTEXT:\n"
                f"Articolul a fost monitorizat live via Google News din secțiunea oficială Rockstar Games. "
                f"Informația completă a fost redactată de către jurnaliștii de la {sursa}."
            )

            stiri_finale.append({
                "id": f"stire-detaliata-{i}",
                "titlu": titlu_curat,
                "data": data_reala,
                "link": link_real,
                "continut": continut_detaliat
            })

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(stiri_finale, f, indent=4, ensure_ascii=False)
    print("Gata! Fișierul stiri.json conține acum detalii structurate.")

if __name__ == "__main__":
    aduna_stiri_detaliate_reale()
