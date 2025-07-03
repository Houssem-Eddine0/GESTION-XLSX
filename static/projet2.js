const inputChemin = document.getElementById("chemin");
const selectFavoris = document.getElementById("favoris");
const resultatZone = document.getElementById("resultats");

document.getElementById("btn-ajouter").addEventListener("click", () => {
  const chemin = inputChemin.value.trim();
  if (!chemin) return;
  const form = new FormData();
  form.append("action", "ajouter");
  form.append("chemin", chemin);

  fetch("/favoris_projet2", { method: "POST", body: form })
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

  fetch("/favoris_projet2", { method: "POST", body: form })
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

  fetch("/projet2", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
      resultatZone.innerHTML = "";
      if (data.erreur) {
        resultatZone.innerHTML = `<p class="erreur">${data.erreur}</p>`;
      } else {
        data.forEach(item => {
          const ligne = ["PAD", "SERIAL", "ASSET"]
             .map(k => `<td>${item.ligne[k] || ""}</td>`)
             .join("");


          const chemin = item.chemin_complet.replace(/\\/g, "/");
          const id = Math.random().toString(36).slice(2);

          resultatZone.innerHTML += `
            <div class="result">
              <p>📄 <strong>${item.fichier}</strong> → ${item.feuille} (ligne ${item.ligne_excel})</p>
              <p class="chemin" id="c-${id}">📁 ${chemin}</p>
              <button onclick="copierChemin('c-${id}')">📋 Copier le chemin</button>
              <table class="ligne"><tr>${ligne}</tr></table>
            </div>`;
        });
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
