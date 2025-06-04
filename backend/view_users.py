import sqlite3

def view_table_structure():
    conn = sqlite3.connect('trackgo.db')
    cursor = conn.cursor()
    
    try:
        # Ottieni informazioni sulla struttura della tabella users
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        
        print("\n=== STRUTTURA TABELLA USERS ===")
        for col in columns:
            print(f"Colonna: {col[1]}, Tipo: {col[2]}")
            
    except sqlite3.Error as e:
        print(f"Errore durante la lettura della struttura: {e}")
    finally:
        conn.close()

def view_users():
    conn = sqlite3.connect('trackgo.db')
    cursor = conn.cursor()
    
    try:
        # Prima vediamo quali colonne sono disponibili
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Ora selezioniamo tutte le colonne disponibili
        cursor.execute(f"SELECT * FROM users")
        users = cursor.fetchall()
        
        # Stampa i risultati in formato leggibile
        print("\n=== UTENTI REGISTRATI ===")
        print(" | ".join(columns))
        print("-" * 80)
        
        for user in users:
            print(" | ".join(str(value) for value in user))
            
    except sqlite3.Error as e:
        print(f"Errore durante la lettura del database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Visualizzazione struttura tabella:")
    view_table_structure()
    print("\nVisualizzazione dati utenti:")
    view_users() 