import type { Metadata } from "next";
import { Manrope } from "next/font/google";
import "./globals.css";

const manrope = Manrope({
  variable: "--font-manrope",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Wenit Solutions",
    template: "%s | Wenit Solutions",
  },
  description: "Strategic Talent Architecture across recruitment, staffing, and payroll.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`dark ${manrope.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col bg-background text-on-surface">
        {children}
      </body>
    </html>
  );
}
