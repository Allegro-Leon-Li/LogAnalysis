#!/usr/bin/env python
import psycopg2

def db_connect():
    try:
        conn = psycopg2.connect("dbname=news")
    except psycopg2.DatabaseError as e:
        print('Database error, please refer to the README to set up the databse')
        print(e)
        exit()
    return (conn, conn.cursor())

def execute_query(query, cur):
    cur.execute(query)
    result = cur.fetchall()
    return result

def print_top_articles(cur):
    query = """SELECT articles.title, count(*) AS num FROM articles, log
                WHERE log.path = '/article/' || articles.slug
                GROUP BY articles.title ORDER BY num DESC LIMIT 3"""

    result = execute_query(query, cur)

    print('Most popular three articles of all time:')
    for row in result:
        print('\t"{0}" -- {1} views'.format(row[0], row[1]))

def print_top_authors(cur):
    query = """SELECT authors.name, count(*) AS num FROM authors
                LEFT JOIN articles ON authors.id=articles.author
                LEFT JOIN log ON log.path = '/article/' || articles.slug
                GROUP BY authors.name ORDER BY num DESC"""
    result = execute_query(query, cur)

    print('Most popular article authors of all time:')
    for row in result:
        print('\t{0} -- {1} views'.format(row[0], row[1]))

def print_errors_over_one(cur):
    query = """SELECT d1,100*cast(err AS float)/cast(total AS float) AS percent
                FROM (SELECT time::date AS d1, count(*) AS err
                FROM log WHERE status LIKE'%404%' GROUP BY d1) AS first
                LEFT JOIN (SELECT time::date AS d2, count(*) AS total
                FROM log GROUP BY d2) AS second ON d1=d2
                WHERE 100*cast(err AS float)/cast(total AS float) > 1"""
    result = execute_query(query, cur)

    print('On which days did more than 1% of requests lead to errors:')
    for row in result:
        print('\t{0:%B %d, %Y} -- {1:.2f}%'.format(row[0], row[1]))

def close_db(conn, cur):
    cur.close()
    conn.close()

def main():
    (conn, cur) = db_connect()
    print_top_articles(cur)
    print_top_authors(cur)
    print_errors_over_one(cur)
    close_db(cur, conn)

if __name__ == '__main__':
    main()
