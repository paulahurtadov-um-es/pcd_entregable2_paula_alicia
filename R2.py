# R2. El sistema notifica al sistema con un nuevo valor de temperatura cada 5 segundos de forma que el sistema 
# pueda recibir actualizaciones de datos en tiempo real y procesarlas adecuadamente.


import asyncio, time, random

async def nueva_temperatura():
    # Iniciamos el bucle con True porque queremos que esté 'siempre' activo, no indicamos parámetros de inicio y/o fin
    while True:
        t = random.randrange(0,50)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        await asyncio.sleep(5)
        print ("Nueva temperatura - Timestamp: {}, Temperatura: {}".format(timestamp,t))
    
if __name__ == "__main__":
    asyncio.run(nueva_temperatura())
        