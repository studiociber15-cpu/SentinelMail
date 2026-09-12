import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TelegramNotifier:
    """Módulo para enviar alertas instantáneas a dispositivos móviles vía Telegram."""

    def __init__(self):
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send_alert(self, basic_info, risk_data):
        """Envía un mensaje formateado si el nivel de riesgo es ALTO o CRÍTICO."""
        # Solo notificar si la amenaza requiere atención urgente (Score > 50)
        if risk_data['score'] <= 50:
            return

        if not self.bot_token or not self.chat_id:
            print("ℹ️ Telegram Notifier: Token o Chat ID no configurados en .env (Omitiendo notificación).")
            return

        message = (
            f"🚨 *ALERTA DE SEGURIDAD — SENTINELMAIL*\n\n"
            f"📧 *Remitente:* `{basic_info.get('from')}`\n"
            f"📌 *Asunto:* {basic_info.get('subject')}\n"
            f"📊 *Score:* {risk_data['score']}/100 ({risk_data['severity']})\n\n"
            f"⚠️ *Recomendación:* {risk_data['recommendation']}\n\n"
            f"🔍 *Hallazgo Clave:* {risk_data['findings'][0] if risk_data['findings'] else 'N/A'}"
        )

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }

        try:
            response = requests.post(url, json=payload, timeout=5)
            if response.status_code == 200:
                print("📱 Alerta móvil enviada con éxito a Telegram.")
            else:
                print(f"⚠️ Error enviando alerta a Telegram: {response.status_code}")
        except Exception as e:
            print(f"⚠️ No se pudo conectar con Telegram: {e}")