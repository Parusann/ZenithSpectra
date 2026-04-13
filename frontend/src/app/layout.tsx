import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import Navbar from "@/components/Navbar";
import GridBackground from "@/components/GridBackground";
import AmbientOrbs from "@/components/AmbientOrbs";
import Footer from "@/components/Footer";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "ZenithSpectra — See the full picture. Trust the source.",
  description:
    "AI-powered science intelligence platform tracking live developments in space exploration and frontier physics.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${jetbrainsMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-bg-primary text-text-primary font-sans">
        <AmbientOrbs />
        <GridBackground />
        <Navbar />
        <main className="relative z-10 flex-1 pt-16">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
