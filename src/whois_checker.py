import whois
from datetime import datetime

class DomainAgeChecker:
    """Módulo para verificar la antigüedad del dominio del remitente mediante consultas WHOIS."""

    def __init__(self, sender_email):
        self.sender_email = sender_email

    def _extract_domain(self):
        """Extrae el dominio del correo del remitente."""
        try:
            if "@" in self.sender_email:
                return self.sender_email.split("@")[1].strip(">");
            return ""
        except Exception:
            return ""

    def check_domain_age(self):
        """Consulta la fecha de creación del dominio y evalúa si es un riesgo por reciente creación."""
        domain = self._extract_domain()
        if not domain:
            return {"penalty": 0, "finding": None}

        try:
            w = whois.whois(domain)
            creation_date = w.creation_date

            # Si devuelve una lista de fechas, tomamos la primera
            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            if not creation_date:
                return {
                    "penalty": 5,
                    "finding": f"⚠️ WHOIS: No se pudo verificar la fecha de creación exacta para '{domain}'. (Posible anonimización)"
                }

            # Calcular la antigüedad en días
            age_days = (datetime.now() - creation_date).days
            penalty = 0
            finding = ""

            if age_days < 30:
                penalty = 25
                finding = f"❌ Dominio de Reciente Creación: El dominio '{domain}' tiene menos de 30 días de vida ({age_days} días)."
            elif age_days < 90:
                penalty = 15
                finding = f"⚠️ Dominio Joven: El dominio '{domain}' fue registrado hace poco ({age_days} días)."
            else:
                finding = f"✅ Dominio Consolidado: El dominio '{domain}' tiene una antigüedad segura ({age_days} días)."

            return {
                "penalty": penalty,
                "finding": finding
            }

        except Exception as e:
            # Si el servidor WHOIS bloquea la petición temporalmente, no rompemos el flujo general
            return {
                "penalty": 5,
                "finding": f"⚠️ WHOIS: Restricción temporal al consultar el dominio '{domain}'."
            }