# 🚀 INICIO RÁPIDO: TikTok + Artok IA Viral Studio

**Tu Guía de 15 Minutos para Tener TikTok Funcionando**

---

## ⏱️ AHORA MISMO (5 minutos)

### 1. Verifica Sistema
```bash
python test_integration.py
```
✅ Deberías ver: "VERIFICACIÓN COMPLETA - SISTEMA LISTO"

### 2. Ve a TikTok Developers
```
https://developers.tiktok.com/
```

### 3. Crea App
```
Sign In → My Apps → Create App
Nombre: "Artok IA Viral Studio"
Categoría: "Content Publisher"
Crear
```

### 4. Agrega Producto
```
Left Menu → Products → Add Product
Busca: "Content Posting API"
Add
```

### 5. Configura Permisos
```
Scopes → Marca estas 3:
✅ user.info.basic
✅ video.upload
✅ video.list
Save
```

---

## 📝 EN 5 MINUTOS (Credenciales)

### 1. Copia Client Key y Secret
```
App Details → Client Key (copiar)
			  Client Secret (copiar)
```

### 2. Edita tu .env
```bash
notepad .env
```

Busca línea de TikTok y completa:
```env
TIKTOK_CLIENT_KEY=abc1234567890def      ← Tu Client Key aquí
TIKTOK_CLIENT_SECRET=xyz9876543210abc   ← Tu Secret aquí
TIKTOK_ACCESS_TOKEN=                    ← Lo obtenemos después
```

Guarda: Ctrl+S → Cierra

### 3. Obtén Access Token
```
En TikTok Developers:
Busca: "Get Access Token" o "Launch OAuth"
Autoriza los permisos
Copia el token (comienza con "act_...")
```

### 4. Completa .env
```env
TIKTOK_ACCESS_TOKEN=act_1234567890abcd...
```
Guarda

---

## ✅ VERIFICA (5 minutos)

### 1. Comprueba Credenciales
```bash
python test_integration.py
```

Deberías ver en TEST 3:
```
✅ TikTok: ✓ Credenciales cargadas
```

### 2. Ejecuta Sistema
```bash
python main.py
```

Deberías ver logs de TikTok:
```
[TT_CONNECTOR] Enviando payload a TikTok...
o
[TT_CONNECTOR] MODO LOCAL: simulado... (si USE_EXTERNAL_APIS=False)
```

---

## 🎯 LISTO!

```
✅ TikTok configurado
✅ Credenciales almacenadas de forma segura
✅ Sistema funcionando
✅ Sandbox activo
```

---

## 📚 SIGUIENTE NIVEL

### Quiero Entender Más
→ Lee: **TIKTOK_SETUP_GUIDE.md** (guía completa)

### Quiero Ir a Producción
→ Lee: TIKTOK_SETUP_GUIDE.md → Sección "Transición a Producción"

### Quiero Configurar Otras Plataformas También
→ Lee: **CREDENTIALS_GUIDE.md**

### Quiero Mapa Completo de Documentación
→ Lee: **DELIVERY_SUMMARY.md** o **INDEX.md**

---

## 🆘 Problemas?

| Problema | Solución |
|----------|----------|
| "No hay credenciales" | Edita `.env` de nuevo, guarda |
| "Token expirado" | Obtén nuevo en portal TikTok |
| ".env no se guarda" | Reinicia PowerShell después |
| "Test falla" | Revisa valores en .env (sin espacios) |

---

## ⏭️ Próximos Pasos

### Hoy
- ✅ Completaste esta guía

### Mañana
- [ ] Prueba publicación de video
- [ ] Integra con tu flujo

### Próxima Semana
- [ ] Submit for Review en TikTok
- [ ] Espera aprobación

### En 2 Semanas
- [ ] Lanzar en Producción
- [ ] USE_EXTERNAL_APIS=True

---

**¡TikTok está configurado! 🎉**

Para detalles: TIKTOK_SETUP_GUIDE.md
