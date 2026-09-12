import re
from bs4 import BeautifulSoup

class NLPEngine:
    """Módulo de análisis de texto para detectar urgencia, coerción y frases de phishing."""

    # Patrones de palabras/frases clasificadas por categoría de riesgo
    URGENCY_TRIGGERS = [
        "urgente", "inmediato", "accion requerida", "cuenta suspendida", 
        "bloqueo permanente", "24 horas", "evite el cierre", "atencion inmediata",
        "urgent", "immediate action", "account suspended", "limited time"
    ]

    CREDENTIAL_TRIGGERS = [
        "verifique su identidad", "actualice su clave", "ingrese sus datos",
        "confirme su tarjeta", "restablecer contraseña", "login", 
        "verify your account", "update password", "confirm details"
    ]

    FINANCIAL_TRIGGERS = [
        "cargo no autorizado", "transaccion sospechosa", "reembolso pendiente",
        "premio ganado", "multa", "factura vencida", "unauthorized transaction"
    ]

    def __init__(self, raw_html_or_text):
        self.raw_content = raw_html_or_text
        self.clean_text = self._extract_clean_text()

    def _extract_clean_text(self):
        """Limpia las etiquetas HTML y obtiene solo el texto plano en minúsculas."""
        soup = BeautifulSoup(self.raw_content, 'html.parser')
        text = soup.get_text(separator=' ')
        return ' '.join(text.split()).lower()

    def analyze_sentiment_and_patterns(self):
        """Escanea el contenido del correo buscando patrones de ingeniería social."""
        findings = []
        risk_score_penalty = 0

        # 1. Análisis de Gatillos de Urgencia/Miedo
        urgency_hits = [phrase for phrase in self.URGENCY_TRIGGERS if phrase in self.clean_text]
        if urgency_hits:
            findings.append(f"⚠️ Lenguaje de Urgencia: Detectadas frases de presión ({', '.join(urgency_hits)})")
            risk_score_penalty += len(urgency_hits) * 10

        # 2. Solicitation de Credenciales
        credential_hits = [phrase for phrase in self.CREDENTIAL_TRIGGERS if phrase in self.clean_text]
        if credential_hits:
            findings.append(f"❌ Petición de Datos: Intento de captura de credenciales ({', '.join(credential_hits)})")
            risk_score_penalty += len(credential_hits) * 15

        # 3. Alertas Financieras / Engaño monetario
        financial_hits = [phrase for phrase in self.FINANCIAL_TRIGGERS if phrase in self.clean_text]
        if financial_hits:
            findings.append(f"⚠️ Alerta Financiera: Mención de transacciones o cobros ({', '.join(financial_hits)})")
            risk_score_penalty += len(financial_hits) * 10

        if not (urgency_hits or credential_hits or financial_hits):
            findings.append("✅ Contenido: No se detectaron patrones lingüísticos de persuasión o coerción.")

        return {
            "findings": findings,
            "penalty": min(risk_score_penalty, 40)  # Límite máximo de penalización por texto
        }