document.addEventListener('DOMContentLoaded', function () {
    const editButtons = document.querySelectorAll('.edit-btn');
    const saveButtons = document.querySelectorAll('.save-btn');

    editButtons.forEach(btn => {
        btn.addEventListener('click', function () {
            const row = btn.closest('tr');
            row.querySelectorAll('span').forEach(span => {
                span.style.display = 'none';
            });
            row.querySelectorAll('input').forEach(input => {
                input.style.display = 'block';
            });
            btn.style.display = 'none';
            row.querySelector('.save-btn').style.display = 'inline-block';
        });
    });

    saveButtons.forEach(btn => {
        btn.addEventListener('click', function (event) {
            event.preventDefault();
            const row = btn.closest('tr');
            const formData = new FormData();
            row.querySelectorAll('input').forEach(input => {
                formData.append(input.name, input.value);
            });
            formData.append('id', row.dataset.id);
            const action = `/${row.closest('table').dataset.table}/edit`;
            fetch(action, {
                method: 'POST',
                body: new URLSearchParams(formData)
            }).then(response => {
                if (response.ok) {
                    window.location.reload();
                } else {
                    console.error('Failed to save changes.');
                }
            }).catch(error => {
                console.error('Error:', error);
            });
        });
    });
});
