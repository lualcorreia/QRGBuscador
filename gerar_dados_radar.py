import json
import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def converter_tempo(texto):
    texto = texto.lower()
    if 'few seconds' in texto: return 10
    match = re.search(r'(\d+)\s+(second|minute|hour|day|month|year)', texto)
    if match:
        v, u = int(match.group(1)), match.group(2)
        if u == 'second': return v
        if u == 'minute': return v * 60
        if u == 'hour': return v * 3600
        if u == 'day': return v * 86400
        if u == 'month': return v * 2592000 
        if u == 'year': return v * 31536000 
    return 999999999 

def traduzir_tempo(t):
    t = t.lower().replace('ago', 'atrás').replace('a few seconds', 'alguns segundos')
    for e, pt in [('seconds','segundos'), ('second','segundo'), ('minutes','minutos'), ('minute','minuto'), 
                  ('hours','horas'), ('hour','hora'), ('days','dias'), ('day','dia'), 
                  ('months','meses'), ('month','mês'), ('years','anos'), ('year','ano')]:
        t = t.replace(e, pt)
    return t.replace('yesterday', 'ontem').strip()

def atualizar_banco_dados():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando extração Airframes.io...")
    
    opcoes = Options()
    opcoes.add_argument("--headless")
    opcoes.add_argument("--disable-gpu")
    opcoes.add_argument("--log-level=3")
    opcoes.add_argument("--window-size=1920,10000") 
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opcoes)
    driver.get("https://tbg.airframes.io/dashboard/hfCPDLC")
    driver.execute_script("document.body.style.zoom='20%'")
    time.sleep(20)
    
    texto = driver.execute_script("return document.body.innerText;")
    driver.quit()

    dados = {}
    for linha in texto.split('\n'):
        p = linha.split(':')
        if len(p) >= 2 and any(x in p[1].lower() for x in ['ago', 'second', 'minute', 'hour', 'day', 'month', 'year']):
            m = re.search(r'\b([A-Z]{4})\b', p[0])
            if m:
                icao = "SBAO" if m.group(1) == "SBRE" else m.group(1)
                idade = converter_tempo(p[1].strip())
                freqs = [n for seg in p[2:] for n in re.findall(r'\d+', seg)] if len(p) > 2 else []
                freqs_str = " | ".join(freqs) + " kHz" if freqs else "N/D (Sem reporte)"
                
                if icao not in dados or idade < dados[icao]['idade_segundos']:
                    dados[icao] = {'freqs': freqs_str, 'hora': traduzir_tempo(p[1].strip()), 'idade_segundos': idade}

    # Salva o arquivo JSON na mesma pasta em que o Python for rodado
    with open('dados_radar.json', 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
        
    print(f"-> Sucesso. Arquivo 'dados_radar.json' gerado com {len(dados)} FIRs.")

if __name__ == "__main__":
    while True:
        try:
            atualizar_banco_dados()
        except Exception as e:
            print("Erro:", e)
        print("Aguardando 2 minutos...")
        time.sleep(120)
