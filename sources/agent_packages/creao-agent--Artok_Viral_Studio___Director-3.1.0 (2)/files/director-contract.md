# Contrato Director — Artok Viral Studio (Protocolo v1)

Documento canonico. El Director es la unica fuente de verdad del contrato. Los roles se construyen EXACTAMENTE con este contrato, sin improvisar conexiones ni campos. Nada de comunicacion importante en texto libre: todo es un mensaje estructurado.

## 1. Topologia (no improvisar)
- **director**: unico orquestador. Habla con todos, recibe de todos.
- **video_producer | editor | publisher**: especialistas que SOLO reciben TASK/COMMAND/DECISION del Director y SOLO responden al Director.
- **scheduler**: NO usa IA. Programa despacho y prioridad de jobs hacia la Queue (proceso externo/cron, no Recurring Runs).
- **queue**: bandeja de trabajos que permite trabajo asincrono entre roles.
- Regla de oro: NUNCA conexiones director↔especialista↔especialista directas. Todo pasa por el Director y la Queue (star topology).

## 2. Queue (bandeja de trabajos)
La Queue es la pieza mas importante despues del Director.
- Estados de job en cola: READY | PROCESSING | WAITING | FAILED | COMPLETED.
- Flujo asincrono: Director → QUEUE → Producer → QUEUE → Editor → QUEUE → Publisher.
- Cada agente toma un job de la cola, trabaja y devuelve el resultado a la cola.
- Cada job tiene job_id unico; cada tarea task_id unico.
- El Director registra el job en la Queue, lo despacha y concilia el resultado; mantiene trazabilidad completa.

QUEUE
- JOB_001 READY
- JOB_002 PROCESSING
- JOB_003 WAITING
- JOB_004 FAILED
- JOB_005 COMPLETED

## 3. Envelope canonico (base de todo mensaje)
```json
{
  "protocol": "v1",
  "message_id": "uuid",
  "correlation_id": "uuid",
  "job_id": "uuid",
  "task_id": "uuid",
  "from": "director|video_producer|editor|publisher",
  "to": "director|video_producer|editor|publisher",
  "type": "TASK|REPORT|QUESTION|ERROR|DECISION|COMMAND",
  "stage": "segment|transcribe|generate|brief|assemble|render|qa|prepare|publish|meta",
  "ts": "ISO8601"
}
```

## 4. Tipos de mensaje (6 tipos) — con ejemplos canonicos

### 4.1 TASK (Director → rol) — asignar trabajo
Ejemplo:
{
  "type": "TASK",
  "from": "director",
  "to": "video_producer",
  "job_id": "job_001",
  "task_id": "task_001",
  "action": "generate_assets",
  "priority": "normal",
  "input": {...},
  "deadline": "ISO8601"
}
Action por rol:
- **Producer**: segment, transcribe_analyze, generate_clips, build_brief.
- **Editor**: assemble, render, qa.
- **Publisher**: prepare_package, publish, rollback.

### 4.2 REPORT (rol → Director) — progreso/finalizacion
Ejemplo:
{
  "type": "REPORT",
  "from": "video_producer",
  "to": "director",
  "job_id": "job_001",
  "task_id": "task_001",
  "status": "completed",
  "progress": 100,
  "outputs": {"artifacts": ["/ruta"]},
  "validation": {"qa_passed": true},
  "metrics": {...}
}
```

### 4.3 QUESTION (rol → Director) — necesita decision
Ejemplo:
{
  "type": "QUESTION",
  "from": "editor",
  "to": "director",
  "job_id": "job_001",
  "task_id": "task_002",
  "severity": "medium",
  "question": "¿Regenerar segmento 12?",
  "context": "...",
  "options": ["si","no"],
  "recommended_option": "si",
  "requires_human": false
}
```
El Director DEBE resolver con reglas/restricciones; si no hay decision segura → requires_human=true → HUMAN_REVIEW.

