import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { ThemeProvider } from "@/components/ThemeProvider";
import { Navigation } from "@/components/Navigation";

const inter = Inter({ 
  subsets: ["latin"],
  variable: "--font-inter",
});

export const metadata: Metadata = {
  title: "Pulse - Solana Insights",
  description: "Detecting emerging narratives on Solana before they become obvious",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <link 
          rel="stylesheet" 
          href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" 
        />
      </head>
      <body className={`${inter.variable} min-h-screen`}>
        <ThemeProvider>
          <div className="flex min-h-screen flex-col">
            <Navigation />
            <main className="flex-1 py-8 lg:py-12">
              <div className="mx-auto max-w-6xl px-6 lg:px-8">
                {children}
              </div>
            </main>
            <footer className="border-t py-8 no-print mt-auto">
              <div className="mx-auto max-w-6xl px-6 lg:px-8">
                <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                  <div className="flex items-center gap-3">
                    <svg width="24" height="24" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <defs>
                        <linearGradient id="footerLogoGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                          <stop offset="0%" stopColor="#6366f1" />
                          <stop offset="50%" stopColor="#a855f7" />
                          <stop offset="100%" stopColor="#ec4899" />
                        </linearGradient>
                      </defs>
                      {/* Outer ring */}
                      <circle cx="18" cy="18" r="16" stroke="url(#footerLogoGradient)" strokeWidth="2" fill="none" />
                      {/* Signal waves */}
                      <path d="M12 18C12 14.686 14.686 12 18 12" stroke="url(#footerLogoGradient)" strokeWidth="2" strokeLinecap="round" />
                      <path d="M8 18C8 12.477 12.477 8 18 8" stroke="url(#footerLogoGradient)" strokeWidth="2" strokeLinecap="round" opacity="0.7" />
                      <path d="M4 18C4 10.268 10.268 4 18 4" stroke="url(#footerLogoGradient)" strokeWidth="2" strokeLinecap="round" opacity="0.4" />
                      {/* Center dot */}
                      <circle cx="18" cy="18" r="3" fill="url(#footerLogoGradient)" />
                    </svg>
                    <span className="font-serif text-lg text-gradient">Pulse</span>
                  </div>
                  <div className="flex items-center gap-6 text-sm text-text-secondary">
                    <span>Solana Ecosystem Intelligence</span>
                    <span className="hidden sm:inline text-text-tertiary">|</span>
                    <span className="text-text-tertiary">Refreshed fortnightly</span>
                  </div>
                  <p className="text-xs text-text-tertiary">
                    Last updated: Feb 11, 2026
                  </p>
                </div>
              </div>
            </footer>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
