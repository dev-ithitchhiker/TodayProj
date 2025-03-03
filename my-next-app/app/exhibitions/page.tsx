"use client";

import { useState, useEffect } from "react";
import { db } from "../../firebase";
import { collection, query, where, getDocs } from "firebase/firestore";
import { retryWithExponentialBackoff } from "../../utils/retry";

export default function Exhibitions() {
    const [exhibitions, setExhibitions] = useState([]);
    const [expandedExhibition, setExpandedExhibition] = useState(null);

    useEffect(() => {
        const fetchExhibitions = async () => {
            try {
                const today = new Date().toISOString().split("T")[0];
                // Modified query to use range: startDate <= today <= endDate
                const q = query(
                    collection(db, "exhibitions"),
                    where("startDate", "<=", today),
                    where("endDate", ">=", today)
                );
                console.log("Query created:", q); // Log query creation
                const querySnapshot = await retryWithExponentialBackoff(() => getDocs(q));
                const data = querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
                console.log("Exhibitions fetched:", data); // Log fetched data
                setExhibitions(data);
            } catch (error) {
                console.error("Error fetching exhibitions:", error);
            }
        };
        fetchExhibitions();
    }, []);

    const toggleExhibition = (id) => {
        setExpandedExhibition(expandedExhibition === id ? null : id);
    };

    return (
        <div className="flex flex-col px-4 py-4">
            {/* Flexible scrollable container with small top margin */}
            <div className="flex-1 overflow-y-auto mt-2 pb-20">
                <div className="grid gap-6 grid-cols-1 md:grid-cols-2">
                    {exhibitions.length > 0 ? (
                        exhibitions.map(exhibition => (
                            <div
                                key={exhibition.id}
                                className="bg-white p-6 rounded-lg shadow-md transform transition duration-300 hover:scale-105"
                                onClick={() => toggleExhibition(exhibition.id)}
                            >
                                <h2 className="text-xl font-semibold mb-3 text-center text-black">
                                    {exhibition.title || "제목 없음"}
                                </h2>
                                <div className="w-full h-64 overflow-hidden rounded-md mb-3">
                                    <img
                                        src={exhibition.image || "https://via.placeholder.com/300x200"}
                                        alt={exhibition.title || "이미지"}
                                        className="w-full h-full object-cover"
                                    />
                                </div>
                                <p className="text-gray-600 text-center">
                                    {exhibition.location || "위치 정보 없음"}
                                </p>
                                {expandedExhibition === exhibition.id && (
                                    <div className="mt-4">
                                        <p className="text-gray-600">
                                            {exhibition.description || "설명 없음"}
                                        </p>
                                        <p className="text-gray-600">
                                            시작 날짜: {exhibition.startDate || "정보 없음"}
                                        </p>
                                        <p className="text-gray-600">
                                            종료 날짜: {exhibition.endDate || "정보 없음"}
                                        </p>
                                    </div>
                                )}
                            </div>
                        ))
                    ) : (
                        <p className="text-center text-gray-500">오늘의 전시회 정보가 없습니다.</p>
                    )}
                </div>
            </div>
        </div>
    );
}
