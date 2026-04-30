-- Set up Venues
INSERT INTO venue (name,slug,address,website,organization_id,id) VALUES
	 ('Drawing Center','drawing-center','35 Wooster Street, New York, NY, 10013','https://drawingcenter.org/',NULL,1);


-- Set up data sources
INSERT INTO data_source (url,last_checked,venue_id,organization_id,id) VALUES
	 ('https://drawingcenter.org/exhibitions',NULL,1,NULL,1);

