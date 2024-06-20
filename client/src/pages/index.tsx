import { Inter as FontSans } from "next/font/google";

import { cn } from "@/lib/utils";

import { Button } from "../components/ui/button";

const fontSans = FontSans({
  subsets: ["latin"],
  variable: "--font-sans",
});

export default function Home() {
  return (
    <main
      className={cn(
        "flex min-h-screen flex-col items-center gap-4 p-24 font-sans",
        fontSans.variable,
      )}
    >
      <h1 className="text-3xl text-primary">Test title</h1>
      <Button>Click me to do nothing</Button>
    </main>
  );
}
