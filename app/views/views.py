from flask import render_template, flash, url_for, redirect, request, abort
from app import app, db
from app.forms.forms import RegisterForm, LoginForm, BusinessesForm, ReviewForm
from flask_login import login_user, logout_user, current_user, login_required
from app.models.models import User, Businesses, Review



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

#create business route
@app.route('/businesses', methods = ['GET', 'POST'])
@login_required
def businesses():
    form = BusinessesForm()
    if form.validate_on_submit():
        business = Businesses(name = form.name.data, owner = current_user, location = form.location.data,
            started = form.date.data, business_description = form.business_description.data )
        db.session.add(business)
        db.session.commit()
        flash(f'you have successfully registered {business.name} business', 'success')
        return redirect(url_for('available'))
    else:
        flash('Your business not registered please check on your details and try again', 'danger')
    return render_template('business.html', title = 'Business', form = form, legend = 'Register Business', btn = 'Register')

#route that display all registered businesses
@app.route('/available-business')
def available():
    businesses = Businesses.query.all()
    return render_template('success.html', businesses = businesses)

#route that get business by id
@app.route('/businesses/<int:business_id>')
@login_required
def single_business(business_id):
    business = Businesses.query.get_or_404(business_id)
    return render_template('bs.html', business = business)


#update a business route
@app.route('/businesses/<int:business_id>/update', methods = ['POST', 'GET'])
@login_required
def update_business(business_id):
    business = Businesses.query.get_or_404(business_id)
    if business.owner != current_user:
        abort(403)
    form = BusinessesForm()
    if form.validate_on_submit():
        business.name = form.name.data
        business.location = form.location.data
        business.business_description = form.business_description.data
        db.session.commit()
        flash(f'Your business has been updated', 'success')
        return redirect(url_for('single_business', business_id = business.id))
    elif request.method == 'GET':
        form.name.data = business.name
        form.location.data = business.location
        form.business_description.data = business.business_description
    return render_template('business.html', title = 'update', form = form, legend = 'Update Business', btn = 'Update')

#route to delete a business
@app.route('/business-delete/<int:business_id>', methods = ['POST'])
@login_required
def deletebusiness(business_id):
    business = Businesses.query.get_or_404(business_id)
    db.session.delete(business)
    db.session.commit()
    flash('Your business has been deleted', 'success')
    return redirect(url_for('available'))


#route to post a review
@app.route('/businesses/<int:business_id>/review', methods = ['GET', 'POST'])
@login_required
def review(business_id):
    form = ReviewForm()
    business = Businesses.query.get_or_404(business_id)
    if form.validate_on_submit():
        review = Review(review_headline = form.review_headline.data,comment = form.comment.data )
        db.session.add(review)
        db.session.commit()
        flash('Thank you for your feedback')
        return redirect(url_for('get_review', business_id = business.id))
    return render_template('review.html', form = form)
#route to get all reviews
@app.route('/businesses/<int:business_id>/reviews')
def get_review(business_id):
    reviews = Review.query.get_or_404(business_id)
    return render_template('all_reviews.html', reviews = reviews)
