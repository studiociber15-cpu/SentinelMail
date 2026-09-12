import re
import requests
from bs4 import BeautifulSoup

class LinkAnalyzer:
    """Módulo avanzado para extraer, seguir redirecciones y analizar enlaces en busca de amenazas."""

    # Dominios de acortadores comunes
    SHORTENER_DOMAINS = ["bit.ly", "t.co", "tinyurl.com", "goo.gl", "ow.ly", "buff.ly", "adf.ly", "is.gd", "lnkd.in"]

    def __init__(self, raw_html_or_text):
        self.raw_content = raw_html_or_text

    def _resolve_url(self, url):
        """Sigue las redirecciones HTTP automáticamente para obtener la URL final."""
        try:
            # Petición HEAD rápida para seguir redirecciones sin descargar todo el contenido
            response = requests.head(url, allow_redirects=True, timeout=3)
            return response.url
        except Exception:
            try:
                # Intento de respaldo con GET si HEAD es bloqueado por el servidor
                response = requests.get(url, allow_redirects=True, timeout=3, stream=True)
                return response.url
            except Exception:
                return url  # Si falla la conexión o el dominio está muerto, retorna el original

    def analyze_links(self):
        """Extrae todas las URLs del correo, detecta acortadores y audita el destino final."""
        soup = BeautifulSoup(self.raw_content, 'html.parser')
        links = []
        
        # 1. Extraer enlaces de etiquetas HTML <a>
        for a in soup.find_all('a', href=True):
            links.append(a['href'])
            
        # 2. Extraer URLs en texto plano mediante expresiones regulares
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        text = soup.get_text()
        text_links = re.findall(url_pattern, text)
        
        all_links = list(set(links + text_links))
        analyzed_links = []
        link_penalties = 0

        for link in all_links:
            is_shortened = any(domain in link.lower() for domain in self.SHORTENER_DOMAINS)
            final_destination = self._resolve_url(link) if (is_shortened or "http" in link) else link
            
            # Verificaciones de seguridad sobre el destino final
            has_https = final_destination.startswith("https://")
            has_ip = bool(re.search(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', final_destination))

            status = "Seguro"
            if not has_https:
                status = "Inseguro (HTTP plano)"
                link_penalties += 5
            if has_ip:
                status = "Peligroso (Usa dirección IP directa)"
                link_penalties += 15
            if is_shortened:
                status = f"Acortado -> Redirige a: {final_destination}"
                link_penalties += 10

            analyzed_links.append({
                "original": link,
                "final": final_destination,
                "is_shortened": is_shortened,
                "status": status
            })

        return {
            "total_links": len(all_links),
            "analyzed_links": analyzed_links,
            "penalty": min(link_penalties, 40)
        }