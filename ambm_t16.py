#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sqlite3, sys, uuid
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT=Path(__file__).resolve().parent
DB=ROOT/'ambm_t16.sqlite3'; EVD=ROOT/'evidence'; REPORT=ROOT/'PILOT_RUN_REPORT.json'
ALLOWED={
 'PAYMENT_CREATED':{'INSTRUCTIONS_DELIVERED'},
 'INSTRUCTIONS_DELIVERED':{'PAYMENT_PENDING'},
 'PAYMENT_PENDING':{'PAYMENT_EVIDENCE_RECEIVED'},
 'PAYMENT_EVIDENCE_RECEIVED':{'PAYMENT_PENDING_VERIFICATION'},
 'PAYMENT_PENDING_VERIFICATION':{'PAYMENT_APPROVED','PAYMENT_REJECTED'},
 'PAYMENT_APPROVED':set(),'PAYMENT_REJECTED':set()}
def now(): return datetime.now(timezone.utc).isoformat()
def rid(p): return f'{p}-{uuid.uuid4().hex[:12].upper()}'
def db():
 DB.parent.mkdir(parents=True,exist_ok=True); c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c
def init():
 EVD.mkdir(exist_ok=True)
 with db() as c:
  c.executescript('''PRAGMA journal_mode=WAL;
  CREATE TABLE IF NOT EXISTS requests(request_id TEXT PRIMARY KEY,client_name TEXT NOT NULL,client_email TEXT NOT NULL,service_id TEXT NOT NULL,amount_mxn REAL NOT NULL,fx_reference REAL NOT NULL,usd_reference_price REAL NOT NULL,quote_locked INTEGER NOT NULL,created_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS payments(payment_id TEXT PRIMARY KEY,request_id TEXT NOT NULL,order_id TEXT NOT NULL,provider TEXT NOT NULL,payment_method TEXT NOT NULL,amount REAL NOT NULL,currency TEXT NOT NULL,status TEXT NOT NULL,created_at TEXT NOT NULL,updated_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS evidence(evidence_id TEXT PRIMARY KEY,payment_id TEXT NOT NULL,request_id TEXT NOT NULL,order_id TEXT NOT NULL,evidence_type TEXT NOT NULL,file_reference TEXT NOT NULL,sha256 TEXT NOT NULL,amount_claimed REAL NOT NULL,currency TEXT NOT NULL,verification_status TEXT NOT NULL,received_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS decisions(decision_id TEXT PRIMARY KEY,payment_id TEXT NOT NULL,evidence_id TEXT NOT NULL,decision TEXT NOT NULL,operator TEXT NOT NULL,reason TEXT,timestamp TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS transitions(transition_id TEXT PRIMARY KEY,request_id TEXT NOT NULL,payment_id TEXT NOT NULL,from_state TEXT,to_state TEXT NOT NULL,actor TEXT NOT NULL,reason TEXT,idempotency_key TEXT NOT NULL UNIQUE,created_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS ledger(ledger_id TEXT PRIMARY KEY,request_id TEXT NOT NULL,order_id TEXT NOT NULL,payment_id TEXT NOT NULL,provider TEXT NOT NULL,payment_method TEXT NOT NULL,amount REAL NOT NULL,currency TEXT NOT NULL,status TEXT NOT NULL,evidence_id TEXT,decision_id TEXT,transition_id TEXT,idempotency_key TEXT NOT NULL UNIQUE,created_at TEXT NOT NULL);
  CREATE TABLE IF NOT EXISTS activations(activation_id TEXT PRIMARY KEY,request_id TEXT NOT NULL,payment_id TEXT NOT NULL,idempotency_key TEXT NOT NULL UNIQUE,result TEXT NOT NULL,created_at TEXT NOT NULL);''')
def tr(c,req,pay,frm,to,actor,reason):
 if to not in ALLOWED.get(frm,set()): raise ValueError(f'Illegal transition {frm}->{to}')
 idem=hashlib.sha256(f'{req}|{pay}|{frm}|{to}'.encode()).hexdigest(); tid=rid('TRN')
 c.execute('INSERT INTO transitions VALUES(?,?,?,?,?,?,?,?,?)',(tid,req,pay,frm,to,actor,reason,idem,now()))
 c.execute('UPDATE payments SET status=?,updated_at=? WHERE payment_id=?',(to,now(),pay)); return tid
