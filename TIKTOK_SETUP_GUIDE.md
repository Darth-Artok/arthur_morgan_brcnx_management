# 🎵 GUÍA COMPLETA: Configuración de TikTok API (Content Posting)

**Artok IA Viral Studio v3.1**  
**Última actualización:** 2024-01-20  
**Estado:** ✅ VERIFICADO

---

## 📋 Contenido

1. [Conceptos Clave: Sandbox vs. Producción](#sandbox-vs-producción)
2. [Paso 1: Crear Aplicación en TikTok Developers](#paso-1-crear-aplicación)
3. [Paso 2: Configurar Productos y Alcances](#paso-2-configurar-productos)
4. [Paso 3: Obtener Credenciales](#paso-3-obtener-credenciales)
5. [Paso 4: Configurar Variables de Entorno](#paso-4-configurar-env)
6. [Paso 5: Probar Conexión](#paso-5-probar-conexión)
7. [Transición a Producción](#paso-6-transición-producción)
8. [Troubleshooting](#troubleshooting)

---

## 🔄 Sandbox vs. Producción

### MODO SANDBOX (Pruebas) ✅ EMPIEZA AQUÍ

```
ESTADO:        Draft (Borrador)
PROPÓSITO:     Pruebas iniciales sin aprobación
REQUISITOS:    ✅ Client Key + Client Secret
LIMITACIONES:  Solo tu cuenta TikTok vinculada
APROBACIÓN:    NO REQUERIDA
TIEMPO:        Inmediato
IDEAL PARA:    Desarrollo, testing, validación
```

**Ventajas:**
- ✅ Acceso inmediato
- ✅ Sin esperas de aprobación
- ✅ Perfecto para desarrollar
- ✅ Credenciales activas desde el inicio

**Limitaciones:**
- ❌ Solo con tu cuenta TikTok
- ❌ No puede publicar en otras cuentas
- ❌ No para producción en vivo

### MODO PRODUCCIÓN (Lanzamiento)

```
ESTADO:        In Review / Approved
PROPÓSITO:     Publicación automatizada en vivo
REQUISITOS:    ✅ Client Key + Secret + Aprobación TikTok
PUBLICACIÓN:   Múltiples cuentas autorizadas
APROBACIÓN:    REQUERIDA (Submit for Review)
TIEMPO:        5-10 días (típicamente)
IDEAL PARA:    Producción, múltiples clientes
```

**Ventajas:**
- ✅ Publicación en varias cuentas
- ✅ Sin limitaciones
- ✅ Acceso permanente y estable

**Limitaciones:**
- ⏱️ Requiere aprobación de TikTok (5-10 días)
- 📋 Necesita cumplir requisitos de TikTok
- 🔍 Revisión del equipo de TikTok

**Timeline Recomendado:**
```
Semana 1: Desarrollo en Sandbox
Semana 2: Solicitar acceso a Producción (Submit for Review)
Semana 3-4: Esperar aprobación de TikTok
Semana 4+: Lanzamiento en Producción
```

---

## 🚀 Paso 1: Crear Aplicación en TikTok

### 1.1 Ir a TikTok Developers

1. Abre: https://developers.tiktok.com/
2. Haz clic en **"Sign in"** (esquina superior derecha)
3. Inicia sesión con tu cuenta TikTok
4. Ve a **"My apps"** o **"Applications"**

### 1.2 Crear Nueva Aplicación

```
1. Haz clic en "+ Create app"
2. Selecciona país/región
3. Nombre de la app: "Artok IA Viral Studio"
4. Descripción: "Sistema automatizado de publicación de contenido multiplatform"
5. Categoría: "Content Publisher" o "Social Media Manager"
6. Acepta términos → "Create app"
```

### 1.3 Verificar que se Creó

- Deberías ver tu app en estado **"Draft"** (Borrador)
- Icono: ⚪ Gris con "Draft"
- Tu app está lista para Sandbox

---

## 🛠️ Paso 2: Configurar Productos y Alcances

### 2.1 Acceder a Configuración de Productos

```
En el portal de tu app:
├─ Left Menu → "Products" (Productos)
└─ O busca sección "Add Products"
```

### 2.2 Agregar Content Posting API

```
1. Haz clic en "+ Add product"
2. Busca: "Content Posting API"
3. Descripción: 
   "API para publicar y gestionar videos de forma automatizada"
4. Haz clic en "Add" o "Request"
```

✅ Deberías ver "Content Posting API" en tu lista de productos

### 2.3 Configurar Alcances (Scopes)

Los **scopes** son permisos que tu aplicación solicita a los usuarios.

#### Scopes Necesarios para TikTokConnector

| Scope | Descripción | Necesario |
|-------|-------------|----------|
| `user.info.basic` | Información básica del perfil (nombre, avatar) | ✅ SÍ |
| `video.upload` | Subir y publicar videos | ✅ SÍ |
| `video.list` | Leer estadísticas de videos | ⚠️ RECOMENDADO |

#### Cómo Configurar los Scopes

```
1. En tu app → "Scopes" (Alcances)
2. Busca cada scope en la lista:
   ├─ user.info.basic ✅
   ├─ video.upload ✅
   └─ video.list ✅ (recomendado)
3. Marca el checkbox de cada uno
4. Haz clic en "Save" o "Update"
```

✅ Deberías ver los 3 scopes marcados como "Requested"

### 2.4 Configuración de OAuth

Si tu app requiere OAuth (autenticación de usuarios):

```
1. Ve a "Redirect URLs" 
2. Agrega URL de callback (para desarrollo local):
   http://localhost:8000/callback
3. Para producción, usa tu dominio real
4. Guarda cambios
```

---

## 🔑 Paso 3: Obtener Credenciales

### 3.1 Acceder a App Details

```
En el portal de TikTok dentro de tu app:
├─ Left Menu → "App Details" (Detalles de la aplicación)
├─ O busca "Credentials" o "Keys"
└─ O busca "Client ID y Secret"
```

### 3.2 Copiar Client Key y Secret

Deberías ver algo como:

```
┌─────────────────────────────────────────┐
│ CLIENT CREDENTIALS                      │
├─────────────────────────────────────────┤
│ Client Key (también llamado App ID):    │
│ abc1234567890def1234567890def123      │
│                                         │
│ Client Secret:                          │
│ xyz9876543210abc9876543210abc987      │
│                                         │
│ [Regenerate] [Copy]                     │
└─────────────────────────────────────────┘
```

### 3.3 Copiar y Guardar Temporalmente

```
✅ Haz clic en [Copy] junto a Client Key
✅ Pégalo en un archivo de texto temporal
✅ Repite para Client Secret
✅ NO cierre esta página (la necesitarás después)
```

### 3.4 Datos que Necesitarás

Anota estos valores:

```
TIKTOK_CLIENT_KEY = [tu_client_key_aqui]
TIKTOK_CLIENT_SECRET = [tu_client_secret_aqui]
TIKTOK_ACCESS_TOKEN = [lo_obtendremos_después]
```

---

## 📝 Paso 4: Configurar Variables de Entorno

### 4.1 En Windows (Recomendado)

#### Opción A: Variables de Entorno del Sistema (Permanente)

```
1. Abre: "Editar variables de entorno del sistema"
   (Presiona Win + X → Busca "Editar variables de entorno")

2. Haz clic en "Variables de entorno"

3. En "Variables de usuario para [tu_usuario]":
   ├─ [Nuevo]
   ├─ Nombre: TIKTOK_CLIENT_KEY
   ├─ Valor: [tu_client_key_aqui]
   └─ [OK]

4. Repite para:
   ├─ TIKTOK_CLIENT_SECRET = [tu_secret]
   └─ TIKTOK_ACCESS_TOKEN = [obtenido_después]

5. Reinicia PowerShell/Terminal
```

✅ Ahora `echo $env:TIKTOK_CLIENT_KEY` mostrará tu clave

#### Opción B: Archivo .env.local (Más Seguro)

```
# En tu proyecto, edita .env
nano .env
o
notepad .env
```

Añade estas líneas:

```env
# TikTok Business API Credentials
TIKTOK_CLIENT_KEY=abc1234567890def1234567890def123
TIKTOK_CLIENT_SECRET=xyz9876543210abc9876543210abc987
TIKTOK_ACCESS_TOKEN=                    # Lo obtendremos

# Modo de operación
USE_EXTERNAL_APIS=False  # Cambia a True cuando tengas token
```

✅ Guarda el archivo con Ctrl+S

### 4.2 Verificar Configuración

```bash
# En PowerShell
python -c "import os; print('CLIENT_KEY:', os.getenv('TIKTOK_CLIENT_KEY'))"

# Deberías ver:
# CLIENT_KEY: abc1234567890def1234567890def123
```

---

## 🧪 Paso 5: Probar Conexión

### 5.1 Ejecutar Script de Verificación

```bash
python test_integration.py
```

**Salida esperada:**

```
[TEST 3] Verificando CredentialsManager...
  ✅ TikTok: ✓ Credenciales cargadas

[TEST 4] Inicializando JohnMarstonCore (Kernel)...
  ✅ TikTok: credenciales disponibles

[TEST 5] Inicializando Conectores...
  ✅ TikTokConnector: Listo
```

Si ves esto ✅ **¡Tus credenciales están configuradas correctamente!**

### 5.2 Si Ves Error: "Sin credenciales"

```
[TEST 3] Verificando CredentialsManager...
  ✅ TikTok: ✗ Sin credenciales (normal en modo simulado)
```

**Posibles causas:**
1. ❌ Las variables no están en `.env`
2. ❌ `.env` está en directorio incorrecto
3. ❌ PowerShell no fue reiniciada después de cambiar variables del sistema

**Soluciones:**
```bash
# 1. Verifica que .env existe en el directorio de main.py
dir .env

# 2. Verifica contenido
type .env

# 3. Reinicia PowerShell/Terminal

# 4. Intenta de nuevo
python test_integration.py
```

---

## 🚀 Paso 6: Obtener Access Token (Sandbox)

### 6.1 Métodos para Obtener Token

#### Método Simple: OAuth Flow (Recomendado para empezar)

```
1. Ve a tu aplicación en TikTok Developers
2. Busca sección "Authorization" o "Get Access Token"
3. Haz clic en "Launch OAuth Flow"
4. TikTok te pedirá permiso para acceder a tu cuenta
5. Autoriza los permisos (scopes)
6. Copiarás un token largo (comienza con "act_")
```

**Ejemplo de token:**
```
act_1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcd
```

#### Método Tools: Graph API Explorer

```
1. Ve a TikTok Developers → "API Explorer" o "Tools"
2. Selecciona tu app
3. Haz clic en "Get Access Token"
4. Autoriza la solicitud
5. Copia el token mostrado
```

### 6.2 Guardar Access Token

```bash
# En tu .env, actualiza:
TIKTOK_ACCESS_TOKEN=act_1234567890abcdef1234567890abcd
```

**Importante:**
- 🔐 Este token es como una contraseña: NUNCA lo publiques
- ⏰ Tokens de Sandbox típicamente expiran en 24-30 días
- 🔄 Tendrás que renovar periodicamente (especialmente durante desarrollo)

---

## 📈 Paso 7: Transición a Producción

### 7.1 Cuándo Solicitar Producción

**Espera hasta que:**
- ✅ Tu script funcione en Sandbox
- ✅ Hayas probado publicar videos
- ✅ Entiendas los límites de rates
- ✅ Tengas documentación de tu app

### 7.2 Solicitar Acceso a Producción

```
1. En tu app en TikTok Developers
2. Ve a "Overview" o "Status"
3. Busca botón "Submit for Review" o "Request Production"
4. Rellena formulario:
   ├─ Descripción de tu aplicación
   ├─ Casos de uso (ej: publicación automatizada de contenido)
   ├─ Cuántos usuarios/clientes
   ├─ Política de privacidad URL
   └─ Términos de servicio URL
5. Adjunta capturas de pantalla de tu app funcionando
6. Haz clic en "Submit"
```

### 7.3 Estados durante la Revisión

```
┌─────────────────────────────────────┐
│ ESTADOS POSIBLES                    │
├─────────────────────────────────────┤
│ Draft           (Inicial)           │
│ In Review       (Esperando)         │
│ Approved        (✅ Aprobado)       │
│ Rejected        (❌ Rechazado)      │
│ Suspended       (⚠️ Suspendido)    │
└─────────────────────────────────────┘
```

### 7.4 Si es Rechazado

```
1. Ve a la sección "Revision History" o "Review History"
2. Lee los comentarios del equipo de TikTok
3. Corrije los problemas indicados
4. Reenvía para revisión
```

Razones comunes de rechazo:
- ❌ Documentación incompleta
- ❌ Política de privacidad ausente
- ❌ CSV/Credenciales inseguras en código
- ❌ App que no claramente identifica que es automatizada

---

## 🔄 Renovar Access Token en Sandbox

### El Token Puede Expirar

**Problema inicial:**
```
TikTok Token válido por 24-30 días
Después expira automáticamente
```

**Solución:**

```bash
1. Antes de que expire:
   - Vuelve a https://developers.tiktok.com/
   - Busca "Refresh Token" o genera uno nuevo

2. Actualiza tu .env:
   TIKTOK_ACCESS_TOKEN=nuevo_token_aqui

3. Prueba: python test_integration.py
```

---

## 🧪 Probar Publicación de Video

### 8.1 Crear Script de Prueba

```python
# test_tiktok_publish.py

from main import TikTokConnector, JohnMarstonCore, MediaPayload

# Inicializa
kernel = JohnMarstonCore()
tt_connector = TikTokConnector(kernel)

# Crea payload de prueba
payload = MediaPayload(
	title="Mi primer video automatizado 🚀",
	description="Publicado desde Artok IA Viral Studio",
	tags=["AI", "Automation", "TikTok", "Viral"],
	script_hooks=["Tech amazing", "Check this out"],
	rendered_file="test_video.mp4",
	platforms=["tiktok"]
)

# Publica
result = tt_connector.publish_video(payload)
print(result)
```

### 8.2 Ejecutar Prueba

```bash
python test_tiktok_publish.py
```

**Resultado esperado en Sandbox:**
```
Si USE_EXTERNAL_APIS=False (Simulado):
  {
	"platform": "TikTok",
	"status": "SIMULATED",
	"post_id": "tt_sim_abc12345",
	"message": "Publicación simulada"
  }

Si USE_EXTERNAL_APIS=True (Real):
  {
	"platform": "TikTok",
	"status": "SUCCESS",
	"post_id": "tt_1234567890123456789",
	"url": "https://tiktok.com/@tu_usuario/video/1234567890123456789"
  }
```

---

## 🆘 Troubleshooting de TikTok

### Error 1: "Credenciales no encontradas"

**Síntoma:**
```
[!] Advertencia: No hay credenciales de tiktok en variables de entorno.
```

**Causas y Soluciones:**
```
1. ❌ .env no existe → Crear: cp .env.example .env
2. ❌ Ruta incorrecta → Verifica: ls .env
3. ❌ Archivo mal formateado → Edita y guarda: notepad .env
4. ❌ Terminal no reiniciada → Reinicia PowerShell
5. ❌ Espacios extra → Edita: TIKTOK_CLIENT_KEY=valor_sin_espacios
```

### Error 2: "Token expirado"

**Síntoma:**
```
Error 401: Unauthorized
Invalid access_token
```

**Solución:**
```
1. Obtén nuevo token:
   https://developers.tiktok.com/ → Get Access Token
2. Actualiza .env:
   TIKTOK_ACCESS_TOKEN=nuevo_token
3. Prueba: python test_integration.py
```

### Error 3: "Scope insuficiente"

**Síntoma:**
```
Error 403: Forbidden
Insufficient permission
```

**Solución:**
```
1. Ve a tu app en TikTok Developers
2. Verifica Scopes configurados:
   ✅ user.info.basic
   ✅ video.upload
   ✅ video.list
3. Si falta alguno, agrégalo
4. Genera nuevo Access Token (con permisos nuevos)
5. Actualiza .env
```

### Error 4: "App en estado Draft"

**Síntoma:**
```
Error: Application not approved for production
```

**Solución:**
```
✅ Es normal en Sandbox
→ Este error aparecerá solo si cambias USE_EXTERNAL_APIS=True
→ Para producción: Submit for Review y espera aprobación
```

### Error 5: "Rate limit exceeded"

**Síntoma:**
```
Error 429: Too Many Requests
```

**Límites TikTok típicos:**
```
Sandbox: 100 videos/día
Producción: Varía según aprobación
```

**Solución:**
```
1. Espera 1 hora
2. Revisa límites específicos en la documentación de TikTok
3. Implementa throttling en tu código
```

---

## 📚 Resumen: Checklist de Setup Completo

```
☐ 1. Crear aplicación en https://developers.tiktok.com/
☐ 2. Agregar producto: Content Posting API
☐ 3. Configurar Scopes (user.info.basic, video.upload, video.list)
☐ 4. Copiar Client Key y Client Secret
☐ 5. Configurar variables de entorno (.env o Sistema)
☐ 6. Verificar: python test_integration.py → ✅ (paso 3)
☐ 7. Obtener Access Token del portal
☐ 8. Guardar token en TIKTOK_ACCESS_TOKEN
☐ 9. Cambiar: USE_EXTERNAL_APIS=False para pruebas
☐ 10. Ejecutar: python main.py (Sandbox)

LISTO PARA DESARROLLO ✅
```

---

## 🎯 Siguientes Pasos

1. **Hoy:** Completa pasos 1-8
2. **Mañana:** Prueba en Sandbox
3. **Esta semana:** Integra con main.py
4. **Próxima semana:** Submit for Review (producción)

---

## 📞 Referencias TikTok Oficiales

- [TikTok Developers Portal](https://developers.tiktok.com/)
- [Content Posting API Documentation](https://developers.tiktok.com/doc/content-posting-api)
- [OAuth Guide](https://developers.tiktok.com/doc/tiktok-api-overview#OAuth-Authorization-Flow)
- [Scopes Reference](https://developers.tiktok.com/doc/tiktok-api-overview#Scopes)

---

**Versión:** 3.1.0  
**Última actualización:** 2024-01-20  
**Estado:** ✅ VERIFICADO Y ACTUALIZADO

*¿Aún tienes dudas? Consulta la sección 🆘 Troubleshooting arriba o contacta a soporte de TikTok.*
