import sqlite3
from datetime import datetime
import os

class SecurityDatabase:
    """Módulo de base de datos SQLite para almacenar el historial de análisis de amenazas de SentinelMail."""

    def __init__(self, db_path="data/sentinel_history.db"):
        self.db_path = db_path
        self._ensure_directory()
        self._init_db()

    def _ensure_directory(self):
        """Asegura que la carpeta de datos exista."""
        directory = os.path.dirname(self.db_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def _init_db(self):
        """Crea la tabla de historial si no existe."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS scan_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT,
                        sender TEXT,
                        recipient TEXT,
                        subject TEXT,
                        risk_score INTEGER,
                        severity TEXT
                    )
                """)
                conn.commit()
        except Exception as e:
            print(f"❌ [DB Error de inicialización]: {e}")

    def save_scan(self, basic_info, risk_data):
        """Guarda un nuevo registro de análisis en la base de datos."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO scan_history (timestamp, sender, recipient, subject, risk_score, severity)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    timestamp,
                    basic_info.get("sender", "Desconocido"),
                    basic_info.get("recipient", "Desconocido"),
                    basic_info.get("subject", "Sin asunto"),
                    risk_data.get("score", 0),
                    risk_data.get("severity", "BAJO")
                ))
                conn.commit()
            print("💾 [DB] Análisis guardado en el historial histórico con éxito.")
        except Exception as e:
            print(f"❌ [DB Error al guardar registro]: {e}")