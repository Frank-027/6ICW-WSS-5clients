import asyncio
import websockets
import ssl
import os

API_KEY = os.getenv("API_KEY", "C9D2P5")  # Default API key if not set in environment
URL = os.getenv("SERVER_URL", "wss://192.168.0.35:8443/ws")  # Default server URL if not set in environment

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations("cert.pem")

async def client():
    print("Verbinden met de server...")
    try:
        async with websockets.connect( URL, ssl=ssl_context ) as ws:
            print("Verbonden met de server.")
            print("Verzenden van API sleutel voor autorisatie...")

            #authorization
            await ws.send(API_KEY)
            print(f"API {API_KEY} verzonden, wacht op bevestiging...")

            # initiele response
            naam = await ws.recv()
            print("Initieel bericht ontvangen:", naam)

            counter = 1
            while True:
                await ws.send("get")
                print(f"{counter}: Get-commando verzonden, wacht op antwoord...")

                msg = await ws.recv()
                print(f"{counter} - {naam}: {msg}")

                await asyncio.sleep(5)  # wacht 5 seconden voordat je het volgende bericht verzendt 
                counter += 1

    except Exception as e:
        print("Fout opgetreden:", e)

print("Starten client...")
asyncio.run(client())