# FLUX Skill Assignment Rules
## How Flux Allocates Skills Weekly

### Schedule
Every Monday 08:00 AM (cronjob)

### FLUX's Decision Logic

For each agent:
1. Check performance (last 4 weeks)
2. Identify skill gaps
3. Check readiness (prerequisites)
4. Consult memory (patterns)
5. Make assignment:
   - Performance >90% → 3 skills
   - Performance >70% → 2 skills
   - Performance <70% → 1 skill

### Rule 1: BASELINE SKILLS
All agents: Communication, Basic reasoning, Error handling, Self-improvement
All Leads: Team coordination, Quality validation, Conflict resolution
Core: Strategic thinking, Architecture, Decision-making

### Rule 2: DOMAIN-SPECIFIC SKILLS

**Tech/Helix:**
- nero: Security skills only
- forge: Engineering skills
- axon: Automation skills
- ventura: Infrastructure skills
- clio: Documentation skills

**Data/Matrix:**
- Pandas, NumPy, SQL, ETL, visualization

**Finance/Finix:**
- Financial modeling, trading, risk metrics

**Language/Zenix:**
- NLP, text generation, summarization

### Rule 3: PERFORMANCE-BASED
- High (>90%): 3 new skills + advanced
- Medium (70-90%): 2 skills + domain-focused
- Learners (<70%): 1 skill + foundational

### Rule 4: STRATEGIC ALLOCATION
- Team gaps: assign to multiple agents
- Cross-domain: 1 secondary skill max
- Growth path: prepare Sentinels for Lead role

### Rule 5: TIMING & PACING
- Max 3 skills/week per agent
- Min 3 days between skills
- Master 70%+ before next skill

### USE CASES

**Use Case 1: Weekly Routine**
- nero (Security): 95% performance → 3 security skills
- Process: Tue assign, Wed-Thu learn, Fri validate

**Use Case 2: Team Gap Filling**
- Tech team weak in testing → pytest to Forge + Axon

**Use Case 3: Career Progression**
- forge (98% performance) → Lead role + management skills

**Use Case 4: Cross-Domain Growth**
- forge (Engineer) learns Pandas (data)

**Use Case 5: Blocker Resolution**
- axon stuck on CI/CD → assign GitHub Actions skill

**Use Case 6: Project Preparation**
- Pre-assign Docker/Kubernetes before deployment project

