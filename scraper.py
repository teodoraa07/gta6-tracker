import feedparser
import json
import urllib.request
import re

# Căutăm pe Google News cele mai noi articole oficiale și știri despre GTA 6
RSS_URL = "https://news.google.com/rss/search?q=GTA+6+Rockstar+Games&hl=ro&gl=RO&ceid=RO:ro"
JSON_FILE = "stiri.json"

def curata_textul(text_html):
    # Funcție care șterge etichetele HTML din rezumatul știrii ca să rămână text curat
    text_curat = re.sub(r'<[^>]+>', '', text_html)
    return text_curat.strip()

def aduna_stiri_reale_gta():
    print("Se adună știrile 100% reale de pe Google News...")
    
    try:
        req = urllib.request.Request(
            RSS_URL, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        with urllib.request.urlopen(req) as response:
            html_content = response.read()
        feed = feedparser.parse(html_content)
    except Exception as e:
        print(f"Eroare la conectare: {e}")
        return

    stiri_finale = []

    if feed and feed.entries:
        # Luăm primele 3 cele mai recente știri reale găsite
        for i, entry in enumerate(feed.entries[:3]):
            titlu_real = entry.get('title', 'Noutăți GTA VI')
            data_reala = entry.get('published', 'Recent')[:16] # Păstrăm doar data și ora
            
            # Luăm descrierea oferită de Google News și o curățăm
            rezumat_real = entry.get('summary', '')
            text_suport = curata_textul(rezumat_real)
            
            if not text_suport or len(text_suport) < 10:
                text_suport = "Apasă pe linkul oficial sau vizitează comunitatea pentru a citi întregul articol publicat în presă."

            stiri_finale.append({
                "id": f"stire-reala-{i}",
                "titlu": titlu_real,
                "data": data_reala,
                "imagine": "", # Nu mai avem nevoie de linkuri de poze, index.html folosește bannerele neon
                "continut": f"{text_suport}\n\nSursa: Google News Tracker"
            })

    # Dacă fluxul e gol din motive de rețea, punem o notificare reală
    if not stiri_finale:
        stiri_finale.append({
            "id": "stire-reala-0",
            "titlu": "Se așteaptă noi comunicate de la Rockstar Games",
            "data": "Astăzi",
            "imagine": "",
            "continut": "Momentan nu au fost publicate articole noi în ultimele ore. Verifică din nou mai târziu pentru actualizări live."
        })

    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(stiri_finale, f, indent=4, ensure_ascii=False)
        
    print("Gata! Fișierul stiri.json conține acum doar informații reale din presă.")

if __name__ == "__main__":
    aduna_stiri_reale_gta()
