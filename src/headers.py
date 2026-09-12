import email
from email.header import decode_header
import re

class HeaderAnalyzer:
    """Módulo para extraer y analizar las cabeceras de autenticación de un correo."""

    def __init__(self, raw_email_content):
        self.msg = email.message_from_string(raw_email_content)

    def decode_str(self, header_value):
        """Decodifica cabeceras que contienen caracteres especiales o codificaciones MIME."""
        if not header_value:
            return ""
        decoded_list = decode_header(header_value)
        header_text = ""
        for bytes_or_str, encoding in decoded_list:
            if isinstance(bytes_or_str, bytes):
                header_text += bytes_or_str.decode(encoding or 'utf-8', errors='ignore')
            else:
                header_text += bytes_or_str
        return header_text

    def get_basic_info(self):
        """Extrae la información elemental del remite, destinatario y asunto."""
        return {
            "from": self.decode_str(self.msg.get("From")),
            "to": self.decode_str(self.msg.get("To")),
            "subject": self.decode_str(self.msg.get("Subject")),
            "date": self.decode_str(self.msg.get("Date"))
        }

    def analyze_authentication(self):
        """
        Analiza las verificaciones Authentication-Results y Received-SPF
        para identificar fallos en SPF, DKIM o DMARC.
        """
        auth_results = self.msg.get("Authentication-Results", "").lower()
        received_spf = self.msg.get("Received-SPF", "").lower()

        findings = []
        risk_score_penalty = 0

        # Validación SPF (Sender Policy Framework)
        if "spf=pass" in auth_results or "pass" in received_spf:
            findings.append("✅ SPF: Validación Correcta (Pass)")
        elif "spf=fail" in auth_results or "fail" in received_spf:
            findings.append("❌ SPF: FALLO DE AUTENTICACIÓN (Posible Spoofing)")
            risk_score_penalty += 35
        elif "spf=softfail" in auth_results:
            findings.append("⚠️ SPF: Softfail (Servidor no autorizado explícitamente)")
            risk_score_penalty += 15
        else:
            findings.append("ℹ️ SPF: Sin registros de autenticación explícitos")
            risk_score_penalty += 10

        # Validación DKIM (DomainKeys Identified Mail)
        if "dkim=pass" in auth_results:
            findings.append("✅ DKIM: Firma digital válida (Pass)")
        elif "dkim=fail" in auth_results:
            findings.append("❌ DKIM: Firma digital INVÁLIDA o alterada")
            risk_score_penalty += 25

        # Validación DMARC
        if "dmarc=pass" in auth_results:
            findings.append("✅ DMARC: Política cumplida (Pass)")
        elif "dmarc=fail" in auth_results:
            findings.append("❌ DMARC: Fallo en alineación de dominio")
            risk_score_penalty += 25

        return {
            "findings": findings,
            "penalty": risk_score_penalty
        }