document.addEventListener("DOMContentLoaded", () => {
    const messagesContainer = document.getElementById("messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");
  
    const createMessage = (content, isUser = false) => {
      const messageDiv = document.createElement("div");
      messageDiv.classList.add("message", isUser ? "user" : "chatbot");
  
      const avatar = document.createElement("img");
      avatar.src = isUser
        ? "static/images/user.png"
        : "static/images/bot.png";
      avatar.classList.add("avatar");
  
      const contentDiv = document.createElement("div");
      contentDiv.classList.add("content");
      contentDiv.textContent = content;
  
      if (isUser) {
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(avatar);
      } else {
        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
      }
  
      messagesContainer.appendChild(messageDiv);
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    };
  
    const createRecommendationCard = (book) => {
      const card = document.createElement("div");
      card.classList.add("recommendation-card");
  
      card.innerHTML = `
        <img src="${book.thumbnail}" alt="${book.title}">
        <div class="details">
          <h3>${book.title}</h3>
          <p>${book.author}</p>
        </div>
      `;
  
      card.addEventListener("click", () => {
        // Expand card logic
        const overlay = document.createElement("div");
        overlay.classList.add("overlay");
        overlay.innerHTML = `
          <div class="expanded-card">
            <img src="${book.thumbnail}" alt="${book.title}">
            <div class="details">
              <h3>${book.title}</h3>
              <p>${book.author}</p>
              <p>${book.description}</p>
            </div>
          </div>
        `;
        document.body.appendChild(overlay);
  
        overlay.addEventListener("click", () => {
          document.body.removeChild(overlay);
        });
      });
  
      messagesContainer.appendChild(card);
    };
  
    sendButton.addEventListener("click", async () => {
      const userText = userInput.value.trim();
      if (!userText) return;
  
      createMessage(userText, true);
      userInput.value = "";
  
      const response = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ book_name: userText }),
      });
  
      const data = await response.json();
      if (data.books) {
        createMessage("Based on your interests, I think you'll love these literary treasures:");
        data.books.forEach(createRecommendationCard);
      } else {
        createMessage("No recommendations found.");
      }
    });
  });