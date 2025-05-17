const API_BASE = ""; // Update if backend is on a different domain

// Generate or retrieve visitor ID
function getVisitorId() {
  let visitorId = localStorage.getItem("visitor_id");
  if (!visitorId) {
    visitorId = crypto.randomUUID();
    localStorage.setItem("visitor_id", visitorId);
  }
  fetch("/api/visitor/visit", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-Visitor-ID": visitorId
          },
          body: JSON.stringify({}) // send empty body or add extra info if needed
});
  
  return visitorId;
}
const VISITOR_ID = getVisitorId();

// DOM Elements
const textInput = document.getElementById("text-input");
const fileInput = document.getElementById("file-input");
const fileNameSpan = document.getElementById("file-name");
const uploadBtn = document.getElementById("upload-btn");
const summarizeBtn = document.getElementById("summarize-btn");
const summaryOutput = document.getElementById("summary-output");
const resultSection = document.getElementById("result-section");
const apiUrlInput = document.getElementById("api-url");
const providerInput = document.getElementById("provider");
const apiKeyInput = document.getElementById("api-key");
const modelInput = document.getElementById("model");
const temperatureInput = document.getElementById("temperature");
const promptInput = document.getElementById("prompt");
const historyList = document.getElementById("history-list");

// File upload handling
fileInput.addEventListener("change", () => {
  fileNameSpan.textContent = fileInput.files[0]?.name || "No file chosen";
});

uploadBtn.addEventListener("click", async () => {
  if (fileInput.files.length === 0) {
    alert("Please select a file to upload.");
    return;
  }
  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  try {
    uploadBtn.disabled = true;
    uploadBtn.textContent = "Uploading...";
    const res = await fetch(`${API_BASE}/api/upload`, {
      method: "POST",
      body: formData,
    });
    if (!res.ok) throw new Error("File upload failed");
    const data = await res.json();
    textInput.value = data.text;
  } catch (err) {
    alert(err.message);
  } finally {
    uploadBtn.disabled = false;
    uploadBtn.textContent = "Upload";
  }
});

// Summarization logic
summarizeBtn.addEventListener("click", async () => {
  const text = textInput.value.trim();
  if (!text) {
    alert("Please enter some text or upload a file first.");
    return;
  }

  const api_url = apiUrlInput.value.trim();
  const api_key = apiKeyInput.value.trim();
  const model = modelInput.value.trim();
  const temperature = parseFloat(temperatureInput.value);
  const provider = providerInput.value.trim();
  let prompt = promptInput.value.trim();
  if (!prompt) prompt = "Summarize the given text into brief info.";

  if (!api_url || !api_key || !model) {
    alert("Please fill API URL, API Key, and Model fields.");
    return;
  }

  summarizeBtn.disabled = true;
  summarizeBtn.textContent = "Summarizing...";

  try {
    const response = await fetch(`${API_BASE}/api/summarize`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Visitor-ID": VISITOR_ID
      },
      body: JSON.stringify({ text, api_url, api_key, model, temperature, prompt, provider }),
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || "Summarization failed");
    }

    const resData = await response.json();
    if (resData){
      window.location.href = window.location.origin+"/summaries-history.html";
    }else{
      alert("something went wrong");
    }
  } catch (err) {
    alert(err.message);
  } finally {
    summarizeBtn.disabled = false;
    summarizeBtn.textContent = "Summarize Text";
  }
});

window.copy_visitor_id = VISITOR_ID;
