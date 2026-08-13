# Contrato Director — Artok Viral Studio (Protocolo v1)

Documento canonico. El Scheduler es un componente de tiempo que despierta al sistema; no decide contenido.

## Rol del Scheduler
- NO necesita IA. Su unico trabajo es disparar el inicio de jobs a horas planificadas (ej. 08:00, 20:00).
- Ejecuta: scheduler → POST /jobs → Director.
- Reemplaza la dependencia del sistema de Recurring Runs: el reloj esta fuera (proceso externo o cron).
- No genera contenido, no decide prioridades creativas; solo despierta el pipeline.

## Flujo
08:00 → START JOB → Director (POST /jobs) → Queue → Producer → Editor → Publisher.

## Integracion
- Trigger: cron / webhook / proceso externo a una hora configurada.
- Cuando dispara, envia al Director la solicitud de nuevo job (audio_url y parametros).
- El Director registra el job (job_id), lo valida (VALIDATING) y lo encola (QUEUE READY).

## Envelope basico (POST /jobs)
{
  "type": "SCHEDULE",
  "from": "scheduler",
  "to": "director",
  "scheduled_at": "ISO8601",
  "job_request": { "audio_url": "...", "params": {...} }
}

## Regla
- Scheduler no cambia el contrato entre Director y roles (TASK/REPORT/QUESTION/ERROR/DECISION/COMMAND).
- Solo activa el arranque. El control de estados y decisiones sigue siendo del Director.
