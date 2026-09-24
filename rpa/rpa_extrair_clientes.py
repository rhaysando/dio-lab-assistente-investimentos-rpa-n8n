# RPA: extrai clientes da pagina HTML (GitHub Pages) e envia ao webhook do n8n
# Rodar no Google Colab: !pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup

URL_CLIENTES = "https://digitalinnovationone.github.io/dio-lab-assistente-investimentos-rpa-n8n/"  # troque pelo seu fork
N8N_WEBHOOK_URL = "https://SEU-N8N/webhook-test/clientes"               # URL de teste ou producao

def extrair_clientes(url):
    html = requests.get(url, timeout=30).text
    soup = BeautifulSoup(html, "html.parser")
    tabela = soup.find("table", id="clientes") or soup.find("table")
    cab = [th.get_text(strip=True).lower() for th in tabela.find_all("th")]
    clientes = []
    for tr in tabela.find_all("tr")[1:]:
        cels = [td.get_text(strip=True) for td in tr.find_all("td")]
        if len(cels) != len(cab):
            continue
        c = dict(zip(cab, cels))
        saldo = c.get("saldo", "0").replace("R$", "").replace(".", "").replace(",", ".").strip()
        c["saldo"] = float(saldo or 0)
        clientes.append(c)
    return clientes

if __name__ == "__main__":
    clientes = extrair_clientes(URL_CLIENTES)
    print(f"{len(clientes)} clientes extraidos")
    r = requests.post(N8N_WEBHOOK_URL, json={"clientes": clientes}, timeout=120)
    print("Status:", r.status_code)
    print(r.text[:1000])
