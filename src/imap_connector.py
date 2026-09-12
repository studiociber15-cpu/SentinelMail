import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

load_dotenv()

class IMAPConnector:
    """Módulo para conectar SentinelMail directamente a servidores de correo corporativos (Gmail, Outlook, IMAP)."""

    def __init__(self):
        self.server_host = os.getenv("IMAP_SERVER")
        self.port = int(os.getenv("IMAP_PORT", 993))
        self.username = os.getenv("IMAP_USER")
        self.password = os.getenv("IMAP_PASSWORD")
        self.mail = None

    def connect(self):
        """Establece conexión segura SSL con el servidor de correo."""
        try:
            if not all([self.server_host, self.username, self.password]):
                print("⚠️ [IMAP] Faltan credenciales IMAP en el archivo .env")
                return False
            
            print(f"🔌 Conectando a {self.server_host}...")
            self.mail = imaplib.IMAP4_SSL(self.server_host, self.port)
            self.mail.login(self.username, self.password)
            print("✅ [IMAP] Conexión establecida con éxito.")
            return True
        except Exception as e:
            print(f"❌ [IMAP Error de conexión]: {e}")
            return False

    def fetch_unseen_emails(self, mailbox="INBOX"):
        """Busca y descarga correos no leídos para su análisis en tiempo real."""
        if not self.mail:
            print("⚠️ No hay conexión activa al servidor IMAP.")
            return []

        unseen_emails = []
        try:
            self.mail.select(mailbox)
            status, messages = self.mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                return []

            email_ids = messages[0].split()
            print(f"📥 Se encontraron {len(email_ids)} correo(s) nuevo(s) en '{mailbox}'.")

            for e_id in email_ids:
                res, msg_data = self.mail.fetch(e_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        unseen_emails.append((e_id, msg))
            
            return unseen_emails
        except Exception as e:
            print(f"❌ [IMAP Error al descargar correos]: {e}")
            return []

    def close(self):
        """Cierra la sesión IMAP de forma segura."""
        try:
            if self.mail:
                self.mail.logout()
                print("🔒 [IMAP] Sesión cerrada correctamente.")
        except:
            pass