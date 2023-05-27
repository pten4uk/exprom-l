let pageContent = document.getElementById('page-content')
let searchInput = document.getElementById('catalog-search')
let dataList = document.getElementById('header-search-list')


function addNewHTML(data) {
    let container = document.createElement('div')
    container.className = 'container'
    let row = document.createElement('div')
    row.className = 'row'
    container.appendChild(row)

    for (let model of data) {
        let elementDiv = document.createElement('div')
        elementDiv.className = 'col col-sm-12 col-md-12 col-lg-3'
        elementDiv.innerHTML = `
                    <a style="text-decoration: inherit; color: inherit;"
                    href="/catalog/${model.category_slug}/${model.slug}">
                    <div class="card mb-3 card-with-hover" style="">
                        <div class="d-flex align-items-center justify-content-center p-1">
                            <img src="${model.photo}" class="card-img-top" alt="...">
                        </div>
                        <div class="card-body">
                            <h5 class="card-title">${model.get_name}</h5>
                            <p class="card-text">${model.shirt_description}</p>
                            <p class="card-text">
                                Размеры (Ш*В*Г): ${model.width}*${model.height}*${model.depth}
                            </p>
                            <p class="card-text text-muted mt-4">${model.price} руб.</p>
                        </div>
                    </div>
                    </a>
                `
        row.appendChild(elementDiv)
    }

    pageContent.innerHTML = ''
    pageContent.appendChild(container)
}

function addTagsToDatalist(data) {

    dataList.innerHTML = ''
    let maxElems = 5
    let counter = 0

    for (let elem of data) {
        if (counter > maxElems) break
        let option = document.createElement('option')
        option.innerText = elem.name
        dataList.appendChild(option)
        counter++
    }
}

function fetchData(search) {
    fetch(`/catalog/api/search/?search=${search}`)
        .then(r => r.json())
        .then(data => {
            addNewHTML(data)
        })
}

function fetchTags(search) {
    fetch(`/catalog/api/search_tags/?search=${search}`)
        .then(r => r.json())
        .then(data => {
            addTagsToDatalist(data)
        })
}

let canFetchTimeout;

searchInput.addEventListener('keydown', e => {
    if (e.keyCode === 13) e.preventDefault()
})

searchInput.addEventListener('input', e => {
    clearTimeout(canFetchTimeout)
    canFetchTimeout = setTimeout(() => {
        if (!e.target.value) return location.reload()
        fetchTags(e.target.value)
        fetchData(e.target.value)
    }, 1000)
})

console.dir(dataList)

