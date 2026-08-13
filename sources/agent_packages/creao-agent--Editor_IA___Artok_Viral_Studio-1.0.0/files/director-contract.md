# Contrato Director — Artok Viral Studio (Protocolo v1)

Documento canonico. Editor responde al Director con ESTE contrato, sin improvisar conexiones.

## 1. Topologia
- director: unico orquestador. Emite TASK/DECISION a editor.
- editor: SOLO recibe TASK/DECISION del Director y SOLO responde al Director (REPORT/QUESTION/ERROR).
- Regla de oro: editor NUNCA habla directo con producer/publisher; todo pasa por el Director.

## 2. Envelope canonico
{
  "protocol": "v1",
  "message_id": "uuid",
  "correlation_id": "uuid",
  "job_id": "uuid",
  "type": "TASK|REPORT|QUESTION|ERROR|DECISION",
  "stage": "assemble|render|qa",
  "ts": "ISO8601"
}

## 3. Mensajes del Editor
### 3.1 TASK (Director -> Editor)
{
  "base": {},
  "assignee": "editor",
  "op": "assemble|render|qa",
  "input": {"param": "value"},
  "deadline": "ISO8601",
  "priority": "low|normal|high"
}
### 3.2 REPORT (Editor -> Director)
{
  "type": "REPORT",
  "status": "ok|partial|failed",
  "summary": "string",
  "artifacts": ["/ruta/al/mp4"],
  "metrics": {"videos_editados":5,"duracion_s":120,"tamano_mb":45,"qa_passed":true},
  "next_suggested": ["assemble","render","qa"]
}
### 3.3 QUESTION (Editor -> Director)
{
  "type": "QUESTION",
  "requires": "string",
  "reason": "string",
  "options": ["a","b"],
  "default": "a",
  "blocks": true
}
### 3.4 ERROR (Editor -> Director)
{
  "type": "ERROR",
  "severity": "warning|error",
  "code": "NO_CLIPS|EDIT_FAILED|RENDER_FAILED|QA_FAILED|UNKNOWN",
  "message": "string",
  "recovery_suggested": "retry|abort|change_plan"
}
### 3.5 DECISION (Director -> Editor)
{
  "type": "DECISION",
  "resolution": "proceed|retry|abort|override|change_plan",
  "instruction": "string",
  "overrides": {"param":"value"},
  "retry_count": 0
}

## 4. Reglas innegociables
1. Cada TASK produce exactamente una respuesta (REPORT|QUESTION|ERROR).
2. retries max 3. Mas alla -> job failed.
3. Los MP4 se guardan en /tmp/creao-artifacts/ y se referencian por ruta real en REPORT.artifacts.
4. protocol v1 fijo.

## 5. Ops del Editor
- assemble: ensambla los clips IA + audio del segmento en un video (concat + crossfade).
- render: exporta el MP4 final de ~2 min (vertical 9:16), opcional titulos/subtitulos.
- qa: verifica calidad, duracion objetivo y tamano; reporta si pasa o no.
