from mavistok import app, db
from flask import render_template, flash, redirect, url_for, session, logging, request
from mavistok.models import Users, Ham_madde, Tedarikci, Tedarik_iliski, Ham_madde_stok, Urun, Urun_stok, Satis_kanali, Odemeler
from mavistok.forms import RegisterForm, LoginForm, RawForm, SupplyRelationForm, SupplierForm, Purchase, ProductForm, ProductionForm, SalesChannelForm, Sales, Payment
from passlib.hash import sha256_crypt
from functools import wraps
from datetime import datetime
# encoding=utf8  

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

@app.route("/")
def index():
    return redirect(url_for("login"))

# kayıt olma
@app.route("/register",methods= ["GET","POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        user = Users(name=form.name.data,username = form.username.data, email = form.email.data, password = sha256_crypt.encrypt(form.password.data))
        db.session.add(user)
        db.session.commit()
        flash("Kayıt Tamamlandı","success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form)
    

#login
@app.route("/login", methods = ["GET","POST"])
def login():
    form=LoginForm(request.form)

    if request.method=="POST":
        user = Users.query.filter_by(username=form.username.data).first()
        pw_entered = form.password.data
        pw=user.password
        if user:
            if sha256_crypt.verify(pw_entered,pw):
                flash("Giriş Yapuldu","success")
                session["logged_in"] = True
                session["username"] = user.username
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
        pass
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

#satın alma/ham madde stok girişi
@app.route("/purchasing",methods= ["GET","POST"])
@login_required
def purchasing():
    form = Purchase(request.form)
    if request.method == "POST" and form.validate():
        rawObj = form.raw_name.data
        suppObj= form.supplier_name.data
        stok = Ham_madde_stok(ham_madde_adi=rawObj.ham_madde_adi, ham_madde_kodu=rawObj.ham_madde_kodu, tedarikci_adi=suppObj.tedarikci_adi, tedarikci_kodu=suppObj.tedarikci_kodu, birim=form.unit.data, adet=form.quantity.data, tarih_alim=form.purchase_date.data, fiyat=form.price.data, aciklama=form.comment.data, kayit_tipi="Satın Alma",kayit_id="b")
        #kayit_id 'b' (purchase) muhasebe ve stok kontrolünde kullanılacak
        db.session.add(stok)
        db.session.commit()
        flash("Kayıt Tamamlandı","success")
        return redirect(url_for("purchasing"))
    else:
        stock = Ham_madde_stok.query.all()
        relation = Tedarik_iliski.query.all()
        return render_template("purchasing.html", stock=stock, relation=relation, form=form)
        
"""
#chained selectfiled için kullanılacak
@app.route("/select_raw")
@login_required
def select_raw(raw):
    return render_template("select_raw.html",raw=raw)
"""

@app.route("/stockEdit")
@login_required
def stockEdit():
    return render_template("stockEdit.html")


#üretim
@app.route("/production")
@login_required
def production():
    return render_template("production.html")

@app.route("/nut_production",methods= ["GET","POST"])
@login_required
def nut_production():
    form = ProductionForm(request.form)
    if request.method == "POST" and form.validate(): 
        stok1 = Ham_madde_stok(ham_madde_adi='Fındık', ham_madde_kodu='18', tedarikci_adi='', tedarikci_kodu='', birim=form.nut_unit.data, adet=form.nut_quantity.data, tarih_alim= datetime.now(), fiyat='', aciklama='Fındık Ezmesi', kayit_tipi="Üretim",kayit_id="p")
        stok2 = Ham_madde_stok(ham_madde_adi='Hurma', ham_madde_kodu='17', tedarikci_adi='', tedarikci_kodu='', birim=form.hurma_unit.data, adet=form.hurma_quantity.data, tarih_alim=datetime.now(), fiyat='', aciklama='Fındık Ezmesi', kayit_tipi="Üretim",kayit_id="p")
        #kayit_id 'p' (production) muhasebe ve stok kontrolünde kullanılacak
        db.session.add(stok1)
        db.session.add(stok2)
        if form.product_quantity1.data > 0:
            urunKG = Urun_stok(urun_kodu='1', urun_adi='Fındık Ezmesi', satis_kanali_kodu='', satis_kanali_adi='', birim='kg', adet=form.product_quantity1.data, tarih_satis= datetime.now(), fiyat='', kayit_tipi='Üretim', kayit_id='p' )
            db.session.add(urunKG)
        if form.product_quantity2.data > 0:
            urunKav = Urun_stok(urun_kodu='1', urun_adi='Fındık Ezmesi', satis_kanali_kodu='', satis_kanali_adi='', birim='kv', adet=form.product_quantity2.data, tarih_satis= datetime.now(), fiyat='', kayit_tipi='Üretim', kayit_id='p' )
            db.session.add(urunKav)
        db.session.commit()
        flash("Kayıt Tamamlandı", "success")
        
        #db.session.execute("SELECT SUM(column_name)FROM table_name WHERE condition")
        return redirect(url_for("nut_production"))
    else:
        prod_hist=Urun_stok.query.all()
        return render_template("nut_production.html",prod_hist=prod_hist, form=form)


#satış kanalı
@app.route("/sales_channel", methods=["POST","GET"])
@login_required
def sales_channel():
    form = SalesChannelForm(request.form)
    if request.method=="POST" and form.validate():
        sales_channel = Satis_kanali(satis_kanali_adi=form.sales_channel_name.data, mail=form.mail.data, tel=form.tel.data, aciklama=form.comment.data)
        db.session.add(sales_channel)
        db.session.commit()
        return redirect(url_for("sales_channel"))
    else:
        sales_channel = Satis_kanali.query.all()
        return render_template("sales_channel.html", sales_channel=sales_channel,form=form)
    return render_template("sales_channel.html")

@app.route("/deleteSalesChannel/<int:id>",methods= ["POST"])
@login_required
def deleteSalesChannel(id):
    toDelete = Satis_kanali.query.filter_by(satis_kanali_kodu=id).first()
    if toDelete:
        db.session.delete(toDelete)
        db.session.commit()
        return redirect(url_for("sales_channel"))


#satış
@app.route("/sales",methods=["GET","POST"])
@login_required
def sales():
    form = Sales(request.form)
    if request.method == "POST" and form.validate():
        prodObj = form.product.data
        salesObj= form.sales_channel.data
        stok = Urun_stok(satis_kanali_kodu=salesObj.satis_kanali_kodu, satis_kanali_adi=salesObj.satis_kanali_adi, urun_adi=prodObj.urun_adi, urun_kodu=prodObj.urun_kodu, birim=form.unit.data, adet=form.quantity.data, tarih_satis=form.sales_date.data, fiyat=form.price.data, aciklama=form.comment.data, kayit_tipi="Satış",kayit_id="s")
        #kayit_id 's' (sales) muhasebe ve stok kontrolünde kullanılacak
        db.session.add(stok)
        db.session.commit()
        flash("Kayıt Tamamlandı","success")
        return redirect(url_for("sales"))
    else:
        stock = Urun_stok.query.all()
        return render_template("sales.html", stock=stock, form=form)
    return render_template("sales.html")


#ham madde tanım
@app.route("/raw_material",methods= ["GET","POST"])
@login_required
def raw_material():
    form = RawForm(request.form)
    if request.method=="POST" and form.validate():
        raw_material = Ham_madde(ham_madde_adi=form.raw_name.data,aciklama=form.comment.data)
        db.session.add(raw_material)
        db.session.commit()
        flash("Kayıt Tamamlandı","success")
        return redirect(url_for("raw_material"))
    else:
        raw_material= Ham_madde.query.all()
        return render_template("raw_material.html", raw_material=raw_material,form=form)

#ham madde silme
@app.route("/deleteRaw/<int:id>",methods= ["POST"])
@login_required
def deleteRaw(id):
    toDelete = Ham_madde.query.filter_by(ham_madde_kodu=id).first()
    if toDelete:
        db.session.delete(toDelete)
        db.session.commit()
        return redirect(url_for("raw_material"))
    


#tedarikçi tanım
@app.route("/vendor",methods= ["GET","POST"])
@login_required
def vendor():
    form = SupplierForm(request.form)
    if request.method=="POST" and form.validate():
        supplier = Tedarikci(tedarikci_adi=form.supplier_name.data, mail=form.mail.data, tel=form.tel.data, aciklama=form.comment.data)
        db.session.add(supplier)
        db.session.commit()
        return redirect(url_for("vendor"))
    else:
        vendor = Tedarikci.query.all()
        return render_template("vendor.html", vendor=vendor,form=form)

#tedarikçi silme
@app.route("/deleteSupp/<int:id>",methods= ["POST"])
@login_required
def deleteSupp(id):
    toDelete = Tedarikci.query.filter_by(tedarikci_kodu=id).first()
    if toDelete:
        db.session.delete(toDelete)
        db.session.commit()
        return redirect(url_for("vendor"))

#tedarik İlişki tanım
@app.route("/supplyRelation",methods= ["GET","POST"])
@login_required
def supplyRelation():
    form = SupplyRelationForm(request.form)
    if request.method == "POST":
        rawObj = form.raw_drop.data
        suppObj= form.supp_drop.data
        relation = Tedarik_iliski(ham_madde_kodu=rawObj.ham_madde_kodu,tedarikci_kodu=suppObj.tedarikci_kodu,tedarikci_adi=suppObj.tedarikci_adi, ham_madde_adi=rawObj.ham_madde_adi)
        db.session.add(relation)
        db.session.commit()
        return redirect(url_for("supplyRelation"))
    else:
        supplyRelation = Tedarik_iliski.query.all()
        return render_template("supplyRelation.html", supplyRelation=supplyRelation, form=form)

#tedarik ilişkisi silme
@app.route("/deleteSupRelation/<int:id>",methods= ["POST"])
@login_required
def deleteSupRelation(id):
    toDelete = Tedarik_iliski.query.filter_by(iliski_kod=id).first()
    if toDelete:
        db.session.delete(toDelete)
        db.session.commit()
        return redirect(url_for("supplyRelation"))



#ürün tanım
@app.route("/product",methods= ["GET","POST"])
@login_required
def product():
    form = ProductForm(request.form)
    if request.method=="POST" and form.validate():
        product = Urun(urun_adi=form.prod_name.data, aciklama=form.comment.data)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for("product"))
    else:
        product = Urun.query.all()
        return render_template("product.html", product=product,form=form)

#ürün silme
@app.route("/deleteProduct/<int:id>",methods= ["POST"])
@login_required
def deleteProduct(id):
    toDelete = Urun.query.filter_by(urun_kodu=id).first()
    if toDelete:
        db.session.delete(toDelete)
        db.session.commit()
        return redirect(url_for("product"))

#ödeme girişi
@app.route("/payment",methods= ["GET","POST"])
@login_required
def payment():
    form = Payment(request.form)
    if request.method=="POST" and form.validate():
        if form.payment_type_id.data == 'g':
            odeme_adi= 'Gelen Ödeme'
        elif form.payment_type_id.data == 'y':
            odeme_adi= 'Yapılan Ödeme'
        payment = Odemeler(odeme_tipi_kodu=form.payment_type_id.data, odeme_tipi_adi=odeme_adi , iliskili_islem_id=form.related_entry_id.data, tutar=form.amount.data, tarih_kayit=datetime.now(), tarih_odeme=form.payment_date.data , aciklama=form.comment.data)
        db.session.add(payment)
        db.session.commit()
        flash("Kayıt Tamamlandı","success")
        return redirect(url_for("payment"))
    else:
        payment= Odemeler.query.all()
        return render_template("payment.html", payment=payment,form=form)

        
#raporlar
@app.route("/reports",methods= ["GET","POST"])
@login_required
def reports():
    #form = Reports(request.form)
    if request.method == "POST":
        
        startDate = Odemeler(odeme_tipi_kodu=form.payment_type_id.data, odeme_tipi_adi=odeme_adi , iliskili_islem_id=form.related_entry_id.data, tutar=form.amount.data, tarih_kayit=datetime.now(), tarih_odeme=form.payment_date.data , aciklama=form.comment.data)
        endDate = Odemeler(odeme_tipi_kodu=form.payment_type_id.data, odeme_tipi_adi=odeme_adi , iliskili_islem_id=form.related_entry_id.data, tutar=form.amount.data, tarih_kayit=datetime.now(), tarih_odeme=form.payment_date.data , aciklama=form.comment.data)
        db.session.add(payment)
        db.session.commit()
        flash("Kayıt Tamamlandı","success")
        return redirect(url_for("payment"))
    else:
        payment= Odemeler.query.all()
        return render_template("payment.html", payment=payment,form=form)