from fastapi import APIRouter, HTTPException
import os, re
from app.config import CODEX_DIR
router = APIRouter()

CHAPTERS = [
    (1,  "CH01_HET_ONTSTAAN"),
    (2,  "CH02_DE_ARCHITECTUUR"),
    (3,  "CH03_HOE_HET_WERKT"),
    (4,  "CH04_DE_DOMEINEN"),
    (5,  "CH05_AUTONOMIE"),
    (6,  "CH06_GEHEUGEN_EN_GROEI"),
    (7,  "CH07_GOVERNANCE"),
    (8,  "CH08_MODELLEN"),
    (9,  "CH09_SKILLS"),
    (10, "CH10_TOOLS"),
    (11, "CH11_MISSION_CONTROL"),
    (12, "CH12_DE_TOEKOMST"),
]

def read_chapter(filename):
    path = f"{CODEX_DIR}/{filename}.md"
    if os.path.exists(path):
        return open(path, errors="ignore").read()
    return ""

@router.get("/canon/toc")
async def get_toc():
    toc = []
    for num, filename in CHAPTERS:
        content = read_chapter(filename)
        title_match = re.search(r'^# (.+)', content, re.MULTILINE)
        title = title_match.group(1) if title_match else filename
        toc.append({
            "id": num,
            "filename": filename,
            "title": title,
            "has_content": len(content) > 0,
            "length": len(content)
        })
    return {"toc": toc, "total": len(toc)}

@router.get("/canon/full")
async def get_full():
    chapters = []
    for num, filename in CHAPTERS:
        content = read_chapter(filename)
        if content:
            chapters.append({"id": num, "filename": filename, "content": content})
    return {"chapters": chapters, "total": len(chapters)}

@router.get("/canon/chapter/{chapter_id}")
async def get_chapter(chapter_id: int):
    chapter = next(((n, f) for n, f in CHAPTERS if n == chapter_id), None)
    if not chapter:
        raise HTTPException(404, "Hoofdstuk niet gevonden")
    content = read_chapter(chapter[1])
    if not content:
        raise HTTPException(404, "Hoofdstuk heeft geen inhoud")
    return {"id": chapter[0], "filename": chapter[1], "content": content}
