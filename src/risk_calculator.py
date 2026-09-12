class RiskCalculator:
    """Consolida las métricas de todos los módulos y calcula el nivel global de amenaza."""

    def __init__(self, header_results, link_results, nlp_results):
        self.header_results = header_results
        self.link_results = link_results
        self.nlp_results = nlp_results

    def calculate_total_risk(self):
        """Calcula el score numérico total de 0 a 100 y asigna el nivel de severidad."""
        h_penalty = self.header_results.get("penalty", 0)
        l_penalty = self.link_results.get("penalty", 0)
        n_penalty = self.nlp_results.get("penalty", 0)

        # Suma ponderada de penalizaciones
        total_score = min(h_penalty + l_penalty + n_penalty, 100)

        # Determinación del nivel de severidad según la matriz del README
        if total_score <= 25:
            severity = "🟢 BAJO"
            color_code = "GREEN"
            recommendation = "Correo aparentemente legítimo. Pasar controles estándar."
        elif total_score <= 50:
            severity = "🟡 MEDIO"
            color_code = "YELLOW"
            recommendation = "Precaución. Inconsistencias menores detectadas en el remitente o texto."
        elif total_score <= 75:
            severity = "🟠 ALTO"
            color_code = "LIGHTRED_EX"
            recommendation = "Alta probabilidad de phishing. No hacer clic en enlaces ni descargar adjuntos."
        else:
            severity = "🔴 CRÍTICO"
            color_code = "RED"
            recommendation = "AMENAZA CONFIRMADA. Intento activo de suplantación de identidad o engaño."

        # Unificar todos los hallazgos para el reporte
        all_findings = (
            self.header_results.get("findings", []) +
            self.link_results.get("findings", []) +
            self.nlp_results.get("findings", [])
        )

        return {
            "score": total_score,
            "severity": severity,
            "color_code": color_code,
            "recommendation": recommendation,
            "findings": all_findings
        }