
const questions = document.querySelectorAll('.strogo');
const par = document.createElement('p')

for (elem of questions){
    const ele = elem.querySelectorAll('p')
    const len = ele.length
    
    const list = Array.from(ele)

    list.slice(3).forEach(element => {
        element.innerHTML = ''
        
    });

    if (len>3){
        par.innerText = `...(${len-3})`;
        elem.appendChild(par)
    }

}
