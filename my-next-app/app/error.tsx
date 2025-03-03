"use client";
import { useEffect } from "react";

export default function GlobalError({
    error,
    reset,
}: {
    error: Error;
    reset: () => void;
}) {
    useEffect(() => {
        console.error("Unhandled error caught:", error);
    }, [error]);

    return (
        <html>
            <head>
                <title>Error</title>
            </head>
            <body className="flex items-center justify-center min-h-screen bg-gray-100">
                <div className="p-4 bg-white rounded-lg shadow-md text-center">
                    <h2 className="text-2xl font-bold mb-2">Something went wrong!</h2>
                    <p className="mb-4">{error.message}</p>
                    {/* Display error stack for debugging */}
                    <pre className="text-left text-xs text-gray-600 overflow-auto max-h-40">
                        {error.stack}
                    </pre>
                    <button
                        onClick={() => reset()}
                        className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                    >
                        Try again
                    </button>
                </div>
            </body>
        </html>
    );
}
