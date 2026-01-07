// Import functions
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/9.15.0/firebase-firestore.js";

// ----------------------------------------------------------------
// TODO: Add your web app's Firebase configuration
// ----------------------------------------------------------------
// ⬇️⬇️⬇️ PASTE YOUR CONFIG OBJECT HERE ⬇️⬇️⬇️
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: " ",
  authDomain: " ",
  databaseURL: " ",
  projectId: " ",
  storageBucket: " ",
  messagingSenderId: " ",
  appId: " ",
  measurementId:" " 
};
// ⬆️⬆️⬆️ PASTE YOUR CONFIG OBJECT HERE ⬆️⬆️⬆️
// ----------------------------------------------------------------

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Export the services you'll need
export const auth = getAuth(app);
export const db = getFirestore(app);