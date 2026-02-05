import os
import re
import csv

def get_coverage_from_file(folder_path):
    """Liest die Coverage-Prozentzahl aus der coverage_results.txt."""
    cov_file = os.path.join(folder_path, "coverage_results.txt")
    if not os.path.exists(cov_file):
        return "N/A"
    
    try:
        # Versuche UTF-8, dann UTF-16 (für PowerShell Output)
        content = ""
        try:
            with open(cov_file, "r", encoding="utf-8") as f: content = f.read()
        except UnicodeDecodeError:
            with open(cov_file, "r", encoding="utf-16") as f: content = f.read()

        # Suche nach "TOTAL ... 85%"
        match = re.search(r"TOTAL\s+\d+\s+\d+\s+(\d+)%", content)
        if match:
            return int(match.group(1))
    except:
        pass
    return "N/A"

def calculate_assertion_density(folder_path):
    """Zählt live Asserts und Tests im tests/ Ordner."""
    test_dir = os.path.join(folder_path, "tests")
    
    # Falls tests ordner nicht existiert (z.B. baseprojekt), suche im Root
    if not os.path.exists(test_dir):
        test_dir = folder_path

    total_tests = 0
    total_asserts = 0
    found_files = False

    for root, _, files in os.walk(test_dir):
        for file in files:
            # Wir schauen uns nur Python-Test-Dateien an
            if file.startswith("test_") and file.endswith(".py"):
                found_files = True
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        # Einfache Zählung
                        tests_in_file = content.count("def test_")
                        asserts_in_file = content.count("assert ")
                        
                        total_tests += tests_in_file
                        total_asserts += asserts_in_file
                except: pass

    if not found_files or total_tests == 0:
        return "N/A"
    
    return round(total_asserts / total_tests, 2)

def main():
    root_dir = "."
    data_rows = []

    print(f"{'Projekt':<40} | {'Cov %':<6} | {'Asserts/Test'}")
    print("-" * 65)

    # Wir gehen durch alle Ordner
    for root, dirs, files in os.walk(root_dir):
        # Wir erkennen ein Projekt daran, dass es eine coverage_results.txt ODER einen tests Ordner hat
        is_project = "coverage_results.txt" in files or "tests" in dirs
        
        # Ignoriere den .venv Ordner selbst und __pycache__
        if ".venv" in root or "__pycache__" in root:
            continue

        if is_project:
            project_name = os.path.basename(root)
            
            # Manche Ordner sind nur Container, wir wollen nur die echten Projekte
            # Filter: Wenn der Name "Vergleich" enthält, ist es meist der Überordner -> überspringen
            if "Vergleich" in project_name and project_name != "FinalerVergleich":
                continue

            # 1. Coverage holen
            cov = get_coverage_from_file(root)
            
            # 2. Density live berechnen
            dens = calculate_assertion_density(root)

            # Nur hinzufügen, wenn wir Daten haben (um leere Ordner auszublenden)
            if cov != "N/A" or dens != "N/A":
                data_rows.append({
                    "Projekt": project_name,
                    "Coverage": cov,
                    "Density": dens
                })
                print(f"{project_name:<40} | {str(cov):<6} | {str(dens)}")

    # Sortieren
    data_rows.sort(key=lambda x: x["Projekt"])

    # CSV Speichern
    with open("Final_Thesis_Data.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["Projekt", "Coverage", "Density"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data_rows)

    # Markdown Speichern
    with open("Final_Thesis_Data.md", "w", encoding="utf-8") as mdfile:
        mdfile.write("| Projekt | Coverage (%) | Assertions/Test (Ø) |\n")
        mdfile.write("| :--- | :--- | :--- |\n")
        for row in data_rows:
            mdfile.write(f"| {row['Projekt']} | {row['Coverage']} | {row['Density']} |\n")

    print("\n" + "="*65)
    print("Fertig! Daten gespeichert in 'Final_Thesis_Data.csv' und '.md'")

if __name__ == "__main__":
    main()