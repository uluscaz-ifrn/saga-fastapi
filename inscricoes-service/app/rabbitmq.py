import pika, json, threading
from .database import SessionLocal
from .models import Inscricao

connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()
channel.exchange_declare(exchange="saga", exchange_type="fanout")

result = channel.queue_declare(queue="", exclusive=True)
queue = result.method.queue
channel.queue_bind(exchange="saga", queue=queue)

def publish(event):
    channel.basic_publish(exchange="saga", routing_key="", body=json.dumps(event))

def callback(ch, method, properties, body):
    event = json.loads(body)
    db = SessionLocal()

    if event.get("tipo") == "vaga_reserva_falhou":
        insc = db.query(Inscricao).get(event["inscricao_id"])
        if insc:
            insc.status = "CANCELADA"
            db.commit()

    if event.get("tipo") == "vaga_reservada":
        insc = db.query(Inscricao).get(event["inscricao_id"])
        if insc:
            insc.status = "CONFIRMADA"
            db.commit()

def start_consumer():
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    threading.Thread(target=channel.start_consuming, daemon=True).start()
