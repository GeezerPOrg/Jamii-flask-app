from flask import render_template, flash, url_for, redirect, request, abort
from app import app, db
from app.forms.forms import RegisterForm, LoginForm, BusinessesForm, DeleteBusiness
from flask_login import login_user, logout_user, current_user, login_required
from app.models.models import User, Businesses



#home route
@app.route('/')
def home():
    return render_template('home.html')

#register route
@app.route('/register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account for {form.username.data} created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'register', form = form)

#login route
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and user.check_password(form.password.data):
            flash('You have successfully logged in', 'success')
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title = 'login', form = form)

#logout 
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#register business route
@app.route('/businesses', methods = ['GET', 'POST'])
@login_required
def businesses():
    form = BusinessesForm()
    if form.validate_on_submit():
        business = Businesses(name = form.name.data, location = form.location.data,
            started = form.date.data, business_description = form.business_description.data )
        db.session.add(business)
        db.session.commit()
        flash(f'you have successfully registered {business.name} business', 'success')
        return redirect(url_for('available'))
    else:
        flash('Your business not registered please check on your details and try again', 'danger')
    return render_template('business.html', title = 'Business', form = form)

#route that display all registered businesses
@app.route('/available-business')
def available():
    businesses = Businesses.query.all()
    return render_template('success.html', businesses = businesses)

#route that get business by id
@app.route('/businesses/<int:id>')
@login_required
def single_business(id):
    business = Businesses.query.get_or_404(id)
    return render_template('bs.html', business = business)


#route update a business
@app.route('/business-update/<int:business_id>', methods = ['POST', 'GET'])
@login_required
def update_business(business_id):
    business = Businesses.query.get_or_404(business_id)
    form = BusinessesForm()
    if form.validate_on_submit():
        business.name = form.name.data
        business.location = form.location.data
        business.business_description = form.business_description.data
        db.session.commit()
        flash(f'Your business has been updated', 'success')
        return redirect(url_for('available', business_id = Businesses.id))
    return render_template('business.html', title = 'update', form = form)

#route to delete a business
@app.route('/business-delete/<int:business_id>', methods = ['GET', 'POST'])
@login_required
def deletebusiness(business_id):
    form = DeleteBusiness()
    if form.validate_on_submit():
        business = Businesses.query.get_or_404(business_id)
        db.session.delete(business)
        db.session.commit()
        flash('Your business has been deleted', 'success')
    return render_template('delete.html', form = form)
