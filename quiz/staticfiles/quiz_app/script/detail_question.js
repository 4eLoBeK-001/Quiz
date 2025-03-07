function toggleInput(checkbox, event){
    const answerId = checkbox.id;
    const input = document.getElementById(`input-${answerId}`);
    const label = document.getElementById(`label-${answerId}`);
    
    if (!checkbox.checked){
        label.style.display = 'flex';
        input.style.display = 'none';
    } else {
        label.style.display = 'none';
        input.style.display = 'block';
        input.style.marginTop = '6.5px';
    }

    adjustWidth();
    transInput(event);
}


let input = document.getElementsByClassName('answer-text-input')[0];

function adjustWidth() {
    let size = input.scrollWidth + 4;
    input.style.width = size + 'px';
    
}



function transInput(event) {
    let saver = document.getElementsByClassName('save-write')[0];

    saver.value = event.target.value;
    input.style.transition = 'none';

    adjustWidth();
};


