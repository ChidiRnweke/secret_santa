create table session {
    id serial primary key,
    created_at timestamp not null default now(),

}

create table user_assignments {
    id serial primary key,
    buys_for varchar(255) not null,
    buys_from varchar(255) not null,
    created_at timestamp not null default now(),
    session_id integer not null references session(id) on delete cascade,
}

