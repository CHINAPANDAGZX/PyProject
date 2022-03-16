from sqlalchemy import create_engine, Table, MetaData

dbUrl = 'mysql://root:root@192.168.1.165/community_db_3.0?charset=utf8'   #will be different for different db's

engine = create_engine(dbUrl)
meta = MetaData()

table = Table('hm_sys_users', meta, autoload=True, autoload_with=engine)

primaryKeyColName = table.primary_key.columns.values()[0].name
print(primaryKeyColName)