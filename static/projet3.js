const inputChemin = document.getElementById("chemin");
const selectFavoris = document.getElementById("favoris");
const selectFichier = document.getElementById("fichier");
const selectFeuille = document.getElementById("feuille");
const resultatZone = document.getElementById("resultat");

// ⭐ Favoris
document.getElementById("btn-ajouter").addEventListener("click", () => {
  const chemin = inputChemin.value.trim();
  if (!chemin) return;
  const form = new FormData();
  form.append("action", "ajouter");
  form.append("chemin", chemin);
  fetch("/favoris_projet3", { method: "POST", body: form })
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
  fetch("/favoris_projet3", { method: "POST", body: form })
    .then(r => r.json())
    .then(data => {
      refreshFavoris(data.favoris);
      alert("🗑️ Favori retiré.");
    });
});

selectFavoris.addEventListener("change", () => {
  if (selectFavoris.value) inputChemin.value = selectFavoris.value;
});

// 📂 Lister fichiers
document.getElementById("btnLister").addEventListener("click", () => {
  const chemin = inputChemin.value.trim();
  const form = new FormData();
  form.append("chemin", chemin);
  fetch("/fichiers_projet3", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        selectFichier.innerHTML = '<option value="">Sélectionnez un fichier</option>';
        data.fichiers.forEach(f => {
          const opt = document.createElement("option");
          opt.value = f;
          opt.textContent = f;
          selectFichier.appendChild(opt);
        });
        selectFichier.hidden = false;
        resultatZone.innerText = "✅ Fichiers listés.";
        resultatZone.style.color = "green";
      } else {
        resultatZone.innerText = data.message;
        resultatZone.style.color = "crimson";
      }
    });
});

// 🧾 Charger feuilles quand un fichier est sélectionné
selectFichier.addEventListener("change", () => {
  const fichier = selectFichier.value;
  const chemin = inputChemin.value.trim();
  if (!fichier) return;
  const form = new FormData();
  form.append("chemin", chemin);
  form.append("fichier", fichier);
  fetch("/feuilles_projet3", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        selectFeuille.innerHTML = '<option value="">Sélectionnez une feuille</option>';
        data.feuilles.forEach(f => {
          const opt = document.createElement("option");
          opt.value = f;
          opt.textContent = f;
          selectFeuille.appendChild(opt);
        });
        selectFeuille.hidden = false;
        resultatZone.innerText = "✅ Feuilles chargées.";
        resultatZone.style.color = "green";
      } else {
        resultatZone.innerText = data.message;
        resultatZone.style.color = "crimson";
      }
    });
});

// 🎛️ Action ciblée
document.getElementById("operation").addEventListener("change", function () {
  const bloc = document.getElementById("bloc-modifier");
  bloc.style.display = this.value === "modifier" ? "block" : "none";
});

document.getElementById("formulaire").addEventListener("submit", function (e) {
  e.preventDefault();
  const form = new FormData(this);
  fetch("/appliquer_projet3", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
      resultatZone.innerText = data.message;
      const msg = data.message.toLowerCase();
      if (msg.includes("✅")) resultatZone.style.color = "green";
      else if (msg.includes("✏️")) resultatZone.style.color = "#0078d7";
      else if (msg.includes("🗑️")) resultatZone.style.color = "#b44415";
      else resultatZone.style.color = "crimson";
    });
});

// ♻️ MAJ favoris
function refreshFavoris(favoris) {
  selectFavoris.innerHTML = '<option value="">— Favoris enregistrés —</option>';
  favoris.forEach(fav => {
    const opt = document.createElement("option");
    opt.value = fav;
    opt.textContent = fav;
    selectFavoris.appendChild(opt);
  });
}
