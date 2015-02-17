drop table if exists users;
create table users (
  id integer primary key autoincrement,
  email text not null,
  password text not null,
  first_name text not null,
  last_name text not null,
  unique (email)
);

create table events (
  id integer primary key autoincrement,
  meetup_id integer not null,
  name text not null,
  event_url text not null,
  start_time integer not null,
  duration integer not null,
  attendee_count integer not null,
  unique(meetup_id)
);

create table volunteer_schedule (
  id integer primary key autoincrement,
  meetup_id integer not null,
  user_id integer not null,
  constraint unq unique (meetup_id, user_id)
);