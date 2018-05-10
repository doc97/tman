# SQL statements

Most of the queries are implemented with SQLAlchemy but a few are written with pure SQL.
I will not show trivial cases such as inserts or deletes.

Since my table names are capitalized they require `""` quotes around them and also the column
`order` requires them since it would otherwise be interpreted as a keyword.

### Getting tags for tasks

This is done by the following query:
```sql
SELECT "Task".id, "Tag".id, "Tag".name
FROM "Tag"
CROSS JOIN "TaskTag"
INNER JOIN "Task" ON
    "Task".id = "TaskTag".task_id AND
    "Tag".id = "TaskTag".tag_id 
```

```sql
SELECT "Tag".id, "Tag".name
FROM "Tag"
INNER JOIN "TaskTag" ON
    "TaskTag".task_id = [TASK_ID] AND
    "TaskTag".tag_id = "Tag".id
```

Important to note here is that `TASK_ID` is guaranteed to be an integer.

### Calculating the new order of a reordered task

If the task has been moved up, the `order` will decrease. If moved down, the `order` will increase.

By limiting the result I can then use the two first results as the tasks in between which the reordered
task should reside. By setting the order to be `(first.order + second.order) / 2` I can place the
reordered task in between the first and second result.

Task has been moved up:
```sql
SELECT *
FROM "Task"
WHERE
    "Task".account_id = [CURRENT_USER_ID] AND
    "Task".tasklist_id = "Task".tasklist_id AND
    "Task"."order" < [TASK_ORDER]
ORDER BY "Task"."order" DESC
LIMIT [OFFSET_AMOUNT]
```

Task has been moved down:
```sql
SELECT *
FROM "Task"
WHERE
    "Task".account_id = [CURRENT_USER_ID] AND
    "Task".tasklist_id = "Task".tasklist_id AND
    "Task"."order" > [TASK_ORDER]
ORDER BY "Task"."order" ASC
LIMIT [OFFSET_AMOUNT]
```

`CURRENT_USER_ID` = The current user's account ID
`TASK_ORDER` = The reordered task's old order
`OFFSET_AMOUNT` = The number of steps the task has been moved up or down in the list.

### Normal query for showing completed tasks in a particular tasklist
```sql
SELECT *
FROM "Task"
WHERE
    "Task".tasklist_id = [TASKLIST_ID] AND
    "Task".account_id = [CURRENT_USER_ID] AND
    "Task".is_completed = true
ORDER BY "Task"."order"
```
