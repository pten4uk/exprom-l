let pageContent = document.getElementById('page-content')
let searchInput = document.getElementById('catalog-search')


function addNewHTML(data) {
    let container = document.createElement('div')
    container.className = 'container'

    for (let model of data) {
        let elementDiv = document.createElement('div')
        elementDiv.className = 'col col-sm-12 col-md-12 col-lg-6'
        elementDiv.innerHTML = `
                    <a style="text-decoration: inherit; color: inherit;"
                    href="/catalog/${model.category_slug}/${model.slug}">
                    <div class="card mb-3 card-with-hover" style="">
                        <div class="d-flex align-items-center justify-content-center p-1">
                            <img src="${model.photo}" class="card-img-top" alt="...">
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">Модель ${model.number}</h5>
                            <p class="card-text">${model.shirt_description}</p>
                            <p class="card-text">
                                Размеры (Ш*В*Г): ${model.width}*${model.height}*${model.depth}
                            </p>
                            <p class="card-text text-muted mt-4">${model.price} руб.</p>
                        </div>
                    </div>
                    </a>
                `
        container.appendChild(elementDiv)
    }

    pageContent.innerHTML = ''
    pageContent.appendChild(container)
}

function fetchData(search) {
    fetch(`/catalog/api/search/?search=${search}`)
        .then(r => r.json())
        .then(data => {
            addNewHTML(data)
        })
}


let canFetchTimeout;

searchInput.addEventListener('input', e => {
    clearTimeout(canFetchTimeout)
    if (!e.target.value) location.reload()
    canFetchTimeout = setTimeout(() => {
        fetchData(e.target.value)
    }, 1000)
})

