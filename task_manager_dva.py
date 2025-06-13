import mysql.connector
from mysql.connector import Error

def pripojeni_db():
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            database='ukoly',
            user='root',
            password='Okurkarka1.'
        )
        if connection.is_connected():
            print("Připojení k databázi bylo úspěšné.")
        return connection
    except Error as e:
        print(f"Chyba při připojování k databázi: {e}")
        return None

def vytvoreni_tabulky(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ukoly (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nazev VARCHAR(50) NOT NULL,
        popis TEXT NOT NULL,
        stav ENUM('nezahájeno', 'probíhá', 'hotovo') DEFAULT 'nezahájeno',
        datum_vytvoreni TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    connection.commit()
    print("Tabulka 'ukol' byla vytvořena nebo již existuje.")

def pridat_ukol(connection):
    nazev = input("Zadejte název úkolu: ")
    popis = input("Zadejte popis úkolu: ")
    if not nazev or not popis:
        print("Název a popis úkolu jsou povinné.")
        return
    cursor = connection.cursor()
    cursor.execute("INSERT INTO ukol (nazev, popis) VALUES (%s, %s)", (nazev, popis))
    connection.commit()
    print("Úkol byl úspěšně přidán.")

def zobrazit_ukoly(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT id, nazev, popis, stav FROM ukol WHERE stav IN ('nezahájeno', 'probíhá')")
    rows = cursor.fetchall()
    if not rows:
        print("Seznam úkolů je prázdný.")
    else:
        for row in rows:
            print(f"ID: {row[0]}, Název: {row[1]}, Popis: {row[2]}, Stav: {row[3]}")

def aktualizovat_ukol(connection):
    zobrazit_ukoly(connection)
    id_ukolu = input("Zadejte ID úkolu, který chcete aktualizovat: ")
    novy_stav = input("Zadejte nový stav úkolu (probíhá/hotovo): ")
    if novy_stav not in ['probíhá', 'hotovo']:
        print("Neplatný stav.")
        return
    cursor = connection.cursor()
    cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
    connection.commit()
    if cursor.rowcount == 0:
        print("Úkol s tímto ID neexistuje.")
    else:
        print("Úkol byl úspěšně aktualizován.")

def odstranit_ukol(connection):
    zobrazit_ukoly(connection)
    id_ukolu = input("Zadejte ID úkolu, který chcete odstranit: ")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ukol WHERE id = %s", (id_ukolu,))
    connection.commit()
    if cursor.rowcount == 0:
        print("Úkol s tímto ID neexistuje.")
    else:
        print("Úkol byl úspěšně odstraněn.")

def hlavni_menu(connection):
    while True:
        print("\nHlavní nabídka:")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")
        volba = input("Vyberte možnost: ")
        if volba == '1':
            pridat_ukol(connection)
        elif volba == '2':
            zobrazit_ukoly(connection)
        elif volba == '3':
            aktualizovat_ukol(connection)
        elif volba == '4':
            odstranit_ukol(connection)
        elif volba == '5':
            print("Ukončuji program.")
            break
        else:
            print("Neplatná volba, zkuste to znovu.")

if __name__ == "__main__":
    connection = pripojeni_db()
    if connection:
        vytvoreni_tabulky(connection)
        hlavni_menu(connection)
        connection.close()
        print("Připojení k databázi bylo uzavřeno.")