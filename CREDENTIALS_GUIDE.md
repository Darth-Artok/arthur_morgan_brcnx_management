# Guía de Configuración de Credenciales para Artok IA Viral Studio

## 📋 Descripción General

El archivo `main.py` ha sido actualizado para soportar múltiples plataformas sociales sin depender de Google Cloud. Ahora puedes integrar:

- **YouTube** (YouTube Data API v3)
- **TikTok** (TikTok Business API)
- **Facebook** (Facebook Graph API v18.0+)
- **Instagram** (Instagram Graph API v18.0+)

Todas las credenciales se cargan de forma **segura** desde variables de entorno.

---

## 🔐 Gestión Segura de Credenciales

### 1. Sistema de Variables de Entorno

El proyecto utiliza un sistema de carga de variables de entorno desde archivo `.env`:

```python
def load_env_file(env_path: str = ".env"):
	"""Carga variables de entorno desde archivo .env"""
	# ...
```

### 2. Archivo .env (LOCAL)

**NUNCA hagas commit de este archivo.** Debe estar en `.gitignore`

```
USE_EXTERNAL_APIS=False
MANUAL_BILLING=True

# YouTube
YOUTUBE_API_KEY=tu_clave_aqui

# TikTok
TIKTOK_CLIENT_KEY=tu_clave_aqui
TIKTOK_CLIENT_SECRET=tu_secreto_aqui
TIKTOK_ACCESS_TOKEN=tu_token_aqui

# Facebook
FACEBOOK_PAGE_ID=tu_id_pagina_aqui
FACEBOOK_ACCESS_TOKEN=tu_token_aqui
FACEBOOK_APP_ID=tu_app_id_aqui
FACEBOOK_APP_SECRET=tu_app_secret_aqui

# Instagram
INSTAGRAM_BUSINESS_ACCOUNT_ID=tu_id_aqui
INSTAGRAM_ACCESS_TOKEN=tu_token_aqui
INSTAGRAM_APP_ID=tu_app_id_aqui
INSTAGRAM_APP_SECRET=tu_app_secret_aqui
```

### 3. Archivo .env.example (PLANTILLA)

Compartir este archivo con el equipo como referencia. Contiene la estructura pero sin valores reales.

---

## 🚀 Pasos de Configuración

### Para Modo Local/Simulado (Recomendado para desarrollo)

```bash
# 1. Copia el archivo de ejemplo
cp .env.example .env

# 2. Deja las credenciales vacías o con USE_EXTERNAL_APIS=False
USE_EXTERNAL_APIS=False

# 3. Ejecuta el proyecto
python main.py
```

**Resultado:** El sistema funciona en modo simulado sin hacer llamadas reales a APIs.

---

### Para Modo Conectado (Producción)

#### 📺 YouTube

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto
3. Habilita **YouTube Data API v3**
4. Crea una credencial de tipo **API Key**
5. Copia la clave en tu `.env`:

```
YOUTUBE_API_KEY=AIzaSyD...tu_clave_completa
```

#### 🎵 TikTok

