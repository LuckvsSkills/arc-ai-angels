# Model Runtime & Providers
## Block 08 — Direct Interface & Command Routing

---

### Purpose

Het Direct Interface & Command Routing block verzorgt de directe communicatie tussen Fea (menselijke gebruikers) en het ARC AI Agents systeem. Het vertaalt natuurlijke taal en commando's naar gestructureerde intenties die het systeem kan verwerken.

| Aspect | Functie |
|--------|---------|
| **Input Parsing** | Natuurlijke taal omzetten naar gestructureerde data |
| **Command Recognition** | Herkennen van specifieke commando's en intenties |
| **Context Binding** | Koppelen van input aan bestaande sessie context |
| **Routing Logic** | Bepalen welke component de request afhandelt |


### System Context

Direct Interface zit tussen de gebruiker en Nova (Gateway). Het ontvangt ruwe input en transformeert deze naar geverifieerde intenties.



**Verbonden met:**
- **Nova**: Ontvangt geparseerde intenties voor validatie
- **Session Manager**: Haalt context op voor bestaande sessies
- **Command Registry**: Bevat alle beschikbare commando definities


### Core Structure

#### 1. Input Parser
Verwerkt natuurlijke taal, commando's, en gestructureerde input.

#### 2. Command Router
Bepaalt welke interne service de request afhandelt.

#### 3. Context Manager
Beheert sessie context en gebruikershistorie.

#### 4. Response Formatter
Formatteert output terug naar gebruiker.


### How It Works

1. **Input Reception**: Gebruiker typt commando of vraag
2. **Parsing**: Systeem herkent intentie en entiteiten
3. **Context Lookup**: Ophalen bestaande sessie data
4. **Routing**: Doorsturen naar juiste handler
5. **Execution**: Verwerking door downstream componenten
6. **Response**: Resultaat terug naar gebruiker


### How to Find / Use It

**Locatie**: Directe interface is de entry point voor alle gebruikersinteractie.

**Gebruik**:
- Web interface: 
- CLI: 


### How to Find / Use It

**Locatie**: Directe interface is de entry point voor alle gebruikersinteractie.

**Gebruik**:
- Web interface: 
- CLI: 


### Why It Exists

Zonder Direct Interface zou elke component individueel moeten omgaan met ruwe gebruikersinput. Dit zorgt voor:

- **Consistentie**: Uniforme verwerking van alle input
- **Herbruikbaarheid**: Parser logica op één plek
- **Testbaarheid**: Geïsoleerde input verwerking
- **Veiligheid**: Centrale sanitization en validatie

## Command Routing Flow

+----------------+      +----------------+      +----------------+
|  User Input    |----->|  Direct        |----->|  Command       |
|  (CLI/GUI)     |      |  Interface     |      |  Parser        |
+----------------+      +----------------+      +----------------+
                               |
                               v
                        +----------------+
                        |  Intent        |
                        |  Router        |
                        +----------------+
                               |
                    +----------+----------+
                    |                     |
                    v                     v
             +------------+        +------------+
             |  Nova      |        |  Internal  |
             |  Gateway   |        |  Command   |
             +------------+        +------------+
