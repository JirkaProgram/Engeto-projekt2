import pytest
import mysql.connector
from mysql.connector import Error

def pripoj_test_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        database="test_ukoly",
        user="root",   
        password="Okurkarka1."  
    )

def vycisti_tabulku(connection):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM test_ukol")
    connection.commit()

def test_pridani_ukolu_ok():
    conn = pripoj_test_db()
    vycisti_tabulku(conn)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_ukol (nazev, popis) VALUES (%s, %s)", ("Test úkol", "Popis"))
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM test_ukol WHERE nazev = 'Test úkol'")
    count = cursor.fetchone()[0]
    assert count == 1
    vycisti_tabulku(conn)
    conn.close()

def test_pridani_ukolu_neplatny():
    conn = pripoj_test_db()
    vycisti_tabulku(conn)
    cursor = conn.cursor()
    with pytest.raises(mysql.connector.Error):
        cursor.execute("INSERT INTO test_ukol (nazev, popis) VALUES (%s, %s)", (None, "Popis bez názvu"))
    conn.close()

def test_aktualizace_ukolu_ok():
    conn = pripoj_test_db()
    vycisti_tabulku(conn)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_ukol (nazev, popis) VALUES (%s, %s)", ("Test úkol", "Popis"))
    conn.commit()
    cursor.execute("UPDATE test_ukol SET stav = %s WHERE nazev = %s", ("hotovo", "Test úkol"))
    conn.commit()

    cursor.execute("SELECT stav FROM test_ukol WHERE nazev = 'Test úkol'")
    stav = cursor.fetchone()[0]
    assert stav == "hotovo"
    vycisti_tabulku(conn)
    conn.close()

def test_aktualizace_neexistujiciho_ukolu():
    conn = pripoj_test_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE test_ukol SET stav = %s WHERE id = %s", ("hotovo", -999))
    conn.commit()
    assert cursor.rowcount == 0
    conn.close()

def test_odstraneni_ukolu_ok():
    conn = pripoj_test_db()
    vycisti_tabulku(conn)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO test_ukol (nazev, popis) VALUES (%s, %s)", ("Test", "Popis"))
    conn.commit()

    cursor.execute("DELETE FROM test_ukol WHERE nazev = %s", ("Test",))
    conn.commit()
    assert cursor.rowcount == 1
    vycisti_tabulku(conn)
    conn.close()

def test_odstraneni_neexistujiciho_ukolu():
    conn = pripoj_test_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM test_ukol WHERE id = %s", (-999,))
    conn.commit()
    assert cursor.rowcount == 0
    conn.close()