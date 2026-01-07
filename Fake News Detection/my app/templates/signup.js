// Import auth and db (Firestore) services
import { auth, db } from './config.js'; 
import { createUserWithEmailAndPassword, updateProfile } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-auth.js";
import { setDoc, doc } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-firestore.js";

// Get DOM Elements
const signupForm = document.getElementById('signup-form');
const signupUsername = document.getElementById('signup-username');
const signupEmail = document.getElementById('signup-email');
const signupPhone = document.getElementById('signup-phone');
const signupPassword = document.getElementById('signup-password');
const signupConfirmPassword = document.getElementById('signup-confirm-password');
const signupError = document.getElementById('signup-error');
const signupButton = document.getElementById('signup-button');

signupForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Get all values
    const username = signupUsername.value;
    const email = signupEmail.value;
    const phone = signupPhone.value;
    const password = signupPassword.value;
    const confirmPassword = signupConfirmPassword.value;

    // --- 1. Client-Side Validation ---
    if (password !== confirmPassword) {
        signupError.textContent = "Passwords do not match.";
        return; // Stop the function
    }
    
    signupButton.disabled = true;
    signupButton.textContent = "Creating account...";
    signupError.textContent = ""; // Clear previous errors

    try {
        // --- 2. Create User in Firebase Auth ---
        const userCredential = await createUserWithEmailAndPassword(auth, email, password);
        const user = userCredential.user;
        console.log("Auth user created:", user.uid);

        // --- 3. Update Auth Profile (with username) ---
        // This saves the username to the main Auth profile
        await updateProfile(user, {
            displayName: username
        });

        // --- 4. Create User Document in Firestore ---
        // This saves all the *extra* data
        const userDocRef = doc(db, "users", user.uid);
        await setDoc(userDocRef, {
            uid: user.uid,
            username: username,
            email: email,
            phone: phone
        });
        
        console.log("User data saved to Firestore.");

        // --- 5. Success and Redirect ---
        alert("Account created successfully! Please log in.");
        window.location.href = 'login.html'; // Redirect to login page

    } catch (error) {
        console.error("Signup error:", error.code, error.message);
        signupError.textContent = getFriendlyErrorMessage(error.code);
    } finally {
        signupButton.disabled = false;
        signupButton.textContent = "Sign Up";
    }
});

// Function to provide user-friendly error messages
function getFriendlyErrorMessage(errorCode) {
    switch (errorCode) {
        case 'auth/email-already-in-use':
            return 'This email address is already in use.';
        case 'auth/invalid-email':
            return 'Please enter a valid email address.';
        case 'auth/weak-password':
            return 'Password is too weak. It must be at least 6 characters.';
        default:
            return 'An error occurred. Please try again.';
    }
}