# CSVBase
This is a very, *very* nacsent project that's being built as a joke. A very dumb, very time consuming joke.

So, MongoDB- it uses JSON to store data. Well, this is like that, but it uses CSV. I'm lifting some of the design elements off of Google's BigTable, and might even steal Cassandra's approach to distributed architecture. The goal isn't to produce something that anyone would actually use, but that they *could*.

# Current Status
Currently, there's an in-memory only REPL that also appends to a commit log. There's no persistent storage, no schema tables, nothing like that.

You can run it in Python3. Note the dependencies, in requirements.txt.

```
python -m CSVBase.REPL
```

Currently supported commands, follow. Note that *in the REPL*, all commands must end with a ";". Quoted fields are accepted, and if you want to use a keyword inside of your data, you MUST quote the field. Type "quit" alone to exit the REPL.

## DDL
###Create Bucket
```
CREATE BUCKET <name> [WITH (KEY COLS <n>)]
```

Creates a new "bucket", the CSVBase equivalent to a table. The optional WITH KEY COLS clause specifies how many, if any columns, should be considered "keys". For some data manipulation operations, this value is significant. Should I expand this to a distributed model, `KEY COLS` will be the partition key.

### Drop Bucket
```
DROP BUCKET <name>
```

Destroys a bucket and all of its data.

## DML
**NB**: Columns are applied from left-to-right in all "where" clause constructions. You do not set conditions or queries. These are strict equality comparisons.

For example:

```
UPDATE foo
SET 5,4,3,2,1
WHERE 5,4
```

This command will find *all* rows that start with "5,4", delete them, and create a single new row "5,4,3,2,1". This is done for efficiency in data access.

### Create Row
```
CREATE ROW IN <bucket> <csv list>
```

Inserts a row into the bucket. If `KEY COLS` was set, the row must contain at *least* that number of columns.

### Update Row
```
UPDATE <bucket>
SET ROW <csv new data list>
WHERE <csv old data list>
```

Updates in CSVBase are actually DELETE and CREATE operations. This is something I'm kind of lifting from Cassandra's design (INSERTs and UPDATEs and DELETEs are actually all UPDATEs in Cassandra), but twisting for comedy purposes. And yes, I think this is funny.

### Delete Row
```
DELETE FROM <bucket>
WHERE <csv data list>
```

Deletes any row that matches the query row. Again, this is evaluated in a L->R order, meaning that commands like: `DELETE FROM foo WHERE 5!` will delete any row starting with 5.

## Queries
Not yet implemented. Due to the underlying storage model, you can't simply implement queries with an in-memory-only model.

# Design Advice
If you *do* decide to design a database with CSVBase, there are some tips to being successful.

In general, you should create buckets using a `KEY COLS` of 2, and the first column should be a letter index, and the second column should be a numeric index, mirroring Excel's design. A3 becomes `A,3,…`.

For example, you might want your bucket to store data like:

```
A,1,This is my first row,it has several pieces of data
A,2,This is my second row,it has different data
```

This mirrors the way your users might think about the data, and in future versions of CSVBase, I'm planning to add cell-reference syntax that allows users to implement Excel-like formulas.

See also, [Remy's Law of Requirements](https://twitter.com/RemyPorter/status/752913168624746497)