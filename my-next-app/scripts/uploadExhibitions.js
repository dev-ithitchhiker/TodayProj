import { initializeApp } from 'firebase/app';
import { getFirestore, collection, setDoc, doc } from 'firebase/firestore';

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
const db = getFirestore(app);

// Example exhibition data with specified document IDs
const exhibitions = [
    {
        id: "exhibition1",
        title: "Exhibition 1",
        date: "2025-03-01",
        location: "Location 1",
        image: "https://example.com/image1.jpg"
    },
    {
        id: "exhibition2",
        title: "Exhibition 2",
        date: "2025-03-01",
        location: "Location 2",
        image: "https://example.com/image2.jpg"
    },
    {
        id: "exhibition3",
        title: "Exhibition 3",
        date: "2025-03-01",
        location: "Location 3",
        image: "https://example.com/image3.jpg"
    }
];

// Function to upload exhibition data
async function uploadExhibitions() {
    try {
        const collectionRef = collection(db, "exhibitions");
        for (const exhibition of exhibitions) {
            const docRef = doc(collectionRef, exhibition.id);
            await setDoc(docRef, exhibition);
            console.log(`Uploaded: ${exhibition.title}`);
        }
        console.log("All exhibitions uploaded successfully.");
    } catch (error) {
        console.error("Error uploading exhibitions:", error);
    }
}

// Run the upload function
uploadExhibitions();