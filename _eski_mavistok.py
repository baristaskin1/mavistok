from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from functools import wraps
from flask_sqlalchemy import sqlalchemy


app = Flask(__name__)
app.secret_key ="mavi"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "mavi_stok"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

#Kullanıcı Giriş Decorater
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Giriş Yapınız","danger")
            return redirect(url_for("login"))
    return decorated_function

#Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name=StringField("İsim Soyisim",validators=[validators.Length(min=4, max=25),validators.data_required()])
    username=StringField("Kullanıcı Adı",validators=[validators.Length(min=5, max=35),validators.data_required()])
    email=StringField("E-Posta",validators=[validators.data_required(),validators.email(message="Lütfen Geçerli Bir E-Posta Adresi Girin.")])
    password=PasswordField("Parola", validators=[
        validators.data_required(message="Lütfen Parola Girin"),
        validators.EqualTo(fieldname="confirm",message="Parolalar uyuşmuyor")
    ])
    confirm=PasswordField("Parola Tekrar")
#Kullanıcı Giriş Formu
class LoginForm(Form):
    username=StringField("Kullanıcı Adı",validators=[validators.Length(min=5, max=35),validators.data_required])
    password=PasswordField("Parola")





@app.route("/")
def index():
    return redirect(url_for("login"))

# kayıt olma
@app.route("/register",methods= ["GET","POST"])
def register():
    form = RegisterForm(request.form)
    
    if request.method=="POST" and form.validate():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)
        cursor = mysql.connection.cursor()
        query = "insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(name,email,username,password)) #değişkenleri bir demet olarak iletmek gerekiyor
        mysql.connection.commit()
        cursor.close()
        flash("Kayıt Tamamlandı","success")
        return redirect(url_for("login"))
    else:    
        return render_template("register.html", form=form)

#login
@app.route("/login", methods = ["GET","POST"])
def login():
    form=LoginForm(request.form)
    
    if request.method=="POST":
        username = form.username.data
        password_entered = form.password.data
        cursor = mysql.connection.cursor()
        query = "select * from users where username = %s"
        result = cursor.execute(query,(username,)) #değişkenleri bir demet olarak iletmek gerekiyor
        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Giriş Yapuldu","success")
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("main"))
            else:
                flash("Şifre Hatalı","danger")
                return redirect(url_for("login"))
        else:
            flash("Uiiy Kullanıcı yok","danger")
            return redirect(url_for("login"))
    else:
        return render_template("login.html",form=form)


#main
@app.route("/main", methods = ["GET","POST"])
@login_required
def main():
    form=RegisterForm(request.form)

    if request.method=="POST":
        cursor = mysql.connection.cursor()
        mysql.connection.commit()
        cursor.close()
    else:
        return render_template("main.html",form=form)

#logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

#tanımlar
@app.route("/definitions")
@login_required
def definitions():
    return render_template("definitions.html")

#satın alma
@app.route("/purchasing")
@login_required
def purchasing():
    return render_template("purchasing.html")


#üretim
@app.route("/production")
@login_required
def production():
    return render_template("production.html")

#satış
@app.route("/sales")
@login_required
def sales():
    return render_template("sales.html")

#Ham Madde Giriş Formu
class RawForm(Form):
    raw_name=StringField("Ham Madde Adı",validators=[validators.data_required()])
    comment=TextAreaField("Açıklama")

#ham madde tanım
@app.route("/raw_material",methods= ["GET","POST"])
@login_required
def raw_material():
    form = RawForm(request.form)
    if request.method=="POST" and form.validate():
        cursor= mysql.connection.cursor()
        raw_name = form.raw_name.data
        comment = form.comment.data
        cursor = mysql.connection.cursor()
        query = "insert into ham_madde (ham_madde_adi, aciklama ) VALUES(%s,%s)"
        cursor.execute(query,(raw_name,comment)) #değişkenleri bir demet olarak iletmek gerekiyor 
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("raw_material"))
    else:
        cursor = mysql.connection.cursor()
        query = "select * from ham_madde"
        cursor.execute(query) #değişkenleri bir demet olarak iletmek gerekiyor 
        raw_material=list(cursor.fetchall())
        mysql.connection.commit()
        cursor.close()
        return render_template("raw_material.html", raw_material=raw_material,form=form)

