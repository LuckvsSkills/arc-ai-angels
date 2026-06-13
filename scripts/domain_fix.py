#!/usr/bin/env python3

import os
from pathlib import Path

ROOT = Path.home() / "arc_ai_angels" / "agents"

OMNI_FUNCTIONS = {
    "helix": "tech",
    "matrix": "intelligence",
    "quantix": "growth",
    "zenix": "operations",
    "finix": "assets",
}

LEADS = {
    "helix": "cortexia",
    "matrix": "saelia",
    "quantix": "lumeria",
    "zenix": "fluentia",
    "finix": "finoria",
}

SPECIALISMS = {
    "helix": {
        "axon": "automation",
        "clio": "documentation",
        "forge": "engineering",
        "nero": "security",
        "ventura": "infrastructure",
    },
    "matrix": {
        "arix": "analysis",
        "daxio": "strategy",
        "enki": "knowledge",
        "sora": "research",
        "tharos": "planning",
    },
    "quantix": {
        "elora": "analytics",
        "kresta": "optimization",
        "luvia": "insights",
        "nura": "modeling",
        "vondra": "forecasting",
    },
    "zenix": {
        "draven": "execution",
        "orizon": "coordination",
        "solis": "monitoring",
        "unia": "support",
        "zena": "control",
    },
    "finix": {
        "kairo": "risk",
        "kenzo": "valuation",
        "odis": "flow",
        "vector": "transactions",
        "zion": "portfolio",
    },
}

def fix_file(path):
    text = path.read_text()

    parts = str(path).split("/")

    # Detect omni lead
    if "omni" in parts and "lead agent" in path.parent.name:
        domain = parts[parts.index("omni")+1]
        agent = path.parent.name.replace("lead agent ", "")
        function = OMNI_FUNCTIONS.get(domain, "core")

        new_domain = f"{domain}/{function}/lead/{agent}"

        text = text.replace("Owner Agent: " + domain, f"Owner Agent: {agent}")
        text = text.replace("Assigned To: " + domain, f"Assigned To: {agent}")

    # Detect sentinel
    elif "omni" in parts and "sentinels" in parts:
        domain = parts[parts.index("omni")+1]
        agent = parts[-2]
        function = OMNI_FUNCTIONS.get(domain, "core")
        specialism = SPECIALISMS.get(domain, {}).get(agent, "specialism")

        lead = LEADS.get(domain)

        new_domain = f"{domain}/{function}/{specialism}/{agent}"

        if lead:
            text = text.replace("Origin: " + domain, f"Origin: {lead}")
            text = text.replace("Assigned By: " + domain, f"Assigned By: {lead}")

        text = text.replace("Owner Agent: " + domain, f"Owner Agent: {agent}")
        text = text.replace("Assigned To: " + domain, f"Assigned To: {agent}")

    else:
        return

    # Fix / add Domain
    if "Domain:" in text:
        lines = text.splitlines()
        for i, line in enumerate(lines):
            if line.startswith("- Domain:"):
                lines[i] = f"- Domain: {new_domain}"
        text = "\n".join(lines)
    else:
        text += f"\n- Domain: {new_domain}\n"

    path.write_text(text)
    print(f"✔ fixed: {path}")

def main():
    for file in ROOT.rglob("TASKS.md"):
        fix_file(file)

if __name__ == "__main__":
    main()