1. Ve a [TikTok Developers](https://developers.tiktok.com/)
2. Crea una aplicación de negocio
3. Solicita permisos de **Content Posting API**
4. Obtén:
   - `Client Key`
   - `Client Secret`
   - `Access Token`

```
TIKTOK_CLIENT_KEY=abc123...
TIKTOK_CLIENT_SECRET=xyz789...
TIKTOK_ACCESS_TOKEN=token_aqui
```

#### 📱 Facebook

1. Ve a [Facebook Developers](https://developers.facebook.com/)
2. Crea una aplicación
3. Habilita **Graph API**
4. Obtén el **Token de Acceso de Página**:
   - Ve a Mi App → Herramientas → **Explorador de Graph**
   - Selecciona tu página
   - Genera token
5. Obtén el **ID de Página** (visible en configuración)

```
FACEBOOK_PAGE_ID=123456789
FACEBOOK_ACCESS_TOKEN=EAABs...token_largo
FACEBOOK_APP_ID=app_id
FACEBOOK_APP_SECRET=app_secret
```

#### 📸 Instagram

1. **Requisito:** Cuenta de negocio de Instagram vinculada a Facebook
2. En Facebook Developers, usa la misma aplicación
3. Obtén el **ID de Business Account de Instagram**
4. Genera **Access Token** con permisos:
   - `instagram_business_content_publish`
   - `instagram_basic`

```
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841407663...
INSTAGRAM_ACCESS_TOKEN=EAABs...token_largo
INSTAGRAM_APP_ID=app_id
INSTAGRAM_APP_SECRET=app_secret
```

---

## 🏗️ Arquitectura de Conectores

### Clases Principales

#### `CredentialsManager`
Gestor centralizado que carga credenciales desde variables de entorno:

```python
# Cargar credenciales de una plataforma
creds = CredentialsManager.load_tiktok_credentials()
# Devuelve: {"client_key": "...", "client_secret": "...", "access_token": "..."}

# Validar que existan
is_valid = CredentialsManager.validate_credentials(creds, "TikTok")
```

#### `YouTubeConnector`
```python
connector = YouTubeConnector(logger)
result = connector.publish_video(payload)
# Devuelve: {"platform": "YouTube", "status": "SUCCESS/SIMULATED", "video_id": "...", ...}
```

#### `TikTokConnector`
```python
connector = TikTokConnector(logger)
result = connector.publish_video(payload)
```

#### `FacebookConnector` (NUEVO)
```python
connector = FacebookConnector(logger)
result = connector.publish_media(payload)
```

#### `InstagramConnector` (NUEVO)
```python
connector = InstagramConnector(logger)
result = connector.publish_media(payload)
```

---

## 📊 Modo de Operación

### Flag: `USE_EXTERNAL_APIS`

**`USE_EXTERNAL_APIS = False` (RECOMENDADO para desarrollo)**
- No hace llamadas reales a APIs
- Las respuestas tienen `status: "SIMULATED"`
- Las URLs son locales (ej: `https://youtube.local/simulated/...`)

**`USE_EXTERNAL_APIS = True` (Requiere credenciales válidas)**
- Hace llamadas reales a las APIs
- Las respuestas tienen `status: "SUCCESS" o "FAILED"`

---

## 🔄 Flujo de Uso en main.py

```python
# 1. Las variables de entorno se cargan automáticamente
load_env_file()  # Carga desde .env

# 2. JohnMarstonCore (Kernel) carga credenciales
john_marston = JohnMarstonCore()
# Internamente:
#   - youtube_creds = CredentialsManager.load_youtube_credentials()
#   - tiktok_creds = CredentialsManager.load_tiktok_credentials()
#   - facebook_creds = CredentialsManager.load_facebook_credentials()
#   - instagram_creds = CredentialsManager.load_instagram_credentials()

# 3. Se instancian los conectores
yt_connector = YouTubeConnector(john_marston)
tt_connector = TikTokConnector(john_marston)
fb_connector = FacebookConnector(john_marston)
ig_connector = InstagramConnector(john_marston)

# 4. GasparAgentManager los gestiona
gaspar = GasparAgentManager(loader, john_marston, 
							 yt_connector, tt_connector, 
							 fb_connector, ig_connector)

# 5. BalthazarOrchestrator orquesta el flujo completo
balthazar.execute_business_goal(...)
```

---

## ⚙️ Campos de Plataforma Ampliados

El campo `platforms` en `MediaPayload` ahora soporta:

```python
payload = MediaPayload(
	title="Mi contenido viral",
	description="Descripción",
	tags=["AI", "Viral", "Artok"],
	script_hooks=[...],
	rendered_file="video.mp4",
	platforms=["youtube", "tiktok", "facebook", "instagram"],  # TODAS LAS PLATAFORMAS
	scheduled_time="2024-01-20 10:00:00"
)
```

---

## 📝 Ejemplo de Ejecución

```bash
# Modo 1: Simulado (sin APIs reales)
python main.py

# Salida esperada:
# [2024-01-20 10:30:45] [JMC] Modo LOCAL: integraciones externas deshabilitadas...
# [2024-01-20 10:30:45] [YT_CONNECTOR] MODO LOCAL: simulado - Publicación en YouTube omitida...
# [2024-01-20 10:30:45] [TT_CONNECTOR] MODO LOCAL: simulado - Publicación en TikTok omitida...
# [2024-01-20 10:30:45] [FB_CONNECTOR] MODO LOCAL: simulado - Publicación en Facebook omitida...
# [2024-01-20 10:30:45] [IG_CONNECTOR] MODO LOCAL: simulado - Publicación en Instagram omitida...
```

---

## 🚨 Seguridad

✅ **Mejores Prácticas Implementadas:**

1. **Variables de Entorno:** Las credenciales nunca están en el código
2. **Archivo .env en .gitignore:** No se hace commit accidentalmente
3. **Validación:** `CredentialsManager.validate_credentials()` verifica disponibilidad
4. **Modo Simulado:** Funciona sin credenciales para desarrollo
5. **Logs Informativos:** Indica si faltan credenciales

⚠️ **NUNCA:**

- ❌ Hardcodees credenciales en el código
- ❌ Hagas commit de `.env`
- ❌ Compartas tokens de acceso públicamente
- ❌ Subas capturas de pantalla con tokens visibles

---

## 🆘 Troubleshooting

### "No hay credenciales de YouTube"
→ Asegúrate de que `.env` existe y tiene `YOUTUBE_API_KEY` configurado

### "401 Unauthorized" en TikTok
→ El token de acceso ha expirado. Regenera uno nuevo en TikTok Developers

### "Pago registrado como PENDING"
→ Modo `MANUAL_BILLING=True`. Confirma la transacción:
```python
bank.confirm_payment("TXN-abc123def")
```

### La conexión es lenta
→ Usa `USE_EXTERNAL_APIS=False` para modo simulado durante desarrollo

---

## 📚 Referencias

- [YouTube Data API](https://developers.google.com/youtube/v3)
- [TikTok Business API](https://developers.tiktok.com/)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)
- [Instagram Graph API](https://developers.instagram.com/docs/instagram-graph-api)

---

**Última actualización:** 2024-01-20  
**Versión:** 3.1.0
