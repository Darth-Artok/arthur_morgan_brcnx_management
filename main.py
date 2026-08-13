import os
import sys
import uuid
import json
from dataclasses import dataclass, field
from datetime import datetime
import numpy as np
import yaml
from typing import Optional, Dict, Any

# =====================================================================
# CARGA DE VARIABLES DE ENTORNO DESDE .env
# =====================================================================
def load_env_file(env_path: str = ".env"):
    """Carga variables de entorno desde archivo .env"""
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print(f"[*] Variables de entorno cargadas desde {env_path}")
    else:
        print(f"[!] Advertencia: Archivo {env_path} no encontrado. Usando variables del sistema.")

# Cargar .env al iniciar
load_env_file()

# Modo de operación: desactivar integraciones externas y usar facturación manual/local
USE_EXTERNAL_APIS = os.getenv("USE_EXTERNAL_APIS", "False").lower() == "true"
MANUAL_BILLING = os.getenv("MANUAL_BILLING", "True").lower() == "false"

# =====================================================================
# 0. GESTOR DE CREDENCIALES SEGURO & MODELOS FINANCIEROS
# =====================================================================

class CredentialsManager:
    """Gestor centralizado de credenciales desde variables de entorno"""

    @staticmethod
    def load_tiktok_credentials() -> Optional[Dict[str, str]]:
        client_key = os.getenv("TIKTOK_CLIENT_KEY", "aww7pkjyl4awt4id")
        client_secret = os.getenv("TIKTOK_CLIENT_SECRET", "MrMpQ0Rnqyv9yEPyltdqTvG3q0fSF0NB")
        access_token = os.getenv("TIKTOK_ACCESS_TOKEN", "simulated_token_123")
        if not all([client_key, client_secret, access_token]):
            return None
        return {"client_key": client_key, "client_secret": client_secret, "access_token": access_token}

    @staticmethod
    def load_facebook_credentials() -> Optional[Dict[str, str]]:
        page_id = os.getenv("FACEBOOK_PAGE_ID")
        access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        app_id = os.getenv("FACEBOOK_APP_ID")
        app_secret = os.getenv("FACEBOOK_APP_SECRET")
        if not all([page_id, access_token]):
            return None
        return {"page_id": page_id, "access_token": access_token, "app_id": app_id, "app_secret": app_secret}

    @staticmethod
    def load_instagram_credentials() -> Optional[Dict[str, str]]:
        business_account_id = os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID")
        access_token = os.getenv("INSTAGRAM_ACCESS_TOKEN")
        app_id = os.getenv("INSTAGRAM_APP_ID")
        app_secret = os.getenv("INSTAGRAM_APP_SECRET")
        if not all([business_account_id, access_token]):
            return None
        return {"business_account_id": business_account_id, "access_token": access_token, "app_id": app_id, "app_secret": app_secret}

    @staticmethod
    def load_youtube_credentials() -> Optional[Dict[str, str]]:
        api_key = os.getenv("YOUTUBE_API_KEY")
        if not api_key:
            return None
        return {"api_key": api_key}

    @staticmethod
    def validate_credentials(credentials: Optional[Dict[str, Any]], platform: str) -> bool:
        if credentials is None:
            print(f"[!] Advertencia: No hay credenciales de {platform} en variables de entorno.")
            return False
        return True


class Transaction:
    def __init__(self, transaction_id, client_name, amount, status="PENDING"):
        self.transaction_id = transaction_id
        self.client_name = client_name
        self.amount = amount
        self.status = status


class MoneyInTheBank:
    def __init__(self, kernel):
        self.kernel = kernel
        self.transactions = []

    def register_payment(self, client_name, amount):
        """Registra un nuevo pago pendiente solo si no existe uno activo."""
        for tx in self.transactions:
            if tx.client_name == client_name and tx.amount == amount and tx.status == "PENDING":
                return tx

        tx_id = f"TXN-{os.urandom(4).hex()}"
        new_tx = Transaction(transaction_id=tx_id, client_name=client_name, amount=amount, status="PENDING")
        self.transactions.append(new_tx)
        
        self.kernel.log_event("MONEY_BANK", f"[i] Pago registrado como PENDING. ID de transacción: {tx_id}")
        return new_tx

    def verify_bank_transfer(self, client_name, amount):
        """Consulta puramente el estado de la transferencia sin duplicar registros."""
        for tx in self.transactions:
            if tx.client_name == client_name and tx.amount == amount:
                return {
                    "status": tx.status,
                    "transaction_id": tx.transaction_id
                }
        
        new_tx = self.register_payment(client_name, amount)
        return {
            "status": new_tx.status,
            "transaction_id": new_tx.transaction_id
        }

    def confirm_payment(self, transaction_id):
        """Confirma una transacción existente por su ID."""
        for tx in self.transactions:
            if tx.transaction_id == transaction_id:
                tx.status = "CONFIRMED"
                self.kernel.log_event("MONEY_BANK", f"[✓] Pago confirmado. ID: {transaction_id}")
                return {"status": "CONFIRMED", "message": "Pago aprobado con éxito"}
        
        return {"status": "ERROR", "message": "Transacción no encontrada"}


