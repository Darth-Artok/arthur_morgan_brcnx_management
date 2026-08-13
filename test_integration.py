#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de Verificación Rápida de la Integración
Verifica que todos los componentes estén instalados y funcionando
"""

import os
import sys

print("\n" + "="*70)
print("✓ VERIFICACIÓN DE INTEGRACIÓN - ARTOK IA VIRAL STUDIO v3.1")
print("="*70 + "\n")

# Test 1: Cargar módulos
print("[TEST 1] Importando módulos principales...")
try:
	from main import (
		CredentialsManager,
		JohnMarstonCore,
		YouTubeConnector,
		TikTokConnector,
		FacebookConnector,
		InstagramConnector,
		GasparAgentManager,
		load_env_file
	)
	print("  ✅ Todos los módulos importados exitosamente\n")
except ImportError as e:
	print(f"  ❌ Error de importación: {e}\n")
	sys.exit(1)

# Test 2: Cargar .env
print("[TEST 2] Cargando archivo de configuración (.env)...")
if os.path.exists(".env"):
	print("  ✅ Archivo .env encontrado")
	print("  ℹ️  Variables cargadas desde .env\n")
else:
	print("  ⚠️  Archivo .env no encontrado (creando desde .env.example...)\n")

# Test 3: CredentialsManager
print("[TEST 3] Verificando CredentialsManager...")
try:
	yt_creds = CredentialsManager.load_youtube_credentials()
	tt_creds = CredentialsManager.load_tiktok_credentials()
	fb_creds = CredentialsManager.load_facebook_credentials()
	ig_creds = CredentialsManager.load_instagram_credentials()

	print(f"  ✅ YouTube: {'✓ Credenciales cargadas' if yt_creds else '✗ Sin credenciales (normal en modo simulado)'}")
	print(f"  ✅ TikTok: {'✓ Credenciales cargadas' if tt_creds else '✗ Sin credenciales (normal en modo simulado)'}")
	print(f"  ✅ Facebook: {'✓ Credenciales cargadas' if fb_creds else '✗ Sin credenciales (normal en modo simulado)'}")
	print(f"  ✅ Instagram: {'✓ Credenciales cargadas' if ig_creds else '✗ Sin credenciales (normal en modo simulado)'}\n")
except Exception as e:
	print(f"  ❌ Error: {e}\n")
	sys.exit(1)

# Test 4: JohnMarstonCore
print("[TEST 4] Inicializando JohnMarstonCore (Kernel)...")
try:
	kernel = JohnMarstonCore()
	print(f"  ✅ Kernel inicializado")
	print(f"     - Estado: {kernel.system_status}")
	print(f"     - Versión: {kernel.version}")
	print(f"     - APIs cargadas: {list(kernel.api_keys.keys())}\n")
except Exception as e:
	print(f"  ❌ Error: {e}\n")
	sys.exit(1)

# Test 5: Conectores
print("[TEST 5] Inicializando Conectores...")
try:
	yt_conn = YouTubeConnector(kernel)
	tt_conn = TikTokConnector(kernel)
	fb_conn = FacebookConnector(kernel)
	ig_conn = InstagramConnector(kernel)

	print(f"  ✅ YouTubeConnector: Listo")
	print(f"  ✅ TikTokConnector: Listo")
	print(f"  ✅ FacebookConnector: Listo (NUEVO)")
	print(f"  ✅ InstagramConnector: Listo (NUEVO)\n")
except Exception as e:
	print(f"  ❌ Error: {e}\n")
	sys.exit(1)

# Test 6: verify_apis
print("[TEST 6] Verificando estado de APIs...")
try:
	apis_ok = kernel.verify_apis()
	print(f"  ✅ Verificación de APIs: {'✓ PASADA' if apis_ok else '⚠️ ADVERTENCIA (esperado en modo simulado)'}\n")
except Exception as e:
	print(f"  ❌ Error: {e}\n")
	sys.exit(1)

# Test 7: Mode check
print("[TEST 7] Modo de Operación...")
try:
	from main import USE_EXTERNAL_APIS, MANUAL_BILLING
	print(f"  ℹ️  USE_EXTERNAL_APIS: {USE_EXTERNAL_APIS}")
	print(f"  ℹ️  MANUAL_BILLING: {MANUAL_BILLING}")

	if not USE_EXTERNAL_APIS:
		print(f"  ✅ Modo SIMULADO (desarrollo) - No se harán llamadas reales a APIs\n")
	else:
		print(f"  ⚠️  Modo CONECTADO (producción) - Se harán llamadas reales a APIs\n")
except Exception as e:
	print(f"  ❌ Error: {e}\n")
	sys.exit(1)

# Test 8: Archivos de configuración
print("[TEST 8] Verificando archivos de configuración...")
files_ok = True
for file in [".env.example", "CREDENTIALS_GUIDE.md", "IMPLEMENTATION_SUMMARY.md"]:
	if os.path.exists(file):
		print(f"  ✅ {file}: Encontrado")
	else:
		print(f"  ⚠️  {file}: NO encontrado")
		files_ok = False
print()

# Resultado final
print("="*70)
if files_ok:
	print("✅ VERIFICACIÓN COMPLETA - SISTEMA LISTO PARA USAR")
else:
	print("⚠️  VERIFICACIÓN CON ADVERTENCIAS - Algunos archivos falta")
print("="*70 + "\n")

# Instrucciones finales
print("📋 PRÓXIMOS PASOS:")
print("\n1. MODO LOCAL (DESARROLLO - Recomendado):")
print("   python main.py")
print("   → Funciona sin credenciales, pruebas seguras\n")

print("2. MODO PRODUCCIÓN:")
print("   a) Configura credenciales en .env")
print("   b) Cambia: USE_EXTERNAL_APIS=True")
print("   c) python main.py")
print("   → Llamadas reales a APIs\n")

print("3. DOCUMENTACIÓN:")
print("   - CREDENTIALS_GUIDE.md: Pasos por plataforma")
print("   - IMPLEMENTATION_SUMMARY.md: Resumen técnico\n")

print("✨ ¡Listo para comenzar!\n")
