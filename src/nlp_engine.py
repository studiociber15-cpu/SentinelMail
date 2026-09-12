import re
from bs4 import BeautifulSoup

class NLPEngine:
    """Módulo de análisis de texto para detectar urgencia, coerción, contenido de adultos y phishing."""

    # 1. Frases de urgencia, presión y suplantación (Ampliado)
    URGENCY_KEYWORDS = [
        # Español (30+ palabras clave)
        "suspendida", "bloqueada", "inmediato", "24 horas", "urgente",
        "verificar cuenta", "pago rechazado", "eliminar datos", "accion requerida",
        "cuenta restringida", "expira hoy", "evitar la suspension", "tiempo limite",
        "ultima oportunidad", "confirmar identidad", "acceso inusual", "intento de acceso",
        "desactivacion de cuenta", "cancelacion inminente", "actualice antes de",
        "bloqueo preventivo", "multa por mora", "notificacion final", "renovar suscripcion",
        "vence hoy", "plazo vencido", "seguridad comprometida", "verificacion obligatoria",
        "regularizar cuenta", "accion inmediata requerida", "advertencia de seguridad",

        # Inglés (30+ palabras clave)
        "blocked", "deleted", "renew", "subscription", "update payment",
        "unable to renew", "lose all your stored data", "free now", "cloud storage",
        "account blocked", "expiration date", "tonight only", "action required",
        "immediate action", "account closure", "account suspended", "expires today",
        "unusual activity", "security alert", "final notice", "prevent suspension",
        "confirm identity", "verify immediately", "time sensitive", "unauthorized access",
        "last chance", "account limited", "update required", "service disruption",
        "urgent notification", "failure to respond", "deactivation notice", "compromised account"
    ]

    # 2. Captura de credenciales y acceso
    CREDENTIAL_TRIGGERS = [
        # Español
        "verifique su identidad", "actualice su clave", "ingrese sus datos",
        "confirme su tarjeta", "restablecer contraseña", "iniciar sesion",
        # Inglés
        "verify your account", "update password", "confirm details", "login",
        "sign in", "reset password", "update my payment information", "join my profile"
    ]

    # 3. Alertas financieras, loterías y engaños monetarios
    FINANCIAL_TRIGGERS = [
        # Español
        "cargo no autorizado", "transaccion sospechosa", "reembolso pendiente",
        "premio ganado", "multa", "factura vencida", "herencia", "donacion",
        # Inglés
        "unauthorized transaction", "claim your prize", "refund pending",
        "lottery winner", "inheritance", "transfer money", "free gift"
    ]

    # 4. Contenido de Adultos / Dating / Spam explícito
    ADULT_SPAM_TRIGGERS = [
        # Inglés
        "lover", "p**ssy", "pussy", "sex", "sexy", "hot girls", "video call now",
        "bed partner", "single girls", "hookup", "nudes", "uploaded picture",
        "sweetheart", "meet tonight", "cam girl",
        # Español
        "chicas calientes", "video llamada", "citas", "fotos intimas", "encuentro casual"
    ]

    def __init__(self, raw_html_or_text):
        self.raw_content = raw_html_or_text
        self.clean_text = self._extract_clean_text()

    def _extract_clean_text(self):
        """Limpia etiquetas HTML y pasa el texto a minúsculas para evaluar."""
        soup = BeautifulSoup(self.raw_content, 'html.parser')
        text = soup.get_text(separator=' ')
        return ' '.join(text.split()).lower()

    def analyze_sentiment_and_patterns(self):
        """Escanea el contenido del correo buscando patrones de ingeniería social y spam."""
        findings = []
        risk_score_penalty = 0

        # 1. Análisis de Gatillos de Urgencia/Miedo
        urgency_hits = [phrase for phrase in self.URGENCY_KEYWORDS if phrase in self.clean_text]
        if urgency_hits:
            findings.append(f"⚠️ Lenguaje de Urgencia: Detectadas frases de presión ({', '.join(urgency_hits)})")
            risk_score_penalty += len(urgency_hits) * 10

        # 2. Solicitud de Credenciales / Registro
        credential_hits = [phrase for phrase in self.CREDENTIAL_TRIGGERS if phrase in self.clean_text]
        if credential_hits:
            findings.append(f"❌ Petición de Datos/Acceso: Intento de captura o registro ({', '.join(credential_hits)})")
            risk_score_penalty += len(credential_hits) * 15

        # 3. Alertas Financieras / Engaño monetario
        financial_hits = [phrase for phrase in self.FINANCIAL_TRIGGERS if phrase in self.clean_text]
        if financial_hits:
            findings.append(f"⚠️ Alerta Financiera: Mención de transacciones o cobros ({', '.join(financial_hits)})")
            risk_score_penalty += len(financial_hits) * 10

        # 4. Spam de Adultos / Dating
        adult_hits = [phrase for phrase in self.ADULT_SPAM_TRIGGERS if phrase in self.clean_text]
        if adult_hits:
            findings.append(f"🔞 Spam de Adultos / Malicioso: Coincidencias explícitas ({', '.join(adult_hits)})")
            risk_score_penalty += len(adult_hits) * 20

        if not (urgency_hits or credential_hits or financial_hits or adult_hits):
            findings.append("✅ Contenido: No se detectaron patrones lingüísticos de persuasión o coerción.")

        return {
            "findings": findings,
            "penalty": min(risk_score_penalty, 60)  # Límite máximo de penalización subido a 60
        }