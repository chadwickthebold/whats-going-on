interface EventTypeConfig {
  label: string;
  badgeClass: string;
}

const EVENT_TYPES: Record<string, EventTypeConfig> = {
  exhibition: { label: "Exhibition", badgeClass: "bg-purple-100 text-purple-800" },
  performance: { label: "Performance", badgeClass: "bg-blue-100 text-blue-800" },
  talk: { label: "Talk", badgeClass: "bg-green-100 text-green-800" },
  screening: { label: "Screening", badgeClass: "bg-orange-100 text-orange-800" },
  other: { label: "Other", badgeClass: "bg-gray-100 text-gray-800" },
};

const FALLBACK: EventTypeConfig = { label: "Event", badgeClass: "bg-gray-100 text-gray-800" };

export function getEventTypeConfig(eventType: string | null): EventTypeConfig {
  if (!eventType) return FALLBACK;
  return EVENT_TYPES[eventType] ?? FALLBACK;
}
