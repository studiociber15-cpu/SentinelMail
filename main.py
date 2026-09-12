import argparse
import os
import sys

from src.headers import HeaderAnalyzer
from src.links import LinkAnalyzer
from src.nlp_engine import NLPEngine
from src.risk_calculator import RiskCalculator
from src.reporter import Reporter
from src.notifier import TelegramNotifier
from src.imap_connector import IMAPConnector

def analyze_raw_content(raw_content):
    """Ejecuta todos los motores de análisis de SentinelMail sobre un contenido de correo en crudo."""
    # 1. Análisis de Cabeceras
    header_analyzer = HeaderAnalyzer(raw_content)
    basic_info = header_analyzer.get_basic_info()
    header_results = header_analyzer.analyze_authentication()

    # 2. Análisis de Enlaces (URLs)
    link_analyzer = LinkAnalyzer(raw_content)
    link_results = link_analyzer.analyze_links()

    # 3. Análisis de Texto (NLP & Urgencia)
    nlp_analyzer = NLPEngine(raw_content)
    nlp_results = nlp_analyzer.analyze_sentiment_and_patterns()

    # 4. Cálculo del Risk Score Global
    calculator = RiskCalculator(header_results, link_results, nlp_results)
    risk_data = calculator.calculate_total_risk()

    # 5. Generación de Reportes y Notificación CLI / HTML
    reporter = Reporter(basic_info, risk_data)
    reporter.print_cli_report()
    reporter.generate_html_report()

    # 6. Notificación Móvil (Telegram)
    notifier = TelegramNotifier()
    notifier.send_alert(basic_info, risk_data)

def process_email(file_path):
    """Procesa un archivo .eml individual desde el disco."""
    if not os.path.exists(file_path):
        print(f"❌ Error: El archivo '{file_path}' no existe.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_content = f.read()

    print(f"\n📁 Analizando archivo local: {file_path}")
    analyze_raw_content(raw_content)

def run_live_scanner(mailbox="INBOX"):
    """Conecta al servidor IMAP y escanea los mensajes nuevos en tiempo real."""
    connector = IMAPConnector()
    if connector.connect():
        emails = connector.fetch_unseen_emails(mailbox)
        
        if not emails:
            print("📭 No hay correos nuevos pendientes de análisis.")
        
        for e_id, email_msg in emails:
            print(f"\n🔄 Procesando correo en vivo ID IMAP: {e_id}")
            # Extraer el contenido crudo completo del mensaje IMAP
            raw_content = email_msg.as_string()
            analyze_raw_content(raw_content)
            
        connector.close()

def main():
    parser = argparse.ArgumentParser(description="SentinelMail — Detector Inteligente de Phishing & Amenazas")
    parser.add_argument("--file", type=str, help="Ruta al archivo .eml local a analizar")
    parser.add_argument("--live", action="store_true", help="Conectar al servidor IMAP configurado en .env para escanear en vivo")
    parser.add_argument("--mailbox", type=str, default="INBOX", help="Carpeta IMAP a escanear (ej. INBOX o Spam), por defecto INBOX")
    
    args = parser.parse_args()

    if args.live:
        run_live_scanner(args.mailbox)
    elif args.file:
        process_email(args.file)
    else:
        # Por defecto si no se pasa ningún argumento, intenta buscar una ruta estándar o muestra ayuda
        print("⚠️ Debes especificar un modo de ejecución.")
        print("Ejemplo local: python main.py --file data/spam_real.eml")
        print("Ejemplo en vivo: python main.py --live --mailbox INBOX")

if __name__ == "__main__":
    main()