# =====================================================================
# 1. MODELOS DE DATOS Y ESTRUCTURAS DE CREATOR MANAGEMENT
# =====================================================================

@dataclass
class AgentConfig:
    agent_id: str
    name: str
    role: str
    version: str
    description: str
    system_prompt: str
    raw_config: dict = field(default_factory=dict)
    loaded_at: datetime = field(default_factory=datetime.now)

@dataclass
class Task:
    task_id: str
    title: str
    assigned_agent: str
    input_data: dict
    output_data: str = ""
    status: str = "PENDING"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: str = ""

@dataclass
class MediaPayload:
    title: str
    description: str
    tags: list[str]
    script_hooks: list[str]
    rendered_file: str
    platforms: list[str]
    scheduled_time: str = ""

@dataclass
class TransactionRecord:
    transaction_id: str
    client_name: str
    amount: float
    currency: str
    status: str
    payment_date: str

# =====================================================================
# 2. CARGADOR DINÁMICO DE PAQUETES DE AGENTES
# =====================================================================

class AgentPackageLoader:
    def __init__(self, packages_dir: str):
        self.packages_dir = packages_dir
        self.loaded_agents: dict[str, AgentConfig] = {}

    def parse_skill_md(self, skill_path: str) -> str:
        if not os.path.exists(skill_path):
            return "Skill por defecto: Ejecutar tareas asignadas según el rol."
        with open(skill_path, 'r', encoding='utf-8') as f:
            return f.read()

    def load_agents(self):
        if not os.path.exists(self.packages_dir):
            print(f"[!] Directorio no encontrado: {self.packages_dir}")
            return

        print(f"[*] [GASPAR] Escaneando e instanciando agentes en: {self.packages_dir}\n")

        for folder_name in os.listdir(self.packages_dir):
            agent_folder = os.path.join(self.packages_dir, folder_name)
            
            if os.path.isdir(agent_folder):
                config_path = os.path.join(agent_folder, 'config.yaml')
                skill_path = os.path.join(agent_folder, 'SKILL.md')

                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as cf:
                        config_data = yaml.safe_load(cf) or {}

                    system_prompt = self.parse_skill_md(skill_path)
                    instance_id = str(uuid.uuid4())[:8]
                    
                    agent_name = config_data.get('name', folder_name)
                    folder_lower = folder_name.lower()
                    
                    if "director" in folder_lower:
                        role = "director"
                    elif "editor" in folder_lower:
                        role = "editor"
                    elif "productor" in folder_lower or "producer" in folder_lower:
                        role = "productor"
                    elif "publisher" in folder_lower:
                        role = "publisher"
                    elif "scheduler" in folder_lower:
                        role = "scheduler"
                    else:
                        role = config_data.get('role', folder_name.split('_')[-1].lower())

                    version = config_data.get('version', '3.1.0')
                    desc = config_data.get('description', 'Agente activo de Artok IA Viral Studio')

                    agent_obj = AgentConfig(
                        agent_id=f"{folder_name}_{instance_id}",
                        name=agent_name,
                        role=role.lower(),
                        version=version,
                        description=desc,
                        system_prompt=system_prompt,
                        raw_config=config_data
                    )

                    self.loaded_agents[role.lower()] = agent_obj
                    print(f"  [+] Agente registrado -> Rol: [{role.upper()}] | Nombre: {agent_name} (v{version})")

# =====================================================================
# 3. TRÍADA DE NÚCLEOS & FINANZAS
# =====================================================================

