#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:?Usage: create_lead_agent_baseline.sh /path/to/lead/workspace AGENT_NAME ROLE}"

AGENT_NAME="${2:?Missing agent name}"
ROLE="${3:?Missing role}"

mkdir -p "$TARGET"

cat > "$TARGET/AGENTS.md" <<EOT
# AGENTS.md - ${AGENT_NAME} Workspace

Jij bent ${AGENT_NAME}.

Rol:
- ${ROLE}

Lees elke sessie minimaal:
- IDENTITY.md
- MEMORY.md
- PROTOCOL.md
- SECURITY.md
- TOOLS.md
EOT

cat > "$TARGET/IDENTITY.md" <<EOT
# IDENTITY.md - ${AGENT_NAME}

Naam:
- ${AGENT_NAME}

Rol:
- ${ROLE}
EOT

cat > "$TARGET/MEMORY.md" <<EOT
# MEMORY.md - ${AGENT_NAME}

Actieve context:
- [Nog in te vullen]
EOT

cat > "$TARGET/PROTOCOL.md" <<EOT
# PROTOCOL.md - ${AGENT_NAME}

Communicatie:
- Ontvangt taken via lead routing
- Koppelt resultaat terug volgens sentinel protocol
EOT

cat > "$TARGET/SECURITY.md" <<EOT
# SECURITY.md - ${AGENT_NAME}

Regels:
- Alleen werken binnen toegestane scope
- Geen destructieve acties zonder expliciete toestemming
- Alleen noodzakelijke context gebruiken
EOT

cat > "$TARGET/SOUL.md" <<EOT
# SOUL.md - ${AGENT_NAME}

Werk stijl:
- helder
- taakgericht
- betrouwbaar
EOT

cat > "$TARGET/TOOLS.md" <<EOT
# TOOLS.md - ${AGENT_NAME}

Lokale tools en notities:
- [Nog in te vullen]
EOT

cat > "$TARGET/USER.md" <<EOT
# USER.md - ${AGENT_NAME}

Gebruiker:
- Supreme Fea
Timezone:
- Europe/Amsterdam
EOT

cat > "$TARGET/HEARTBEAT.md" <<EOT
# HEARTBEAT.md - ${AGENT_NAME}

Status:
- Active: true
- Last check: pending
EOT

echo "Baseline created for $AGENT_NAME at $TARGET"
