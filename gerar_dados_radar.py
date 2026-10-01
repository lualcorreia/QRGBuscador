import json
import time
import re
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Iniciando extração no Airframes.io...")
    
    opcoes = Options()
    opcoes.add_argument("--headless=new")
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")
    opcoes.add_argument("--window-size=1920,10000")
    
    # --- SISTEMA DE CAMUFLAGEM (STEALTH) ---
    opcoes.add_argument("--disable-blink-features=AutomationControlled")
    opcoes.add_experimental_option("excludeSwitches", ["enable-automation"])
    opcoes.add_experimental_option('useAutomationExtension', False)
    opcoes.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    try:
        # Removido o webdriver-manager. O Selenium agora usa o Chrome nativo do GitHub!
        driver = webdriver.Chrome(options=opcoes)
        
        # Esconde a bandeira de "WebDriver" do navegador
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        driver.get("https://tbg.airframes.io/dashboard/hfCPDLC")
        print("Aguardando 35 segundos para o Grafana processar os dados pesados...")
        time.sleep(35)
        
        texto = driver.execute_script("return document.body.innerText;")
        print(f"-> Leitura concluída. Foram capturados {len(texto)} caracteres de texto da página.")
        driver.quit()
    except Exception as e:
        print(f"[ERRO] Falha crítica no WebDriver: {e}")
        return

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

    if len(dados) == 0:
        print("\n[ALERTA] Nenhuma FIR foi decifrada! O site pode estar vazio ou a bloquear o robô.")
        print(f"O que o robô leu na tela:\n{texto[:300]}")
    else:
        caminho_arquivo = os.path.join(os.environ.get('GITHUB_WORKSPACE', '.'), 'dados_radar.json')
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print(f"-> Sucesso. Arquivo 'dados_radar.json' gerado com {len(dados)} FIRs ativas.")

if __name__ == "__main__":
    atualizar_banco_dados()
