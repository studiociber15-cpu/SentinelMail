import argparse
import os
import sys

from src.headers import HeaderAnalyzer
from src.links import LinkAnalyzer
from src.nlp_engine import NLPEngine
from src.risk_calculator import RiskCalculator
from src.reporter import Reporter
from src.notifier import TelegramNotifier

def process_email(file_path):
    """Procesa un archivo .eml individual y genera los reportes correspondientes."""
    if not os.path.exists(file_path):
        print(f"❌ Error: El archivo '{file_path}' no existe.")
        sys.exit(1)

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        raw_content = f.read()

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

    # 5. Generación de Reportes y Notificación
    reporter = Reporter(basic_info, risk_data)
    reporter.print_cli_report()
    reporter.generate_html_report()

    # 6. Notificación Móvil
    notifier = TelegramNotifier()
    notifier.send_alert(basic_info, risk_data)

def main():
    parser = argparse.ArgumentParser(description="SentinelMail — Detector Inteligente de Phishing")
    parser.add_argument("--file", type=str, default="data/phishing_email.eml", help="Ruta al archivo .eml a analizar")
    args = parser.parse_args()

    process_email(args.file)

if __name__ == "__main__":
    main()