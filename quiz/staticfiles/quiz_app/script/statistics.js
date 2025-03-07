const histories = document.querySelectorAll('.history');
const historiesArray = Array.from(histories);
const btn = document.getElementById('showAll');

if (historiesArray.length > 3) {
    historiesArray.slice(3).forEach(item => {
        item.style.display = 'none';
    });
} else {
    btn.style.display = 'none';
}


btn.addEventListener('click', () => {
    btn.style.display = 'none';

    historiesArray.slice(3).forEach(item => {
        item.style.display = 'block';
    });
});

