// Import the auth service from your config file
import { auth } from './config.js';
import { 
    signInWithEmailAndPassword,
    onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/9.15.0/firebase-auth.js";

const loginForm = document.getElementById('login-form');
const loginEmail = document.getElementById('login-email');
const loginPassword = document.getElementById('login-password');
const loginError = document.getElementById('login-error');
const loginButton = document.getElementById('login-button');

// Redirect user to a 'dashboard' if they are already logged in
onAuthStateChanged(auth, (user) => {
    if (user) {
        // User is signed in, redirect them.
        console.log('User already logged in, redirecting...');
        window.location.href = 'homepage.html'; // Create this page
    }
});

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = loginEmail.value;
    const password = loginPassword.value;
    
    loginButton.disabled = true; // Disable button
    loginButton.textContent = "Logging in...";
    loginError.textContent = "";

    try {
        // 
        // Sign in the user with Firebase Auth
        const userCredential = await signInWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        
        console.log("Login successful:", user);
        
        // Redirect to a welcome/dashboard page
        window.location.href = 'homepage.html'; // You should create this page

    } catch (error) {
        console.error("Login error:", error.code, error.message);
        loginError.textContent = getFriendlyErrorMessage(error.code);
    } finally {
        loginButton.disabled = false; // Re-enable button
        loginButton.textContent = "Login";
    }
});

// Function to provide user-friendly error messages
function getFriendlyErrorMessage(errorCode) {
    switch (errorCode) {
        case 'auth/user-not-found':
        case 'auth/wrong-password':
            return 'Invalid email or password.';
        case 'auth/invalid-email':
            return 'Please enter a valid email address.';
        case 'auth/too-many-requests':
            return 'Access to this account has been temporarily disabled. Please reset your password or try again later.';
        default:
            return 'An error occurred. Please try again.';
    }
}