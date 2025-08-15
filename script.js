let cards = [];

fetch('/get_cards')
    .then(res => res.json())
    .then(data => {
        cards = data;
        renderBoard();
    });

function renderBoard() {
    let board = document.getElementById('board');
    board.innerHTML = '';
    cards.forEach((card) => {
        let div = document.createElement('div');
        div.className = 'card';
        div.innerHTML = '?';
        div.onclick = () => openCard(card.text, div);
        board.appendChild(div);
    });
}

function openCard(text, element) {
    element.innerHTML = text;
    fetch('/check_match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text })
    })
    .then(res => res.json())
    .then(result => {
        document.getElementById('score').innerText = result.score;
        document.getElementById('life').innerText = result.life;
        if (result.life <= 0) {
            window.location.href = '/end';
        }
    });
}
