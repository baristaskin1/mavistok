from flask_wtf import FlaskForm
from wtforms import Form, StringField, TextAreaField,PasswordField,validators,SelectField, DateField,DecimalField, IntegerField
from wtforms.validators import ValidationError
from mavistok.models import Users, Tedarikci, Ham_madde, Tedarik_iliski, Satis_kanali, Urun
from flask_sqlalchemy import SQLAlchemy
from wtforms.ext.sqlalchemy.fields import QuerySelectField

#Kullanıcı Kayıt Formu
class RegisterForm(Form):
    name=StringField("İsim Soyisim",validators=[validators.Length(min=4, max=25),validators.data_required()])
    username=StringField("Kullanıcı Adı",validators=[validators.Length(min=5, max=35),validators.data_required()])
    email=StringField("E-Posta",validators=[validators.data_required(),validators.email(message="Lütfen Geçerli Bir E-Posta Adresi Girin.")])
    password=PasswordField("Parola", validators=[
        validators.data_required(message="Lütfen Parola Girin"),
        validators.EqualTo(fieldname="confirm",message="Parolalar uyuşmuyor")
    ])
    confirm = PasswordField("Parola Tekrar")
    
    def validate_username(self, username):
        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Kullanıcı adı daha önce kullanılmış')
    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-Posta daha önce kullanılmış')
        
#Kullanıcı Giriş Formu
class LoginForm(Form):
    username = StringField("Kullanıcı Adı", validators=[validators.Length(min=5, max=35), validators.data_required])
    password = PasswordField("Parola")


#Ham Madde Giriş Formu
class RawForm(Form):
    raw_name = StringField("Ham Madde Adı", validators=[validators.data_required()])
    comment = TextAreaField("Açıklama")

def raw_drop():
    return Ham_madde.query

def supp_drop():
    return Tedarikci.query


#Tedarik İlişki Giriş Formu
class SupplyRelationForm(FlaskForm):
    #queryler eklenerek değişkenlere atılacak. değişkenler de drop'a iletilecek
    raw_drop = QuerySelectField("Ham Madde", query_factory=raw_drop,validators=[validators.data_required()],get_label='ham_madde_adi')
    supp_drop = QuerySelectField("Tedarikçi", query_factory=supp_drop,validators=[validators.data_required()],get_label='tedarikci_adi')

#Tedarikçi Giriş Formu
class SupplierForm(Form):
    supplier_name = StringField("Tedarikci Adı", validators=[validators.data_required()])
    mail = StringField("Mail")
    tel = StringField("Telefon")
    comment = TextAreaField("Açıklama")

def purchase_drop():
    return Tedarik_iliski.query


#Ham Madde Satın Alma Formu
class Purchase(Form):
    raw_name = QuerySelectField("Ham Madde",query_factory=purchase_drop, validators=[validators.data_required()],get_label='ham_madde_adi')
    supplier_name = QuerySelectField("Tedarikci", query_factory=purchase_drop, validators=[validators.data_required()],get_label='tedarikci_adi')
    unit = SelectField("Birim",choices=[('kg','Kilogram'),('gr','Gram')] , validators=[validators.data_required()])
    quantity = DecimalField("Adet", validators=[validators.data_required()])
    purchase_date = DateField("Alım Tarihi", validators=[validators.data_required()], format='%d.%m.%Y')
    price = DecimalField("Fiyat", validators=[validators.data_required()])
    comment = TextAreaField("Açıklama")

#Ürün Giriş Formu
class ProductForm(Form):
    prod_name = StringField("Ürün Adı", validators=[validators.data_required()])
    comment = TextAreaField("Açıklama")

#Ham Madde Satın Alma Formu
class ProductionForm(Form):
    nut_unit = SelectField("Birim",choices=[('kg','Kilogram'),('gr','Gram')] , validators=[validators.data_required()])
    nut_quantity = DecimalField("Adet", validators=[validators.data_required()])
    hurma_unit = SelectField("Birim",choices=[('kg','Kilogram'),('gr','Gram')] , validators=[validators.data_required()])
    hurma_quantity = DecimalField("Adet", validators=[validators.data_required()])
    product_quantity1 = DecimalField("Kilo")
    product_quantity2 = IntegerField("Kavanoz Adet")

#Satış Kanalı Giriş Formu
class SalesChannelForm(Form):
    sales_channel_name = StringField("Satış Kanalı Adı", validators=[validators.data_required()])
    mail = StringField("Mail")
    tel = StringField("Telefon")
    comment = TextAreaField("Açıklama")

def sales_channel_drop():
    return Satis_kanali.query

def product_drop():
    return Urun.query

#Satış Formu 
class Sales(Form):
    product = QuerySelectField("Ürün", query_factory=product_drop, validators=[validators.data_required()], get_label='urun_adi')
    sales_channel = QuerySelectField("Satış Kanalı", query_factory=sales_channel_drop, validators=[validators.data_required()],get_label='satis_kanali_adi')
    unit = SelectField("Birim", choices=[('kg', 'Kilogram'),('kv','Kavanoz')] , validators=[validators.data_required()])
    quantity = DecimalField("Adet", validators=[validators.data_required()])
    sales_date = DateField("Satış Tarihi", validators=[validators.data_required()], format='%d.%m.%Y')
    price = DecimalField("Fiyat", validators=[validators.data_required()])
    comment = TextAreaField("Açıklama")


#Ödeme Formu 
class Payment(Form):
    payment_type_id = SelectField("Ödeme Türü", choices=[('g', 'Gelen Ödeme'),('y','Yapılan Ödeme')] , validators=[validators.data_required()])
    related_entry_id = IntegerField("İlişkili İşlem ID (Zorunlu değil)")
    amount = DecimalField("Ödeme Tutarı", validators=[validators.data_required()]) 
    payment_date = DateField("Ödeme Tarihi", validators=[validators.data_required()], format='%d.%m.%Y')
    comment = TextAreaField("Açıklama")