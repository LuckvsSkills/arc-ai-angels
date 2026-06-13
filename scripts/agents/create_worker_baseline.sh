#!/usr/bin/env bash
set -euo pipefail

TARGET="${1:?Usage: create_worker_baseline.sh /path/to/worker NAME ROLE PARENT_SENTINEL PARENT_LEAD}"
NAME="${2:?Missing worker name}"
ROLE="${3:?Missing worker role}"
PARENT_SENTINEL="${4:?Missing parent sentinel}"
PARENT_LEAD="${5:?Missing parent lead}"

mkdir -p "$TARGET"

cat > "$TARGET/AGENTS.md" <<EOT
# AGENTS.md - ${NAME}

Jij bent ${NAME}.

Rol:
- ${ROLE}

Parent sentinel:
- ${PARENT_SENTINEL}

Lead AI agent:
- ${PARENT_LEAD}

Werkwijze:
- voer alleen afgebakende subtaken uit
- rapporteer terug aan ${PARENT_LEAD}
- neem geen domeinbrede beslissingen zelfstandig
EOT

cat > "$TARGET/IDENTITY.md" <<EOT
# IDENTITY.md - ${NAME}

Naam:
- ${NAME}

Rol:
- ${ROLE}

Parent sentinel:
- ${PARENT_SENTINEL}

Lead AI agent:
- ${PARENT_LEAD}
EOT

cat > "$TARGET/PROTOCOL.md" <<EOT
# PROTOCOL.md - ${NAME}

Communicatie:
- ontvangt taken van ${PARENT_LEAD}
- koppelt resultaat terug aan ${PARENT_LEAD}
- communiceert niet rechtstreeks met operator
- communiceert niet rechtstreeks met Flux tenzij expliciet toegestaan
EOT

cat > "$TARGET/SECURITY.md" <<EOT
# SECURITY.md - ${NAME}

Beperkingen:
- werk alleen binnen toegewezen subtaak
- gebruik alleen noodzakelijke context
- geen destructieve acties zonder expliciete toestemming
- geen directe externe communicatie zonder policy
EOT

cat > "$TARGET/TOOLS.md" <<EOT
# TOOLS.md - ${NAME}

Toegestane tools en notities:
- [Nog in te vullen]
EOT

echo "Worker baseline created for $NAME at $TARGET"
