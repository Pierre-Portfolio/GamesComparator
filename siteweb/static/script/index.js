let loading = false;

// On ajoute un listener pour savoir quand l'utilisateur appuie sur la touche entrer
document.addEventListener("keypress", async function(e) {
  if (e.key === "Enter" && loading != true) {
    loading = true;
    const valueSearch = document.getElementById('searchbar').value;
    const response = await fetch('http://127.0.0.1:8000/api/?q=' + valueSearch);
    const data = await response.json();
    console.log(data);

    // Récupère tous les éléments de la page
    var elements = document.querySelectorAll("*");

    // Parcoure chaque élément
    elements.forEach(function(element) {
      // Vérifie si l'élément possède la classe "hidden"
      if (element.classList.contains("hidden")) {
        // Retire la classe "hidden" de l'élément
        element.classList.remove("hidden");
      }

      // Vérifie si c'est actuellement l'image
      if (element.classList.contains("w-9/12")) {
        // Retire la classe "hidden" de l'élément
        element.classList.add("hidden");
      }
    });
    loading = false;
  }
});