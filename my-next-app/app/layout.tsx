import Link from "next/link";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({
  weight: ["400", "500", "700"],
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Today",
  description: "Today's recommendations",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className={`${inter.className} antialiased`}>
        {/* Updated main container without fixed header */}
        <div className="min-h-screen bg-gray-100">
          <div className="container mx-auto px-4 py-6">
            <main className="p-4">
              {children}
            </main>
          </div>
          <nav className="fixed bottom-0 left-0 w-full bg-white shadow-lg flex justify-around py-3 z-40">
            <Link href="/food" className="text-gray-700 hover:text-black">음식</Link>
            <Link href="/exhibitions" className="text-gray-700 hover:text-black">전시회</Link>
            <Link href="/" className="text-gray-700 hover:text-black">홈</Link>
            <Link href="/products" className="text-gray-700 hover:text-black">물건</Link>
            <Link href="/news" className="text-gray-700 hover:text-black">이슈</Link>
          </nav>
        </div>
      </body>
    </html>
  );
}
