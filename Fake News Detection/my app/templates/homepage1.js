// Import auth service from your config and auth functions
import { auth } from './config.js'; 
import { onAuthStateChanged, signOut } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-auth.js";

// --- Gemini API Configuration ---
// Leave as-is. The platform provides the key.
const apiKey = " "; 
const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-09-2025:generateContent?key=${apiKey}`;

// --- DOM Elements ---
const userDisplay = document.getElementById('user-display');
const logoutButton = document.getElementById('logout-button');
const articleForm = document.getElementById('article-form');
const articleTextarea = document.getElementById('article-text');
const analyzeButton = document.getElementById('analyze-button');
const resultsContainer = document.getElementById('results-container');
const loadingSpinner = document.getElementById('loading-spinner');
const apiError = document.getElementById('api-error');
const resultsContent = document.getElementById('results-content');
const resultVerdict = document.getElementById('result-verdict');
const resultConfidence = document.getElementById('result-confidence');
const resultBias = document.getElementById('result-bias');
const resultExplanation = document.getElementById('result-explanation');

// --- 1. Authentication Check (Protected Route) ---
onAuthStateChanged(auth, (user) => {
    if (user) {
        // User is signed in.
        
        // --- NEW LOGIC FOR DISPLAY NAME ---
        let displayName = user.displayName || user.email; // Fallback to email
        
        // Check if the name is an email, and if so, split it
        const atIndex = displayName.indexOf('@');
        if (atIndex !== -1) {
            displayName = displayName.substring(0, atIndex); // Get part before '@'
        }
        
        // Capitalize the first letter for a cleaner look
        displayName = displayName.charAt(0).toUpperCase() + displayName.slice(1);
        
        userDisplay.textContent = displayName;
        // --- END OF NEW LOGIC ---

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
        window.location.href = 'login.html'; // Redirect to login after signout
    } catch (error) {
        console.error("Sign out error:", error);
    }
});

// --- 3. Article Analysis Form Logic ---
articleForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent form from reloading the page
    const article = articleTextarea.value;

    if (!article.trim()) {
        displayError("Please paste an article to analyze.");
        return;
    }

    // --- Set UI to Loading State ---
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

        // 
        const payload = {
            contents: [{ parts: [{ text: userPrompt }] }],
            systemInstruction: {
                parts: [{ text: systemPrompt }]
            },
        };

        // --- Make the API Call ---
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

        // Robustly parse the JSON (in case the model adds "```json" tags)
        const jsonMatch = text.match(/\{[\s\S]*\}/);
        if (!jsonMatch) {
            throw new Error("The API returned an invalid JSON format.");
        }

        const data = JSON.parse(jsonMatch[0]);
        displayResults(data);

    } catch (error) {
        console.error("Analysis error:", error);
        displayError(`An error occurred: ${error.message}`);
    } finally {
        // --- Reset UI from Loading State ---
        setLoadingState(false);
    }
});

// --- Helper Functions ---

function setLoadingState(isLoading) {
    analyzeButton.disabled = isLoading;
    analyzeButton.textContent = isLoading ? "Analyzing..." : "Analyze Article";
    resultsContainer.style.display = "block";
    
    if (isLoading) {
        loadingSpinner.style.display = "block";
        apiError.textContent = "";
        resultsContent.style.display = "none";
    } else {
        loadingSpinner.style.display = "none";
    }
}

function displayError(message) {
    apiError.textContent = message;
    resultsContent.style.display = "none";

    // Play animation
    apiError.style.animation = 'slideUp 0.5s ease-out forwards';
}

function displayResults(data) {
    // Clear any previous errors
    apiError.textContent = "";
    resultsContent.style.display = "block";

    // Play animation
    resultsContent.style.animation = 'slideUp 0.5s ease-out forwards';

    // Populate the fields
    resultVerdict.textContent = data.verdict || "N/A";
    resultConfidence.textContent = `${data.confidence || 0}%`;
    resultBias.textContent = data.bias || "N/A";
    resultExplanation.textContent = data.explanation || "No explanation provided.";

    // Add styling based on verdict
    resultVerdict.className = ""; // Clear old classes
    if (data.verdict === "Fake") {
        resultVerdict.classList.add("verdict-fake");
    } else if (data.verdict === "Real") {
        resultVerdict.classList.add("verdict-real");
    } else {
        resultVerdict.classList.add("verdict-uncertain");
    }
}
