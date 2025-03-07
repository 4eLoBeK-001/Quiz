
document.addEventListener('DOMContentLoaded', function() {
    
    document.querySelector('.avatar').addEventListener('click', () => {
        document.getElementById('id_photo').click();
    });

    document.getElementById('id_photo').addEventListener('change', () => {
        document.getElementById('upload_form').submit();
    });
    
});
