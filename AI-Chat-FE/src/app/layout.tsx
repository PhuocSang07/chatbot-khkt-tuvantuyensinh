import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

import { Toaster } from "@/components/ui/sonner";
import { ConvexClientProvider } from "@/providers/convex-client-provider";
import { ThemeProvider } from "@/providers/theme-provider";

export const metadata: Metadata = {
    title: "AI Chat ư| THPT UNG VĂN KHIÊM",
    description: "Hệ thống chatbot AI được xây dựng bởi THPT Ung Văn Khiêm",
};

const inter = Inter({
    subsets: ["latin"],
});

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en" suppressHydrationWarning>
            <body className={inter.className}>
                <ThemeProvider
                    attribute="class"
                    defaultTheme="dark"
                    enableSystem
                    disableTransitionOnChange
                >
                    <ConvexClientProvider>{children}</ConvexClientProvider>
                    <Toaster richColors theme="light" position="top-center" />
                </ThemeProvider>
            </body>
        </html>
    );
}
