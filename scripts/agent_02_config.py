from pathlib import Path

BASE = Path("/home/prime/arc_ai_angels")

AGENTS = {

    # =========================
    # CORE SYSTEM
    # =========================

    "nova": {
        "name": "nova",
        "path": BASE / "agents/nova",
        "template_type": "custom_gateway",
        "layer": "gateway",
        "domain": "intake/gateway",
        "parent": "none",
        "role": "First-Line Operator",
        "mission": "Ontvangt en normaliseert externe input.",
    },

    "flux": {
        "name": "flux",
        "path": BASE / "agents/flux",
        "template_type": "custom_orchestrator",
        "layer": "orchestration",
        "domain": "system/orchestration",
        "parent": "nova",
        "role": "Orchestrator",
        "mission": "Stuurt routing en agent-activatie.",
    },

    # =========================
    # HELIX
    # =========================

    "cortexia": {
        "name": "cortexia",
        "path": BASE / "agents/omni/helix/lead agent cortexia",
        "template_type": "custom_omni",
        "layer": "omni",
        "domain": "helix/tech",
        "parent": "flux",
        "role": "Omni Lead",
        "mission": "Stuurt Helix Sentinels aan.",
    },

    "nero": {
        "name": "nero",
        "path": BASE / "agents/omni/helix/sentinels/nero",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "helix/tech/security/nero",
        "parent": "cortexia",
        "role": "Security Sentinel",
        "mission": "Beheert security binnen Helix.",
    },

    "forge": {
        "name": "forge",
        "path": BASE / "agents/omni/helix/sentinels/forge",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "helix/tech/engineering/forge",
        "parent": "cortexia",
        "role": "Engineering Sentinel",
        "mission": "Bouwt technische implementaties.",
    },

    "axon": {
        "name": "axon",
        "path": BASE / "agents/omni/helix/sentinels/axon",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "helix/tech/automation/axon",
        "parent": "cortexia",
        "role": "Automation Sentinel",
        "mission": "Automatiseert processen.",
    },

    "ventura": {
        "name": "ventura",
        "path": BASE / "agents/omni/helix/sentinels/ventura",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "helix/tech/infrastructure/ventura",
        "parent": "cortexia",
        "role": "Infrastructure Sentinel",
        "mission": "Beheert infrastructuur.",
    },

    "clio": {
        "name": "clio",
        "path": BASE / "agents/omni/helix/sentinels/clio",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "helix/tech/documentation/clio",
        "parent": "cortexia",
        "role": "Documentation Sentinel",
        "mission": "Beheert documentatie.",
    },

    # =========================
    # FINIX
    # =========================

    "finoria": {
        "name": "finoria",
        "path": BASE / "agents/omni/finix/lead agent finoria",
        "template_type": "custom_omni",
        "layer": "omni",
        "domain": "finix",
        "parent": "flux",
        "role": "Omni Lead",
        "mission": "Stuurt Finix Sentinels aan.",
    },

    "kairo": {
        "name": "kairo",
        "path": BASE / "agents/omni/finix/sentinels/kairo",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "finix/kairo",
        "parent": "finoria",
        "role": "Sentinel",
        "mission": "Voert Finix taken uit.",
    },

    "kenzo": {
        "name": "kenzo",
        "path": BASE / "agents/omni/finix/sentinels/kenzo",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "finix/kenzo",
        "parent": "finoria",
        "role": "Sentinel",
        "mission": "Voert Finix taken uit.",
    },
    "odis": {
        "name": "odis",
        "path": BASE / "agents/omni/finix/sentinels/odis",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "finix/odis",
        "parent": "finoria",
        "role": "Sentinel",
        "mission": "Voert Finix taken uit.",
    },

    "vector": {
        "name": "vector",
        "path": BASE / "agents/omni/finix/sentinels/vector",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "finix/vector",
        "parent": "finoria",
        "role": "Sentinel",
        "mission": "Voert Finix taken uit.",
    },

    "zion": {
        "name": "zion",
        "path": BASE / "agents/omni/finix/sentinels/zion",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "finix/zion",
        "parent": "finoria",
        "role": "Sentinel",
        "mission": "Voert Finix taken uit.",
    },

    # =========================
    # MATRIX
    # =========================

    "saelia": {
        "name": "saelia",
        "path": BASE / "agents/omni/matrix/lead agent saelia",
        "template_type": "custom_omni",
        "layer": "omni",
        "domain": "matrix",
        "parent": "flux",
        "role": "Omni Lead",
        "mission": "Stuurt Matrix Sentinels aan.",
    },

    "arix": {
        "name": "arix",
        "path": BASE / "agents/omni/matrix/sentinels/arix",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "matrix/arix",
        "parent": "saelia",
        "role": "Sentinel",
        "mission": "Voert Matrix taken uit.",
    },

    "daxio": {
        "name": "daxio",
        "path": BASE / "agents/omni/matrix/sentinels/daxio",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "matrix/daxio",
        "parent": "saelia",
        "role": "Sentinel",
        "mission": "Voert Matrix taken uit.",
    },

    "enki": {
        "name": "enki",
        "path": BASE / "agents/omni/matrix/sentinels/enki",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "matrix/enki",
        "parent": "saelia",
        "role": "Sentinel",
        "mission": "Voert Matrix taken uit.",
    },

    "sora": {
        "name": "sora",
        "path": BASE / "agents/omni/matrix/sentinels/sora",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "matrix/sora",
        "parent": "saelia",
        "role": "Sentinel",
        "mission": "Voert Matrix taken uit.",
    },

    "tharos": {
        "name": "tharos",
        "path": BASE / "agents/omni/matrix/sentinels/tharos",
        "template_type": "custom_sentinel",
        "layer": "sentinel",
        "domain": "matrix/tharos",
        "parent": "saelia",
        "role": "Sentinel",
        "mission": "Voert Matrix taken uit.",
    },

}

# =========================
# PROTECTION (BELANGRIJK)
# =========================

PROTECTED_TEMPLATE_TYPES = {
    "nova": "custom_gateway",
    "flux": "custom_orchestrator",
    "cortexia": "custom_omni",
    "nero": "custom_sentinel",
    "forge": "custom_sentinel",
    "axon": "custom_sentinel",
    "ventura": "custom_sentinel",
    "clio": "custom_sentinel",
}

