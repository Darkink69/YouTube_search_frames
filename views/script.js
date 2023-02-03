'use strict'

const read = async () => {
    let response = await fetch('1.json');
    let parsed = await response.json();

    for (let i = 0; i < parsed.length; i++) {
        let div = document.createElement('div');
        // div.className = 'col s6'
        div.innerHTML = `
            <p>Найдено ${i + 1} / ${parsed.length}</p>
            <a href="${parsed[i].link}" target="_blank"><img src="${parsed[i].thumbnail_url}" alt="" class="preview"></a>
            <h4 class="title">${parsed[i].title}</h4>
            <p class="disc">${parsed[i].description}</p>
            <p class="disc">${parsed[i].length} секунд</p>
            <a href="${parsed[i].channel_url}" target="_blank"><p class="disc">${parsed[i].author}</p></a>
            
            `;
        document.querySelector('.container').append(div);

    }
}

read()




