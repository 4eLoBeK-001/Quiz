function confirmDelete(link) {
    const confirmed = confirm('Вы действительно хотите удалить?');

    if (confirmed){
        window.location.href = link.href;
    } else{
        return false;
    }
}