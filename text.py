import cx_Oracle

db = cx_Oracle.connect(user="c##cf", password="cf", encoding="UTF-8")

cur = db.cursor()
cur.execute('select * from users')
def makeNamedTupleFactory(cursor):
    columnNames = [d[0].lower() for d in cursor.description]
    import collections
    Row = collections.namedtuple('Row', columnNames)
    return Row

cur.rowfactory = makeNamedTupleFactory(cur)
print(cur.fetchone().username)
