# Agent Autonomy Framework - Complete Design

## Roles
NOVA: Orchestrator (simple tasks, status aggregation)
FLUX: Project Manager (complex projects, routing)
LEAD AGENTS: Domain Managers (domain ops, assist FLUX)
TARGET AGENTS: Executors (tasks, self-manage)

## Cronjob Rights
NOVA: Create for self + all others
FLUX: Create for self + target agents
Lead Agent: Create for self + domain agents
Target Agent: Create for self only

## Status Flow
Target Agent → Lead Agent → NOVA → Fea

## Commands
Fea → NOVA → FLUX → Lead Agent → Agent

## Rules
1. Any agent creates own cronjobs
2. NOVA creates for any agent
3. FLUX creates for targets
4. Lead Agent creates for domain agents
5. Status flows UP
6. Commands flow DOWN

