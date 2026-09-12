# 🛡️ SentinelMail — Detector Inteligente de Phishing & Amenazas de Correo

> Un sistema avanzado de análisis defensivo que evalúa la autenticidad, reputación y contenido de correos electrónicos para neutralizar ataques de phishing antes de que afecten a la organización.

---

## 📌 Visión General

El correo electrónico sigue siendo el vector de ataque **#1 en ciberseguridad**. Los ataques de *phishing* modernos ya no son simples mensajes mal redactados; hoy utilizan suplantación de identidad (spoofing), manipulación psicológica (urgencia, miedo) y dominios maliciosos disfrazados para engañar a los usuarios.

**SentinelMail** actúa como un analista de seguridad digital automatizado. Evalúa cada correo entrante desde tres ángulos críticos:
1. **Autenticidad Técnica:** ¿El remitente es realmente quien dice ser?
2. **Reputación de Enlaces:** ¿Los enlaces internos dirigen a sitios seguros o a trampas digitales?
3. **Análisis Lingüístico Heurístico:** ¿El mensaje intenta manipular al usuario para realizar acciones de riesgo?

Al finalizar el análisis, el sistema asigna un **Score de Riesgo Global** y genera alertas visuales e informes ejecutivos claros para la toma de decisiones.

---

## 🚀 Características Principales

* **🔍 Inspección DNS & Autenticación (SPF / DKIM / DMARC):** Detecta la suplantación directa de identidad validando los registros del servidor emisor.
* **🔗 Escáner Heurístico de URLs:** Desenmascara enlaces acortados, redirecciones sospechosas y dominios impostores (typosquatting).
* **🧠 Procesamiento de Lenguaje (NLP & Heurística):** Identifica patrones de urgencia financiera, solicitudes de credenciales o amenazas de suspensión de cuenta.
* **📊 Alerta & Scoring Cuantitativo:** Asigna una escala de riesgo clara (*Bajo, Medio, Alto, Crítico*) junto a un desglose detallado de los hallazgos.
* **📄 Reportes Ejecutivos Automáticos:** Genera informes limpios en HTML/JSON entendibles tanto para equipos de TI como para personal no técnico.

---

## 📸 Demostración Visual & Alertas en Tiempo Real

| Consola de Análisis (CLI) | Reporte Ejecutivo (HTML) | Alerta Móvil (Telegram) |
| :---: | :---: | :---: |
| ![CLI Alert](docs/images/cli_preview.png) | ![HTML Report](docs/images/report_preview.png) | ![Telegram Alert](docs/images/telegram_preview.png) |

---

---

## 📸 Pruebas de Campo con Spam y Phishing Real

SentinelMail fue probado con muestras reales (`.eml`) de campañas de phishing y spam activas, logrando identificar los patrones de ingeniería social, alertas de urgencia e intentos de captura de credenciales:

### Caso 1: Phishing de Suplantación de Servicio (iCloud/Cloud Storage)
* **Score Obtenido:** 60/100 (Severidad ALTA)
* **Detección:** Frases de coerción/urgencia y solicitud de actualización de datos de pago.

![Caso 1 - Phishing de iCloud](data/spam_real.png)

---

### Caso 2: Spam Malicioso / Adultos (Engaño de Citas)
* **Score Obtenido:** 60/100 (Severidad ALTA)
* **Detección:** Patrones de spam explícito y enlaces de redirección a perfiles externos.

![Caso 2 - Spam Malicioso](data/spam_real2.png)

## 🛠️ Arquitectura del Sistema

El flujo de procesamiento sigue un modelo en capas modular:

