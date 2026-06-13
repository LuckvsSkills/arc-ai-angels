# Model Runtime & Providers
## Block 09 — Team & Subagent Architecture

---

### Purpose

Het Team & Subagent Architecture block definieert hoe agents zijn georganiseerd in hierarchische teams. Het bepaalt de relaties tussen parent agents en subagents, en hoe verantwoordelijkheden worden verdeeld.

| Aspect | Functie |
|--------|---------|
| **Hierarchy** | Parent-child relaties tussen agents |
| **Delegation** | Taakverdeling van parent naar subagents |
| **Coordination** | Samenwerking tussen teamleden |
| **Reporting** | Resultaten terugstromen naar parent |


### System Context

Team architectuur zit tussen Flux (orchestrator) en Sentinel (specialist teams). Het definieert hoe agents zijn gegroepeerd.

Flux -> Team Manager -> Subagents -> Workers

Verbonden met:
- Flux: Ontvangt orchestration commands
- Sentinel: Specialist teams binnen hierarchie
- Workers: Uitvoerende agents aan de onderkant


### Core Structure

#### 1. Team Manager
Coordinatiepunt voor een team van agents.

#### 2. Parent Agent
Delegeert taken naar subagents.

#### 3. Subagent
Voert specifieke subtaken uit.

#### 4. Communication Bus
Berichtenverkeer tussen teamleden.


### How It Works

1. Flux delegeert taak aan Team Manager
2. Manager verdeelt werk over subagents
3. Subagents executeren parallel
4. Resultaten aggregeren naar Manager
5. Manager rapporteert terug naar Flux

### How to Find / Use It

Team structuur wordt gedefinieerd in agent configuratie bestanden.

### Why It Exists

Hierarchische organisatie maakt complexe taken beheersbaar door verdeling van verantwoordelijkheid.


### How It Works

1. Flux delegeert taak aan Team Manager
2. Manager verdeelt werk over subagents
3. Subagents executeren parallel
4. Resultaten aggregeren naar Manager
5. Manager rapporteert terug naar Flux

### How to Find / Use It

Team structuur wordt gedefinieerd in agent configuratie bestanden.

### Why It Exists

Hierarchische organisatie maakt complexe taken beheersbaar door verdeling van verantwoordelijkheid.

## Team Hierarchy Flow

+----------------+
|  Flux Master   |
+----------------+
        |
        v
+----------------+
|  Team Manager  |
+----------------+
        |
   +----+----+
   |         |
   v         v
+------+  +------+
|Sub A |  |Sub B |
+------+  +------+
   |         |
   v         v
+------+  +------+
|Work  |  |Work  |
+------+  +------+
