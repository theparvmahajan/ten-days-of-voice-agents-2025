import { Button } from '@/components/livekit/button';

function AnimatedShoppingIcon() {
  return (
    <div className="relative mb-8">
      {/* Soft halo */}
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="h-28 w-28 rounded-full bg-emerald-200/40 blur-2xl" />
      </div>
      <div className="absolute inset-0 flex items-center justify-center">
        <div className="h-20 w-20 rounded-full bg-sky-200/60 blur-xl" />
      </div>

      {/* Main icon */}
      <div className="relative flex h-24 w-24 items-center justify-center rounded-3xl bg-gradient-to-br from-emerald-500 via-sky-500 to-indigo-500 shadow-lg animate-[float_3s_ease-in-out_infinite]">
        <span className="text-4xl">🛍️</span>
      </div>
    </div>
  );
}

function FeatureCard({
  title,
  description,
  badge,
}: {
  title: string;
  description: string;
  badge: string;
}) {
  return (
    <div className="group relative rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-1 hover:shadow-md">
      <div className="mb-2 inline-flex items-center gap-1 rounded-full bg-slate-100 px-2 py-1 text-xs font-medium text-slate-600">
        <span>{badge}</span>
      </div>
      <h3 className="text-base font-semibold text-slate-900 mb-1.5">
        {title}
      </h3>
      <p className="text-sm text-slate-600 leading-relaxed">
        {description}
      </p>
    </div>
  );
}

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ...props
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div
      className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-emerald-50"
      {...props}
    >
      <style jsx>{`
        @keyframes float {
          0%,
          100% {
            transform: translateY(0px);
          }
          50% {
            transform: translateY(-8px);
          }
        }
      `}</style>

      <section className="container mx-auto px-4 py-12 flex flex-col items-center text-center">
        {/* Hero icon */}
        <AnimatedShoppingIcon />

        {/* Small badge */}
        <div className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-4 py-1.5 text-xs font-semibold text-emerald-700 mb-5">
          <span className="inline-flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
          <span>AI Voice Shopping Assistant</span>
        </div>

        {/* Headline */}
        <h1 className="text-3xl md:text-5xl font-extrabold tracking-tight text-slate-900 mb-3 max-w-3xl">
          Shop Smarter Just by Talking
        </h1>

        {/* Subheadline */}
        <p className="text-base md:text-lg text-slate-600 max-w-2xl mb-8 leading-relaxed">
          Browse products, compare options and place your order — all through a natural
          voice conversation with your AI shopping companion.
        </p>

        {/* CTA button */}
        <Button
          onClick={onStartCall}
          className="group relative inline-flex items-center gap-2 rounded-full bg-slate-900 px-10 py-4 text-sm font-semibold text-white shadow-lg hover:bg-slate-800 hover:shadow-xl transition-all duration-200 mb-14"
        >
          <span className="text-lg">🎙️</span>
          <span>{startButtonText}</span>
          <span className="text-lg group-hover:translate-x-0.5 transition-transform">
            ➜
          </span>
        </Button>

        {/* How it works */}
        <div className="w-full max-w-5xl mb-12">
          <h2 className="text-2xl md:text-3xl font-bold text-slate-900 mb-2">
            How Voice Shopping Works
          </h2>
          <p className="text-sm md:text-base text-slate-600 mb-7 max-w-2xl mx-auto">
            Just speak naturally. Your assistant understands what you want, finds
            products that match, and helps you confirm and place the order.
          </p>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
            <FeatureCard
              badge="1"
              title="Start a Conversation"
              description='Say something like "Show me black hoodies" or "I need a coffee mug under ₹500".'
            />
            <FeatureCard
              badge="2"
              title="Browse Suggestions"
              description="The assistant reads out a few matching options with prices so you can compare quickly."
            />
            <FeatureCard
              badge="3"
              title="Refine & Decide"
              description='Ask follow-up questions, change sizes or colors, or say "tell me about the second one".'
            />
            <FeatureCard
              badge="4"
              title="Confirm Your Order"
              description='Say "place my order" when you are ready. The assistant summarizes your cart before checkout.'
            />
          </div>
        </div>

        {/* Quick categories / features */}
        <div className="w-full max-w-4xl rounded-3xl border border-slate-200 bg-white p-7 shadow-sm mb-10">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-5">
            <div className="text-left">
              <p className="text-xs font-semibold uppercase tracking-wide text-slate-500">
                What you can shop
              </p>
              <h3 className="text-xl font-bold text-slate-900">
                Curated basics for everyday use
              </h3>
            </div>
            <div className="flex flex-wrap items-center gap-2 justify-center md:justify-end">
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-700">
                ☕ Mugs
              </span>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-700">
                👕 T-Shirts
              </span>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-700">
                🧥 Hoodies
              </span>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-700">
                📦 Accessories
              </span>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-3 text-left text-sm text-slate-600">
            {[
              'Quality cotton tees from ₹799',
              'Premium hoodies from ₹1,799',
              'Everyday mugs from ₹299',
              'Multiple colors and sizes',
              'Simple, clean catalog — no clutter',
              'Voice-first experience for quick shopping',
            ].map((item, idx) => (
              <div key={idx} className="flex items-start gap-2">
                <span className="mt-0.5 text-emerald-500">●</span>
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Example voice commands */}
        <div className="w-full max-w-2xl rounded-2xl border border-slate-200 bg-slate-50 p-6 mb-10">
          <p className="text-xs font-semibold text-slate-500 mb-3">
            Try saying:
          </p>
          <div className="grid md:grid-cols-2 gap-3 text-left text-sm text-slate-700">
            <div className="rounded-lg bg-white border border-slate-200 px-3 py-2">
              <span className="text-xs text-slate-400">Example 1</span>
              <p>“Show me black hoodies under ₹1500.”</p>
            </div>
            <div className="rounded-lg bg-white border border-slate-200 px-3 py-2">
              <span className="text-xs text-slate-400">Example 2</span>
              <p>“I want a mug for office use.”</p>
            </div>
            <div className="rounded-lg bg-white border border-slate-200 px-3 py-2">
              <span className="text-xs text-slate-400">Example 3</span>
              <p>“Tell me more about the second option.”</p>
            </div>
            <div className="rounded-lg bg-white border border-slate-200 px-3 py-2">
              <span className="text-xs text-slate-400">Example 4</span>
              <p>“Add that in size medium and place my order.”</p>
            </div>
          </div>
        </div>

        {/* Trust strip */}
        <div className="flex flex-wrap items-center justify-center gap-4 text-xs text-slate-500 mb-6">
          <div className="flex items-center gap-2 rounded-full bg-white border border-slate-200 px-3 py-1">
            <span>🔒</span>
            <span>Secure shopping experience</span>
          </div>
          <div className="flex items-center gap-2 rounded-full bg-white border border-slate-200 px-3 py-1">
            <span>⭐</span>
            <span>Designed for clarity & speed</span>
          </div>
          <div className="flex items-center gap-2 rounded-full bg-white border border-slate-200 px-3 py-1">
            <span>⚡</span>
            <span>Low-friction voice ordering</span>
          </div>
        </div>
      </section>

      {/* Footer */}
      <div className="border-t border-slate-200 bg-white py-4">
        <p className="text-center text-xs text-slate-500">
          Powered by your AI voice assistant —{" "}
          <span className="font-medium text-slate-800">
            speak naturally, shop easily.
          </span>
        </p>
      </div>
    </div>
  );
};
