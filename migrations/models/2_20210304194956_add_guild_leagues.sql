-- upgrade --
CREATE TABLE "guild_leagues" ("guild_id" CHAR(36) NOT NULL REFERENCES "guild" ("id") ON DELETE CASCADE,"league_id" CHAR(36) NOT NULL REFERENCES "league" ("id") ON DELETE CASCADE);
-- downgrade --
DROP TABLE IF EXISTS "guild_leagues";
