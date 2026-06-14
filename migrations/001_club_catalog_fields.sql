-- StudentSpot 001 - club catalog fields.
-- Use only for an existing database. Fresh deployments can run:
-- flask --app wsgi:app init-db --reset && flask --app wsgi:app seed-demo

ALTER TABLE majors ADD COLUMN slug VARCHAR(120);
CREATE UNIQUE INDEX IF NOT EXISTS ix_majors_slug ON majors (slug);

ALTER TABLE clubs ADD COLUMN slug VARCHAR(160);
ALTER TABLE clubs ADD COLUMN campus VARCHAR(80) NOT NULL DEFAULT 'lodz';
ALTER TABLE clubs ADD COLUMN guardian_name VARCHAR(255);
ALTER TABLE clubs ADD COLUMN website_url VARCHAR(500);
ALTER TABLE clubs ADD COLUMN tags_csv VARCHAR(600);
ALTER TABLE clubs ADD COLUMN suggested_rooms_csv VARCHAR(400);
ALTER TABLE clubs ADD COLUMN is_public BOOLEAN NOT NULL DEFAULT 1;
ALTER TABLE clubs ADD COLUMN is_featured BOOLEAN NOT NULL DEFAULT 0;
CREATE UNIQUE INDEX IF NOT EXISTS ix_clubs_slug ON clubs (slug);
CREATE INDEX IF NOT EXISTS ix_clubs_is_public ON clubs (is_public);
CREATE INDEX IF NOT EXISTS ix_clubs_is_featured ON clubs (is_featured);
