"use client"; // Add this directive at the top of the file

// To install the necessary libraries, run the following commands:
// npm install firebase
// npm install next

import { useState, useEffect } from "react";
import { db } from "../firebase"; // Update this line
import { collection, query, where, getDocs } from "firebase/firestore";
import Link from "next/link";

export default function Home() {
  const [exhibitions, setExhibitions] = useState([]);

  useEffect(() => {
    const fetchExhibitions = async () => {
      try {
        const today = new Date().toISOString().split("T")[0];
        const q = query(collection(db, "exhibitions"), where("date", "==", today));
        const querySnapshot = await getDocs(q);
        const data = querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
        console.log("Exhibitions fetched:", data);
        setExhibitions(data);

      } catch (error) {
        console.error("Error fetching exhibitions:", error);
      }
    };
    fetchExhibitions();
  }, []);

  return (

    <div className="min-h-screen flex flex-col justify-between bg-gray-100">
      <main className="p-4">
        <h1 className="text-2xl font-bold text-center mb-4">오늘의 추천 전시회</h1>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {exhibitions.length > 0 ? (
            exhibitions.map(exhibition => (
              <div key={exhibition.id} className="bg-white p-4 rounded-lg shadow-md">
                <img src={exhibition.image} alt={exhibition.title} className="w-full h-48 object-cover rounded-md" />
                <h2 className="text-lg font-semibold mt-2">{exhibition.title}</h2>
                <p className="text-gray-600">{exhibition.location}</p>
                <Link href={`/exhibition/${exhibition.id}`} className="text-blue-500 mt-2 inline-block">
                  자세히 보기
                </Link>
              </div>
            ))
          ) : (
            <p className="text-center text-gray-500">오늘의 전시회 정보가 없습니다.</p>
          )}
        </div>
      </main>
      <nav className="fixed bottom-0 left-0 w-full bg-white shadow-md flex justify-around p-3">
        <Link href="/" className="text-gray-700">홈</Link>
        <Link href="/categories" className="text-gray-700">카테고리</Link>
      </nav>
    </div>
  );
}
