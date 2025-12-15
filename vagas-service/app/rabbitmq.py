import pika, json, threading

connection = pika.BlockingConnection(pika.ConnectionParameters(host="rabbitmq"))
channel = connection.channel()
channel.exchange_declare(exchange="saga", exchange_type="fanout")

result = channel.queue_declare(queue="", exclusive=True)
queue = result.method.queue
channel.queue_bind(exchange="saga", queue=queue)

def callback(ch, method, properties, body):
    event = json.loads(body)

    if event.get("tipo") == "inscricao_criada":
        if event.get("evento_id") == 99:
            channel.basic_publish(exchange="saga", routing_key="", body=json.dumps({
                "tipo": "vaga_reserva_falhou",
                "inscricao_id": event["inscricao_id"]
            }))
        else:
            channel.basic_publish(exchange="saga", routing_key="", body=json.dumps({
                "tipo": "vaga_reservada",
                "inscricao_id": event["inscricao_id"]
            }))

def start_consumer():
    channel.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    threading.Thread(target=channel.start_consuming, daemon=True).start()
