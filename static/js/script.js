document.addEventListener('DOMContentLoaded', function() {
    // Cargar las marcas cuando la página principal se cargue
    if (document.getElementById('marcas-list')) {
        fetch('/api/marcas')
            .then(response => response.json())
            .then(data => {
                const marcasList = document.getElementById('marcas-list');
                marcasList.innerHTML = ''; // Limpiar la lista antes de actualizar
                data.marcas.forEach(marca => {
                    const marcaItem = document.createElement('li');
                    marcaItem.innerHTML = `<a href="/marca/${marca.id}">${marca.nombre}</a>`;
                    marcasList.appendChild(marcaItem);
                });
            })
            .catch(error => console.error('Error al cargar las marcas:', error));
    }
});

document.getElementById('delete-marca-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const nombre = document.getElementById('delete-nombre').value;

    fetch('/api/marcas/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            nombre: nombre
        })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.message.includes('exitosamente')) {
            location.reload();
        }
    })
    .catch(error => console.error('Error al eliminar la marca:', error));
});