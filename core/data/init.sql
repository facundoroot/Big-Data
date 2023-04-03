CREATE TABLE public.employee (
    id int8 NOT NULL,
    name varchar(120) NOT NULL,
    salary int8 NOT NULL,
    CONSTRAINT emp_pk PRIMARY KEY (id)
);

WITH salary_list AS (
    SELECT '{1000, 2000, 5000}'::INT[] salary
)
INSERT INTO public.employee
(id, name, salary)
SELECT n, 'Employee ' || n as name, salary[1 + mod(n, array_length(salary, 1))]
FROM salary_list, generate_series(1, 100) as n

