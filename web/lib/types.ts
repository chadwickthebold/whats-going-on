export interface EventResponse {
  id: number;
  title: string;
  event_type: string | null;
  event_start_timestamp: string | null;
  source_url: string | null;
  venue_id: number | null;
}

export interface PaginatedResponse<T> {
  total: number;
  limit: number;
  offset: number;
  items: T[];
}
