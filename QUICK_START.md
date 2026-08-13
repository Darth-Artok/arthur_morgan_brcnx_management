# ⚡ QUICK START - Empieza en 5 Minutos

**Artok IA Viral Studio v3.1** - Multi-Plataforma Sin Google Cloud

---

## 🚀 Instalación (1 minuto)

### Requisitos
- Python 3.8+ instalado
- Archivo `main.py` en tu directorio
- Archivo `.env` (se crea automáticamente)

### Verificar instalación
```bash
python --version
# Debe mostrar: Python 3.x.x (3.8 o mayor)
```

---

## ⏱️ Primer Ejecución (2 minutos)

### Paso 1: Verificar que todo está listo
```bash
python test_integration.py
```

**Resultado esperado:**
```
======================================================================
✓ VERIFICACIÓN DE INTEGRACIÓN - ARTOK IA VIRAL STUDIO v3.1
======================================================================

[TEST 1] Importando módulos principales...
  ✅ Todos los módulos importados exitosamente

[TEST 2] Cargando archivo de configuración (.env)...
  ✅ Archivo .env encontrado

...

======================================================================
✅ VERIFICACIÓN COMPLETA - SISTEMA LISTO PARA USAR
======================================================================
```

### Paso 2: Ejecutar en modo simulado
```bash
python main.py
```

**Resultado esperado:**
```
[2024-01-20 10:30:45] [JMC] Modo LOCAL: integraciones externas deshabilitadas...
[2024-01-20 10:30:45] [GASPAR] Invocando agente...
[2024-01-20 10:30:45] [YT_CONNECTOR] MODO LOCAL: simulado...
[2024-01-20 10:30:45] [TT_CONNECTOR] MODO LOCAL: simulado...
[2024-01-20 10:30:45] [FB_CONNECTOR] MODO LOCAL: simulado...
[2024-01-20 10:30:45] [IG_CONNECTOR] MODO LOCAL: simulado...
```

✅ ¡Éxito! El sistema está funcionando.

---

## 🎯 Próximos Pasos (2 minutos)

### Opción A: Solo Desarrollo (Recomendado para empezar)
```bash
# Todo está configurado, ejecuta:
python main.py

# Funciona sin credenciales, modo simulado
# Perfecto para pruebas y desarrollo
```

No necesitas configurar credenciales para comenzar a explorar.

### Opción B: Usar APIs Reales (Producción)

