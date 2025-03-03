// Import the functions you need from the SDKs you need
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCXlhqk-NvJU8rNzWT6dXUhVZbCpHQAVh4",
    authDomain: "today1990.firebaseapp.com",
    projectId: "today1990",
    storageBucket: "today1990.firebasestorage.app",
    messagingSenderId: "619877222403",
    appId: "1:619877222403:web:39161e5f42d4fa66db6636"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore
export const db = getFirestore(app);
