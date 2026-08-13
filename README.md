# Arthur Morgan Brcnx Management

Primer entorno local para probar agentes y multiagentes del pipeline:

Director -> Video Producer -> Editor -> Publisher

Este MVP usa una Queue en memoria y mensajes estructurados. No publica, no renderiza
video real y no usa credenciales. Sirve para validar el contrato inicial.

## Ejecutar

```powershell
python .\arthur_morgan_brcnx_management\main.py
```

## Siguiente paso

Cambiar `MemoryQueue` por una Queue persistente y mover los mensajes a esquemas JSON
versionados.
