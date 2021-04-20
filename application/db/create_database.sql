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
    link_photo_1 varchar(200) not null unique,
    likes_count_photo_1 integer not null,
    link_photo_2 varchar(200) not null unique,
    likes_count_photo_2 integer not null,
    link_photo_3 varchar(200) not null unique,
    likes_count_photo_3 integer not null,
    );
