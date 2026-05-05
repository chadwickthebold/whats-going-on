import { EventResponse, PaginatedResponse } from "./types";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchEvents(): Promise<EventResponse[]> {
  const res = await fetch(`${API_URL}/events?limit=100`);
  if (!res.ok) throw new Error(`Failed to fetch events: ${res.status}`);
  const data: PaginatedResponse<EventResponse> = await res.json();
  return data.items;
}
