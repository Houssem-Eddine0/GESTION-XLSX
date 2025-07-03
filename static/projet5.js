const inputChemin = document.getElementById("chemin");
const selectFavoris = document.getElementById("favoris");
const resultatZone = document.getElementById("resultats");

document.getElementById("btn-ajouter").addEventListener("click", () => {
  const chemin = inputChemin.value.trim();
  if (!chemin) return;
  const form = new FormData();
  form.append("action", "ajouter");
  form.append("chemin", chemin);
  fetch("/favoris_projet5", { method: "POST", body: form })
    .then(r => r.json())
    .then(data => {
      refreshFavoris(data.favoris);
      alert("✅ Favori ajouté.");
    });
});

document.getElementById("btn-supprimer").addEventListener("click", () => {
  const chemin = inputChemin.value.trim();
  if (!chemin) return;
  const form = new FormData();
  form.append("action", "supprimer");
  form.append("chemin", chemin);
  fetch("/favoris_projet5", { method: "POST", body: form })
    .then(r => r.json())
    .then(data => {
      refreshFavoris(data.favoris);
      alert("🗑️ Favori retiré.");
    });
});

selectFavoris.addEventListener("change", () => {
  if (selectFavoris.value) inputChemin.value = selectFavoris.value;
});

document.getElementById("formulaire").addEventListener("submit", function (e) {
  e.preventDefault();
  const form = new FormData(this);
  fetch("/projet5", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
      resultatZone.innerHTML = "";

      if (data.erreur) {
        resultatZone.innerHTML = `<p class="erreur">${data.erreur}</p>`;
        return;
      }

      refreshFavoris(data.favoris || []);

      if (data.groupes.length) {
        data.groupes.forEach(g => {
          const id = Math.random().toString(36).slice(2);
          const chemin = g.chemin.replace(/\\/g, "/");
          const serials = g.serials.map(s => s.toUpperCase()).join(", ");
          resultatZone.innerHTML += `
            <div class="result">
              <p>📄 <strong>${g.fichier}</strong> → ${g.feuille}</p>
              <p>✔️ Trouvés : ${serials}</p>
              <p id="c-${id}">📁 ${chemin}</p>
              <button onclick="copierChemin('c-${id}')">📋 Copier le chemin</button>
            </div>`;
        });
      }

      if (data.non_trouves.length) {
        resultatZone.innerHTML += `
          <div class="result">
            <p class="non-trouve">❌ Non trouvés : ${data.non_trouves.join(", ")}</p>
          </div>`;
      }
    });
});

function copierChemin(id) {
  const texte = document.getElementById(id).innerText.replace("📁 ", "");
  navigator.clipboard.writeText(texte).then(() => {
    alert("📎 Chemin copié !");
  });
}

function refreshFavoris(favoris) {
  selectFavoris.innerHTML = '<option value="">— Favoris enregistrés —</option>';
  favoris.forEach(fav => {
    const opt = document.createElement("option");
    opt.value = fav;
    opt.textContent = fav;
    selectFavoris.appendChild(opt);
  });
}
