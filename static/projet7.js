document.getElementById("prefixForm").addEventListener("submit", function(e) {
  e.preventDefault();
  const lignes = document.getElementById("zoneSerials").value.split("\n");
  const mode = document.querySelector("input[name='mode']:checked").value;

  const traitées = lignes.map(l => {
    const s = l.trim();
    if (!s) return "";
    if (mode === "ajouter" && !s.startsWith("S")) return "S" + s;
    if (mode === "retirer" && s.startsWith("S")) return s.slice(1);
    return s;
  });

  document.getElementById("resultats").value = traitées.join("\n");
});
