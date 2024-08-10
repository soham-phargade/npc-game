// firebase-config.js
import { initializeApp } from 'firebase/app';
import { getAnalytics } from 'firebase/analytics';

// Your Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA13UcUYVermzwm5XHbN-DkLxkHiav7zXA",
  authDomain: "reverse-turing-test-game.firebaseapp.com",
  projectId: "reverse-turing-test-game",
  storageBucket: "reverse-turing-test-game.appspot.com",
  messagingSenderId: "180613192932",
  appId: "1:180613192932:web:841492ed3ad8d28852a0f1",
  measurementId: "G-G0Q283C3WL"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

export { app, analytics };
