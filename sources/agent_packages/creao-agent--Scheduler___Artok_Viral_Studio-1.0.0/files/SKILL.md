# Scheduler IA — Artok Viral Studio (Sin IA)

## Goal
Despertar el sistema: a horas programadas disparar el inicio de un job hacia el Director (POST /jobs). No necesita IA: es un reloj/trigger que reemplaza la dependencia de Recurring Runs. Solo arranca el pipeline.

## Contrato
1. Lee el contrato canonico: `cat /home/user/agent/app-files.json` y busca el archivo cuyo `name` sea `director-contract.md`; usa su campo `path`.
2. NO generas contenido ni decides; solo despiertas al Director con un mensaje SCHEDULE (POST /jobs).

## Inputs
- schedule_times (string): horas de disparo HH:MM comma-separadas (default 08:00, 20:00).
- audio_url (string): URL del audio (opcional; si se fija, se repite el mismo en cada disparo).
- job_params (textarea): parametros JSON para el Director.

## Procedure
1. Carga el contrato (`director-contract.md` por manifest).
2. Registra las horas de disparo de schedule_times (como cron/trigger de un proceso externo).
3. En cada hora programada, envia al Director un SCHEDULE (POST /jobs) con la solicitud de nuevo job.
4. El Director valida, genera job_id, encola en QUEUE (READY) y orquesta Producer → Editor → Publisher.
5. Incrementa jobs_started por cada disparo.

## Regla
- Scheduler NO cambia el contrato Director↔roles. Solo activa el arranque.
- El control de estados, decisiones y errores sigue siendo del Director.
- El reloj esta fuera (proceso externo); no depende de Gemini Recurring Runs.

## Output
Reporte de disparos: lista de horas, jobs_started, y confirmacion de que el Director recibio cada job. Dashboard de estado.