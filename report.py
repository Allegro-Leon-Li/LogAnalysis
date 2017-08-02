#!/usr/bin/python
import psycopg2

conn = psycopg2.connect("dbname=news")

cur = conn.cursor()

query1 = "SELECT articles.title, count(*) AS num FROM articles, log " \
    "WHERE log.path LIKE concat('%', articles.slug) GROUP BY " \
    "articles.title ORDER BY num DESC"
cur.execute(query1)
result = cur.fetchall()

print('Most popular three articles of all time:')
for row in result[:3]:
    print('\t"' + row[0] + '" -- ' + str(row[1]) + ' views')

query2 = "SELECT authors.name, count(*) AS num FROM authors " \
    "LEFT JOIN articles ON authors.id=articles.author " \
    "LEFT JOIN log ON log.path LIKE concat('%', articles.slug) " \
    "GROUP BY authors.name ORDER BY num DESC"
cur.execute(query2)
result = cur.fetchall()

print('Most popular article authors of all time:')
for row in result:
    print('\t' + row[0] + ' -- ' + str(row[1]) + ' views')


query3 = "SELECT d1,100*cast(err AS float)/cast(total AS float) AS percent " \
    "FROM (SELECT time::date AS d1, count(*) AS err " \
    "FROM log WHERE status LIKE'%404%' GROUP BY d1) AS first " \
    "LEFT JOIN (SELECT time::date AS d2, count(*) AS total " \
    "FROM log GROUP BY d2) AS second ON d1=d2"
cur.execute(query3)
result = cur.fetchall()

print('On which days did more than 1% of requests lead to errors:')
for row in result:
    if (row[1] >= 1):
        print('\t' + str(row[0]) + ' -- ' + '{0:.2f}'.format(row[1]) + '%')
cur.close()
conn.close()