def create(args):
 floor=Decimal(str(args.amount)); fx=Decimal(str(args.fx)); usd=(floor/fx).quantize(Decimal('.01'),ROUND_HALF_UP); dep=(floor/2).quantize(Decimal('.01'))
 req,order,pay=rid('req'),rid('ORD'),rid('PAY')
 with db() as c:
  c.execute('INSERT INTO requests VALUES(?,?,?,?,?,?,?,?,?)',(req,args.client_name,args.client_email,args.service_id,float(floor),float(fx),float(usd),1,now()))
  c.execute('INSERT INTO payments VALUES(?,?,?,?,?,?,?,?,?,?)',(pay,req,order,'BANK_TRANSFER','BANK_TRANSFER',float(dep),'MXN','PAYMENT_CREATED',now(),now()))
  t1=tr(c,req,pay,'PAYMENT_CREATED','INSTRUCTIONS_DELIVERED','SYSTEM','Payment instructions created')
  t2=tr(c,req,pay,'INSTRUCTIONS_DELIVERED','PAYMENT_PENDING','SYSTEM','Awaiting bank transfer')
 print(json.dumps({'request_id':req,'order_id':order,'payment_id':pay,'quote':{'service_id':args.service_id,'price_floor_mxn':float(floor),'deposit_mxn':float(dep),'balance_mxn':float(floor-dep),'fx_reference':float(fx),'usd_reference_price':float(usd),'quote_locked':True},'transitions':[t1,t2],'note':'No money was moved by this starter.'},indent=2))
def evidence(args):
 p=Path(args.file).resolve()
 if not p.is_file(): raise FileNotFoundError(p)
 h=hashlib.sha256(p.read_bytes()).hexdigest(); evid=rid('EVD')
 with db() as c:
  pay=c.execute('SELECT * FROM payments WHERE payment_id=?',(args.payment_id,)).fetchone()
  if not pay: raise ValueError('Unknown payment_id')
  if pay['status']!='PAYMENT_PENDING': raise ValueError(f"Expected PAYMENT_PENDING, got {pay['status']}")
  c.execute('INSERT INTO evidence VALUES(?,?,?,?,?,?,?,?,?,?,?)',(evid,args.payment_id,pay['request_id'],pay['order_id'],'TRANSFER_RECEIPT',str(p),h,args.amount_claimed,args.currency,'PENDING',now()))
  t1=tr(c,pay['request_id'],args.payment_id,'PAYMENT_PENDING','PAYMENT_EVIDENCE_RECEIVED','CLIENT_SUBMISSION','Receipt received; not approved')
  t2=tr(c,pay['request_id'],args.payment_id,'PAYMENT_EVIDENCE_RECEIVED','PAYMENT_PENDING_VERIFICATION','SYSTEM','Human verification required')
 print(json.dumps({'evidence_id':evid,'sha256':h,'verification_status':'PENDING','transitions':[t1,t2],'critical_rule':'COMPROBANTE != PAYMENT_APPROVED'},indent=2))
