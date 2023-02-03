'use strict'

const read = async () => {
    let response = await fetch('nsfw.json');
    let parsed = await response.json();

    // let response2 = await fetch('timecode.json');
    // let parsed2 = await response2.json();

    // for (let i = 0; i < parsed.length; i++) {
    //     let div = document.createElement('div');
    //     div.innerHTML = `
    //         <p>${i + 1} / ${parsed.length}</p>
    //         <a href="out/${parsed[i].file}" target="_blank"><img src="out/${parsed[i].file}" alt="" style="width:200px;" class="preview"></a>
    //         <p class="disc">Porn: ${parsed[i].porn}</p>
    //         <p class="disc">Sexy: ${parsed[i].sexy}</p>
    //         <p>${parsed2[i]}</p>
                        
    //         `;
    //     document.querySelector('.container').append(div);

    // }
    for (let i = 0; i < parsed.length; i++) {
        let div = document.createElement('div');
        div.innerHTML = `
            // <p>${i + 1} / ${parsed.length}</p>
            // <a href="out/${parsed[i].file}" target="_blank"><img src="out/${parsed[i].file}" alt="" style="width:200px;" class="preview"></a>
            <p>${parsed[i].porn}   ${parsed[i].sexy} </p>
                        
            `;
        document.querySelector('.container').append(div);

    }
}

read()
