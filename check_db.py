import sqlite3

def check():
    conn = sqlite3.connect('C:/SAT/sat_lab.db')
    c = conn.cursor()
    
    topics = c.execute("SELECT DISTINCT topic, subtopic FROM questions").fetchall()
    print("Topics:", topics)
    
if __name__ == '__main__':
    check()
