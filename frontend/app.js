// Exemple simple d'appel API sécurisé
fetch('https://localhost:8000/', { method: 'GET' })
  .then(res => res.json())
  .then(data => {
    document.getElementById('app').innerText = JSON.stringify(data, null, 2);
  })
  .catch(err => {
    document.getElementById('app').innerText = "Erreur de connexion à l’API : " + err;
  });