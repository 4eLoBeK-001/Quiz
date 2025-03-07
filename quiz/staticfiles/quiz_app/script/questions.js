
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

function hideMessage(button) {
    const div = button.closest('div');
    const div2 = document.getElementsByClassName('container-question')[0]
    div.classList.add('hidden');

    setTimeout( () => {
        div.style.opacity = '0';
    }, 700);

    setTimeout( () => {
        div.style.display = 'none';
        div2.style.transition = 'none';
        div2.style.transform = 'translate(0,0)';
    }, 2700);
    
    div2.style.transform = 'translate(0,-186px)';
}

function confirmDelete(link) {
    const confirmed = confirm('Вы действительно хотите удалить?');

    if (confirmed){
        window.location.href = link.href;
    } else{
        return false;
    }
}

function changeActivity() {
    document.getElementById('isActiveForm').submit();
}

function hideInactive(button) {
    
    const cards = document.querySelectorAll('.card');

    for(card of cards){
        const checkbox = card.querySelector('input');
        // Если нажато то скрывает все неактивные вопросы
        if (!button.checked && !checkbox.checked) { 
            card.style.display = 'none';
        } else{
            card.style.display = 'inline';
        }
    }
}