```text
[ Correo Entrante (.eml / raw) ]
               │
               ▼
 ┌───────────────────────────┐
 │   1. Módulo de Cabeceras  │ ──► Validar SPF, DKIM y DMARC
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │    2. Extractor de URLs   │ ──► Decodificar enlaces y consultar reputación
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │   3. Analizador de Texto  │ ──► Detección de patrones NLP / Gatillos de urgencia
 └─────────────┬─────────────┘
               │
               ▼
 ┌───────────────────────────┐
 │   4. Motor de Riesgo      │ ──► Cálculo del Score de Riesgo (0 - 100)
 └─────────────┬─────────────┘
               │
               ▼
 [ Alerta Generada + Reporte Ejecutivo HTML ]

---

## 📸 Demostración Visual & Reportes

El sistema genera salidas visuales claras para ayudar a los equipos de respuesta a incidentes a actuar rápidamente:

### 1. Consola de Análisis en Tiempo Real
> *(Espacio reservado para captura de pantalla de la terminal analizando un correo .eml)*
*Figura 1: Detección en terminal mostrando el desglose de fallos en SPF y enlaces maliciosos.*

### 2. Reporte Ejecutivo Generado (HTML)
> *(Espacio reservado para captura de pantalla del reporte web/HTML final)*
*Figura 2: Informe interactivo con nivel de severidad en rojo (Alto/Crítico) y recomendaciones tácticas.*

---

## 🚦 Niveles de Severidad y Matriz de Riesgo

SentinelMail clasifica las amenazas en cuatro categorías para facilitar la priorización:

| Nivel | Rango de Score | Descripción / Acción Recomendada |
| :--- | :--- | :--- |
| **🟢 BAJO** | 0 - 25 | Correo legítimo. Pasa los controles de autenticación y no contiene enlaces sospechosos. |
| **🟡 MEDIO** | 26 - 50 | Inconsistencias menores. Requiere precaución (ej. dominio nuevo o lenguaje persuasivo). |
| **🟠 ALTO** | 51 - 75 | Alta probabilidad de phishing. Fallo en firmas digitales o enlaces con redirecciones ocultas. |
| **🔴 CRÍTICO** | 76 - 100 | Amenaza confirmada. Suplantación de identidad directa, enlaces maliciosos o peticiones de credenciales. |

---

## 📁 Estructura del Proyecto

```text
sentinelmail/
│
├── data/                  # Correos de prueba (.eml) y datasets
├── src/                   # Código fuente modular
│   ├── __init__.py
│   ├── headers.py         # Validación de DNS, SPF, DKIM y DMARC
│   ├── links.py           # Extracción y análisis de reputación de URLs
│   ├── nlp_engine.py      # Analizador heurístico de texto y urgencia
│   ├── risk_calculator.py # Motor de puntuación (Scoring)
│   └── reporter.py        # Generador de alertas y reportes HTML/JSON
│
├── tests/                 # Pruebas unitarias
├── .env.example           # Plantilla de claves API (VirusTotal, etc.)
├── .gitignore             # Filtro para carpetas basura y claves privadas
├── LICENSE                # Licencia de código abierto MIT
├── main.py                # Punto de entrada principal del programa
├── requirements.txt       # Dependencias de Python
└── README.md              # Documentación del proyecto

⚡ Instalación y Uso Rápido
Prerrequisitos
Python 3.10 o superior instalado en el sistema.


1. Clonar el repositorio
Bash
git clone [https://github.com/tu-usuario/sentinelmail.git](https://github.com/tu-usuario/sentinelmail.git)
cd sentinelmail

2. Crear un entorno virtual e instalar dependencias
# En Linux/macOS:
python3 -m venv venv
source venv/bin/activate

# En Windows:
python -m venv venv
.venv\Scripts\activate

# Instalar dependencias:
pip install -r requirements.txt

3. Configurar variables de entorno
Copia la plantilla .env.example a un nuevo archivo .env y añade tus claves de API si deseas habilitar la verificación en tiempo real con servicios externos (ej. VirusTotal):
cp .env.example .env

4. Ejecutar un análisis de prueba
python main.py --file data/sample_phishing.eml


⚖️ Licencia
Este proyecto está bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.

👨‍💻 Autor
Creado con pasión por la ciberseguridad y el desarrollo defensivo.

GitHub: @tu-usuario

LinkedIn: Tu Nombre