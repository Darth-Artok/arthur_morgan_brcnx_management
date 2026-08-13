# 🔐 TIKTOK OAUTH 2.0: Autenticación Completa para Publisher

**Artok IA Viral Studio v3.1**  
**Flujo de Autenticación OAuth 2.0 + Persistencia de Tokens**

---

## 📋 Contenido

1. [Conceptos OAuth 2.0](#conceptos-oauth)
2. [Primera Vez: Autorización Manual](#primera-vez)
3. [Ejecuciones Posteriores: Automáticas](#ejecuciones-posteriores)
4. [Clases TikTokAuth](#clases-tiktokauth)
5. [Implementación en main.py](#implementacion)
6. [Agente Publisher Completo](#agente-publisher)
7. [Gestión de Tokens](#gestión-tokens)
8. [Troubleshooting](#troubleshooting)

---

## 🔐 Conceptos OAuth 2.0

### ¿Qué es OAuth 2.0?

```
Sistema de autorización seguro que permite que apps accedan
a cuentas sin almacenar contraseñas.

VENTAJA: Tu contraseña NUNCA se comparte con código. Solo tokens.
```

### Flujo de Tres Etapas

```
ETAPA 1: Authorization (Obtener Code)
  ├─ Usuario abre URL de autorización
  ├─ Inicia sesión en TikTok
  ├─ Acepta permisos (Scopes)
  └─ TikTok redirige con ?code=ABC123

ETAPA 2: Token Exchange (Cambiar Code por Tokens)
  ├─ Envías code junto con Client ID, Secret
  ├─ TikTok verifica la info
  └─ Devuelve: access_token + refresh_token

ETAPA 3: API Calls (Usar el Token)
  ├─ Usas access_token en las llamadas a API
  ├─ El token expira después de 24h (típico)
  └─ Usas refresh_token para obtener uno nuevo
```

### Diferencia: access_token vs. refresh_token

```
access_token
├─ Corta duración: 24 horas (típico)
├─ Usado en: Llamadas a APIs
├─ Si expira: No puedes publicar
└─ Solución: Renovar con refresh_token

refresh_token
├─ Larga duración: 365+ días
├─ Usado en: Obtener nuevo access_token
├─ Si expira: Necesitas re-autorizar manualmente
└─ Almacenar: De forma segura en .env o DB
```

---

## 🚀 PRIMERA VEZ: Autorización Manual

### Paso 1: Obtener URL de Autorización

```python
from tiktok_auth import TikTokAuth

# Obtener URL para que usuario autorice
auth_url = TikTokAuth.obtener_url_autorizacion()

print(f"Abre esta URL en tu navegador:\n{auth_url}")
```

**URL resultante será algo como:**
```
https://www.tiktok.com/v2/oauth/authorize/?
  client_key=tu_client_key&
  response_type=code&
  scope=user.info.basic,video.upload,video.list&
  redirect_uri=https://localhost/&
  state=random_security_string
```

### Paso 2: Usuario Autoriza en Navegador

```
1. Usuario abre la URL en navegador
2. Inicia sesión TikTok (si no lo está)
3. Lee permisos solicitados (Scopes)
4. Hace clic en "Autorizar" o "Permitir"
5. TikTok redirige a:
   https://localhost/?code=abc123xyz&state=random
```

### Paso 3: Copiar Code de la URL

```
Usuario ve URL redirigida:
https://localhost/?code=abc123xyz&state=random

Copia solo el valor de code:
abc123xyz
```

### Paso 4: Cambiar Code por Tokens

```python
# Usuario pega el code
code = "abc123xyz"

# Intercambiar por tokens
resultado = TikTokAuth.intercambiar_codigo_por_token(code)

# Resultado:
{
  "data": {
	"access_token": "act_1234567890...",
	"refresh_token": "ref_9876543210...",
	"expires_in": 86400  # 24 horas en segundos
  },
  "message": "success"
}
```

### Paso 5: Guardar Tokens en .env

```bash
# En tu .env archivo, actualiza:

TIKTOK_ACCESS_TOKEN=act_1234567890...
TIKTOK_REFRESH_TOKEN=ref_9876543210...
TIKTOK_TOKEN_EXPIRES_AT=2024-01-21T10:30:00Z  # Timestamp
```

**✅ LISTO: Ya tienes autorización permanente**

---

## 🔄 EJECUCIONES POSTERIORES: Automáticas

### Sin Interacción Manual

```python
# Primera ejecución (este archivo cargado)
access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
refresh_token = os.getenv("TIKTOK_REFRESH_TOKEN")

# Segunda ejecución en adelante:
# 1. Lee access_token de .env (existe)
# 2. USA access_token directamente
# 3. Si expira: renovado automáticamente con refresh_token
# 4. Sin solicitar al usuario

print("[PUBLISHER] Access token cargado de .env ✅")
print("[PUBLISHER] Publicando directamente...")
```

### Renovación Automática de Token

```python
def renovar_access_token_si_necesario():
	"""Si access_token está cerca de expirar, renueva."""

	# 1. Verificar si expira pronto
	expires_at = os.getenv("TIKTOK_TOKEN_EXPIRES_AT")
	ahora = datetime.now()

	if ahora > datetime.fromisoformat(expires_at):
		# 2. Token expirado, renovar
		refresh_token = os.getenv("TIKTOK_REFRESH_TOKEN")
		nuevo_token = TikTokAuth.renovar_con_refresh_token(refresh_token)

		# 3. Guardar nuevo token y fecha de expiración
		os.environ["TIKTOK_ACCESS_TOKEN"] = nuevo_token["access_token"]
		os.environ["TIKTOK_TOKEN_EXPIRES_AT"] = nuevo_token["expires_at"]

		print("[PUBLISHER] Token renovado automáticamente ✅")
		return nuevo_token["access_token"]

	else:
		# Token aún válido
		return os.getenv("TIKTOK_ACCESS_TOKEN")
```

---

## 🔑 Clases TikTokAuth

### Estructura Completa

```python
class TikTokAuth:
	"""Gestión de autenticación OAuth 2.0 para TikTok API."""

	# Credenciales obtenidas del portal TikTok
	CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
	CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
	REDIRECT_URI = "http://localhost:8000/callback"  # O tu dominio

	@staticmethod
	def obtener_url_autorizacion():
		"""
		Genera URL para que usuario autorize la app.

		Retorna: URL completa que usuario debe abrir en navegador
		"""

		scopes = "user.info.basic,video.upload,video.list"
		state = secrets.token_urlsafe(16)  # Para seguridad

		url = (
			"https://www.tiktok.com/v2/oauth/authorize/?"
			f"client_key={TikTokAuth.CLIENT_KEY}&"
			f"response_type=code&"
			f"scope={scopes}&"
			f"redirect_uri={TikTokAuth.REDIRECT_URI}&"
			f"state={state}"
		)

		return url

	@staticmethod
	def intercambiar_codigo_por_token(code: str):
		"""
		Intercambia authorization code por tokens.

		Parámetro: code (obtenido de URL redireccionada)
		Retorna: {"data": {"access_token": "...", "refresh_token": "..."}}
		"""

		url = "https://open.tiktokapis.com/v2/oauth/token/"

		datos = {
			"client_key": TikTokAuth.CLIENT_KEY,
			"client_secret": TikTokAuth.CLIENT_SECRET,
			"code": code,
			"grant_type": "authorization_code",
			"redirect_uri": TikTokAuth.REDIRECT_URI
		}

		respuesta = requests.post(url, json=datos)
		return respuesta.json()

	@staticmethod
	def renovar_con_refresh_token(refresh_token: str):
		"""
		Obtiene nuevo access_token usando refresh_token.

		Parámetro: refresh_token (guardado en .env)
		Retorna: {"access_token": "...", "expires_in": 86400}
		"""

		url = "https://open.tiktokapis.com/v2/oauth/token/"

		datos = {
			"client_key": TikTokAuth.CLIENT_KEY,
			"client_secret": TikTokAuth.CLIENT_SECRET,
			"grant_type": "refresh_token",
			"refresh_token": refresh_token
		}

		respuesta = requests.post(url, json=datos)
		resultado = respuesta.json()

		if "data" in resultado:
			# Calcular cuándo expira
			expires_in = resultado["data"].get("expires_in", 86400)
			expires_at = (datetime.now() + timedelta(seconds=expires_in)).isoformat()

			return {
				"access_token": resultado["data"]["access_token"],
				"expires_at": expires_at,
				"expires_in": expires_in
			}

		return resultado

	@staticmethod
	def validar_access_token(access_token: str) -> bool:
		"""
		Verifica si un access_token es válido.

		Retorna: True si válido, False si expirado o inválido
		"""

		url = "https://open.tiktokapis.com/v2/user/info/"

		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/json"
		}

		params = {
			"fields": "id,data.user.username"
		}

		respuesta = requests.get(url, headers=headers, params=params)

		if respuesta.status_code == 200:
			return True  # Token válido
		elif respuesta.status_code == 401:
			return False  # Token expirado o inválido
		else:
			return False  # Error desconocido
```

---

## 📝 Implementación en main.py

### 1. Agregar Imports

```python
# En la parte superior de main.py, agregar:

import os
import sys
import requests
import secrets
from datetime import datetime, timedelta
import json
```

### 2. Crear Clase TikTokAuth en main.py

```python
# Crear esta clase DESPUÉS de imports, ANTES de otros código

class TikTokAuth:
	"""Gestión OAuth 2.0 para TikTok"""

	CLIENT_KEY = os.getenv("TIKTOK_CLIENT_KEY")
	CLIENT_SECRET = os.getenv("TIKTOK_CLIENT_SECRET")
	REDIRECT_URI = os.getenv("TIKTOK_REDIRECT_URI", "http://localhost:8000/callback")

	@staticmethod
	def obtener_url_autorizacion():
		"""Genera URL de autorización"""
		scopes = "user.info.basic,video.upload,video.list"
		state = secrets.token_urlsafe(16)

		url = (
			"https://www.tiktok.com/v2/oauth/authorize/?"
			f"client_key={TikTokAuth.CLIENT_KEY}&"
			f"response_type=code&"
			f"scope={scopes}&"
			f"redirect_uri={TikTokAuth.REDIRECT_URI}&"
			f"state={state}"
		)
		return url

	@staticmethod
	def intercambiar_codigo_por_token(code: str):
		"""Intercambia code por access_token y refresh_token"""
		url = "https://open.tiktokapis.com/v2/oauth/token/"

		datos = {
			"client_key": TikTokAuth.CLIENT_KEY,
			"client_secret": TikTokAuth.CLIENT_SECRET,
			"code": code,
			"grant_type": "authorization_code",
			"redirect_uri": TikTokAuth.REDIRECT_URI
		}

		try:
			respuesta = requests.post(url, json=datos, timeout=10)
			return respuesta.json()
		except Exception as e:
			return {"error": str(e)}

	@staticmethod
	def renovar_con_refresh_token(refresh_token: str):
		"""Obtiene nuevo access_token"""
		url = "https://open.tiktokapis.com/v2/oauth/token/"

		datos = {
			"client_key": TikTokAuth.CLIENT_KEY,
			"client_secret": TikTokAuth.CLIENT_SECRET,
			"grant_type": "refresh_token",
			"refresh_token": refresh_token
		}

		try:
			respuesta = requests.post(url, json=datos, timeout=10)
			resultado = respuesta.json()

			if "data" in resultado:
				expires_in = resultado["data"].get("expires_in", 86400)
				expires_at = (datetime.now() + timedelta(seconds=expires_in)).isoformat()

				return {
					"access_token": resultado["data"]["access_token"],
					"expires_at": expires_at
				}
			return resultado
		except Exception as e:
			return {"error": str(e)}

	@staticmethod
	def validar_access_token(access_token: str) -> bool:
		"""Valida si el token es válido"""
		url = "https://open.tiktokapis.com/v2/user/info/"

		headers = {
			"Authorization": f"Bearer {access_token}",
			"Content-Type": "application/json"
		}

		params = {"fields": "id,data.user.username"}

		try:
			respuesta = requests.get(url, headers=headers, params=params, timeout=10)
			return respuesta.status_code == 200
		except:
			return False
```

### 3. Actualizar .env.example

```env
# TIKTOK OAUTH 2.0
TIKTOK_CLIENT_KEY=tu_client_key
TIKTOK_CLIENT_SECRET=tu_client_secret
TIKTOK_REDIRECT_URI=http://localhost:8000/callback

# Tokens (se llenan automáticamente después de primera autorización)
TIKTOK_ACCESS_TOKEN=act_xxxxx     # Generado por OAuth
TIKTOK_REFRESH_TOKEN=ref_xxxxx    # Generado por OAuth
TIKTOK_TOKEN_EXPIRES_AT=2024-01-21T10:30:00Z
```

---

## 👨‍💼 Agente Publisher Completo

### Implementación Recomendada

```python
class PublisherAgent:
	"""Agente que maneja publicación en TikTok con OAuth 2.0"""

	def __init__(self, logger=None):
		self.logger = logger or print
		self.access_token = None
		self.refresh_token = None

	def inicializar_autenticacion(self):
		"""
		Verifica si hay tokens en .env.
		Si no: solicita autorización manual.
		Si sí: carga los existentes.
		"""

		self.access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
		self.refresh_token = os.getenv("TIKTOK_REFRESH_TOKEN")

		if not self.access_token:
			self.logger("[PUBLISHER] Requiere autorización primera vez...")
			self._autorizar_primera_vez()
		else:
			# Verificar que el token sea válido
			if TikTokAuth.validar_access_token(self.access_token):
				self.logger("[PUBLISHER] Token cargado de .env ✅")
			else:
				self.logger("[PUBLISHER] Token expirado, renovando...")
				self._renovar_token()

	def _autorizar_primera_vez(self):
		"""Flujo de autorización manual primera vez"""

		# 1. Obtener URL
		auth_url = TikTokAuth.obtener_url_autorizacion()
		self.logger(f"\n[PUBLISHER] Abre esta URL en tu navegador:")
		self.logger(f"{auth_url}\n")

		# 2. Esperar code del usuario
		code = input("[PUBLISHER] Pega aquí el 'code' de la URL redireccionada: ").strip()

		# 3. Intercambiar code por tokens
		resultado = TikTokAuth.intercambiar_codigo_por_token(code)

		if "data" in resultado and "access_token" in resultado["data"]:
			self.access_token = resultado["data"]["access_token"]
			self.refresh_token = resultado["data"]["refresh_token"]

			# 4. Guardar en .env
			self._guardar_tokens_en_env()
			self.logger("[PUBLISHER] Autorización exitosa ✅")
		else:
			self.logger(f"[PUBLISHER] Error en autorización: {resultado}")

	def _renovar_token(self):
		"""Renueva access_token usando refresh_token"""

		refresh_token = os.getenv("TIKTOK_REFRESH_TOKEN")

		if not refresh_token:
			self.logger("[PUBLISHER] No hay refresh_token, requier re-autorización")
			self._autorizar_primera_vez()
			return

		resultado = TikTokAuth.renovar_con_refresh_token(refresh_token)

		if "access_token" in resultado:
			self.access_token = resultado["access_token"]
			self._guardar_tokens_en_env()
			self.logger("[PUBLISHER] Token renovado ✅")
		else:
			self.logger(f"[PUBLISHER] Error al renovar: {resultado}")

	def _guardar_tokens_en_env(self):
		"""Guarda tokens en archivo .env"""

		# Leer .env actual
		env_path = ".env"
		contenido = {}

		if os.path.exists(env_path):
			with open(env_path, 'r') as f:
				for linea in f:
					if '=' in linea and not linea.startswith('#'):
						clave, valor = linea.split('=', 1)
						contenido[clave.strip()] = valor.strip()

		# Actualizar tokens
		contenido["TIKTOK_ACCESS_TOKEN"] = self.access_token
		contenido["TIKTOK_REFRESH_TOKEN"] = self.refresh_token

		expires_at = (datetime.now() + timedelta(hours=24)).isoformat()
		contenido["TIKTOK_TOKEN_EXPIRES_AT"] = expires_at

		# Guardar .env actualizado
		with open(env_path, 'w') as f:
			for clave, valor in contenido.items():
				f.write(f"{clave}={valor}\n")

	def publicar_video(self, paquete_video: dict):
		"""
		Publica un video en TikTok.

		Parámetro paquete_video:
		  {
			"video_file": "ruta/al/video.mp4",
			"titulo": "Mi video viral",
			"descripcion": "Descripción del video",
			"cta": "Call to action"
		  }
		"""

		# 1. Asegurar que tenemos token válido
		self.inicializar_autenticacion()

		# 2. Preparar headers con token
		headers = {
			"Authorization": f"Bearer {self.access_token}",
			"Content-Type": "application/json"
		}

		# 3. Publicar
		self.logger(f"[PUBLISHER] Publicando: '{paquete_video.get('titulo', 'Sin título')}'...")

		# Aquí ir endpoint de TikTok para publicar
		# POST https://open.tiktokapis.com/v2/post/publish/video/init/

		return {
			"status": "SUCCESS",
			"platform": "TikTok",
			"message": "Video publicado exitosamente"
		}
```

---

## 🔄 Gestión de Tokens

### Ciclo de Vida del Token

```
CREACIÓN (Primera vez)
  ├─ Usuario autoriza
  └─ Obtienes: access_token + refresh_token

ALMACENAMIENTO
  ├─ Guardar en .env (seguro)
  └─ Disponible para futuras ejecuciones

VALIDACIÓN (Cada vez que ejecutas)
  ├─ Verificar que token sea válido
  └─ Si no: renovar con refresh_token

EXPIRACIÓN (Después de 24h típical)
  ├─ access_token deja de funcionar
  ├─ refresh_token aún válido
  └─ Renovar automáticamente

RE-AUTORIZACIÓN (Si refresh_token expira)
  ├─ Típicamente 365+ días
  └─ Solicitar nueva autorización manual
```

### Renovación Automática Recomendada

```python
def ensure_valid_token():
	"""Garantiza que tenemos un token válido"""

	access_token = os.getenv("TIKTOK_ACCESS_TOKEN")
	refresh_token = os.getenv("TIKTOK_REFRESH_TOKEN")
	expires_at_str = os.getenv("TIKTOK_TOKEN_EXPIRES_AT")

	# 1. Si no hay access_token, necesita re-autorización
	if not access_token:
		return PublisherAgent().inicializar_autenticacion()

	# 2. Si no hay fecha de expiración, asumir que expiró
	if not expires_at_str:
		resultado = TikTokAuth.renovar_con_refresh_token(refresh_token)
		# Guardar nuevo token
		return resultado.get("access_token")

	# 3. Verificar si está próximo a expirar (renovar si faltan <1 hora)
	expires_at = datetime.fromisoformat(expires_at_str)
	si_faltan_menos_de_1h = (expires_at - datetime.now()).total_seconds() < 3600

	if si_faltan_menos_de_1h:
		resultado = TikTokAuth.renovar_con_refresh_token(refresh_token)
		return resultado.get("access_token")

	# 4. Token válido
	return access_token
```

---

## 🆘 Troubleshooting

### Error 1: "Invalid code"

**Síntoma:**
```
{"error": "invalid_code", "error_description": "The code has expired"}
```

**Causa:** El `code` es válido solo por ~5 minutos

**Solución:**
1. Abre URL de autorización nuevamente
2. Copia el code INMEDIATAMENTE
3. Intercambia por tokens SIN DEMORA

### Error 2: "Invalid client secret"

**Síntoma:**
```
{"error": "invalid_client_secret"}
```

**Causa:** Credenciales incorrectas en .env

**Solución:**
```bash
# Verificar en .env:
echo $env:TIKTOK_CLIENT_KEY
echo $env:TIKTOK_CLIENT_SECRET

# Deben coincidir con portal TikTok exactamente
```

### Error 3: "Token expired"

**Síntoma:**
```
{"error": "authorize failed"}
```

**Causa:** access_token expiró (>24h)

**Solución:**
```python
# Renovar automáticamente
nuevo_token = TikTokAuth.renovar_con_refresh_token(refresh_token)
```

### Error 4: "Refresh token expired"

**Síntoma:**
```
{"error": "invalid_grant"}
```

**Causa:** refresh_token expiró (>365 días)

**Solución:**
- ⚠️ No hay automático
- Solicitar nueva autorización manual
- Re-ejecutar flujo OAuth completo

### Error 5: "Redirect URI mismatch"

**Síntoma:**
```
{"error": "redirect_uri_mismatch"}
```

**Causa:** REDIRECT_URI en código ≠ configurado en portal

**Solución:**
```python
# En main.py verifica:
REDIRECT_URI = "http://localhost:8000/callback"

# Debe coincidir exactamente con:
# Portal TikTok → App Details → OAuth Settings → Redirect URI
```

---

## 📊 Checklist: OAuth 2.0 Implementado

```
☐ Clase TikTokAuth en main.py
☐ Método obtener_url_autorizacion()
☐ Método intercambiar_codigo_por_token()
☐ Método renovar_con_refresh_token()
☐ Método validar_access_token()
☐ PublisherAgent class
☐ Guardar tokens en .env
☐ Renovación automática
☐ Trimestral check (365 días)
☐ Test de flujo completo

LISTO: OAuth 2.0 COMPLETO ✅
```

---

## 🎯 Flujo Operacional Resumido

### PRIMERA VEZ (Inicial)

```bash
1. usuario ejecuta: python main.py
2. Sistema detecta: NO hay access_token en .env
3. Sistema genera: URL de autorización
4. Usuario abre URL en navegador
5. Usuario autoriza permisos
6. TikTok redirige con code
7. Usuario copia code
8. Sistema intercambia: code → access_token + refresh_token
9. Sistema guarda: tokens en .env
10. Sistema publica: video ✅
```

### VECES POSTERIORES (Automático)

```bash
1. usuario ejecuta: python main.py
2. Sistema detecta: access_token en .env
3. Sistema valida: token aún válido
4. Sistema publica: video ✅

# Si token expiró:
5. Sistema detecta: expiración
6. Sistema renueva: con refresh_token
7. Sistema guarda: nuevo token en .env
8. Sistema publica: video ✅
```

---

**Versión:** 3.1.0 OAuth  
**Fecha:** 2024-01-20  
**Estado:** ✅ COMPLETO

*Para implementar: Agrega clases a main.py y actualiza .env.example*
