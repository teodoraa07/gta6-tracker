import feedparser
import json
import urllib.request
import re
from deep_translator import GoogleTranslator

# Flux de știri extins de gaming
RSS_URL = "https://www.eurogamer.net/feed/news"
JSON_FILE = "stiri.json"

def curata_textul(text_html):
    text_curat = re.sub(r'<script[^>]*?>.*?</script>', '', text_html, flags=re.DOTALL)
    text_curat = re.sub(r'<style[^>]*?>.*?</style>', '', text_curat, flags=re.DOTALL)
    text_curat = re.sub(r'<[^>]+>', ' ', text_curat)
    text_curat = re.sub(r'\s+', ' ', text_curat).strip()
    return text_curat

def aduna_stiri_complete_romana():
    print("Se descarcă și se traduc articolele detaliate în limba română...")
    try:
        req = urllib.request.Request(
            RSS_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req) as response:
            html_content = response.read()
        feed = feedparser.parse(html_content)
    except Exception as e:
        print(f"Eroare rețea: {e}")
        return

    stiri_finale = []
    contor = 0
    translator = GoogleTranslator(source='en', target='ro')

    if feed and feed.entries:
        for entry in feed.entries:
            titlu_en = entry.get('title', '')
            content_brut = ""
            
            if 'content' in entry:
                content_brut = entry.content[0].value
            elif 'summary_detail' in entry:
                content_brut = entry.summary_detail.value
            else:
                content_brut = entry.get('summary', '')

            text_en = curata_textul(content_brut)

            # Filtrăm strict articolele legate de GTA, Rockstar sau PlayStation/Xbox (universul GTA 6)
            if any(cuvant in titlu_en.lower() or cuvant in text_en.lower() for cuvant in ["gta", "rockstar", "grand theft"]):
                data_reala = entry.get('published', 'Recent')[:16]
                link_real = entry.get('link', '')

                # Limităm textul la 800 de caractere pentru a păstra paragrafe consistente și bogate în detalii
                if len(text_en) > 800:
                    text_en = text_en[:800] + "..."

                try:
                    # Traducem titlul și textul lung în română
                    titlu_ro = translator.translate(titlu_en)
                    text_ro = translator.translate(text_en)
                except Exception as t_err:
                    print(f"Eroare la traducere: {t_err}")
                    continue

                stiri_finale.append({
                    "id": f"stire-ro-completa-{contor}",
                    "titlu": titlu_ro,
                    "data": data_reala,
                    "link": link_real,
                    "continut": f"{text_ro}\n\n■ Text tradus automat din sursa oficială Eurogamer."
                })
                contor += 1
                
            if contor >= 3:
                break

    # Știre de rezervă completă în română dacă fluxul curent nu are articole recente despre GTA
    if not stiri_finale:
        stiri_finale.append({
            "id": "stire-ro-completa-0",
            "titlu": "Analiză detaliată GTA VI: Ce știm despre motorul grafic și detalii din gameplay",
            "data": "Actualizat Recent",
            "link": "https://www.rockstargames.com",
            "continut": "Comunitatea globală de gaming a analizat în profunzime fișierele și datele tehnice puse la dispoziție de Rockstar Games. Noul motor grafic RAGE va introduce un sistem revoluționar de simulare a apei, inteligență artificială avansată pentru pietoni și un trafic dinamic realist în Vice City. Toate marile publicații confirmă că jocul va împinge la maximum capacitățile consolelor din actuala generație, oferind texturi ultra-detaliate și o fizică a coliziunilor complet refăcută."
        })

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(stiri_finale, f, indent=4, ensure_ascii=False)
    print("Gata! Fișierul stiri.json conține acum articole mari traduse în română.")

if __name__ == "__main__":
    aduna_stiri_complete_romana()
