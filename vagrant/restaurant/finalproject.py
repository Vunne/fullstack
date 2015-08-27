from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/restaurant')
def allRestaurants():
	"""Show all restaurants"""
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)

@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	"""Show restaurant menu"""
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	return render_template('restaurantMenu.html', restaurant = restaurant, items = items)

@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
	"""Create new restaurant"""
	if request.method == "POST":
		newRestaurant = Restaurant(name = request.form['name'])
		print 'newRestaurant', newRestaurant
		session.add(newRestaurant)
		session.commit()
		flash("New restaurant created")
		return redirect(url_for('allRestaurants'))
	else:
		return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
	"""Create a new menu item"""
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], 
			description = request.form['description'],
			price = request.form['price'],
			course = request.form['course'], restaurant_id = restaurant_id)
		print 'newItem', newItem
		session.add(newItem)
		session.commit()
		flash("New menu item created")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newMenuItem.html', restaurant_id = restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
	"""Edit a restaurant"""
	editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedRestaurant.name = request.form['name']
		session.add(editedRestaurant)
		session.commit()
		flash("Restaurant edited")
		return redirect(url_for('allRestaurants'))
	else:
		return render_template(
			'editRestaurant.html', restaurant_id = restaurant_id, restaurant = editedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	"""Edit a menu item"""
	editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if request.form['name']:
			editedItem.name = request.form['name']
		session.add(editedItem)
		session.commit()
		flash("Menu item edited")
		return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template(
			'editMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
	"""Delete a restaurant"""
	restaurantToDelete = session.query(Restaurant).filter_by(id=restaurant_id).one()
	if request.method == 'POST':
		if restaurantToDelete != []:
			session.delete(restaurantToDelete)
			session.commit()
			flash("Restaurant deleted")
			return redirect(url_for('allRestaurants'))
	else:
		return render_template(
			'deleteRestaurant.html', restaurant_id = restaurant_id, restaurant=restaurantToDelete)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	"""Delete a menu item"""
	itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
	if request.method == 'POST':
		if itemToDelete != []:
			session.delete(itemToDelete)
			session.commit()
			flash("Menu item deleted")
			return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
	else:
		return render_template(
			'deleteMenuItem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=itemToDelete)

# Making an API Endpoint (GET Request)
@app.route('/restaurant/JSON')
def restaurantJSON():
	restaurants = session.query(Restaurant).all()
	print '\nRESTAURANTS\n', [r for r in restaurants], '\n'
	return jsonify(Restaurants = [r.serialize for r in restaurants])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
	print '\nMENU ITEMS\n', [i for i in items], '\n'
	return jsonify(MenuItems = [i.serialize for i in items])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuItemJSON(restaurant_id, menu_id):
	menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
	return jsonify(MenuItem = menuItem.serialize)

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port=5000)