import os
from colorama import Fore, Style, init

# Inicializar colorama para compatibilidad con Windows/Linux
init(autoreset=True)

class Reporter:
    """Generador de visualizaciones en consola e informes ejecutivos en HTML."""

    def __init__(self, basic_info, risk_data):
        self.info = basic_info
        self.risk = risk_data

    def print_cli_report(self):
        """Imprime el análisis en consola con código de colores."""
        print("\n" + "=" * 65)
        print(Fore.CYAN + Style.BRIGHT + " 🛡️  SENTINELMAIL — REPORTES DE ANÁLISIS DE SEGURIDAD")
        print("=" * 65)
        print(f"📧 Remitente : {self.info.get('from')}")
        print(f"📥 Destino    : {self.info.get('to')}")
        print(f"📌 Asunto     : {self.info.get('subject')}")
        print(f"📅 Fecha      : {self.info.get('date')}")
        print("-" * 65)

        # Determinar color según severidad
        color_attr = getattr(Fore, self.risk['color_code'], Fore.WHITE)
        print(f"📊 Score de Riesgo : {color_attr}{Style.BRIGHT}{self.risk['score']}/100")
        print(f"🚨 Severidad       : {color_attr}{Style.BRIGHT}{self.risk['severity']}")
        print(f"💡 Recomendación   : {self.risk['recommendation']}")
        print("-" * 65)
        print(Style.BRIGHT + "🔍 Hallazgos Principales:")
        for finding in self.risk['findings']:
            print(f"  • {finding}")
        print("=" * 65 + "\n")

    def generate_html_report(self, output_path="data/reporte_ejecutivo.html"):
        """Genera un archivo HTML visual para presentación o auditoría."""
        html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Análisis — SentinelMail</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f6f9; margin: 0; padding: 20px; }}
        .card {{ background: #ffffff; border-radius: 8px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 700px; margin: auto; }}
        .header {{ border-bottom: 2px solid #eaedf2; padding-bottom: 15px; margin-bottom: 20px; }}
        .header h2 {{ margin: 0; color: #1e293b; }}
        .score-box {{ background-color: #f8fafc; border-left: 5px solid #0284c7; padding: 15px; margin: 20px 0; border-radius: 4px; }}
        .findings-list {{ list-style-type: none; padding-left: 0; }}
        .findings-list li {{ padding: 8px 0; border-bottom: 1px solid #f1f5f9; }}
    </style>
</head>
<body>
    <div class="card">
        <div class="header">
            <h2>🛡️ SentinelMail — Informe Ejecutivo</h2>
            <p><strong>Asunto:</strong> {self.info.get('subject')}</p>
        </div>
        <p><strong>De:</strong> {self.info.get('from')}</p>
        <p><strong>Para:</strong> {self.info.get('to')}</p>
        <div class="score-box">
            <h3>Nivel de Riesgo: {self.risk['severity']} ({self.risk['score']}/100)</h3>
            <p><strong>Recomendación:</strong> {self.risk['recommendation']}</p>
        </div>
        <h4>Desglose de Hallazgos:</h4>
        <ul class="findings-list">
            {"".join([f"<li>{item}</li>" for item in self.risk['findings']])}
        </ul>
    </div>
</body>
</html>"""
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(Fore.GREEN + f"📄 Reporte HTML generado exitosamente en: {output_path}")