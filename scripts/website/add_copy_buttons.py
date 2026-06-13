#!/usr/bin/env python3
from pathlib import Path

page = Path.home() / "arc_strategic_control_center" / "prompts.html"
html = page.read_text(encoding="utf-8")

# 1) voeg CSS toe
copy_css = """
.copy-row{
  display:flex;
  justify-content:flex-end;
  margin-top:12px;
}
.copy-btn{
  appearance:none;
  border:1px solid color-mix(in oklab,var(--c) 26%, var(--line));
  background:
    radial-gradient(160px 70px at 0% 0%, color-mix(in oklab,var(--c) 14%, transparent), transparent 70%),
    color-mix(in oklab,var(--panel2) 88%, transparent);
  color:var(--text);
  padding:10px 14px;
  border-radius:12px;
  font-size:14px;
  font-weight:800;
  cursor:pointer;
  transition:transform .14s ease, border-color .14s ease, box-shadow .14s ease;
}
.copy-btn:hover{
  transform:translateY(-1px);
  border-color:color-mix(in oklab,var(--c) 44%, var(--line));
  box-shadow:0 0 0 1px color-mix(in oklab,var(--c) 18%, transparent);
}
.copy-btn.copied{
  border-color:color-mix(in oklab,var(--accent) 46%, var(--line));
  color:var(--accent2);
}
"""
if ".copy-btn" not in html:
    html = html.replace("</style>", copy_css + "\n</style>")

# 2) injecteer copy buttons na elke prompt-body
html = html.replace(
    '</div>\n        </article>',
    '</div>\n          <div class="copy-row"><button class="copy-btn" type="button">Copy Prompt</button></div>\n        </article>'
)

# 3) voeg JS toe
copy_js = """
document.querySelectorAll('.prompt-card').forEach(card => {
  const btn = card.querySelector('.copy-btn');
  const body = card.querySelector('.prompt-body');
  if(!btn || !body) return;

  btn.addEventListener('click', async () => {
    const text = body.innerText.trim();
    try{
      await navigator.clipboard.writeText(text);
      const old = btn.textContent;
      btn.textContent = 'Copied';
      btn.classList.add('copied');
      setTimeout(() => {
        btn.textContent = old;
        btn.classList.remove('copied');
      }, 1400);
    }catch(err){
      btn.textContent = 'Copy failed';
      setTimeout(() => {
        btn.textContent = 'Copy Prompt';
      }, 1400);
    }
  });
});
"""
if "navigator.clipboard.writeText" not in html:
    html = html.replace("</script>", copy_js + "\n</script>")

page.write_text(html, encoding="utf-8")
print(f"Updated {page} with copy buttons")
