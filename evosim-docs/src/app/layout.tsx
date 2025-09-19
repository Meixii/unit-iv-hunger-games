import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { SidebarProvider, SidebarInset } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { PageNavigationWrapper } from "@/components/page-navigation-wrapper";
import { RightSidebar } from "@/components/right-sidebar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "EvoSim Documentation",
  description: "Evolve or Perish: AI-Driven Animal Survival in a Neural Network Battle Royale",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <SidebarProvider>
          <AppSidebar />
          <SidebarInset>
            <div className="flex-1 space-y-4 p-4 md:p-8 pt-6">
              <div className="flex gap-8 max-w-7xl mx-auto">
                <div className="flex-1 min-w-0">
                  {children}
                  <PageNavigationWrapper />
                </div>
                <RightSidebar />
              </div>
            </div>
          </SidebarInset>
        </SidebarProvider>
      </body>
    </html>
  );
}
