import "@/styles/globals.css";

import type { Metadata } from "next";
import { Inter } from "next/font/google";

import Providers from "@/components/main/providers";

export const metadata: Metadata = {
  title: "Template - Please rename to project",
  description: "Home Page",
};

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <main className={`${inter.variable} text-soil-800 font-sans`}>
          <Providers>{children}</Providers>
        </main>
      </body>
    </html>
  );
}