### 4.4 ERROR (rol → Director) — fallo
Ejemplo:
{
  "type": "ERROR",
  "from": "publisher",
  "to": "director",
  "job_id": "job_001",
  "task_id": "task_003",
  "severity": "error",
  "error_code": "TIKTOK_AUTH_FAILED",
  "message": "...",
  "retryable": false,
  "attempt": 1,
  "maximum_attempts": 3,
  "recommended_action": "abort"
}
```

### 4.5 DECISION (Director → rol) — resolucion operativa
Ejemplo:
{
  "type": "DECISION",
  "from": "director",
  "to": "editor",
  "job_id": "job_001",
  "task_id": "task_002",
  "decision": "continue_without_segment",
  "reason": "Asset unavailable",
  "instructions": "..."
}
```

### 4.6 COMMAND (Director → rol) — accion inmediata
Valores: RETRY_TASK | CANCEL_TASK | REGENERATE_ASSET | SKIP_SEGMENT | REQUEST_HUMAN_REVIEW | CONTINUE | PAUSE_JOB.
{
  "type": "COMMAND",
  "from": "director",
  "to": "publisher",
  "command": "RETRY_TASK",
  "target_task_id": "task_id",
  "instruction": "..."
}
```

## 5. Maquina de estados del job
SCHEDULED → RECEIVED → VALIDATING → PLANNED → PRODUCING → EDITING → VALIDATING_OUTPUT → PUBLISHING → COMPLETED.
En incidencias: → RETRYING | → WAITING_DECISION | → HUMAN_REVIEW | → FAILED.
- REPORT ok → avanzar. 
- QUESTION (decision segura) → DECISION y continua.
- QUESTION sin decision segura → HUMAN_REVIEW.
- ERROR retryable (attempt<3) → RETRYING; tras 3º fallo → fallback/HUMAN_REVIEW/FAILED.
- ERROR no retryable → fallback/HUMAN_REVIEW/FAILED.
Cada transicion se registra en el log del job (job_id).

## 6. Reglas de conexion (innegociables)
1. El Director es el UNICO emisor de TASK/COMMAND/DECISION.
2. Los roles devuelven SOLO REPORT/QUESTION/ERROR al Director con el mismo job_id/task_id.
3. Cada TASK tiene exactamente una respuesta (REPORT|QUESTION|ERROR) antes de la siguiente.
4. retries max 3 (maximum_attempts). Pasado eso: fallback, revision o FAILED.
5. Nunca marcar tarea completada sin REPORT valido.
6. Nunca publicar sin validacion del Editor (control de calidad).
7. Nunca inventar autorizacion humana.
8. protocolo v1 fijo. Si cambia → v2 y TODOS los roles migran juntos.
9. Los artifacts se guardan en files/ o /tmp/creao-artifacts/ y se referencian por ruta real en REPORT.outputs.

## 7. Interfaz por rol
### video_producer
- Ops: segment | transcribe_analyze | generate_clips | build_brief.
- Recibe: audio_url, segment_minutes, scenes_per_segment, story_theme, protagonist_image, cover_image.
### editor
- Ops: assemble | render | qa.
- Recibe: clips, audio de segmento, brief (titulo), estilo crossfade/titulos.
### publisher
- Ops: prepare_package | publish | rollback.
- Recibe: MP4 + metadata, plataformas objetivo.
- Respeta publish=only. Ante TIKTOK_AUTH_FAILED no retryable → HUMAN_REVIEW.

## 8. Dashboard final
- Resumen del audio (duracion, N segmentos, N videos).
- Brief por video.
- Estado por segmento y plataforma (tabla listos vs subidos).
- Estado de la Queue.
- Hoja de ruta de monetizacion.

## 9. Roadmap de roles
1. Producer → 2. Editor → 3. Publisher. Cada uno implementa su columna y habla por TASK/REPORT/QUESTION/ERROR/DECISION/COMMAND, sin cambiar el contrato.
