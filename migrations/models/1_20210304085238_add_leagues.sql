-- upgrade --
CREATE TABLE IF NOT EXISTS "league" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "iracing_id" VARCHAR(30) NOT NULL
);;
CREATE TABLE IF NOT EXISTS "leagueseason" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "iracing_id" VARCHAR(30) NOT NULL,
    "name" TEXT NOT NULL,
    "active" INT NOT NULL,
    "league_points_system_description" TEXT,
    "league_points_system_name" TEXT,
    "league_points_system_id" VARCHAR(30),
    "league_id" CHAR(36) NOT NULL REFERENCES "league" ("id") ON DELETE CASCADE
);;
-- downgrade --
DROP TABLE IF EXISTS "league";
DROP TABLE IF EXISTS "leagueseason";
