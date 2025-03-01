// firebase.ts
import { initializeApp } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
    apiKey: "AIzaSyD-8n8mMjVfYyO4hP1b2WQpZxg",
    authDomain: "myapp.firebaseapp.com",
    projectId: "myapp",
    storageBucket: "myapp.appspot.com",
    messagingSenderId: "1234567890",
    appId: "1:1234567890:web:0123456789"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore
const db = getFirestore(app);
export { db };
