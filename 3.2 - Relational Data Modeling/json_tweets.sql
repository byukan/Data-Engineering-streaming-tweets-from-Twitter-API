

DROP MATERIALIZED VIEW IF EXISTS tweets;

CREATE MATERIALIZED VIEW tweets as
SELECT CAST((regexp_replace(CAST(status AS text), '\\u0000', '', 'g')) AS json) ->> 'id' AS tweeter_id,
CAST(json_array_elements(CAST((regexp_replace(CAST(status AS text), '\\u0000', '', 'g')) as json) -> 'entities' -> 'hashtags') -> 'text' AS text) AS raw_hashtag,
LOWER(CAST(json_array_elements(CAST((regexp_replace(CAST(status AS text), '\\u0000', '', 'g')) as json) -> 'entities' -> 'hashtags') -> 'text' AS text)) AS normalized_hashtag
FROM raw_tweets
limit 10;



select json_array_elements(status->'entities'->'hashtags')->'text' from raw_tweets
where status->'entities'->'hashtags' is not null
limit 10000;


select json_array_elements(status->'entities'->'hashtags')->'text' from raw_tweets
where status->'entities'->'hashtags' is not null
limit 10000;

select count(1) from raw_tweets;
