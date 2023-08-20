const chatInput = document.querySelector("#chat-input");
const sendButton = document.querySelector("#send-btn");
const chatContainer = document.querySelector(".chat-container");
const themeButton = document.querySelector("#theme-btn");
const deleteButton = document.querySelector("#delete-btn");
const downloadButton = document.querySelector("#download-btn");
const feedButton = document.querySelector("#feed-btn");

let userText = null;

const loadDataFromLocalStorage = () => {
    // Load saved chats and theme from local storage and apply/add them to the page
    const themeColor = localStorage.getItem("themeColor");

    document.body.classList.toggle("light-mode", themeColor === "light_mode");
    themeButton.innerText = document.body.classList.contains("light-mode")
        ? "dark_mode"
        : "light_mode";

    chatContainer.innerHTML = `
    <div class="default-text">
      <h1>IKYET</h1>
      <p>Let's code!<br> Your chat history will be displayed here.</p>
    </div>`;
    chatContainer.scrollTo(0, chatContainer.scrollHeight); // Scroll to the bottom of the chat container
};

const createChatElement = (content, className) => {
    // Create a new div, apply the chat and specified class, and set the HTML content of the div
    const chatDiv = document.createElement("div");
    chatDiv.classList.add("chat", className);
    chatDiv.innerHTML = content;
    return chatDiv; // Return the created chat div
};

const getChatResponse = (incomingChatDiv, responseText) => {
    // Remove the typing animation, append the response text, and save the chats to local storage
    incomingChatDiv.querySelector(".typing-animation").remove();

    const pElement = document.createElement("p");
    pElement.textContent = responseText;

    incomingChatDiv.querySelector(".chat-details").appendChild(pElement);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    localStorage.setItem("all-chats", chatContainer.innerHTML);
    chatInput.value = "";
};

const copyResponse = (copyBtn) => {
    // Copy the text content of the response to the clipboard
    const responseTextElement = copyBtn.parentElement.querySelector("p");
    navigator.clipboard.writeText(responseTextElement.textContent);
    copyBtn.textContent = "done";
    setTimeout(() => (copyBtn.textContent = "content_copy"), 1000);
};

const showTypingAnimation = () => {
    // Display the typing animation and call the getChatResponse function
    const html = `<div class="chat-content">
    <div class="chat-details">
      <img src="images/chatbot.jpg" alt="chatbot-img">
      <div class="typing-animation">
        <div class="typing-dot" style="--delay: 0.2s"></div>
        <div class="typing-dot" style="--delay: 0.3s"></div>
        <div class="typing-dot" style="--delay: 0.4s"></div>
      </div>
    </div>
    <span onclick="copyResponse(this)" class="material-symbols-rounded">content_copy</span>
  </div>`;

    // Create an incoming chat div with typing animation and append it to the chat container
    const incomingChatDiv = createChatElement(html, "incoming");
    chatContainer.appendChild(incomingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);

    // Call the handleChatResponse function after a delay
    setTimeout(() => {
        const userText = chatInput.value.trim();
        handleChatResponse(incomingChatDiv, userText);
    }, 500);
};

const handleChatResponse = (incomingChatDiv, userText) => {
    // Send the user's message to the server
    fetch("/get_files", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            userText: userText,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            const responseText = data.response;
            getChatResponse(incomingChatDiv, responseText);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
};

const handleOutgoingChat = (userText) => {
    userText = userText.trim(); // Get chatInput value and remove extra spaces
    if (!userText) return; // If chatInput is empty, return from here

    // Clear the input field and reset its height
    //chatInput.value = "";
    chatInput.style.height = `${initialInputHeight}px`;

    const html = `<div class="chat-content">
    <div class="chat-details">
      <img src="images/user.jpg" alt="user-img">
      <p>${userText}</p>
    </div>
  </div>`;

    // Create an outgoing chat div with the user's message and append it to the chat container
    const outgoingChatDiv = createChatElement(html, "outgoing");
    chatContainer.querySelector(".default-text")?.remove();
    chatContainer.appendChild(outgoingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);
    setTimeout(showTypingAnimation, 500);
};

const handleFeedback = (userText) => {
    userText = userText.trim();
    if (!userText) return;

    chatInput.style.height = `${initialInputHeight}px`;

    const html = `
    <div class="chat-content">
      <div class="chat-details">
        <img src="images/user.jpg" alt="user-img">
        <h1>Feedback:</h1>
        <p>${userText}</p>
      </div>
    </div>
  `;

    const outgoingChatDiv = createChatElement(html, "outgoing");
    chatContainer.querySelector(".default-text")?.remove();
    chatContainer.appendChild(outgoingChatDiv);
    chatContainer.scrollTo(0, chatContainer.scrollHeight);

    sendFeedbackToServer(userText, outgoingChatDiv);
};

const sendFeedbackToServer = (userText, outgoingChatDiv) => {
    fetch("/get_feedback", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            userText: userText,
        }),
    })
        .then((response) => response.json())
        .then((data) => {
            const responseText = data.response;
            getChatResponse(outgoingChatDiv, responseText);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
};

const handleChatDelete = () => {
    // Remove the chats from local storage and reload the chat history
    if (confirm("Are you sure you want to delete all the chats?")) {
        localStorage.removeItem("all-chats");
        loadDataFromLocalStorage();
    }
};

const handleThemeToggle = () => {
    // Toggle the body's class for the theme mode and save the updated theme to local storage
    document.body.classList.toggle("light-mode");
    localStorage.setItem("themeColor", themeButton.innerText);
    themeButton.innerText = document.body.classList.contains("light-mode")
        ? "dark_mode"
        : "light_mode";
};

const handleDownload = () => {
    // Fetch the chat history from the server and initiate the download
    fetch("/files_download")
        .then((response) => response.blob())
        .then((blob) => {
            // Create a URL for the blob
            const url = URL.createObjectURL(blob);
            // Create a link element and set its properties for the download
            const link = document.createElement("a");
            link.href = url;
            link.download = "ikyet.zip";
            // Simulate a click on the link to trigger the download
            link.click();
            // Clean up the URL object after the download
            URL.revokeObjectURL(url);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
};

const initializeEventListeners = () => {
    sendButton.addEventListener("click", () => handleOutgoingChat(chatInput.value));
    deleteButton.addEventListener("click", handleChatDelete);
    themeButton.addEventListener("click", handleThemeToggle);
    downloadButton.addEventListener("click", handleDownload);
    feedButton.addEventListener("click", () => {
        const userText = chatInput.value.trim();
        handleFeedback(userText);
    });
};

const initialInputHeight = chatInput.scrollHeight;

chatInput.addEventListener("input", () => {
    // Adjust the height of the input field dynamically based on its content
    chatInput.style.height = `${initialInputHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
});

chatInput.addEventListener("keydown", (e) => {
    // If the Enter key is pressed without Shift and the window width is larger than 800 pixels, handle the outgoing chat
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
        e.preventDefault();
        handleOutgoingChat(chatInput.value);
    }
});

// Load data from local storage on page load
loadDataFromLocalStorage();

initializeEventListeners();