#### Subpaso 1: Obtener credenciales
- 📺 YouTube: [Google Cloud Console](https://console.cloud.google.com/)
- 🎵 TikTok: [TikTok Developers](https://developers.tiktok.com/)
- 📱 Facebook: [Facebook Developers](https://developers.facebook.com/)
- 📸 Instagram: [Instagram Developers](https://developers.instagram.com/)

*Consulta `CREDENTIALS_GUIDE.md` para instrucciones detalladas*

#### Subpaso 2: Configurar .env
```bash
# Edita el archivo .env
# Copia tus credenciales en las variables correspondientes

# Ejemplo (reemplaza con tus valores reales):
USE_EXTERNAL_APIS=True
TIKTOK_CLIENT_KEY=abc123xyz
TIKTOK_CLIENT_SECRET=xyz789abc
TIKTOK_ACCESS_TOKEN=token_real_aqui
FACEBOOK_PAGE_ID=123456789
FACEBOOK_ACCESS_TOKEN=token_facebook_real
# ... etc
```

#### Subpaso 3: Ejecutar en producción
```bash
python main.py

# Ahora sí hace llamadas reales a las APIs
# Publicará contenido en YouTube, TikTok, Facebook, Instagram
```

---

## 📚 Documentación

| Documento | Para Quién | Cuándo Leerlo |
|-----------|-----------|--------------|
| **INDEX.md** | Cualquiera | Cuando necesites orientación |
| **CREDENTIALS_GUIDE.md** | DevOps/Sysadmin | Cuando configures APIs |
| **ARCHITECTURE_DIAGRAM.md** | Developers | Cuando entres en el código |
| **IMPLEMENTATION_SUMMARY.md** | Project Leads | Cuando necesites resumen técnico |

---

## 🆘 Troubleshooting Básico

### P: ¿Recibo error "module not found"?
**R:** Asegúrate de estar en el directorio correcto:
```bash
cd /ruta/a/tu/proyecto
python test_integration.py
```

### P: ¿.env no se crea?
**R:** Créalo manually desde .env.example:
```bash
cp .env.example .env
```

### P: ¿Me dice que faltan credenciales?
**R:** Es normal. Estás en modo simulado (`USE_EXTERNAL_APIS=False`). Para APIs reales:
1. Configura credenciales en `.env`
2. Cambia `USE_EXTERNAL_APIS=True`

### P: ¿"Facebook Connector no disponible"?
**R:** Conectade Instagram también se instancian correctamente. Si ves esto:
- Verifica que todos los imports funcionan: `python test_integration.py`
- Revisa que no hay errores de sintaxis en main.py

### Más problemas
→ Consulta sección 🆘 TROUBLESHOOTING en `CREDENTIALS_GUIDE.md`

---

## ⚡ Comandos Essenciales

```bash
# Verificar que todo está instalado
python test_integration.py

# Ejecutar en modo simulado (recomendado para empezar)
python main.py

# Validar sintaxis de Python
python -m py_compile main.py

# Ver estructura del proyecto
ls -la              # En macOS/Linux
dir                 # En Windows

# Editar archivo .env
nano .env           # En macOS/Linux
notepad .env        # En Windows
```

---

## 🎬 Flujo de Tu Primer Día

```
10:00 - Instalación y verificación (5 min)
		python test_integration.py

10:05 - Primer ejecución (5 min)
		python main.py
		(Observa los logs)

10:10 - Exploración (20 min)
		Abre main.py en tu editor
		Revisa las 4 clases de conectores:
		- YouTubeConnector
		- TikTokConnector
		- FacebookConnector (NUEVO)
		- InstagramConnector (NUEVO)

10:30 - Lectura de arquitectura (10 min)
		Lee sección "Flujo de Ejecución" en ARCHITECTURE_DIAGRAM.md

10:40 - Próximos pasos
		¿Quieres agregar credenciales?
		→ Ve a CREDENTIALS_GUIDE.md
```

---

## 🎯 Objetivos Rápidos

### Objetivo 1: Entender la arquitectura
```bash
# 1. Ejecuta
python test_integration.py

# 2. Lee
ARCHITECTURE_DIAGRAM.md (sección "Flujo de Ejecución")

# 3. Responde
"¿Cuál es el orden de inicialización de componentes?"
"¿Cuántas plataformas soporta?"
```

### Objetivo 2: Modificar código
```bash
# 1. Abre main.py en tu editor favorito
# 2. Busca: class FacebookConnector
# 3. Lee el método publish_media()
# 4. Modifica: Agrega logging personalizado
# 5. Ejecuta: python main.py
# 6. Observa: Tu cambio en los logs
```

### Objetivo 3: Configurar primera plataforma
```bash
# 1. Lee
CREDENTIALS_GUIDE.md → Sección "YouTube"

# 2. Ejecuta pasos
(Obtén API Key de Google Cloud)

# 3. Configura
Edita .env → YOUTUBE_API_KEY=tu_clave

# 4. Verifica
python test_integration.py
```

---

## 💡 Consejos Pro

1. **Siempre empieza en modo simulado**
   - `USE_EXTERNAL_APIS=False` en .env
   - Sin riesgo de errores de APIs reales

2. **Usa .env.example como referencia**
   - Contiene todos los variables posibles
   - Úsalo para crear tu .env personal

3. **Lee los logs**
   - Formato: `[TIMESTAMP] [COMPONENT] MESSAGE`
   - Indica qué está pasando en cada paso

4. **Verifica frecuentemente**
   - `python test_integration.py` después de cambios
   - Rápido y exhaustivo

5. **Consulta la documentación**
   - Antes de googlear, busca en `CREDENTIALS_GUIDE.md`
   - Hay soluciones para problemas comunes

---

## 📊 Estado del Sistema

```
✅ Componentes: 13 clases principales
✅ Plataformas: 4 (YouTube, TikTok, Facebook, Instagram)
✅ Modo simulado: Disponible (desarrollo)
✅ Modo producción: Disponible (con credenciales)
✅ Seguridad: Variables de entorno (sin hardcoding)
✅ Documentación: Exhaustiva (4 archivos)
✅ Tests: Automatizados (test_integration.py)

LISTO PARA USAR ✨
```

---

## 🚀 Cheat Sheet

### Para diferentes usuarios

**Desarrollador**
```bash
python main.py                    # Ejecutar
python -c "from main import ..." # Testear imports
nano main.py                      # Editar código
git add .gitignore               # No hagas commit de .env
```

**DevOps**
```bash
cp .env.example .env             # Crear configuración
nano .env                        # Editar credenciales
python test_integration.py       # Verificar
export USE_EXTERNAL_APIS=True  # Activar APIs reales
```

**Project Manager**
```bash
cat IMPLEMENTATION_SUMMARY.md    # Leer resumen
cat ARCHITECTURE_DIAGRAM.md      # Ver diagramas
python test_integration.py       # Demostración
```

---

## ❓ Preguntas Frecuentes

**P: ¿Necesito credenciales para empezar?**
No. Modo simulado funciona sin credenciales. `USE_EXTERNAL_APIS=False`

**P: ¿Cuántas plataformas soporta?**
4: YouTube, TikTok, Facebook, Instagram

**P: ¿Dónde pongo mis credenciales?**
Archivo `.env` (nunca en código, nunca en git)

**P: ¿Cómo agrego una plataforma nueva?**
Crea un conector siguiendo el patrón de FacebookConnector

**P: ¿Es seguro?**
Sí. Credenciales en variables de entorno, validaciones integradas

**P: ¿Hay más documentación?**
Sí. Ve a `INDEX.md` para guía completa

---

## 🎉 ¡Ya Estás Listo!

```
✨ 5 minutos
├─ ✅ Instalación verificada
├─ ✅ Sistema ejecutándose
├─ ✅ Logs visible
├─ ✅ Próximos pasos claros
└─ ✅ Listo para desarrollo

BIENVENIDO A ARTOK IA VIRAL STUDIO v3.1 🚀
```

---

## 📞 Siguientes Lecturas Recomendadas

1. **ARCHITECTURE_DIAGRAM.md** - Entiende la estructura completa
2. **CREDENTIALS_GUIDE.md** - Cuando necesites configurar APIs
3. **IMPLEMENTATION_SUMMARY.md** - Detalles técnicos (si eres tech lead)

---

**Versión:** 3.1.0 | **Fecha:** 2024-01-20 | **Estado:** ✅ LISTO

*¿Aún tienes dudas? Consulta `INDEX.md` para acceso a documentación completa*
