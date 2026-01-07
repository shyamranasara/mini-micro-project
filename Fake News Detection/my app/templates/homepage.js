// Import auth service from your config and auth functions
import { auth } from './config.js'; 
import { onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-auth.js";

// --- Gemini API Configuration ---
const apiKey = " "; // Leave as-is. Canvas will handle this.
const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;

// --- DOM Elements ---
const userDisplay = document.getElementById('user-display');
const logoutButton = document.getElementById('logout-button');
const articleForm = document.getElementById('article-form');
const articleTextarea = document.getElementById('article-text');
const analyzeButton = document.getElementById('analyze-button');
const resultsContainer = document.getElementById('results-container');
const loadingContainer = document.getElementById('loading-container'); // New loader
const apiError = document.getElementById('api-error');
const resultsContent = document.getElementById('results-content');
const resultVerdict = document.getElementById('result-verdict');
const resultConfidenceText = document.getElementById('result-confidence-text'); // New
const confidenceRadialBar = document.getElementById('confidence-radial-bar'); // New
const resultBias = document.getElementById('result-bias');
const resultExplanation = document.getElementById('result-explanation');

// --- 1. Authentication Check (Protected Route) ---
onAuthStateChanged(auth, (user) => {
    if (user) {
        // User is signed in.
        // Try to get displayName first (from signup), fallback to email
        let displayName = user.displayName || user.email;
        const atIndex = displayName.indexOf('@');
        
        // If it's an email, split it
        if (atIndex !== -1) {
            displayName = displayName.substring(0, atIndex);
        }
        
        // Capitalize first letter
        displayName = displayName.charAt(0).toUpperCase() + displayName.slice(1);
        userDisplay.textContent = displayName;
    } else {
        // No user is signed in. Redirect to login.
        console.log("No user found, redirecting to login.");
        window.location.href = 'login.html';
    }
});

// --- 2. Logout Button Logic ---
logoutButton.addEventListener('click', async () => {
    try {
        await signOut(auth);
        console.log("User signed out.");
        window.location.href = 'login.html';
    } catch (error) {
        console.error("Sign out error:", error);
    }
});

// --- 3. Article Analysis Form Logic ---
articleForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const article = articleTextarea.value;

    if (!article.trim()) {
        displayError("Input required. Please paste an article to analyze.");
        return;
    }

    setLoadingState(true);

    try {
        // --- Define the prompt and payload ---
        const systemPrompt = `You are a Fake News Detection AI.
Analyze the following article and determine if it is real, fake, or uncertain.

Respond strictly in JSON format as shown below:
{
  "verdict": "Real or Fake or Uncertain",
  "confidence": (0-100),
  "explanation": "Brief reasoning for your decision",
  "bias": "Detected bias (e.g., political, emotional, sensational, none)"
}`;

        const userPrompt = `ARTICLE:
"""
${article}
"""`;

        const payload = {
            contents: [{ parts: [{ text: userPrompt }] }],
            systemInstruction: {
                parts: [{ text: systemPrompt }]
            },
        };

        // --- Make the API Call ---
        // 
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }

        const result = await response.json();

        // --- Extract and Parse the JSON Response ---
        const text = result.candidates?.[0]?.content?.parts?.[0]?.text;
        if (!text) {
            throw new Error("The API returned an empty response.");
        }

        // Look for the JSON block within the response text
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        if (!jsonMatch) {
            throw new Error("The API returned an invalid JSON format.");
        }

        const data = JSON.parse(jsonMatch[0]);
        displayResults(data);

    } catch (error) {
        console.error("Analysis error:", error);
        displayError(`Analysis Failed: ${error.message}`);
    } finally {
        setLoadingState(false);
    }
});

// --- Helper Functions ---

function setLoadingState(isLoading) {
    analyzeButton.disabled = isLoading;
    // Update button text and icon based on loading state
    analyzeButton.innerHTML = isLoading ? 
        `<svg class="spinner" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line></svg> Analyzing...` 
        : `<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M10 10l-6 6m0 0l6-6m-6 6h18v-4"></path><path d="M14 14l6-6m0 0l-6 6m6-6H0v4"></path></svg> Initiate Analysis`;
    
    resultsContainer.style.display = "block"; // Show the container
    
    if (isLoading) {
        loadingContainer.style.display = "flex"; // Show loader
        apiError.textContent = "";
        resultsContent.style.display = "none"; // Hide old results
    } else {
        loadingContainer.style.display = "none"; // Hide loader
    }
}

function displayError(message) {
    resultsContainer.style.display = "block"; // Show container
    apiError.textContent = message;
    resultsContent.style.display = "none"; // Hide results
    apiError.style.display = "block"; // Show error message
}

function displayResults(data) {
    apiError.textContent = ""; // Clear error
    resultsContent.style.display = "block"; // Show results
    apiError.style.display = "none"; // Hide error

    // --- Populate Text Fields ---
    resultVerdict.textContent = data.verdict || "N/A";
    resultBias.textContent = data.bias || "N/A";
    resultExplanation.textContent = data.explanation || "No explanation provided.";

    // --- Update Verdict Color ---
    resultVerdict.className = ""; // Clear old classes
    if (data.verdict === "Fake") {
        resultVerdict.classList.add("verdict-fake");
    } else if (data.verdict === "Real") {
        resultVerdict.classList.add("verdict-real");
    } else {
        resultVerdict.classList.add("verdict-uncertain");
    }

    // --- Update Confidence Chart ---
    const confidence = parseInt(data.confidence, 10) || 0;
    resultConfidenceText.textContent = `${confidence}%`;

    // Calculate circumference and offset for the radial bar
    const radius = 54;
    const circumference = 2 * Math.PI * radius; // 339.29...
    const offset = circumference - (confidence / 100) * circumference;
    
    // Set the CSS property to animate the bar
    confidenceRadialBar.style.strokeDashoffset = offset;
}

// --- Dynamic Spinner Animation ---
// Inject the @keyframes rule for the button spinner dynamically
// This is necessary because it's not in the main style.css <head>
try {
    const styleSheet = document.styleSheets[0];
    // Check if the rule already exists to avoid duplication
    let ruleExists = false;
    for (let i = 0; i < styleSheet.cssRules.length; i++) {
        if (styleSheet.cssRules[i].name === 'spin') {
            ruleExists = true;
            break;
        }
    }

    if (!ruleExists) {
        styleSheet.insertRule(`
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
        `, style_sheet.cssRules.length);
        
        styleSheet.insertRule(`
            .spinner {
                animation: spin 1s linear infinite;
            }
        `, style_sheet.cssRules.length);
    }
} catch (e) {
    console.error("Could not inject spinner keyframes:", e);
}