#ham madde silme
@app.route("/deleteRaw/<int:id>",methods= ["POST"])
@login_required
def deleteRaw(id):

    cursor= mysql.connection.cursor()
    query = "Select * from ham_madde where ham_madde_kodu = %s"
    result= cursor.execute(query,(id,))
    if result>0:
        querydel = "delete from ham_madde where ham_madde_kodu=%s"
        cursor.execute(querydel,(id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("raw_material"))
    
#Tedarikçi Giriş Formu
class SupplierForm(Form):
    supplier_name=StringField("Tedarikci Adı",validators=[validators.data_required()])
    mail=StringField("Mail") 	
    tel=StringField("Telefon")
    comment=TextAreaField("mail")

#tedarikçi tanım
@app.route("/vendor",methods= ["GET","POST"])
@login_required
def vendor():
    form = SupplierForm(request.form)
    if request.method=="POST" and form.validate():
        cursor= mysql.connection.cursor()
        supplier_name = form.supplier_name.data
        mail = form.mail.data
        tel = form.tel.data
        comment = form.comment.data
        cursor = mysql.connection.cursor()
        query = "INSERT into tedarikci (tedarikci_adi, mail, tel, aciklama ) VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(supplier_name,mail,tel,comment)) #değişkenleri bir demet olarak iletmek gerekiyor 
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("vendor"))
    else:
        cursor = mysql.connection.cursor()
        query = "select * from tedarikci"
        cursor.execute(query) #değişkenleri bir demet olarak iletmek gerekiyor 
        vendor=list(cursor.fetchall())
        mysql.connection.commit()
        cursor.close()
        return render_template("vendor.html", vendor=vendor,form=form)
#tedarikçi silme
@app.route("/deleteSupp/<int:id>",methods= ["POST"])
@login_required
def deleteSupp(id):

    cursor= mysql.connection.cursor()
    query = "Select * from tedarikci where tedarikci_kodu = %s"
    result= cursor.execute(query,(id,))
    if result>0:
        querydel = "delete from tedarikci where tedarikci_kodu=%s"
        cursor.execute(querydel,(id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("vendor"))


#Tedarik İlişki Giriş Formu
class SupplyRelationForm(Form):
    #queryler eklenerek değişkenlere atılacak. değişkenler de choices'a iletilecek
    supplier_name=SelectField(u'Tedarikci Adı',validators=[validators.data_required()])
    raw_name=SelectField(u'Ham Madde Adı',validators=[validators.data_required()])

#tedarik İlişki tanım
@app.route("/supplyRelation",methods= ["GET","POST"])
@login_required
def supplyRelation():
    form = SupplyRelationForm(request.form)
    if request.method=="POST":
        cursor = mysql.connection.cursor()
        supplier_name = form.supplier_name.data
        raw_name = form.raw_name.data
        query="select ham_madde_kodu from ham_madde where ham_madde_adi=%s"
        raw_id = int(cursor.execute(query, (raw_name,)))
        query="select tedarikci_kodu from tedarikci where tedarikci_adi=%s"
        supplier_id = int(cursor.execute(query, (supplier_name,)))
        query = "INSERT into tedarik_iliski (ham_madde_kodu,ham_madde_adi,tedarikci_kodu,tedarikci_adi) VALUES(%s,%s,%s,%s)"
        cursor.execute(query,(raw_id,raw_name,supplier_id,supplier_name)) #değişkenleri bir demet olarak iletmek gerekiyor 
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("supplyRelation"))
    else:
        cursor = mysql.connection.cursor()
        query = "select * from tedarik_iliski"
        cursor.execute(query) #değişkenleri bir demet olarak iletmek gerekiyor 
        supplyRelation = list(cursor.fetchall())
        cursor.execute("select * from ham_madde")
        raw_drop = list(cursor.fetchall())
        cursor.execute("select * from tedarikci")
        supp_drop = list(cursor.fetchall())
        mysql.connection.commit()
        cursor.close()
        return render_template("supplyRelation.html", supplyRelation=supplyRelation, raw_drop=raw_drop, supp_drop=supp_drop, form=form)

#tedarik ilişkisi silme
@app.route("/deleteSupRelation/<int:id>",methods= ["POST"])
@login_required
def deleteSupRelation(id):
    cursor= mysql.connection.cursor()
    query = "Select * from tedarik_iliski where iliski_kod = %s"
    result= cursor.execute(query,(id,))
    if result>0:
        querydel = "delete from tedarik_iliski where iliski_kod=%s"
        cursor.execute(querydel,(id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("supplyRelation"))

if __name__ == "__main__":
    app.run(debug=True)

    