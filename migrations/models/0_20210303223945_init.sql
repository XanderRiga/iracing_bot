-- upgrade --
CREATE TABLE IF NOT EXISTS "base" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "car" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "iracing_id" VARCHAR(30) NOT NULL,
    "name" TEXT NOT NULL,
    "sku" TEXT
);
CREATE TABLE IF NOT EXISTS "driver" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "discord_id" VARCHAR(30) NOT NULL UNIQUE,
    "iracing_name" TEXT,
    "iracing_id" TEXT
);
CREATE TABLE IF NOT EXISTS "guild" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "discord_id" VARCHAR(30) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "irating" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "value" INT NOT NULL,
    "timestamp" TEXT NOT NULL,
    "category" SMALLINT NOT NULL  /* oval: 1\nroad: 2\ndirt_oval: 3\ndirt_road: 4 */,
    "driver_id" CHAR(36) NOT NULL REFERENCES "driver" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "license" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "license_number" INT NOT NULL,
    "timestamp" TEXT NOT NULL,
    "category" SMALLINT NOT NULL  /* oval: 1\nroad: 2\ndirt_oval: 3\ndirt_road: 4 */,
    "driver_id" CHAR(36) NOT NULL REFERENCES "driver" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "series" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "iracing_id" VARCHAR(30) NOT NULL UNIQUE,
    "name" TEXT NOT NULL,
    "category" SMALLINT NOT NULL  /* oval: 1\nroad: 2\ndirt_oval: 3\ndirt_road: 4 */
);
CREATE TABLE IF NOT EXISTS "season" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "iracing_id" VARCHAR(30) NOT NULL UNIQUE,
    "minimum_team_drivers" INT NOT NULL  DEFAULT 1,
    "start_time" TIMESTAMP NOT NULL,
    "end_time" TIMESTAMP NOT NULL,
    "season_quarter" INT,
    "season_year" INT,
    "is_fixed" INT,
    "is_official" INT,
    "active" INT,
    "series_id" CHAR(36) NOT NULL REFERENCES "series" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "stat" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "category" SMALLINT NOT NULL  /* oval: 1\nroad: 2\ndirt_oval: 3\ndirt_road: 4 */,
    "stat_type" SMALLINT NOT NULL  /* career: 0\nyearly: 1 */,
    "avg_incidents" TEXT,
    "total_laps" INT,
    "laps_led" INT,
    "laps_led_percentage" TEXT,
    "points_avg" INT,
    "points_club" INT,
    "poles" INT,
    "avg_start_pos" INT,
    "avg_finish_pos" INT,
    "total_starts" INT,
    "top_five_percentage" INT,
    "total_top_fives" INT,
    "win_percentage" INT,
    "total_wins" INT,
    "year" TEXT,
    "driver_id" CHAR(36) NOT NULL REFERENCES "driver" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "track" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "iracing_id" VARCHAR(30) NOT NULL,
    "name" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "seasoncombo" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "race_week" INT NOT NULL,
    "track_layout" TEXT,
    "time_of_day" INT,
    "track_id" CHAR(36) NOT NULL REFERENCES "track" ("id") ON DELETE CASCADE,
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "driver_guild" (
    "driver_id" CHAR(36) NOT NULL REFERENCES "driver" ("id") ON DELETE CASCADE,
    "guild_id" CHAR(36) NOT NULL REFERENCES "guild" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "favorite_series" (
    "guild_id" CHAR(36) NOT NULL REFERENCES "guild" ("id") ON DELETE CASCADE,
    "series_id" CHAR(36) NOT NULL REFERENCES "series" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "season_cars" (
    "season_id" CHAR(36) NOT NULL REFERENCES "season" ("id") ON DELETE CASCADE,
    "car_id" CHAR(36) NOT NULL REFERENCES "car" ("id") ON DELETE CASCADE
);
