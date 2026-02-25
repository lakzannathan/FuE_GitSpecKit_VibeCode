# FuE_GitSpecKit_VibeCode

Dieses Repository enthält das Replikationsmaterial zur Arbeit **„Vibe Coding vs. Spec-Driven Development: Ein empirischer Vergleich von Ad-hoc-Prompting und strukturierten Agenten-Workflows in Brownfield-Systemen“**.

## Inhalt

Das Repository umfasst die experimentellen Artefakte und Auswertungsergebnisse der Fallstudie, darunter:

- synthetische Brownfield-Szenarien
- generierte Implementierungen für beide Prompting-Paradigmen
- erzeugte Testartefakte
- Auswertungsskripte zur Analyse struktureller Codequalität
- Ergebnisdaten der untersuchten Szenarien

## Ziel

Ziel dieses Repositories ist es, die in der Arbeit beschriebenen Experimente nachvollziehbar zu dokumentieren und die zugrunde liegenden Artefakte für Replikation, Prüfung und Weiterverwendung bereitzustellen.

Untersucht werden zwei unterschiedliche Ansätze der LLM-gestützten Softwareentwicklung:

- **Ad-hoc-Prompting (Vibe Coding)**
- **spezifikationsgetriebener Workflow mit GitHub Spec-Kit**

## Szenarien

Die Untersuchung basiert auf drei synthetischen Brownfield-Szenarien mit steigender struktureller Komplexität:

1. **Rate-Limiter** (geringe Komplexität)
2. **Inventory** (mittlere Komplexität)
3. **Legacy HR** (hohe Komplexität)

## Evaluation

Die Bewertung der generierten Artefakte erfolgt anhand von:

- **Maintainability Index (MI)**
- **Cyclomatic Complexity (CC)**
- qualitativer Analyse des Fehlerverhaltens
- Analyse der Teststruktur und Orakelstärke

Ein besonderer Fokus liegt auf den beobachteten Mustern:

- **Fail-Silent**
- **Fail-Loud**

## Reproduzierbarkeit

Das Repository dient als Replikationspaket zur begleitenden wissenschaftlichen Arbeit. Es stellt die wesentlichen Daten und Artefakte bereit, um die beschriebenen Ergebnisse nachvollziehen zu können.

## Hinweis

Die verwendeten Szenarien sind synthetisch konstruiert und dienen der kontrollierten Untersuchung struktureller Unterschiede zwischen den betrachteten Prompting-Paradigmen. Die Ergebnisse sind daher als explorative Befunde zu verstehen.

## Autor

**Lakzan Nathan**  
FH Münster – Fachbereich Wirtschaft

## Zugehörige Arbeit

Falls dieses Repository im wissenschaftlichen Kontext verwendet wird, bitte auf die zugehörige Arbeit verweisen:

> Lakzan Nathan: *Vibe Coding vs. Spec-Driven Development: Ein empirischer Vergleich von Ad-hoc-Prompting und strukturierten Agenten-Workflows in Brownfield-Systemen*.
