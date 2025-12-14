 drop database Expense_Data;
create database Expense_Data;
use Expense_Data;
create table Expenses(
Id int auto_increment primary key,
Date date ,
Amount decimal,
Category char(25),
Note varchar(225)
);
select * from expenses;