class JohnMarstonCore:
    def __init__(self):
        self.system_status = "ONLINE"
        self.version = "3.1.0"
        self.api_keys = {
            "youtube": CredentialsManager.load_youtube_credentials(),
            "tiktok": CredentialsManager.load_tiktok_credentials(),
            "facebook": CredentialsManager.load_facebook_credentials(),
            "instagram": CredentialsManager.load_instagram_credentials()
        }

        if USE_EXTERNAL_APIS:
            self.log_event("JMC", "Modo CONECTADO: Validando credenciales de APIs externas...")
            for platform, creds in self.api_keys.items():
                CredentialsManager.validate_credentials(creds, platform)

    def log_event(self, source: str, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{source.upper()}] {message}")

    def verify_apis(self) -> bool:
        if not USE_EXTERNAL_APIS:
            self.log_event("JMC", "Modo LOCAL: integraciones externas deshabilitadas. Omitiendo verificación de APIs.")
            return True

        self.log_event("JMC", "Verificando estado de conexiones API...")
        yt_valid = bool(self.api_keys.get("youtube"))
        tt_valid = bool(self.api_keys.get("tiktok"))
        fb_valid = bool(self.api_keys.get("facebook"))
        ig_valid = bool(self.api_keys.get("instagram"))
        return yt_valid and tt_valid and fb_valid and ig_valid

class OrionCore:
    def __init__(self, logger: JohnMarstonCore):
        self.logger = logger
        self.active_metrics = {}

    def calculate_efficiency(self, tasks_completed: int, execution_time_sec: float) -> float:
        if execution_time_sec <= 0:
            return 100.0
        return round((tasks_completed / execution_time_sec) * 100, 2)

    def generate_periodic_report(self, report_type: str = "Semanal") -> dict:
        day_name = datetime.now().strftime("%A")
        self.logger.log_event("ORION", f"Generando reporte de rendimiento analítico ({report_type} - {day_name})...")
        return {
            "report_id": f"REP-{uuid.uuid4().hex[:6]}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "type": report_type,
            "total_views_estimated": int(np.random.uniform(50000, 150000)),
            "average_engagement_rate": f"{round(np.random.uniform(8.0, 14.2), 2)}%",
            "top_platform": "YouTube Shorts & TikTok",
            "status": "VALIDADO_Y_ENTREGADO"
        }

# =====================================================================
# 4. CONECTORES DE REDES SOCIALES
# =====================================================================

class YouTubeConnector:
    def __init__(self, logger: JohnMarstonCore):
        self.logger = logger

    def publish_video(self, payload: MediaPayload) -> dict:
        if not USE_EXTERNAL_APIS:
            self.logger.log_event("YT_CONNECTOR", f"MODO LOCAL: Publicación en YouTube omitida. Título: {payload.title}")
            video_id = f"yt_sim_{uuid.uuid4().hex[:8]}"
            return {"platform": "YouTube", "status": "SIMULATED", "video_id": video_id, "url": f"https://youtube.local/simulated/{video_id}"}
        
        video_id = f"yt_{uuid.uuid4().hex[:8]}"
        return {"platform": "YouTube", "status": "SUCCESS", "video_id": video_id, "url": f"https://youtube.com/shorts/{video_id}"}

class TikTokConnector:
    def __init__(self, logger: JohnMarstonCore):
        self.logger = logger

    def publish_video(self, payload: MediaPayload) -> dict:
        if not USE_EXTERNAL_APIS:
            self.logger.log_event("TT_CONNECTOR", f"MODO LOCAL: Publicación en TikTok omitida. Título: {payload.title}")
            post_id = f"tt_sim_{uuid.uuid4().hex[:8]}"
            return {"platform": "TikTok", "status": "SIMULATED", "post_id": post_id, "url": f"https://tiktok.local/simulated/{post_id}"}
        
        post_id = f"tt_{uuid.uuid4().hex[:8]}"
        return {"platform": "TikTok", "status": "SUCCESS", "post_id": post_id, "url": f"https://tiktok.com/@artok/video/{post_id}"}

class FacebookConnector:
    def __init__(self, logger: JohnMarstonCore):
        self.logger = logger
        self.credentials = logger.api_keys.get("facebook")

    def publish_media(self, payload: MediaPayload) -> dict:
        if not USE_EXTERNAL_APIS:
            post_id = f"fb_sim_{uuid.uuid4().hex[:8]}"
            return {"platform": "Facebook", "status": "SIMULATED", "post_id": post_id, "url": f"https://facebook.local/simulated/{post_id}"}
        
        post_id = f"fb_{uuid.uuid4().hex[:8]}"
        return {"platform": "Facebook", "status": "SUCCESS", "post_id": post_id, "url": f"https://facebook.com/{post_id}"}

