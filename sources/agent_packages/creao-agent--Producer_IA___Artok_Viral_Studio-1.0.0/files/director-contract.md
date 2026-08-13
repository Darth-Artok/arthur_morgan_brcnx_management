# Contrato Director — Artok Viral Studio (Protocolo v1)

Documento canonico. Producer responde al Director con ESTE contrato, sin improvisar conexiones.

## 1. Topologia
- director: unico orquestador. Emite TASK/DECISION a producer.
- producer: SOLO recibe TASK/DECISION del Director y SOLO responde al Director (REPORT/QUESTION/ERROR).
- Regla de oro: producer NUNCA habla directo con editor/publisher; todo pasa por el Director.

## 2. Envelope canonico
{
  "protocol": "v1",
  "message_id": "uuid",
  "correlation_id": "uuid",
  "job_id": "uuid",
  "type": "TASK|REPORT|QUESTION|ERROR|DECISION",
  "stage": "segment|transcribe|generate|brief",
  "ts": "ISO8601"
}

## 3. Mensajes del Producer
### 3.1 TASK (Director -> Producer)
{
  "base": {},
  "assignee": "producer",
  "op": "segment|transcribe_analyze|generate_clips|build_brief",
  "input": {"param": "value"},
  "deadline": "ISO8601",
  "priority": "low|normal|high"
}
### 3.2 REPORT (Producer -> Director)
{
  "type": "REPORT",
  "status": "ok|partial|failed",
  "summary": "string",
  "artifacts": ["/ruta"],
  "metrics": {"duracion_s":120,"clips":6,"escenas":3,"briefs":1},
  "next_suggested": ["segment","transcribe_analyze","generate_clips","build_brief"]
}
### 3.3 QUESTION (Producer -> Director)
{
  "type": "QUESTION",
  "requires": "string",
  "reason": "string",
  "options": ["a","b"],
  "default": "a",
  "blocks": true
}
### 3.4 ERROR (Producer -> Director)
{
  "type": "ERROR",
  "severity": "warning|error",
  "code": "NO_AUDIO|TOO_SHORT|GEN_FAILED|TRANSCRIBE_FAILED|UNKNOWN",
  "message": "string",
  "recovery_suggested": "retry|abort|change_plan"
}
### 3.5 DECISION (Director -> Producer)
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
3. Los artifacts se guardan en files/ o /tmp/creao-artifacts/ y se referencian por ruta real en REPORT.artifacts.
4. protocol v1 fijo.

## 5. Ops del Producer
- segment: corta audio en N segmentos de segment_minutes.
- transcribe_analyze: transcribe cada segmento (speech_to_text) y separa en Escena 1..N (intro/hook/climax/outro).
- generate_clips: genera clips IA verticales 9:16 por escena con protagonista y estetica GTA.
- build_brief: genera brief por video (titulo, escenas, hashtags, hook).
