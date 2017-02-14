create materialized view clean_tweets
as
(select
(regexp_replace(status::text, '\\u0000', '', 'g'))::json as status
from raw_tweets);

drop materialized view if exists tweets;
create materialized view tweets
as
(select
status->'id' as tweet_id
,status->'user'->'id' as user_id
,status->'lang' as language
,status->'retweet_count' as retweets
from clean_tweets);

create materialized view tweets_hashtags
as
(select
status->'id' as tweet_id
,json_array_elements(status->'entities'->'hashtags')->'text' as hashtag
from clean_tweets
);

create materialized view users
as
(select
user_id
,followers
from
(select
cast(status->'user'->'id' as text) as user_id
,cast(cast(status->'user'->'followers_count' as text) as int) as followers
from clean_tweets) t1
group by
user_id
,followers);

create view hashtag_frequency
as
(select
hashtag::json
,hashtag_count
from
(select
lower(cast(hashtag as text)) as hashtag
,count(*) as hashtag_count
from tweets_hashtags
group by
lower(cast(hashtag as text))
) t1
order by
hashtag_count desc)
