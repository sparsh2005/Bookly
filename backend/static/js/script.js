document.getElementById('send-btn').addEventListener('click', async () => {
    const input = document.getElementById('user-input').value;
  
    if (!input) {
      alert('Please enter a book name!');
      return;
    }
  
    const messages = document.getElementById('messages');
  
    // Append user message
    const userMsg = document.createElement('div');
    userMsg.className = 'user-message';
    userMsg.textContent = input;
    messages.appendChild(userMsg);
  
    // Fetch recommendations
    const response = await fetch('/recommend', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ book_name: input }),
    });
  
    const data = await response.json();
  
    // Append bot message
    const botMsg = document.createElement('div');
    botMsg.className = 'bot-message';
  
    if (data.error) {
      botMsg.textContent = data.error;
    } else {
      data.books.forEach((book) => {
        botMsg.innerHTML += `
          <div>
            <h3>${book.title}</h3>
            <p>${book.author}</p>
            <img src="${book.thumbnail}" alt="${book.title}" />
            <p>${book.description}</p>
          </div>
        `;
      });
    }
  
    messages.appendChild(botMsg);
    document.getElementById('user-input').value = '';
  });