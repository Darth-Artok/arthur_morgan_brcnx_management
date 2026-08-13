# Contrato Director — Artok Viral Studio (Protocolo v1)

Documento canonico. Publisher responde al Director con ESTE contrato, sin improvisar conexiones.

## 1. Topologia
- director: unico orquestador. Emite TASK/COMMAND/DECISION a publisher.
- publisher: SOLO recibe TASK/COMMAND/DECISION del Director y SOLO responde al Director (REPORT/QUESTION/ERROR).
- Regla de oro: publisher NUNCA habla directo con producer/editor; todo pasa por el Director.
- Star topology: todos los subordinados se comunican unicamente con el Director (sin conexiones peer-to-peer).

## 2. Envelope canonico
{
  "protocol": "v1",
  "message_id": "uuid",
  "correlation_id": "uuid",
  "job_id": "uuid",
  "task_id": "uuid",
  "from": "director|publisher",
  "to": "director|publisher",
  "type": "TASK|REPORT|QUESTION|ERROR|DECISION|COMMAND",
  "stage": "prepare|publish|meta|rollback",
  "ts": "ISO8601"
}

## 3. Mensajes del Publisher
### 3.1 TASK (Director -> Publisher)
{
  "base": {},
  "assignee": "publisher",
  "op": "prepare_package|publish|rollback",
  "input": {"video":"/path.mp4","metadata":{...},"platforms":["youtube","tiktok"]},
  "deadline": "ISO8601",
  "priority": "low|normal|high"
}
### 3.2 REPORT (Publisher -> Director)
{
  "type": "REPORT",
  "status": "ok|partial|failed",
  "summary": "string",
  "outputs": {"status":"PARTIAL_SUCCESS","youtube":{"status":"PUBLISHED","url":"..."},"tiktok":{"status":"READY","requires_user_action":true}},
  "metrics": {"videos_uploaded":1,"platforms_ok":1,"requires_user_action":1},
  "next_suggested": ["publish","rollback"]
}
### 3.3 QUESTION (Publisher -> Director)
{
  "type": "QUESTION",
  "question": "string",
  "context": "string",
  "options": ["a","b"],
  "recommended_option": "a",
  "severity": "low|medium|high",
  "requires_human": false
}
### 3.4 ERROR (Publisher -> Director)
{
  "type": "ERROR",
  "severity": "warning|error",
  "error_code": "UPLOAD_FAILED|YOUTUBE_AUTH_FAILED|TIKTOK_AUTH_FAILED|CONTENT_ID|UNKNOWN",
  "message": "string",
  "retryable": true,
  "attempt": 1,
  "maximum_attempts": 3,
  "recommended_action": "retry|fallback|abort"
}
### 3.5 DECISION (Director -> Publisher)
{
  "type": "DECISION",
  "decision": "proceed|retry|abort|override|continue_without_segment|change_plan",
  "reason": "string",
  "instructions": "string"
}
### 3.6 COMMAND (Director -> Publisher)
{
  "type": "COMMAND",
  "command": "RETRY_TASK|CANCEL_TASK|REGENERATE_ASSET|SKIP_SEGMENT|REQUEST_HUMAN_REVIEW|CONTINUE|PAUSE_JOB",
  "target_task_id": "task_id",
  "instruction": "string"
}

## 4. Reglas innegociables
1. Cada TASK produce exactamente una respuesta (REPORT|QUESTION|ERROR).
2. retries max 3 (maximum_attempts). Pasado eso: fallback, revision o FAILED.
3. Nunca marcar tarea completada sin REPORT valido.
4. El Publisher NO toca el contenido del video: solo distribuye.
5. Respeta publish=only (solo prepare_package, no sube).
6. Si una plataforma requiere accion manual (TIKTOK_AUTH_FAILED), reportar con requires_user_action=true para HUMAN_REVIEW (el Director NO auto-publica sin aprobacion).
7. Ante TIKTOK_AUTH_FAILED no retryable -> QUESTION/ERROR requires_human=true.
8. Los artifacts (MP4) se referencian por ruta real en REPORT.outputs.
9. protocol v1 fijo.

## 5. Ops del Publisher
- prepare_package: recibe video+metadata+platforms, arma el paquete de subida por plataforma.
- publish: distribuye el video a YouTube/TikTok (o deja READY si requiere accion manual).
- rollback: despublica si el Director lo ordena (fallo grave o reclamo).
- El Publisher NO depende de Recurring Runs de Gemini: el Scheduler lo despierta.

## 6. Interfaz de entrada/salida
Entrada (TASK publish):
{
  "task_id": "task_003",
  "video": "/output/video_001.mp4",
  "metadata": {"title":"...", "description":"...", "tags":[...]},
  "platforms": ["youtube","tiktok"]
}
Salida (REPORT):
{
  "status": "PARTIAL_SUCCESS",
  "youtube": {"status":"PUBLISHED","url":"..."},
  "tiktok": {"status":"READY","requires_user_action":true}
}
