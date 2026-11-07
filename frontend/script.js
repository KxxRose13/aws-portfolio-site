document.getElementById("visitor-count").innerText = "Local test";

// AWS Serverless Visitor Counter

const visitorCounterApi =
    "https://duwnutlk8k.execute-api.us-east-2.amazonaws.com/visitor-count";

async function updateVisitorCount() {
    const visitorCountElement = document.getElementById("visitor-count");

    if (!visitorCountElement) {
        return;
    }

    try {
        const response = await fetch(visitorCounterApi);

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        visitorCountElement.textContent = data.count;

    } catch (error) {
        console.error("Visitor counter error:", error);
        visitorCountElement.textContent = "Unavailable";
    }
}

updateVisitorCount();