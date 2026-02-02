import time
import math
from decimal import Decimal

# Globale "Konstanten"
TAX_BRACKETS = {
    "I": Decimal("0.14"), "II": Decimal("0.12"), "III": Decimal("0.0"),
    "IV": Decimal("0.14"), "V": Decimal("0.25"), "VI": Decimal("0.42")
}
SOLI_ZUSCHLAG = Decimal("0.055")
KIRCHENSTEUER_NRW = Decimal("0.09")
KIRCHENSTEUER_BAYERN = Decimal("0.08")
BBG_KRANKENVERSICHERUNG = Decimal("4837.50")

def legacy_calculate_net_salary(
    gross_amount: Decimal, 
    tax_class: str, 
    has_children: bool, 
    is_church_member: bool,
    state: str,
    year_of_birth: int = 1980
) -> dict:
    """
    CORE CALCULATION ENGINE (v20.0.1 Enterprise Edition)
    Komplexität: EXTREM (Rank C).
    Enthält Blockierende I/O und CPU-Last.
    """
    print(f"📠 [Legacy] Starte Berechnung für {gross_amount}€ (Klasse {tax_class})...")
    
    # 1. BLOCKER: Datenbank-Simulation (I/O)
    time.sleep(0.4) 
    
    # 2. BLOCKER: CPU-Last Simulation (Sinnlose Mathematik)
    start_cpu = time.time()
    while time.time() - start_cpu < 0.3:
        _ = [math.sqrt(i) * math.sin(i) for i in range(150)]

    # 3. Validierungs-Hölle (Treibt CC hoch)
    if gross_amount < 0:
        raise ValueError("Negative Salary")
    if tax_class not in TAX_BRACKETS:
        raise ValueError("Invalid Tax Class")
    if state not in ["NRW", "BY", "BE", "SN"]:
        # Fallback Logik für unbekannte Bundesländer
        if gross_amount > 10000:
            print("Warning: High salary in unknown state")
        state = "NRW" # Default

    # 4. Steuer-Logik (Verschachtelt)
    base_tax_rate = TAX_BRACKETS[tax_class]
    
    # Kinderfreibetrag
    if has_children:
        if tax_class == "I":
            base_tax_rate -= Decimal("0.01")
        elif tax_class == "III":
            base_tax_rate -= Decimal("0.03") # Mehr Entlastung bei III
        else:
            base_tax_rate -= Decimal("0.02")
    
    # Reichensteuer-Check
    if gross_amount > Decimal("23000.00"): # Monatlich sehr hoch
        base_tax_rate += Decimal("0.03")
        if not has_children:
             base_tax_rate += Decimal("0.01")

    # Safety Cap
    if base_tax_rate < 0: 
        base_tax_rate = 0
    if base_tax_rate > Decimal("0.50"):
        base_tax_rate = Decimal("0.50")

    income_tax = gross_amount * base_tax_rate
    soli = income_tax * SOLI_ZUSCHLAG
    
    # Kirchensteuer (Sonderlocken)
    church_tax = Decimal("0.00")
    if is_church_member:
        if state == "BY":
            church_tax = income_tax * KIRCHENSTEUER_BAYERN
        elif state == "SN": # Sachsen Sonderregeln (historisch)
            if gross_amount > 2000:
                church_tax = income_tax * Decimal("0.09")
            else:
                church_tax = income_tax * Decimal("0.085")
        else:
            church_tax = income_tax * KIRCHENSTEUER_NRW
            
    # Sozialabgaben (Der CC-Booster)
    kv_beitrag = Decimal("0.00")
    # Beitragsbemessungsgrenze prüfen
    relevant_salary = gross_amount
    if relevant_salary > BBG_KRANKENVERSICHERUNG:
        relevant_salary = BBG_KRANKENVERSICHERUNG
        
    if year_of_birth < 1960:
        # Altfall-Regelung
        kv_beitrag = relevant_salary * Decimal("0.07")
    else:
        # Normalfall
        kv_beitrag = relevant_salary * Decimal("0.073")
        if not has_children and year_of_birth > 1980:
             # PV-Zuschlag für Kinderlose
             kv_beitrag += relevant_salary * Decimal("0.006")

    # Netto
    net_salary = gross_amount - income_tax - soli - church_tax - kv_beitrag
    
    # Plausibilitäts-Check am Ende
    if net_salary < 0:
        net_salary = 0
        print("CRITICAL: Net salary negative. Adjustment applied.")

    return {
        "gross": round(gross_amount, 2),
        "tax_class": tax_class,
        "details": {
            "income_tax": round(income_tax, 2),
            "soli": round(soli, 2),
            "church_tax": round(church_tax, 2),
            "social_security": round(kv_beitrag, 2)
        },
        "net": round(net_salary, 2),
        "timestamp": time.time()
    }