def verify(args):
 with db() as c:
  p=c.execute('SELECT * FROM payments WHERE payment_id=?',(args.payment_id,)).fetchone()
  if not p: raise ValueError('Unknown payment_id')
  if p['status']!='PAYMENT_PENDING_VERIFICATION': raise ValueError(f"Expected PAYMENT_PENDING_VERIFICATION, got {p['status']}")
  e=c.execute('SELECT * FROM evidence WHERE payment_id=? ORDER BY received_at DESC LIMIT 1',(args.payment_id,)).fetchone()
  if not e: raise ValueError('No evidence')
  did=rid('DEC'); dec=args.decision.upper(); final='PAYMENT_APPROVED' if dec=='APPROVE' else 'PAYMENT_REJECTED'
  c.execute('INSERT INTO decisions VALUES(?,?,?,?,?,?,?)',(did,args.payment_id,e['evidence_id'],dec,args.operator,args.reason,now()))
  c.execute('UPDATE evidence SET verification_status=? WHERE evidence_id=?',('VERIFIED' if dec=='APPROVE' else 'REJECTED',e['evidence_id']))
  tid=tr(c,p['request_id'],args.payment_id,'PAYMENT_PENDING_VERIFICATION',final,args.operator,args.reason or ('Human approval' if dec=='APPROVE' else 'Human rejection'))
  activation='DENY_PRODUCTION'
  if dec=='APPROVE':
   idem=hashlib.sha256(f"{p['request_id']}|{p['payment_id']}|ACTIVATE".encode()).hexdigest()
   c.execute('INSERT OR IGNORE INTO ledger VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(rid('LED'),p['request_id'],p['order_id'],p['payment_id'],p['provider'],p['payment_method'],p['amount'],p['currency'],'PAYMENT_APPROVED',e['evidence_id'],did,tid,idem,now()))
   if c.execute('SELECT 1 FROM activations WHERE idempotency_key=?',(idem,)).fetchone(): activation='DENY_DUPLICATE_ACTIVATION'
   else:
    c.execute('INSERT INTO activations VALUES(?,?,?,?,?,?)',(rid('ACT'),p['request_id'],p['payment_id'],idem,'ALLOW_TO_JMC',now())); activation='ALLOW_TO_JMC'
 print(json.dumps({'decision_id':did,'payment_status':final,'activation':activation,'transition_id':tid,'next_step':'JMC' if activation=='ALLOW_TO_JMC' else 'HUMAN_REVIEW'},indent=2))
def status(args):
 with db() as c:
  p=c.execute('SELECT * FROM payments WHERE payment_id=?',(args.payment_id,)).fetchone()
  if not p: raise ValueError('Unknown payment_id')
  def q(sql): return [dict(x) for x in c.execute(sql,(args.payment_id,)).fetchall()]
  print(json.dumps({'payment':dict(p),'transitions':q('SELECT * FROM transitions WHERE payment_id=? ORDER BY created_at'),'evidence':q('SELECT * FROM evidence WHERE payment_id=? ORDER BY received_at'),'decisions':q('SELECT * FROM decisions WHERE payment_id=? ORDER BY timestamp'),'activations':q('SELECT * FROM activations WHERE payment_id=? ORDER BY created_at')},indent=2))
def report(_):
 with db() as c:
  data={'report_type':'AMBM_PILOT_RUN_REPORT','generated_at':now(),'pilot_result':'PENDING','real_cash_collected':0,'simulated_cash_collected':0,'felix_status':'FUTURE','n8n_dependency':'NOT_REQUIRED_FOR_THIS_LOCAL_STARTER','final_acceptance':'NOT_SUCCESS','payments':[dict(x) for x in c.execute('SELECT * FROM payments ORDER BY created_at DESC')]}
 REPORT.write_text(json.dumps(data,indent=2),encoding='utf-8'); print(REPORT)
def main():
 ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
 sp.add_parser('init').set_defaults(fn=lambda a:(init(),print(f'Initialized {DB}')))
 p=sp.add_parser('pilot'); p.add_argument('--client-name',required=True); p.add_argument('--client-email',required=True); p.add_argument('--service-id',default='ARTOK_CONTENT'); p.add_argument('--amount',type=Decimal,default=Decimal('3500')); p.add_argument('--fx',type=Decimal,default=Decimal('17')); p.set_defaults(fn=create)
 p=sp.add_parser('evidence'); p.add_argument('--payment-id',required=True); p.add_argument('--file',required=True); p.add_argument('--amount-claimed',type=float,required=True); p.add_argument('--currency',default='MXN'); p.set_defaults(fn=evidence)
 p=sp.add_parser('verify'); p.add_argument('--payment-id',required=True); p.add_argument('--decision',choices=['APPROVE','REJECT'],required=True); p.add_argument('--operator',required=True); p.add_argument('--reason',default=''); p.set_defaults(fn=verify)
 p=sp.add_parser('status'); p.add_argument('--payment-id',required=True); p.set_defaults(fn=status)
 sp.add_parser('report').set_defaults(fn=report)
 a=ap.parse_args(); init()
 try: a.fn(a)
 except Exception as e: print(f'ERROR: {e}',file=sys.stderr); sys.exit(1)
if __name__=='__main__': main()
