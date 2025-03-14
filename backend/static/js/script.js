document.addEventListener("DOMContentLoaded", () => {
    const messagesContainer = document.getElementById("messages");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-btn");
  
    // Function to create and append the initial chatbot message
    const appendInitialMessage = () => {
        const initialMessage = createMessage(
            "Hi! I'm Bookly, your personal library companion. I'm here to help you discover your next literary adventure. Give me the titles of the books you enjoyed, and I'll recommend some perfect matches for your reading list. We are working on some amazing updates for this app, so stay tuned!",
            null,
            false
        );
        messagesContainer.appendChild(initialMessage);
    };
  
    const createMessage = (content, books = null, isUser = false) => {
      const messageDiv = document.createElement("div");
      messageDiv.classList.add("message", isUser ? "user" : "chatbot");
  
      const avatar = document.createElement("div");
      avatar.classList.add("avatar");
      const avatarImg = document.createElement("img");
      avatarImg.src = isUser ? "static/images/user.png" : "static/images/bot.png";
      avatar.appendChild(avatarImg);
  
      const contentDiv = document.createElement("div");
      contentDiv.classList.add("content");
      
      // Add the text content
      const textDiv = document.createElement("div");
      textDiv.textContent = content;
      contentDiv.appendChild(textDiv);
  
      // Add recommendations if they exist
      if (books) {
          const recommendationsDiv = document.createElement("div");
          recommendationsDiv.classList.add("recommendation-container");
          
          books.forEach(book => {
              const card = document.createElement("div");
              card.classList.add("recommendation-card");
              
              card.innerHTML = `
                  <div class="image-container">
                      <img src="${book.thumbnail}" alt="${book.title}">
                  </div>
                  <div class="details">
                      <h3>${book.title}</h3>
                      <p>${book.author}</p>
                  </div>
              `;
              
              recommendationsDiv.appendChild(card);
          });
          
          contentDiv.appendChild(recommendationsDiv);
      }
  
      if (isUser) {
          messageDiv.appendChild(contentDiv);
          messageDiv.appendChild(avatar);
      } else {
          messageDiv.appendChild(avatar);
          messageDiv.appendChild(contentDiv);
      }
  
      return messageDiv;
    };
  
    // Call the function to append the initial message
    appendInitialMessage();
  
    sendButton.addEventListener("click", async () => {
      const userText = userInput.value.trim();
      if (!userText) return;
  
      // Add user message
      messagesContainer.appendChild(createMessage(userText, null, true));
      userInput.value = "";
  
      const response = await fetch("/recommend", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ book_name: userText }),
      });
  
      const data = await response.json();
      if (data.books) {
          // Create single message with text and recommendations
          const message = createMessage(
              "Based on your interests, I think you'll love these literary treasures:",
              data.books,
              false
          );
          messagesContainer.appendChild(message);
  
          // Apply inline style for bold text
          const boldText = message.querySelector('.content div:first-child');
          if (boldText) {
              boldText.style.fontWeight = '500';
          }
      } else {
          messagesContainer.appendChild(createMessage("No recommendations found.", null, false));
      }
    });
  });