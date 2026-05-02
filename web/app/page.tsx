import Link from "next/link";

export default function Home() {
  return (
    <main className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-semibold text-gray-900 mb-2">
        What&apos;s Going On
      </h1>
      <p className="text-gray-500 mb-6">
        Track upcoming events across NYC cultural venues.
      </p>
      <Link
        href="/events"
        className="inline-block bg-gray-900 text-white text-sm font-medium px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
      >
        View upcoming events
      </Link>
    </main>
  );
}
