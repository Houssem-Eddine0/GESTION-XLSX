const cheminInput = document.getElementById("chemin");
const favoris = document.getElementById("favoris");
const feuilleSelect = document.getElementById("feuille");
const resultat = document.getElementById("resultat");

// 🔁 Rafraîchir la liste des favoris
function majFavoris(favorisData) {
  favoris.innerHTML = `<option value="">⭐ Favoris enregistrés</option>`;
  favorisData.forEach(c => {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = c;
    favoris.appendChild(opt);
  });
}

// ⭐ Remplir champ chemin depuis favori
favoris.addEventListener("change", () => {
  if (favoris.value) cheminInput.value = favoris.value;
});

// ➕ Ajouter aux favoris
document.getElementById("btn-ajouter").addEventListener("click", () => {
  const chemin = cheminInput.value.trim();
  if (!chemin) return;
  const form = new FormData();
  form.append("action", "ajouter");
  form.append("chemin", chemin);
  fetch("/favoris_projet4", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
      resultat.textContent = "✅ Favori ajouté.";
      majFavoris(data.favoris);
    });
});

// 🗑️ Supprimer des favoris
document.getElementById("btn-supprimer").addEventListener("click", () => {
  const chemin = cheminInput.value.trim();
  if (!chemin) return;
  const form = new FormData();
  form.append("action", "supprimer");
  form.append("chemin", chemin);
  fetch("/favoris_projet4", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
      resultat.textContent = "🗑️ Favori supprimé.";
      majFavoris(data.favoris);
    });
});

// 📄 Charger les feuilles disponibles
document.getElementById("btnFeuilles").addEventListener("click", () => {
  const form = new FormData();
  form.append("chemin", cheminInput.value);
  fetch("/feuilles_projet4", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
      if (data.success) {
        feuilleSelect.hidden = false;
        feuilleSelect.innerHTML = "";
        data.feuilles.forEach(nom => {
          const opt = document.createElement("option");
          opt.value = nom;
          opt.textContent = nom;
          feuilleSelect.appendChild(opt);
        });
        resultat.textContent = "✅ Feuilles chargées.";
      } else {
        feuilleSelect.hidden = true;
        feuilleSelect.innerHTML = "";
        resultat.textContent = data.message;
      }
    });
});

// 💾 Soumettre le formulaire d’ajout
document.getElementById("formulaire").addEventListener("submit", function(e) {
  e.preventDefault();
  const form = new FormData(this);
  fetch("/ajout_serials", { method: "POST", body: form })
    .then(res => res.json())
    .then(data => {
      resultat.textContent = data.message;
    });
});
