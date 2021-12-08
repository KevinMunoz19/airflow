
CREATE TABLE test.conf(
    id int primary key auto_increment,
    state varchar(256),
    country varchar(256),
    lat decimal(20,5),
    lon decimal(20,5),
    value int,
    year int,
    month int,
    day int,
    weekday int,
    date_d date
);

CREATE TABLE test.recovered(
    id int primary key auto_increment,
    state varchar(256),
    country varchar(256),
    lat decimal(20,5),
    lon decimal(20,5),
    value int,
    year int,
    month int,
    day int,
    weekday int,
    date_d date
);

CREATE TABLE test.deaths(
    id int primary key auto_increment,
    state varchar(256),
    country varchar(256),
    lat decimal(20,5),
    lon decimal(20,5),
    value int,
    year int,
    month int,
    day int,
    weekday int,
    date_d date
);