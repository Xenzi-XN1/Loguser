document.getElementById('addUserForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('username').value;
    const expiredDate = document.getElementById('expired_date').value;
    const userType = document.getElementById('user_type').value;

    const response = await fetch('/add_user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, expired_date: expiredDate, user_type: userType })
    });

    const data = await response.json();
    document.getElementById('addUserResponse').innerText = JSON.stringify(data);
});

document.getElementById('checkUserForm').addEventListener('submit', async function(e) {
    e.preventDefault();

    const username = document.getElementById('checkUsername').value;

    const response = await fetch(`/check_user/${username}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const data = await response.json();
    document.getElementById('checkUserResponse').innerText = JSON.stringify(data);
});
