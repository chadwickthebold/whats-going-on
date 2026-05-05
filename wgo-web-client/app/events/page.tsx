"use client";

import { useEffect, useState } from "react";
import { fetchEvents } from "@/lib/api";
import { EventResponse } from "@/lib/types";
import EventCard from "@/components/EventCard";

export default function EventsPage() {
  const [events, setEvents] = useState<EventResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchEvents()
      .then(setEvents)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <main className="max-w-2xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-semibold text-gray-900 mb-6">
        Upcoming Events
      </h1>

      {loading && <p className="text-gray-500">Loading events...</p>}

      {error && (
        <p className="text-red-600">Failed to load events: {error}</p>
      )}

      {!loading && !error && events.length === 0 && (
        <p className="text-gray-500">No upcoming events found.</p>
      )}

      {!loading && !error && events.length > 0 && (
        <div className="flex flex-col gap-3">
          {events.map((event) => (
            <EventCard key={event.id} event={event} />
          ))}
        </div>
      )}
    </main>
  );
}
