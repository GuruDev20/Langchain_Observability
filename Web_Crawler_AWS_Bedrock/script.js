const API_ENDPOINT = import.meta.env.VITE_API_ENDPOINT;

const urlInput = document.getElementById("url");
const output = document.getElementById("output");
const button = document.getElementById("crawlBtn");

button.addEventListener("click", crawl);

async function crawl() {
    const url = urlInput.value.trim();

    if (!url) {
        output.textContent = "Please enter a URL.";
        return;
    }

    output.textContent = "Crawling...";

    try {
        const res = await fetch(API_ENDPOINT, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                message: `Crawl this URL: ${url}`,
            }),
        });

        const data = await res.json();
        output.textContent = data.reply || data.error || "No response received.";
    } catch (err) {
        output.textContent = "Request failed.";
    }
}
