import './globals.css';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const now = new Date().toLocaleString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    // hour: 'numeric',
    // minute: 'numeric',
    // second: 'numeric',
    hour12: true
  });

  return (
    <html lang="en">
      <head>
        <title>My Stock App</title>
      </head>
      <body className="bg-gray-100 font-sans flex flex-col min-h-screen">
        <header className="bg-blue-600 text-white shadow-md">
          <nav className="container mx-auto flex justify-between items-center p-4">
            <div className="text-xl font-bold">
              <a href="/" className="hover:text-gray-200 transition-colors">My Stock App</a>
            </div>
            <ul className="flex space-x-6 bg-blue-600 rounded-md py-1 px-2">
              <li>
                <a href="/" className="hover:bg-blue-500 px-4 py-2 rounded transition-colors text-white">
                  Home
                </a>
              </li>
              <li>
                <a href="/next-page" className="hover:bg-blue-500 px-4 py-2 rounded transition-colors text-white">
                  Dashboard
                </a>
              </li>
              <li>
                <a href="/report-generation" className="hover:bg-blue-500 px-4 py-2 rounded transition-colors text-white">
                  Report Generation
                </a>
              </li>
            </ul>
            <div className="text-sm">{now}</div>
          </nav>
        </header>
        <main className="flex-grow container mx-auto px-4 sm:px-6 md:px-8 py-6">
          {children}
        </main>
        <footer className="bg-gray-800 text-white text-center py-4 mt-8">
          <p>&copy; 2024 My Next.js App. All rights reserved.</p>
        </footer>
      </body>
    </html>
  );
}
