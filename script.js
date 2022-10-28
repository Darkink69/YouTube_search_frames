'use strict'

const read = async () => {
    let response = await fetch('1.json');
    let parsed = await response.json();
    let div = document.createElement('div');
    div.innerHTML = `
        <a href="${parsed.link}" target="_blank"><img src="${parsed.thumbnail_url}" alt="" class="preview"></a>
        <p class="title">${parsed.title}</p>
        <p class="disc">${parsed.description}</p>
        <p class="disc">${parsed.length} секунд</p>
        <a href="${parsed.channel_url}" target="_blank"><p class="disc">${parsed.author}</p></a>
        
        `;
    document.body.append(div);

}

read()




