create table agents (
    id serial primary key,
    full_name varchar(100) not null,
    email varchar(100) unique not null,
    phone varchar(15),
    license_number varchar(50) unique not null,
    hire_date date not null,
    is_active boolean default true
);

create table clients (
    id serial primary key,
    full_name varchar(100) not null,
    email varchar(100) unique not null,
    phone varchar(15),
    client_type text check (client_type in ('buyer','seller','both')),
    created_at timestamp default current_timestamp
);

create table properties (
    id serial primary key,
    title text not null,
    description text,
    property_type text check (property_type in ('apartment','villa','plot','commercial')),
    price numeric(15,2),
    area_sqft numeric(10,2) check (area_sqft > 0),
    city varchar(50),
    locality varchar(100),
    status text check (status in ('available', 'sold', 'rented')),
    created_at timestamp default current_timestamp
);

create table listings (
    id serial primary key,
    property_id int references properties(id) on delete cascade,
    agent_id int references agents(id) on delete cascade,
    seller_id int references clients(id) On delete cascade,
    list_price numeric(15,2),
    expires_at timestamp default current_timestamp,
    status text check (status in('active', 'expired' , 'sold')),
    listed_at timestamp default current_timestamp
);

create table leads (
    id serial primary key,
    property_id int references properties(id) on delete cascade,
    agent_id int references agents(id) on delete cascade,
    client_id int references clients(id) on delete cascade,
    interest_level text check (interest_level in('low','medium','high')),
    created_at timestamp default current_timestamp,
    notes text
);

create table transactions (
    id serial primary key,
    listing_id int references listings(id)  on delete cascade,
    buyer_id int references clients(id)  on delete cascade,
    agent_id int references agents(id) on delete cascade,
    final_price numeric(15,2),
    transaction_date timestamp default current_timestamp,
    payment_mode text check (payment_mode in('cash','loan','cheque'))
);

create table interactions (
    id serial primary key,
    agent_id int references agents(id)  on delete cascade,
    client_id int references clients(id)  on delete cascade,
    interaction_type text check (interaction_type in('call', 'email', 'visit')),
    notes text,
    interacted_at timestamp default current_timestamp
);