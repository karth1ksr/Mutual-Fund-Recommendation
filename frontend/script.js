//const API_BASE_URL = "https://mf-backend-geou.onrender.com/api/v1";
const API_BASE_URL = "http://localhost:8000/api/v1";

let currentUserId = null;

function createCollapsibleCard(title, contentHTML, index = null) {
    const id = `card-${Math.random().toString(36).substr(2, 9)}`;
    const num = index !== null ? `${index + 1}. ` : "";

    return `
        <div class="collapsible">
            <button class="collapse-btn" onclick="toggleCollapse('${id}')">
                ${num}${title}
            </button>
            <div id="${id}" class="collapse-content">
                ${contentHTML}
            </div>
        </div>
    `;
}

function toggleCollapse(id) {
    const el = document.getElementById(id);
    el.style.display = el.style.display === "block" ? "none" : "block";
}

async function fetchRecommendation() {
    const userIdInput = document.getElementById("userIdInput");
    const userId = userIdInput.value.trim();
    const output = document.getElementById("output");
    const feedbackContainer = document.getElementById("feedbackContainer");

    if (!userId) {
        output.innerHTML = "<p>Please enter a user ID</p>";
        feedbackContainer.style.display = "none";
        return;
    }

    output.innerHTML = "<p>Loading...</p>";
    feedbackContainer.style.display = "none";
    currentUserId = null; // Reset current user

    try {
        const res = await fetch(`${API_BASE_URL}/mf/recommendations/${userId}`);
        if (!res.ok) throw new Error("Failed to fetch");
        const data = await res.json();

        // Store the user ID for feedback submission
        currentUserId = userId;

        const userFunds = data.recommendation.user_fund_details;
        const recs = data.recommendation.recommendations;
        const ranking = data.recommendation.ranking;

        output.innerHTML = `<h2>User Fund Details</h2>`;

        // ---------- USER FUNDS (COLLAPSIBLE) ----------
        userFunds.forEach(fund => {
            const details = `
                <p><b>Category:</b> ${fund.category}</p>
                <p><b>NAV:</b> ${fund.nav}</p>
                <p><b>AUM:</b> ${fund.aum}</p>

                <h4>Returns</h4>
                <p><b>1Y:</b> ${fund.returns["1Y"]}</p>
                <p><b>3Y:</b> ${fund.returns["3Y"]}</p>
                <p><b>5Y:</b> ${fund.returns["5Y"]}</p>

                <p><b>Risk:</b> ${fund.risk_level}</p>
                <p><b>URL:</b> <a href="${fund.resource_url}" target="_blank">${fund.resource_url}</a></p>
            `;

            output.innerHTML += createCollapsibleCard(fund.name, details);
        });

        // ---------- RECOMMENDATIONS IN RANK ORDER ----------
        output.innerHTML += `<h2>Recommendations (Ranked)</h2>`;

        ranking.forEach((fundName, rankIndex) => {
            const rec = recs.find(r => r.name === fundName);
            if (!rec) return;

            const details = `
                <p><b>Category:</b> ${rec.category}</p>
                <p><b>NAV:</b> ${rec.nav}</p>
                <p><b>AUM:</b> ${rec.aum}</p>

                <h4>Returns</h4>
                <p><b>1Y:</b> ${rec.returns["1Y"]}</p>
                <p><b>3Y:</b> ${rec.returns["3Y"]}</p>
                <p><b>5Y:</b> ${rec.returns["5Y"]}</p>

                <h4>Pros</h4>
                <p>${rec.pros}</p>

                <h4>Cons</h4>
                <p>${rec.cons}</p>

                <p><b>Risk:</b> ${rec.risk_level}</p>
                <p><b>URL:</b> <a href="${rec.resource_url}" target="_blank">${rec.resource_url}</a></p>
            `;

            output.innerHTML += createCollapsibleCard(rec.name, details, rankIndex);
        });

        // Show feedback container on success (ID is now captured)
        feedbackContainer.style.display = "block";

    } catch (err) {
        output.innerHTML = "<p style='color:red;'>Error fetching data (User might not exist or backend is down).</p>";
    }
}

async function submitFeedback() {
    const feedbackText = document.getElementById("feedbackText").value;
    const msg = document.getElementById("feedbackMessage");

    // We use currentUserId which was set during fetch
    if (!currentUserId) {
        msg.style.color = "red";
        msg.innerText = "Error: No active user session. Please fetch data first.";
        return;
    }

    if (!feedbackText) {
        msg.style.color = "red";
        msg.innerText = "Please enter feedback.";
        return;
    }

    try {
        const res = await fetch(`${API_BASE_URL}/mf/feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: currentUserId, feedback: feedbackText })
        });

        if (res.ok) {
            msg.style.color = "green";
            msg.innerText = "Feedback submitted successfully! It will be used for your next recommendation.";
            document.getElementById("feedbackText").value = ""; // clear input
        } else {
            throw new Error("Failed");
        }
    } catch (err) {
        msg.style.color = "red";
        msg.innerText = "Error submitting feedback.";
    }
}
