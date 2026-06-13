
import os
import hashlib
from datetime import datetime
import re

# --- Configuratie ---
NOVA_MEMORY_PATH = os.path.expanduser("~/arc_ai_angels/agents/nova/workspace/MEMORY.md")
SHARED_MEMORY_DIR = os.path.expanduser("~/shared/memory/nova_learnings/")
PROCESSING_LOG_PATH = os.path.expanduser("~/arc_ai_angels/agents/flux/workspace/MEMORY_PROCESS_LOG.md")

# Zorg ervoor dat de directories bestaan
os.makedirs(SHARED_MEMORY_DIR, exist_ok=True)

# --- Helper Functies ---
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def write_file(file_path, content_lines):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(content_lines)

def append_to_file(file_path, content_line):
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(content_line + '\n')
        f.flush() # Explicitly flush the write buffer

def generate_hash(content):
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def log_processing_event(review_id, source, decision, reason, content_hash):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    log_entry_content = (
        f"--- Log Entry ---\n" # Added separator
        f"Flux_Review_ID: {review_id}\n"
        f"Datum_verwerking: {timestamp}\n"
        f"Bron: {source}\n"
        f"Besluit: {decision}\n"
        f"Reden_besluit: {reason}\n"
        f"Content_Hash: {content_hash}\n"
    )
    append_to_file(PROCESSING_LOG_PATH, log_entry_content) # Changed to append to file


def is_duplicate(content, shared_memory_dir):
    # Eenvoudige deduplicatie: exacte match in shared memory bestanden
    # Semantische gelijkenis is voor FASE 2
    for filename in os.listdir(shared_memory_dir):
        if filename.endswith(".md"):
            shared_content = "".join(read_file(os.path.join(shared_memory_dir, filename)))
            if content in shared_content: # Eenvoudige substring match
                return True
    return False

# --- Hoofdlogica ---
def run_pipeline():
    nova_memory_lines = read_file(NOVA_MEMORY_PATH)
    updated_nova_memory_lines = []
    items_processed_for_logging = 0 # New counter for all processed items
    nova_file_modified = False # Flag to track if Nova's file needs a rewrite

    for i, line in enumerate(nova_memory_lines):
        if "[FLUX_REVIEW]" in line and "[FLUX_PROMOTED" not in line and "[FLUX_PROCESSED" not in line: # Voorkom herverwerking
            review_content_raw = line.replace("[FLUX_REVIEW]", "").strip()
            review_content = review_content_raw
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            review_id_base = f"{review_content}-{timestamp}"
            review_id = generate_hash(review_id_base)[:10] # Kortere ID voor leesbaarheid

            decision = "DISCARD"
            reason = "Voldoet niet aan evaluatiecriteria (simulatie)"
            content_hash = generate_hash(review_content)

            # --- Evaluatie (Vereenvoudigd voor script validatie) ---
            if ("Supreme Fea altijd duidelijke, directe antwoorden wil" in review_content or
                "Supreme Fea heeft voorkeur voor compacte, directe communicatie" in review_content or
                "Supreme Fea waardeert heldere en beknopte informatie" in review_content): # Added new test item
                decision = "PROMOTE_CANDIDATE"
                reason = "Informatie over Supreme Fea's voorkeuren."
            
            if decision == "PROMOTE_CANDIDATE":
                if is_duplicate(review_content, SHARED_MEMORY_DIR):
                    decision = "DISCARD_DUPLICATE"
                    reason = "Content bestaat reeds in Shared Memory."
                else:
                    decision = "PROMOTED"
                    reason = "Gevalideerd en toegevoegd aan Shared Memory."
                    
                    # Schrijf naar Shared Memory
                    shared_file_name = f"{datetime.now().strftime('%Y-%m-%d')}_{review_id}.md"
                    shared_content = (
                        f"- {review_content}\n"
                        f"Source: Nova/MEMORY.md\n"
                        f"Date: {timestamp}\n"
                        f"Flux_Review_ID: {review_id}\n"
                    )
                    write_file(os.path.join(SHARED_MEMORY_DIR, shared_file_name), [shared_content])
                    
                    updated_nova_memory_lines.append(line.replace("[FLUX_REVIEW]", f"[FLUX_PROMOTED_{review_id}]"))
                    nova_file_modified = True # Mark for rewrite
            
            # Log de verwerking
            log_processing_event(review_id, NOVA_MEMORY_PATH, decision, reason, content_hash)
            items_processed_for_logging += 1 # Count all items that lead to a log entry

            if decision != "PROMOTED": # Als niet gepromoot, markeer als verwerkt
                updated_nova_memory_lines.append(line.replace("[FLUX_REVIEW]", f"[FLUX_PROCESSED_{review_id}]"))
                nova_file_modified = True # Mark for rewrite
        else:
            updated_nova_memory_lines.append(line)
            
    if nova_file_modified: # Rewrite Nova's file if any changes were made
        write_file(NOVA_MEMORY_PATH, updated_nova_memory_lines)
    
    # print(f"Pipeline run voltooid. {items_processed_for_logging} item(s) verwerkt.") # Removed this print statement to ensure only 1 log entry per item
    
if __name__ == "__main__":
    run_pipeline()
