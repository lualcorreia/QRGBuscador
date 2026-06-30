# 📻 PP2LA Signal Intelligence System

[ 🇧🇷 Português ](#-português) | [ 🇺🇸 English ](#-english)

---

## 🇧🇷 Português

### Visão Geral
O **PP2LA Signal Intelligence System** é uma ferramenta web de alta performance desenvolvida para radioescutas e operadores de rádio. O sistema permite a busca, filtragem e geolocalização de estações utilitárias em HF (Alta Frequência). 

Construído com uma arquitetura *Serverless* (sem servidor backend), todo o processamento de dados ocorre localmente no navegador do usuário, garantindo respostas quase instantâneas e privacidade total.

### 🚀 Funcionalidades
* **Processamento Local Avançado:** Lê e descompacta a base de dados oficial (`ILGADATA.zip`) diretamente na memória RAM do navegador.
* **Sistema de Abas Duplas:**
  * **Buscador:** Varredura focada com filtros de frequência, margem de erro, modo e protocolo.
  * **Tabela Completa:** Visualização em massa de toda a base de dados de uma só vez, com rolagem otimizada.
* **Geolocalização Integrada:** Clique em qualquer interceptação na tabela para plotar a localização da antena transmissora em um mapa via satélite.
* **Dashboard Profissional:** Modo Escuro (Dark Mode) padrão para operações noturnas e design responsivo que se adapta a computadores, tablets e smartphones.
* **Multi-idioma:** Interface disponível em Português, Inglês e Espanhol, trocada em tempo real.

### 📖 Como Usar a Interface
1. **Aguarde o Carregamento:** Ao abrir o site, aguarde o aviso verde indicando que a base `ILGADATA` foi descompactada e carregada.
2. **Busca Específica:** Na aba **Buscador ILG**, insira uma Frequência Central (ex: `10150`).
3. **Ajuste de Tolerância:** Se houver desvio de VFO, use o filtro de "Tolerância" para varrer, por exemplo, `+/- 2 kHz` ao redor da frequência desejada.
4. **Filtros de Sinal:** Isole emissões selecionando o modo (`Voice`, `Data`, `Morse`) ou protocolos específicos como `STANAG`, `ALE` ou `NAVTEX`.
5. **Plotagem no Mapa:** Após clicar em "Buscar Sinais", clique sobre qualquer linha da tabela que aparecer. O sistema fará a leitura das coordenadas em tempo real e criará um marcador no mapa.

### ⚙️ Como o Código Funciona (Arquitetura)
O projeto é construído em um único arquivo de página (`index.html`) e utiliza tecnologias *Client-Side* nativas e bibliotecas leves:
* **`JSZip`:** Usado para realizar um `fetch()` do arquivo estático `ILGADATA.zip` hospedado no servidor e extrair o arquivo `.TXT` bruto para a memória sem sobrecarregar a banda do usuário.
* **Motor Baseado em RegEx:** A leitura dos dados de texto não usa bancos SQL. O JavaScript utiliza Expressões Regulares (`RegEx`) para interpretar cada linha do `.TXT`, extraindo cirurgicamente os blocos de Frequência, Indicativo (posição 42-52), Modo, Protocolo e Coordenadas.
* **`Leaflet.js` & Google Hybrid Tiles:** O motor de renderização do mapa utiliza a API gratuita do Leaflet, alimentada com os *tiles* de satélite de alta resolução do Google Maps. O sistema possui lógica de prevenção de erros: se a base de dados não fornecer latitude e longitude para uma estação, o mapa não é acionado e um alerta visual seguro é emitido.
* **Tradução Dinâmica (i18n):** O sistema varre elementos com o atributo `data-i18n` e substitui o texto com base no dicionário (objeto JS) carregado na memória, permitindo trocar o idioma sem recarregar a página (Flicker-free).

---

## 🇺🇸 English

### Overview
The **PP2LA Signal Intelligence System** is a high-performance web tool designed for radio listeners and radio operators. The system allows searching, filtering, and geolocating HF (High Frequency) utility stations.

Built on a *Serverless* architecture, all data processing takes place locally in the user's browser, ensuring near-instant responses and total privacy.

### 🚀 Features
* **Advanced Local Processing:** Reads and unzips the official database (`ILGADATA.zip`) directly into the browser's RAM.
* **Dual-Tab System:**
  * **Scanner:** Focused scanning with frequency, tolerance, mode, and protocol filters.
  * **Full Table:** Mass viewing of the entire database at once, with optimized scrolling.
* **Integrated Geolocation:** Click on any intercept in the table to plot the transmitting antenna's location on a satellite map.
* **Professional Dashboard:** Default Dark Mode for night operations and a responsive design that adapts to desktops, tablets, and smartphones.
* **Multi-language:** Interface available in Portuguese, English, and Spanish, switchable in real-time.

### 📖 How to Use the Interface
1. **Wait for Loading:** Upon opening the site, wait for the green prompt indicating that the `ILGADATA` base has been extracted and loaded.
2. **Specific Search:** On the **ILG Scanner** tab, enter a Center Frequency (e.g., `10150`).
3. **Tolerance Adjustment:** If there is VFO drift, use the "Tolerance" filter to scan, for example, `+/- 2 kHz` around the desired frequency.
4. **Signal Filters:** Isolate emissions by selecting the mode (`Voice`, `Data`, `Morse`) or specific protocols such as `STANAG`, `ALE`, or `NAVTEX`.
5. **Map Plotting:** After clicking "Scan Signals", click on any row in the resulting table. The system will read the coordinates in real-time and drop a pin on the map.

### ⚙️ How the Code Works (Architecture)
The project is built as a single-page application (`index.html`) using native *Client-Side* technologies and lightweight libraries:
* **`JSZip`:** Used to `fetch()` the static `ILGADATA.zip` file hosted on the server and extract the raw `.TXT` file into memory without overloading the user's bandwidth.
* **RegEx-Based Engine:** Text data parsing does not use SQL databases. The JavaScript engine employs Regular Expressions (`RegEx`) to parse each line of the `.TXT` file, surgically extracting blocks of Frequency, Callsign (positions 42-52), Mode, Protocol, and Coordinates.
* **`Leaflet.js` & Google Hybrid Tiles:** The map rendering engine uses the free Leaflet API, powered by high-resolution Google Maps satellite tiles. The system has error-prevention logic: if the database does not provide latitude and longitude for a station, the map is not triggered, and a safe visual alert is displayed.
* **Dynamic Translation (i18n):** The system scans elements with the `data-i18n` attribute and replaces text based on the dictionary (JS object) loaded in memory, allowing language switching without reloading the page (Flicker-free).
