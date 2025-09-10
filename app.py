# Importăm clasele necesare: Flask pentru a crea serverul, request pentru a accesa datele trimise,
# render_template pentru a afișa paginile HTML și redirect/url_for pentru a redirecționa utilizatorul.
from flask import Flask, request, render_template, redirect, url_for
import smtplib # Acesta este modulul Python pentru a trimite emailuri
from email.mime.text import MIMEText # Pentru a formata emailul frumos

# Creează o instanță a aplicației Flask
app = Flask(__name__)

# --- Datele tale de email (COMPLETEAZĂ AICI!) ---
# !!! ATENȚIE: Folosește parola de aplicație generată la Pasul 1, NU parola ta de Gmail!
EMAIL_ADRESA = "magicianulmintii@gmail.com" 
EMAIL_PAROLA = "kobdbmwbuloytbne"

# Definim o "rută" pentru pagina principală. Când cineva accesează "/", funcția de mai jos va rula.
@app.route('/')
def acasa():
    # Afișăm fișierul index.html
    return render_template('index.html')

# Definim rute pentru celelalte pagini, pentru a le putea accesa prin serverul Flask
@app.route('/<string:nume_pagina>')
def pagina(nume_pagina):
    # Afișează orice pagină .html (ex: /despre.html, /contact.html)
    return render_template(nume_pagina)

# Definim ruta care va PROCESA datele formularului. Aceasta acceptă doar cereri de tip POST.
@app.route('/trimite-formular', methods=['POST'])
def trimite_formular():
    # Preluăm datele trimise din formular
    nume = request.form['nume']
    email_client = request.form['email']
    mesaj = request.form['mesaj']

    # Creăm conținutul emailului
    subiect = f"Mesaj nou de pe site de la {nume}"
    corp_email = f"""
    Ai primit un mesaj nou prin formularul de contact:

    Nume: {nume}
    Email: {email_client}

    Mesaj:
    {mesaj}
    """

    # Configurăm emailul
    msg = MIMEText(corp_email)
    msg['Subject'] = subiect
    msg['From'] = EMAIL_ADRESA
    msg['To'] = EMAIL_ADRESA

    try:
        # Ne conectăm la serverul SMTP al Google și trimitem emailul
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADRESA, EMAIL_PAROLA)
        server.send_message(msg)
        server.quit()
        print("Email trimis cu succes!")
        # Acum, re-afișăm pagina de contact, trimițându-i variabila `succes=True`
        return render_template('contact.html', succes=True)
    except Exception as e:
        print(f"Eroare la trimiterea emailului: {e}")
        # Dacă apare o eroare, re-afișăm pagina de contact cu un mesaj de eroare
        mesaj_eroare = "A apărut o eroare la trimiterea mesajului. Te rugăm să încerci mai târziu."
        return render_template('contact.html', eroare=True, mesaj_eroare=mesaj_eroare)

# Această linie pornește serverul când rulăm fișierul `python app.py`
if __name__ == '__main__':
    # debug=True face ca serverul să se restarteze automat când salvăm fișierul.
    # NU folosi debug=True când site-ul este live!
    app.run(debug=False)