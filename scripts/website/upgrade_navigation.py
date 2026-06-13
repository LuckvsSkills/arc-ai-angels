from pathlib import Path

index = Path.home() / "arc_strategic_control_center" / "index.html"
html = index.read_text()

html = html.replace(
"position:sticky;top:0;z-index:60;",
"position:sticky;top:0;z-index:1000;"
)

html = html.replace(
"backdrop-filter:blur(14px);",
"backdrop-filter:blur(16px);"
)

# add floating shadow on scroll
script = """

window.addEventListener("scroll", ()=>{
  const nav = document.querySelector(".topbar");

  if(window.scrollY > 20){
    nav.style.boxShadow = "0 14px 40px rgba(0,0,0,.55)";
  }else{
    nav.style.boxShadow = "0 10px 24px rgba(0,0,0,.22)";
  }
});

"""

if "nav.style.boxShadow" not in html:
    html = html.replace("</script>", script + "\n</script>")

index.write_text(html)

print("Navigation upgraded")
