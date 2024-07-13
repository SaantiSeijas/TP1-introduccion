document.addEventListener('DOMContentLoaded', function() {
    // Cargar las latas cuando la página principal se cargue
    if (document.getElementById('latas-list')) {
        fetch('/api/latas')
            .then(response => response.json())
            .then(data => {
                const latasList = document.getElementById('latas-list');
                data.latas.forEach(lata => {
                    const lataItem = document.createElement('li');
                    lataItem.innerHTML = `<a href="/lata/${lata.id}">${lata.tamanio} - $${lata.precio}</a>`;
                    latasList.appendChild(lataItem);
                });
            })
            .catch(error => console.error('Error al cargar las latas:', error));
    }
});
