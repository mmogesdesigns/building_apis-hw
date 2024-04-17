CREATE DATABASE	fitness_tracker;

use	fitness_tracker;

create table Members(
	member_id int auto_increment primary key,
    name varchar(100),
    email varchar(100),
    phone varchar(15),
    bench_amount int,
    membership_type varchar(30)
);

create table Dank_sesh(
	sesh_id int auto_increment primary key,
    date date,
    member_id int,
    workout_type varchar(50),
    foreign key (member_id) references members(member_id)
    
); 

insert into	Members (name, email, phone, bench_amount, membership_type)
values ("Goku", "songoku@gmail.com", "1234567890", 9001, "platinum");

insert	into Dank_sesh (date, member_id, workout_type)
values	("2024-04-10", 1, "strength");

select *
from dank_sesh;

select *
from members;