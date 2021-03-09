-- upgrade --
ALTER TABLE "league" ADD COLUMN "name" TEXT;
-- downgrade --
ALTER TABLE "league" DROP COLUMN "name" TEXT;
