create table if not exists main_user (
    id serial primary key,
    user_id integer not null,
    first_name varchar(30) not null,
    last_name varchar(35) not null
    );

create table if not exists search_result (
    id serial primary key,
    user_id integer not null,
    owner_id integer not null,
    first_name varchar(20) not null,
    last_name varchar(35) not null
    );

create table if not exists sorted_data (
    owner_id integer not null,
    link_photo_1 varchar(400) not null,
    likes_count_photo_1 integer not null,
    link_photo_2 varchar(400) not null,
    likes_count_photo_2 integer not null,
    link_photo_3 varchar(400) not null,
    likes_count_photo_3 integer not null
    );

create table if not exists viewed_candidates (
    owner_id integer not null unique,
    name varchar(50) not null
    );

create table if not exists favorites (
    id serial primary key,
    owner_id integer not null unique,
    photo_link varchar(1500) not null
    );

create table if not exists ban_list (
    owner_id integer not null
    );
