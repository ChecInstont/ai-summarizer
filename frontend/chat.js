const chatBox = document.getElementById("chat-box");
const userInput = document.getElementById("chat-input");
const sendBtn = document.getElementById("send-btn");

const apiUrlWrapper = document.querySelector(".api-url-wrapper");
const apiVersionWrapper = document.querySelector(".api-version-wrapper");
const provider = document.getElementById("provider");

const visitor_id = localStorage.getItem("visitor_id");

const summarizedContext = localStorage.getItem("summarized_context") || "";

document.addEventListener("DOMContentLoaded", () => {

  // Initially hide
  apiUrlWrapper.style.display = "none";
  apiVersionWrapper.style.display = "none";

  provider.addEventListener("change", () => {
    if (provider.value === "azureopenai") {
      apiUrlWrapper.style.display = "block";
      apiVersionWrapper.style.display = "block";
    } else {
      apiUrlWrapper.style.display = "none";
      apiVersionWrapper.style.display = "none";
    }
  });
});



let chatHistory = [];

sendBtn.addEventListener("click", async () => {
  const question = userInput.value.trim();
  if (!question) return;

  appendMessage("You", question, "user-msg");
  userInput.value = "";



  // Extract config values from the AI Config Sidebar
  const apiUrl = document.getElementById("api-url")?.value.trim() || "";
  const apiKey = document.getElementById("api-key").value.trim();
  const model = document.getElementById("model").value.trim();
  const temperature = parseFloat(document.getElementById("temperature").value.trim()) || 0.7;
  const apiVersion = document.getElementById("api-version")?.value.trim() || ""; // Optional field

  // Construct history
// Clean the history before sending
const history = [
  ...chatHistory,
  { role: "user", content: question }
].filter(m => m.role && m.content && m.content.trim().length > 0);


  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" }, 
      body: JSON.stringify({
        message: question,
        api_url: apiUrl,
        api_key: apiKey,
        model: model,
        temperature: temperature,
        provider: provider.value,
        api_version: apiVersion,
        visitor_id: visitor_id
      }),
    });

    const data = await res.json();
    appendMessage("AI", data.answer || "[No response]", "ai-msg");

chatHistory.push({ role: "user", content: question });

if (data.answer) {
  chatHistory.push({ role: "assistant", content: data.answer });
}


  } catch (err) {
    appendMessage("Error", "Something went wrong.", "ai-msg");
    console.error(err);
  }
});


function appendMessage(_, text, className) {
  const div = document.createElement("div");
  div.className = className;
  div.textContent = text;
  div.classList.add("chat-msg", className);
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}