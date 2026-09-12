# ⚙️ Guía de Configuración Rápida — SentinelMail

Esta guía te muestra paso a paso cómo configurar tus credenciales de correo (Gmail / Outlook) y tu bot de Telegram para usar el escaneo en tiempo real de **SentinelMail**.

---

## 🔑 1. ¿Cómo obtener la Contraseña de Aplicación (App Password)?

Por seguridad, los proveedores de correo no permiten usar tu contraseña personal en scripts externos. Debes generar una clave especial de 16 dígitos.

### Para Gmail:
1. Ve a tu cuenta de Google en [myaccount.google.com](https://myaccount.google.com).
2. En el menú de la izquierda, haz clic en **Seguridad y acceso**.
3. Asegúrate de tener activada la **Verificación en 2 pasos** (si está desactivada, el sistema no te dejará crear la contraseña).
4. Una vez activa, busca en la barra superior **"Contraseñas de aplicaciones"** o entra directamente a la sección de seguridad avanzada.
5. Asigna un nombre (ej. *SentinelMail*) y haz clic en **Generar**.
6. Copia la clave de 16 caracteres que te aparecerá en pantalla.

### Para Outlook / Hotmail:
1. Inicia sesión en [account.microsoft.com/security](https://account.microsoft.com/security).
2. Entra en **Opciones de seguridad avanzadas**.
3. Busca el apartado de **Contraseñas de aplicaciones** y crea una nueva.
4. Copia la contraseña generada.

---

## 🛠️ 2. Dónde colocar los datos (Archivo .env)

1. En la carpeta raíz de tu proyecto `sentinelmail`, busca el archivo de ejemplo llamado .env.example.
2. Duplica ese archivo y cámbiale el nombre a **.env** (sin la palabra *example*).
3. Ábrelo con un editor (como Bloc de notas o VS Code) y pega tus credenciales de la siguiente manera:

```env
# Configuración IMAP para Gmail o Outlook
IMAP_SERVER=imap.gmail.com        # (o imap-mail.outlook.com para Hotmail/Outlook)
IMAP_PORT=993
IMAP_USER=tu_correo@gmail.com
IMAP_PASSWORD=abcd efgh ijkl mnop   # Pega aquí tu contraseña de aplicación de 16 caracteres

🤖 3. ¿Cómo configurar el Bot de Telegram para las alertas?
Para recibir notificaciones automáticas en tu teléfono cuando SentinelMail detecte un correo peligroso:

Abre Telegram y busca al usuario @BotFather.

Envíale el comando /newbot, asígnale un nombre a tu bot y un nombre de usuario (ej. MiSentinelBot).

BotFather te dará un Token HTTP (ej. 123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ). Ese es tu TELEGRAM_BOT_TOKEN.

Para obtener tu ID numérico personal de chat, busca en Telegram al bot @userinfobot y envíale un mensaje cualquiera; te devolverá tu ID (ej. 987654321). Ese es tu TELEGRAM_CHAT_ID.

Copia ambos valores en tu archivo .env tal como se mostró en el paso anterior.

# Configuración de Alertas en Telegram (Paso 3)
TELEGRAM_BOT_TOKEN=tu_token_aqui
TELEGRAM_CHAT_ID=tu_chat_id_aqui

🚀 4. ¡Listo a Ejecutar!
Una vez configurado tu archivo .env, ya puedes correr el sistema en vivo en tu terminal:

Bash
python main.py --live --mailbox INBOX