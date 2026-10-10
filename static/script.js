async function checkURL() {

    const urlInput = document.getElementById("urlInput");

    const result = document.getElementById("result");

    const loading = document.getElementById("loading");

    const url = urlInput.value.trim();


    if (url === "") {

        result.innerHTML =
            `<div class="result-card">
                ⚠️ Please enter a URL.
             </div>`;

        return;
    }


    result.innerHTML = "";

    loading.style.display = "block";


    try {

        const response = await fetch("/predict", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })

        });


        const data = await response.json();


        loading.style.display = "none";


        if (data.error) {

            result.innerHTML =
                `<div class="result-card">
                    ⚠️ ${data.error}
                 </div>`;

            return;
        }


        let icon;

        if (data.result === "Phishing") {

            icon = "🚨";

        } else {

            icon = "🛡️";

        }


        result.innerHTML =

            `<div class="result-card">

                <h2>
                    ${icon} ${data.result}
                </h2>

                <p>
                    ${data.url}
                </p>

                <p class="confidence">
                    AI Confidence: ${data.confidence}%
                </p>

            </div>`;


        // Display URL analysis

        if (data.features) {

            document.getElementById("url-length").innerText =
                data.features.url_length + " characters";


            document.getElementById("https-status").innerText =
                data.features.https
                    ? "Secure"
                    : "Not Secure";


            document.getElementById("ip-status").innerText =
                data.features.has_ip
                    ? "Detected"
                    : "Not Detected";


            document.getElementById("suspicious-status").innerText =
                data.features.suspicious_words +
                " detected";

        }


    } catch (error) {

        loading.style.display = "none";

        result.innerHTML =
            `<div class="result-card">
                ❌ Unable to analyze URL.
             </div>`;

        console.error(error);
    }
}