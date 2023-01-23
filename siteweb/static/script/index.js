const picture_url_error = "http://127.0.0.1:8000/static/img/error404.png"
let loading = false;

// On ajoute un listener pour savoir quand l'utilisateur appuie sur la touche entrer
document.addEventListener("keypress", async function(e) {
  if (e.key === "Enter" && loading != true) {
    let loadingpage = document.getElementById("loadingpage");
    loadingpage.classList.remove("hidden");
    loading = true;
    const valueSearch = document.getElementById('searchbar').value;
    const response = await fetch('http://127.0.0.1:8000/api/?q=' + valueSearch);
    const data = await response.json();

    const boxJeux = document.querySelectorAll(".col-span-1")
    for (let i = 0; i < boxJeux.length ; i++) {
      // Modification de l'image
      boxJeux[i].querySelectorAll("img")[1].src = data[i]['picture_url'] != " - " ? data[i]['picture_url'] : picture_url_error

      // modification des spans
      const listSpan = boxJeux[i].querySelectorAll("span")
      listSpan[0].innerText = data[i]['title']
      listSpan[1].innerText = data[i]['opinion']
      listSpan[2].innerText = data[i]['price']
      listSpan[3].innerHTML = data[i]['link'] != " - " ? '<a href="' + data[i]['link'] + '">Cliquez ici</a>' : data[i]['link']
    }

    // Récupère tous les éléments de la page
    var element = document.querySelector(".container");
    var elements = element.querySelectorAll("*");

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
    loadingpage.classList.add("hidden");
  }
});