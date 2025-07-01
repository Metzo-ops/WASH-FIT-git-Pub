# Structure minimale d'une application WASH-FIT avec Flask, HTML/CSS et PostgreSQL

# 1. app.py (Back-end Flask principal)
from flask import Flask, render_template, request, redirect, url_for
import psycopg2, os

app = Flask(__name__)

# Configuration de la base de données PostgreSQL

conn = psycopg2.connect(
    dbname=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    host=os.environ.get("DB_HOST"),
    # port=os.environ.get("DB_PORT")
)

cursor = conn.cursor()

@app.route('/')
def home():
    cursor.execute("SELECT * FROM evaluations")
    evaluations = cursor.fetchall()
    return render_template('index.html', evaluations=evaluations)

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter():
    if request.method == 'POST':
        localite = request.form['localite']
        indicateur = request.form['indicateur']
        score = request.form['score']
        commentaire = request.form['commentaire']
        cursor.execute("INSERT INTO evaluations (indicateur, localite, score, commentaire) VALUES (%s, %s, %s, %s)",
                       (indicateur,localite , score, commentaire))
        conn.commit()
        return redirect(url_for('home'))
    return render_template('addEval.html')

@app.route('/supprimer/<int:id>', methods=['POST'])
def supprimer(id):
    cursor.execute("DELETE FROM evaluations WHERE id = %s", (id,))
    conn.commit()
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
