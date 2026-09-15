# AMBM T16 Pilot Starter

Starter local para la frontera de control financiero del piloto T16.

**No mueve dinero, no contacta clientes y no sustituye la verificación bancaria humana.**

## Inicio
Windows: doble clic en `START_T16.bat`.

PowerShell:
```powershell
python ambm_t16.py init
python ambm_t16.py pilot --client-name "CLIENTE" --client-email "correo@ejemplo.com"
```

El comando `pilot` crea una orden local con ARTOK CONTENT, $3,500 MXN, anticipo de $1,750 MXN y referencia FX de $17 MXN/USD.

## Después de una transferencia real
Cuando el cliente haya transferido y entregue su comprobante:
```powershell
python ambm_t16.py evidence --payment-id PAY-XXXXXXXXXXXX --file "C:\ruta\comprobante.pdf" --amount-claimed 1750
```

Esto registra SHA-256 y deja el pago en `PAYMENT_PENDING_VERIFICATION`. **No lo aprueba.**

Después de comprobar humanamente que el dinero está acreditado:
```powershell
python ambm_t16.py verify --payment-id PAY-XXXXXXXXXXXX --decision APPROVE --operator "ARTURO" --reason "Transferencia acreditada y conciliada"
```

O rechazar:
```powershell
python ambm_t16.py verify --payment-id PAY-XXXXXXXXXXXX --decision REJECT --operator "ARTURO" --reason "No se acredita la transferencia"
```

## Inspección
```powershell
python ambm_t16.py status --payment-id PAY-XXXXXXXXXXXX
python ambm_t16.py report
```

Este starter demuestra la frontera `Evidence -> Human Verification -> PAYMENT_APPROVED -> Ledger -> Activation`, pero todavía no ejecuta por sí solo el Producer/QA/Delivery de AMBM.
