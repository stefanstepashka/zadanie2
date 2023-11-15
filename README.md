# zadanie2

Задание 1:

Документация API
```
POST /upload: Загрузите файл JSON или YML формата
POST /select-methods: Выберите и сохраните методы из анализированного файла.
```

Задание 2:

```
Запрос SQL
CREATE TABLE sick_patients (
user_id INT,
dt_start DATE,
dt_end DATE
);
INSERT INTO sick_patients (user_id, dt_start, dt_end) VALUES
(1, '2023-09-15', '2023-10-15'),
(2, '2023-10-10', '2023-10-25'),
(3, '2023-10-27', '2023-11-05');
SELECT a.user_id,
EXISTS (
SELECT 1
FROM sick_patients b
WHERE a.user_id != b.user_id
AND a.dt_start <= b.dt_end
AND a.dt_end >= b.dt_start
) AS overlap
FROM sick_patients a;
```
