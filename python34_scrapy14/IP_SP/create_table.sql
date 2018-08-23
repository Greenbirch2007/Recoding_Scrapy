


create table proxy(
id int primary key auto_increment,
ip varchar(20) not null,
port varchar(20) not null,
type varchar(20) not null)
engine=InnoDB  charset=utf8;