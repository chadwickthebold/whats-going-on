import { EventResponse } from "@/lib/types";
import { getEventTypeConfig } from "@/lib/event-types";

export default function EventCard({ event }: { event: EventResponse }) {
  const typeConfig = getEventTypeConfig(event.event_type);

  const formattedDate = event.event_start_timestamp
    ? new Date(event.event_start_timestamp).toLocaleDateString("en-US", {
        weekday: "short",
        month: "short",
        day: "numeric",
        year: "numeric",
      })
    : null;

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:shadow-sm transition-shadow">
      <div className="flex items-start justify-between gap-4">
        <h2 className="text-base font-medium text-gray-900">{event.title}</h2>
        <span
          className={`shrink-0 text-xs font-medium px-2 py-1 rounded-full ${typeConfig.badgeClass}`}
        >
          {typeConfig.label}
        </span>
      </div>
      <div className="mt-2 flex items-center gap-4 text-sm text-gray-500">
        {formattedDate && <span>{formattedDate}</span>}
        {event.source_url && (
          <a
            href={event.source_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-600 hover:underline"
          >
            Source
          </a>
        )}
      </div>
    </div>
  );
}
