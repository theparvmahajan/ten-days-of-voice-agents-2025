interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const storeName = "VoiceShop";

  return (
    <>
      {/* Header */}
      <header className="fixed top-0 left-0 z-50 w-full border-b border-slate-200 bg-white/90 backdrop-blur-md">
        <nav className="container mx-auto px-4 sm:px-6 py-3 flex items-center justify-between">
          {/* Logo + Brand */}
          <a
            href="/"
            className="group flex items-center gap-3 transition-all duration-200"
          >
            <div className="relative">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-tr from-indigo-200 via-sky-200 to-emerald-200 blur-md opacity-70 group-hover:opacity-100 transition-opacity" />
              <div className="relative flex h-9 w-9 items-center justify-center rounded-2xl bg-gradient-to-tr from-indigo-500 via-sky-500 to-emerald-500 text-white text-lg font-semibold shadow-md group-hover:shadow-lg group-hover:-translate-y-0.5 transition-all">
                🛒
              </div>
            </div>

            <div className="flex flex-col">
              <span className="font-semibold text-lg text-slate-900">
                {storeName}
              </span>
              <span className="text-xs text-slate-500 font-medium">
                Voice Shopping Assistant
              </span>
            </div>
          </a>

          {/* Desktop right side */}
          <div className="hidden md:flex items-center gap-6">
            {/* AI Status */}
            <div className="flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
              <span className="inline-flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>AI Assistant Online</span>
            </div>

            {/* Quick stats */}
            <div className="hidden lg:flex items-center gap-4 text-xs text-slate-500">
              <div className="flex flex-col items-start">
                <span className="font-semibold text-slate-900">100+ products</span>
                <span>Curated catalog</span>
              </div>
              <span className="h-6 w-px bg-slate-200" />
              <div className="flex flex-col items-start">
                <span className="font-semibold text-slate-900">24/7</span>
                <span>Voice support</span>
              </div>
            </div>

            {/* Help */}
            <a
              href="#"
              className="text-sm text-slate-500 hover:text-slate-900 transition-colors font-medium"
            >
              Help &amp; Support
            </a>

            {/* Small “badge” */}
            <div className="hidden lg:flex items-center gap-2 rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-xs font-medium text-amber-800">
              <span>⭐</span>
              <span>Premium Experience</span>
            </div>
          </div>

          {/* Mobile badges */}
          <div className="flex md:hidden items-center gap-2">
            <div className="flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-700">
              <span className="inline-flex h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse" />
              <span>AI</span>
            </div>
            <div className="flex items-center gap-1.5 rounded-full border border-slate-200 bg-slate-50 px-3 py-1 text-xs font-medium text-slate-700">
              <span>🛍️</span>
              <span>Cart</span>
            </div>
          </div>
        </nav>
      </header>

      {/* Main content */}
      <main className="pt-16 min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50">
        {children}
      </main>

      {/* Simple bottom helper on mobile */}
      <div className="fixed bottom-0 left-0 right-0 z-40 md:hidden bg-white/95 backdrop-blur-md border-t border-slate-200 px-4 py-3">
        <p className="text-xs text-slate-600 text-center">
          💡 Try saying{" "}
          <span className="font-semibold text-slate-900">
            "Show me hoodies"
          </span>{" "}
          or{" "}
          <span className="font-semibold text-slate-900">
            "I need a coffee mug"
          </span>
        </p>
      </div>
    </>
  );
}
