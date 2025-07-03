const zoneFeuilles = document.getElementById("zone-feuilles");
const btnAjouterFeuille = document.getElementById("ajouter-feuille");
const btnGenRetour = document.getElementById("gen-retour");
const feedbackRetour = document.getElementById("feedback-retour");

btnAjouterFeuille.addEventListener("click", () => {
  const bloc = document.createElement("div");
  bloc.style.marginTop = "20px";
  bloc.innerHTML = `
    <input type="text" placeholder="Nom de la feuille" class="nom-feuille" required>
    <textarea class="liste-serials" placeholder="Serials (1 par ligne)" rows="5"></textarea>
  `;
  zoneFeuilles.appendChild(bloc);
});

btnGenRetour.addEventListener("click", () => {
  const to = document.getElementById("to").value.trim();
  const noms = document.querySelectorAll(".nom-feuille");
  const serials = document.querySelectorAll(".liste-serials");

  const data = new FormData();
  data.append("to", to);

  const feuilles = {};
  for (let i = 0; i < noms.length; i++) {
    const nom = noms[i].value.trim().toUpperCase();
    const contenu = serials[i].value.trim();
    if (nom && contenu) {
      feuilles[nom] = contenu;
    }
  }

  if (Object.keys(feuilles).length === 0) {
    feedbackRetour.innerText = "❌ Ajoute au moins une feuille avec des serials.";
    feedbackRetour.style.color = "crimson";
    return;
  }

  data.append("feuilles_json", JSON.stringify(feuilles));

  fetch("/gen_retour", { method: "POST", body: data })
    .then(r => r.json())
    .then(data => {
      feedbackRetour.innerText = data.message;
      feedbackRetour.style.color = data.message.includes("✅") ? "green" : "crimson";
    });
});
