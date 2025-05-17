

const API_BASE = ""; // Change if backend hosted elsewhere

const copy_visitor_id = localStorage.getItem("visitor_id");

const summaryOutput = document.getElementById("summary-output");
const resultSection = document.getElementById("result-section");
const historyList = document.getElementById("history-list");


// Load summary history
async function loadHistory() {
  try {
    const res = await fetch(`${API_BASE}/api/history?visitor_id=${copy_visitor_id}`);
    if (!res.ok) throw new Error("Failed to load history");
    const data = await res.json();
    historyList.innerHTML = "";

    data.history.forEach(item => {
      const div = document.createElement("div");
      div.className = "history-item";

      const time = document.createElement("time");

      time.textContent = new Date(item.created_at);

      const model = document.createElement("h4");
      model.textContent = `AI Model Used: ${item.model}`;

      const summary = document.createElement("p");
      summary.textContent = `Summary: \n ${item.summary_text}`;

      div.appendChild(time);
      div.appendChild(model);
      div.appendChild(summary);

      historyList.appendChild(div);
    });


  } catch (err) {
    console.error("History error:", err);
  }
}

// Load history on page load
window.onload = loadHistory;
