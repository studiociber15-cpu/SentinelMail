import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup

class LinkAnalyzer:
    """Módulo para extraer y evaluar la reputación/riesgo de los enlaces dentro de un correo."""

    # Palabras clave sospechosas en dominios imitación
    SUSPICIOUS_KEYWORDS = ["login", "verify", "secure", "update", "account", "banco", "soporte", "signin"]

    # Lista de acortadores conocidos
    URL_SHORTENERS = ["bit.ly", "tinyurl.com", "goo.gl", "is.gd", "buff.ly", "ow.ly", "t.co"]

    def __init__(self, raw_html_or_text):
        self.raw_content = raw_html_or_text

    def extract_urls(self):
        """Extrae todas las URLs tanto del HTML como del texto plano."""
        urls = set()
        
        # 1. Extraer enlaces desde etiquetas <a> en HTML
        soup = BeautifulSoup(self.raw_content, 'html.parser')
        for a_tag in soup.find_all('a', href=True):
            urls.add(a_tag['href'])

        # 2. Extraer URLs mediante expresiones regulares (por si hay texto plano)
        regex_urls = re.findall(r'https?://[^\s<>"]+|www\.[^\s<>"]+', self.raw_content)
        for url in regex_urls:
            urls.add(url)

        return list(urls)

    def analyze_links(self):
        """Evalúa cada URL encontrada y determina factores de riesgo."""
        urls = self.extract_urls()
        findings = []
        risk_score_penalty = 0

        if not urls:
            return {
                "urls_found": [],
                "findings": ["ℹ️ Enlaces: No se detectaron URLs en el cuerpo del correo."],
                "penalty": 0
            }

        findings.append(f"🔗 Enlaces: Se encontraron {len(urls)} enlace(s) para análisis.")

        for url in urls:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()

            # 1. Detección de uso de dirección IP directa en lugar de dominio
            if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', domain):
                findings.append(f"❌ Riesgo Crítico: Enlace usa dirección IP directa en lugar de dominio ({url})")
                risk_score_penalty += 30

            # 2. Detección de acortadores de URLs (Ocultamiento de destino)
            if any(shortener in domain for shortener in self.URL_SHORTENERS):
                findings.append(f"⚠️ Advertencia: Uso de acortador de URL para ocultar destino ({domain})")
                risk_score_penalty += 15

            # 3. Detección de palabras clave de engaño (Typosquatting / Spoofing)
            for kw in self.SUSPICIOUS_KEYWORDS:
                if kw in domain and not domain.endswith((".com", ".net", ".org", ".gob.ve", ".co")):
                    findings.append(f"⚠️ Dominio Sospechoso: Contiene palabra clave de trampa '{kw}' ({domain})")
                    risk_score_penalty += 20
                    break

        return {
            "urls_found": urls,
            "findings": findings,
            "penalty": min(risk_score_penalty, 50)  # Límite máximo de penalización por enlaces
        }