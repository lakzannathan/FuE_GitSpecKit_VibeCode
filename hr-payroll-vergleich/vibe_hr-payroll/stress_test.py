import asyncio
import httpx
import time
import sys

# Konfiguration
BASE_URL = "http://127.0.0.1:8000"
# ID 1 ist der Max Mustermann, der beim Start angelegt wird
EMPLOYEE_ID = 1 

async def trigger_payroll(client, emp_id):
    """
    Startet die langsame Legacy-Berechnung (POST Request).
    """
    start = time.time()
    print(f"   🔨 [Heavy Task] Starte Payroll-Berechnung für MA {emp_id}...")
    try:
        # Timeout hochsetzen, da die Legacy Engine langsam ist
        response = await client.post(
            f"{BASE_URL}/hr/payroll/calculate/{emp_id}", 
            timeout=10.0
        )
        duration = time.time() - start
        if response.status_code == 200:
            print(f"   ✅ [Heavy Task] Fertig in {duration:.3f}s")
        else:
            print(f"   ⚠️ [Heavy Task] Fehler: Status {response.status_code}")
        return duration
    except Exception as e:
        print(f"   ❌ [Heavy Task] Request fehlgeschlagen: {e}")
        return 0

async def check_responsiveness(client):
    """
    Versucht, den Server während der Berechnung anzupingen (GET Request).
    Sollte eigentlich sofort (< 0.1s) antworten.
    """
    start = time.time()
    print("   🔎 [Ping] Versuche Server zu erreichen...")
    try:
        # Kurzer Timeout: Wenn der Server blockiert, läuft das hier in den Timeout
        response = await client.get(f"{BASE_URL}/", timeout=2.0)
        duration = time.time() - start
        print(f"   📨 [Ping] Antwort erhalten in {duration:.3f}s")
        return duration
    except httpx.ReadTimeout:
        print("   🐌 [Ping] TIMEOUT! Server antwortet nicht.")
        return 99.9
    except Exception as e:
        print(f"   ❌ [Ping] Fehler: {e}")
        return 99.9

async def main():
    async with httpx.AsyncClient() as client:
        print("="*50)
        print("💰 Starte Payroll Stress-Test (Blocking Check)")
        print("="*50)
        
        # 1. Wir starten die schwere Berechnung als Task (läuft im Hintergrund los)
        task_payroll = asyncio.create_task(trigger_payroll(client, EMPLOYEE_ID))
        
        # 2. Kurze Kunstpause (0.1s), damit der Request sicher beim Server ankommt 
        # und die blockierende Berechnungsschleife startet.
        await asyncio.sleep(0.1)
        
        # 3. Jetzt versuchen wir, den Server anzupingen
        ping_duration = await check_responsiveness(client)
        
        # 4. Auf das Ende der Berechnung warten
        await task_payroll
        
        print("-" * 50)
        # Auswertung
        if ping_duration > 0.5:
            print("❌ ERGEBNIS: FAIL - Server blockiert!")
            print(f"   Der Ping dauerte {ping_duration:.3f}s (erwartet: < 0.1s).")
            print("   Ursache: Synchroner Legacy-Code blockiert den Event Loop.")
        else:
            print("✅ ERGEBNIS: PASS - Server ist responsive.")
            print(f"   Der Ping ging schnell durch ({ping_duration:.3f}s).")
            print("   Lösung: BackgroundTasks oder ThreadPool wurden korrekt genutzt.")
        print("="*50)

if __name__ == "__main__":
    # Prüfen, ob Server läuft
    try:
        httpx.get(BASE_URL)
    except:
        print(f"❌ Fehler: Der Server unter {BASE_URL} ist nicht erreichbar.")
        print("   Bitte starte ihn zuerst mit: uvicorn src.main:app --reload")
        sys.exit(1)
        
    asyncio.run(main())