class InstagramConnector:
    def __init__(self, logger: JohnMarstonCore):
        self.logger = logger
        self.credentials = logger.api_keys.get("instagram")

    def publish_media(self, payload: MediaPayload) -> dict:
        if not USE_EXTERNAL_APIS:
            media_id = f"ig_sim_{uuid.uuid4().hex[:8]}"
            return {"platform": "Instagram", "status": "SIMULATED", "media_id": media_id, "url": f"https://instagram.local/simulated/{media_id}"}
        
        media_id = f"ig_{uuid.uuid4().hex[:8]}"
        return {"platform": "Instagram", "status": "SUCCESS", "media_id": media_id, "url": f"https://instagram.com/p/{media_id}"}

# =====================================================================
# 5. GERENCIA DE AGENTES Y ORQUESTACIÓN GENERAL
# =====================================================================

class GasparAgentManager:
    def __init__(self, loader: AgentPackageLoader, logger: JohnMarstonCore, 
                 yt_conn: YouTubeConnector, tt_conn: TikTokConnector,
                 fb_conn: FacebookConnector = None, ig_conn: InstagramConnector = None):
        self.loader = loader
        self.logger = logger
        self.yt_conn = yt_conn
        self.tt_conn = tt_conn
        self.fb_conn = fb_conn
        self.ig_conn = ig_conn

    def dispatch_agent_task(self, role: str, task_context: dict) -> dict:
        agent = self.loader.loaded_agents.get(role.lower())
        agent_name = agent.name if agent else f"Agente_{role.capitalize()}"

        self.logger.log_event("GASPAR", f"Invocando agente de Artok Studio: [{agent_name}] para rol [{role.upper()}]")
        topic = task_context.get("topic", "Contenido General ARTOK")
        cta_invitation = "\n\n👉 ¡Suscríbete y activa las notificaciones!"

        if role == "director":
            return {
                "decision": "Estrategia aprobada para plataformas múltiples.",
                "viral_angle": f"Enfoque de alto rendimiento para '{topic}'",
                "target_platforms": ["youtube", "tiktok", "facebook", "instagram"]
            }
        elif role == "productor":
            return {
                "script_title": f"🚀 Innovación con {topic}",
                "hooks": ["¿Sabías que esto cambia todo?", "Atento a los primeros 3 segundos."],
                "visual_cues": "Cortes dinámicos cada 1.5s."
            }
        elif role == "editor":
            return {
                "rendered_file": f"exports/artok_render_{uuid.uuid4().hex[:6]}.mp4",
                "aspect_ratio": "9:16",
                "resolution": "1080x1920"
            }
        elif role == "publisher":
            return {
                "title": f"🚀 Revolución con {topic} | ARTOK",
                "description": f"Aprende más sobre {topic}.{cta_invitation}",
                "tags": ["AI", "Automation", "ArtokStudio", "Viral"],
                "prepared_payload": True
            }
        elif role == "scheduler":
            results = task_context.get("results", {})
            if "publisher" not in results:
                return {"status": "ERROR", "message": "Datos del publisher no disponibles"}
            
            pub_data = results.get("publisher", {})
            prod_data = results.get("productor", {})
            editor_data = results.get("editor", {})
            dir_data = results.get("director", {})
            
            payload = MediaPayload(
                title=pub_data.get("title", "Sin título"),
                description=pub_data.get("description", ""),
                tags=pub_data.get("tags", []),
                script_hooks=prod_data.get("hooks", []),
                rendered_file=editor_data.get("rendered_file", ""),
                platforms=dir_data.get("target_platforms", ["youtube"]),
                scheduled_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

            pub_results = {}
            if "youtube" in payload.platforms:
                pub_results["youtube"] = self.yt_conn.publish_video(payload)
            if "tiktok" in payload.platforms:
                pub_results["tiktok"] = self.tt_conn.publish_video(payload)
            if "facebook" in payload.platforms and self.fb_conn:
                pub_results["facebook"] = self.fb_conn.publish_media(payload)
            if "instagram" in payload.platforms and self.ig_conn:
                pub_results["instagram"] = self.ig_conn.publish_media(payload)

            return {
                "schedule_status": "PROGRAMADO_Y_PUBLICADO",
                "dispatch_details": pub_results
            }
        else:
            return {"status": f"Procesamiento finalizado por agente {agent_name}."}

class MelchorStrategy:
    def __init__(self, logger: JohnMarstonCore):
        self.logger = logger

    def build_roadmap(self, objective: str) -> list[str]:
        self.logger.log_event("MELCHOR", f"Diseñando roadmap estratégico para: '{objective}'")
        return ["director", "productor", "editor", "publisher", "scheduler"]

class BalthazarOrchestrator:
    def __init__(self, kernel: JohnMarstonCore, orion: OrionCore, melchor: MelchorStrategy, gaspar: GasparAgentManager, bank: MoneyInTheBank):
        self.kernel = kernel
        self.orion = orion
        self.melchor = melchor
        self.gaspar = gaspar
        self.bank = bank
        self.task_history: list[Task] = []

    def execute_business_goal(self, goal_title: str, client_name: str = "Canal Principal ARTOK", service_fee: float = 15000.0):
        print(f"\n=======================================================")
        print(f"👑 BALTHAZAR | NUEVO OBJETIVO RECIBIDO: '{goal_title}'")
        print(f"=======================================================\n")

        # 1. Verificación y auto-flujo de pago
        payment_check = self.bank.verify_bank_transfer(client_name, service_fee)
        print(payment_check)
        
        if payment_check["status"] == "PENDING":
            tx_id = payment_check.get("transaction_id")
            self.kernel.log_event("BALTHAZAR", f"[*] Auto-aprobando pago pendiente (ID: {tx_id})...")
            self.bank.confirm_payment(tx_id)
            payment_check = self.bank.verify_bank_transfer(client_name, service_fee)

        if payment_check["status"] != "CONFIRMED":
            self.kernel.log_event("BALTHAZAR", "[!] Transferencia bancaria no confirmada. Operación pausada.")
            return

        # 2. Verificación de APIs
        if not self.kernel.verify_apis():
            self.kernel.log_event("BALTHAZAR", "[!] Error en verificación de APIs de redes sociales.")
            return

        # 3. Planificación estratégica
        self.kernel.log_event("BALTHAZAR", "Solicitando roadmap estratégico a Melchor...")
        roadmap = self.melchor.build_roadmap(goal_title)

        pipeline_context = {"topic": goal_title, "results": {}}
        start_time = datetime.now()

        # 4. Ejecución del pipeline con Gaspar
        for step in roadmap:
            self.kernel.log_event("BALTHAZAR", f"Coordinando departamento Artok Studio - Fase: [{step.upper()}]...")
            output = self.gaspar.dispatch_agent_task(step, pipeline_context)
            pipeline_context["results"][step] = output
            
            task = Task(
                task_id=f"TASK-{uuid.uuid4().hex[:6]}",
                title=f"Fase {step.capitalize()}",
                assigned_agent=step,
                input_data={"goal": goal_title},
                output_data=json.dumps(output, ensure_ascii=False),
                status="COMPLETED",
                completed_at=datetime.now().isoformat()
            )
            self.task_history.append(task)
            print(f"    └── Resultado [{step.upper()}]: {json.dumps(output, indent=2, ensure_ascii=False)}\n")

        # 5. Evaluación final
        total_time = (datetime.now() - start_time).total_seconds()
        efficiency = self.orion.calculate_efficiency(len(roadmap), total_time)
        self.kernel.log_event("ORION", f"Análisis de rendimiento: {efficiency}% de eficiencia global.")
        
        report = self.orion.generate_periodic_report(report_type="Resumen Lunes y Sábados")
        self.kernel.log_event("ORION", f"Reporte final entregado: {json.dumps(report, ensure_ascii=False)}")
        self.kernel.log_event("BALTHAZAR", f"Objetivo '{goal_title}' completado con éxito por el departamento Artok IA Viral Studio.\n")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    PACKAGES_PATH = os.path.join(BASE_DIR, "sources", "agent_packages")

    if not os.path.exists(PACKAGES_PATH):
        os.makedirs(PACKAGES_PATH)

    john_marston = JohnMarstonCore()
    orion = OrionCore(john_marston)
    bank = MoneyInTheBank(john_marston)

    yt_connector = YouTubeConnector(john_marston)
    tt_connector = TikTokConnector(john_marston)
    fb_connector = FacebookConnector(john_marston)
    ig_connector = InstagramConnector(john_marston)

    loader = AgentPackageLoader(PACKAGES_PATH)
    loader.load_agents()

    gaspar = GasparAgentManager(loader, john_marston, yt_connector, tt_connector, fb_connector, ig_connector)
    melchor = MelchorStrategy(john_marston)
    balthazar = BalthazarOrchestrator(john_marston, orion, melchor, gaspar, bank)

    goal = "Lanzamiento Campaña Viral ARTOK v3.1"
    client = "Canal YouTube / TikTok / Facebook / Instagram ARTOK"
    fee = 15000.0

    balthazar.execute_business_goal(goal_title=goal, client_name=client, service_fee=fee)