import "./globals.css";
import AppNavbar from "@/app/components/app-navbar";

export const metadata = {
  title: "Paravantis News - news.paravantis.org",
};

export default function RootLayout({children}) {
  return (
    <html lang="en">
    <body className="bg-gray-100">
      <AppNavbar/>
      {children}
    </body>
    </html>
  );
}
