# 🎵 QUICK GUIDE: TikTok Setup (5 minutos)

**Para empezar con TikTok de forma rápida**

---

## 🎯 Flujo Rápido

### Sandbox (Hoy - 10 minutos)

```bash
1. Ve a: https://developers.tiktok.com/
2. Crea app "Artok IA Viral Studio"
3. Agrega producto: Content Posting API
4. Configura Scopes:
   ✅ user.info.basic
   ✅ video.upload
   ✅ video.list
5. Copia Client Key y Secret
6. Edita .env y pega:
   TIKTOK_CLIENT_KEY=tu_key
   TIKTOK_CLIENT_SECRET=tu_secret
7. Obtén Access Token desde portal
8. Pega en .env:
   TIKTOK_ACCESS_TOKEN=tu_token
9. Ejecuta: python test_integration.py
   ✅ Deberías ver TikTok: OK
```

### Uso (Hoy - mismo)

```bash
# Modo simulado (sin APIs reales)
USE_EXTERNAL_APIS=False
python main.py

# Resultado: Verás logs de publicación simulada
```

### Producción (Próxima semana)

```bash
1. Submit for Review en el portal TikTok
2. Espera aprobación (5-10 días)
3. Una vez aprobado:
   USE_EXTERNAL_APIS=True
4. python main.py
   # ¡Ahora publicará en TikTok de verdad!
```

---

## 📚 Para más detalles

→ Lee: **TIKTOK_SETUP_GUIDE.md** (guía completa con screenshots)

---

## ⚡ Comandos Esenciales

```bash
# Verificar credenciales
python test_integration.py

# Ver si .env existe
ls .env  (o dir .env en Windows)

# Ver contenido de .env
type .env  (Windows) o cat .env (Mac/Linux)

# Editar .env
notepad .env  (Windows) o nano .env (Mac/Linux)

# Ejecutar en sandbox
python main.py
```

---

## ✅ Checklist Sandbox

```
☐ App CREADA en TikTok Developers
☐ Producto AGREGADO: Content Posting API
☐ Scopes CONFIGURADOS (3 scopes)
☐ Credenciales COPIADAS (Key + Secret)
☐ .env ACTUALIZADO (ambas credenciales)
☐ Access Token OBTENIDO
☐ .env COMPLETADO (Token)
☐ test_integration.py ✅ PASÓ
☐ main.py EJECUTÁNDOSE en simulado

LISTO PARA USAR 🚀
```

---

## 🚨 Problemas Comunes

| Problema | Solución |
|----------|----------|
| "No hay credenciales" | Edita `.env`, guarda, reinicia Terminal |
| "Token expirado" | Obtén nuevo token en portal TikTok |
| "Scope insuficiente" | Revisa que los 3 scopes estén marcados |
| ".env no encontrado" | Crea: `cp .env.example .env` |

---

## 📞 Necesito más detalles

1. **Setup completo:** TIKTOK_SETUP_GUIDE.md
2. **Todas las plataformas:** CREDENTIALS_GUIDE.md
3. **Arquitectura del sistema:** ARCHITECTURE_DIAGRAM.md

---

**Tiempo total:** ~10 minutos hasta tener TikTok funcionando en Sandbox ✅
