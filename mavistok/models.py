from datetime import datetime
from mavistok import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25))
    email = db.Column(db.String)
    username= db.Column(db.String(35),nullable=False)
    password = db.Column(db.String(77),nullable=False)

    def __repr__(self):
        return f"USer(''{self.name}',{self.username}','{self.email}')"

class Ham_madde(db.Model):
    ham_madde_kodu = db.Column(db.Integer,primary_key=True, autoincrement=True)
    ham_madde_adi = db.Column(db.String(32), nullable=False)
    aciklama = db.Column(db.String, nullable=False)
    eklenme_zamani = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tedarik_iliski = db.relationship('Tedarik_iliski',backref='ham_madde', lazy=True) #backref key wordü ile direkt bu classa ulaşılabiliyor. ex: Tedarik_iliski.ham_madde


class Tedarikci(db.Model):
    tedarikci_kodu = db.Column(db.Integer,primary_key=True, autoincrement=True)
    tedarikci_adi = db.Column(db.String(64), nullable=False)
    mail = db.Column(db.String(64))
    tel = db.Column(db.Text)
    aciklama = db.Column(db.Text)
    eklenme_zamani = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tedarik_iliski = db.relationship('Tedarik_iliski',backref='tedarikci', lazy=True) #backref key wordü ile direkt bu classa ulaşılabiliyor. ex: Tedarik_iliski.tedarikci


class Tedarik_iliski(db.Model):
    iliski_kod = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ham_madde_kodu = db.Column(db.Integer, db.ForeignKey(Ham_madde.ham_madde_kodu))
    ham_madde_adi = db.Column(db.String(32), nullable=False)
    tedarikci_kodu = db.Column(db.Integer, db.ForeignKey(Tedarikci.tedarikci_kodu))
    tedarikci_adi = db.Column(db.String(64), nullable=False)
    eklenme_zamani = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Ham_madde_stok(db.Model):
    hm_stok_id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    tedarikci_kodu = db.Column(db.Integer, db.ForeignKey(Tedarik_iliski.tedarikci_kodu))
    tedarikci_adi = db.Column(db.String(64), nullable=False)
    ham_madde_kodu = db.Column(db.Integer, db.ForeignKey(Tedarik_iliski.ham_madde_kodu))
    ham_madde_adi = db.Column(db.String(32), nullable=False)
    birim = db.Column(db.String, nullable=False)
    adet = db.Column(db.Float, nullable=False)
    tarih_kayit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tarih_alim = db.Column(db.DateTime, nullable=False)
    fiyat = db.Column(db.Float, nullable=False)
    aciklama = db.Column(db.Text)
    kayit_tipi = db.Column(db.String(100), nullable=False)
    kayit_id = db.Column(db.String(1), nullable=False)

#Ürün 
class Urun(db.Model):
    urun_kodu = db.Column(db.Integer,primary_key=True, autoincrement=True)
    urun_adi = db.Column(db.String(32), nullable=False)
    aciklama = db.Column(db.String, nullable=False)
    eklenme_zamani = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#Ürün Stok
class Urun_stok(db.Model):
    urun_stok_id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    urun_kodu = db.Column(db.Integer, db.ForeignKey(Tedarik_iliski.tedarikci_kodu))
    urun_adi = db.Column(db.String(64), nullable=False)
    satis_kanali_kodu = db.Column(db.Integer, db.ForeignKey(Tedarik_iliski.tedarikci_kodu))
    satis_kanali_adi = db.Column(db.String(64), nullable=False)
    birim = db.Column(db.String, nullable=False)
    adet = db.Column(db.Float, nullable=False)
    tarih_kayit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tarih_satis = db.Column(db.DateTime, nullable=False)
    fiyat = db.Column(db.Float, nullable=False)
    aciklama = db.Column(db.Text)
    kayit_tipi = db.Column(db.String(100), nullable=False)
    kayit_id = db.Column(db.String(1), nullable=False)


class Satis_kanali(db.Model):
    satis_kanali_kodu = db.Column(db.Integer,primary_key=True, autoincrement=True)
    satis_kanali_adi = db.Column(db.String(64), nullable=False)
    mail = db.Column(db.String(64))
    tel = db.Column(db.Text)
    aciklama = db.Column(db.Text)
    eklenme_zamani = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


#Ödemeler
class Odemeler(db.Model):
    odeme_id =db.Column(db.Integer, primary_key=True, autoincrement=True)
    odeme_tipi_adi = db.Column(db.String(100), nullable=False)
    odeme_tipi_kodu = db.Column(db.String(1), nullable=False)
    iliskili_islem_id = db.Column(db.Integer)
    tutar = db.Column(db.Float, nullable=False)
    tarih_kayit = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    tarih_odeme = db.Column(db.DateTime, nullable=False)
    aciklama = db.Column(db.Text)

