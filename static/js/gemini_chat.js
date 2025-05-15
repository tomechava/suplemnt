document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("chat-form");
    const chatBox = document.getElementById("chat-box");
    const questionInput = document.getElementById("question");
    const resetBtn = document.getElementById("reset-chat");

    function appendMessage(sender, text) {
        const message = document.createElement("div");
        message.classList.add("mb-2");

        if (sender === "Gemini") {
            message.innerHTML = `<strong>${sender}:</strong><div class="mt-1">${marked.parse(text)}</div>`;
        } else {
            message.innerHTML = `<strong>${sender}:</strong> ${text}`;
        }

        chatBox.appendChild(message);
        chatBox.scrollTop = chatBox.scrollHeight;
    }


    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const question = questionInput.value.trim();
        if (!question) return;

        appendMessage("You", question);
        questionInput.value = "";

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken,
            },
            body: new URLSearchParams({ question }),
        })
            .then((res) => res.json())
            .then((data) => {
                if (data.answer) {
                    appendMessage("Gemini", data.answer);
                } else {
                    appendMessage("Gemini", "Sorry, no answer received.");
                }
            })
            .catch((err) => {
                console.error(err);
                appendMessage("Gemini", "An error occurred.");
            });
    });

    resetBtn.addEventListener("click", function () {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                "X-CSRFToken": csrfToken,
            },
            body: new URLSearchParams({ clear: "true" }),
        })
            .then((res) => res.json())
            .then((data) => {
                chatBox.innerHTML = "";
                appendMessage("System", data.answer);
            })
            .catch((err) => {
                console.error(err);
                appendMessage("System", "Failed to reset chat.");
            });
    });
});
