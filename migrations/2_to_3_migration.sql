
ALTER TABLE media add column task uuid;
ALTER TABLE media add column submission uuid;
ALTER TABLE media add column project uuid;

ALTER TABLE projects add column anonymous_allowed bool;
ALTER TABLE projects add column platform varchar;
ALTER TABLE projects add column "group" uuid;

ALTER TABLE oauth_tokens add column expiry timestamp;
ALTER TABLE oauth_tokens add column token uuid;
ALTER TABLE oauth_tokens add column owner uuid;

ALTER TABLE users add column anonymous bool;

ALTER TABLE submissions add column response jsonb;

ALTER TABLE tasks add column part_of uuid;
