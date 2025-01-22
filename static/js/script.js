var index = 0;
var flag;
const numbers = Array.from({ length: 45 }, (_, i) => i + 1);
const genNonce = () => {
    const numbers = Array.from({ length: 45 }, (_, i) => i + 1);
    const nonce = "_".repeat(16).replace(/_/g, () => numbers[Math.floor(Math.random() * numbers.length)] + ' ');

    return nonce;
};
const getColorByRange = (num) => {
    if (num >= 1 && num <= 10) return '#f1c40f';
    if (num >= 11 && num <= 20) return '#3498db';
    if (num >= 21 && num <= 30) return '#ff9e80';
    if (num >= 31 && num <= 40) return '#95a5a6';
    if (num >= 41 && num <= 45) return '#2ecc71';

    return '#ffffff';
};
const addNumbers = (numbers) => {
    index = index + 1;
    const row = document.createElement('tr');
    const cell1 = document.createElement('th');
    const cell2 = document.createElement('td');
    
    cell1.scope = 'row';
    cell1.textContent = index;

    const lottoNumbers = numbers.trim().split(' ');

    lottoNumbers.forEach(num => {
        const span = document.createElement('span');
        span.className = 'lotto-ball';
        span.textContent = num;
        span.style.backgroundColor = getColorByRange(parseInt(num, 10));

        cell2.appendChild(span);
    });
    
    row.appendChild(cell1);
    row.appendChild(cell2);
    tableBody.appendChild(row);
}
const tableBody = document.querySelector("#numbersTable tbody");

[...Array(5)].forEach((_, index) => {
    addNumbers(genNonce());
});

const lottoForm = document.getElementById('lottoForm');
const messageDiv = document.getElementById('message');

lottoForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const userNumbers = document.getElementById('userNumbers').value.trim();
    
    if (userNumbers.split(' ').length !== 16 || userNumbers.split(' ').some(num => num < 1 || num > 45 || isNaN(num))) {
        messageDiv.innerHTML = `<div class="alert alert-danger">Invalid input. Ensure you submit 16 numbers between 1 and 45.</div>`;
        return;
    }

    const lottoNumbers = genNonce().trim();

    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ lottoNumbers: lottoNumbers, numbers: userNumbers })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to send nonce to server');
        }

        return response.text();
    })
    .then(data => {
        flag = data;
        
        if (userNumbers != lottoNumbers) {
            addNumbers(lottoNumbers);
            messageDiv.innerHTML = `<div class="alert alert-danger">Wrong numbers.</div>`;
        }
        else {
            document.getElementById('userNumbers').disabled = true;
            document.getElementById('submitButton').disabled = true;
            messageDiv.innerHTML = `<div class="alert alert-primary">${flag}</div>`;
        }
    })
});
