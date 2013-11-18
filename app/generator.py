from app import app

import flask
from flask import request, redirect

from database import connection, models

def generateFromIterator(data):

	parts = {}
	output = '''
# File generated by Multicraft.jar.conf. This is a user generated file, YOU are
# responsible for reading it and ensuring its safety and accuracy. We take zero
# responsibility if you're stupid and you screw up something by using this file.

	'''

	for name_, value in data.iteritems():

		name = name_.replace('opt_', '')

		if len(name) != len(name_):
			section, attribute = name.rsplit('_', 1)
			if section not in parts:
				parts[section] = {}

			parts[section][attribute] = value

	for section, attributes in parts.iteritems():
		output += '\n[' + section + ']\n'

		for attribute, value in attributes.iteritems():

			if not value:
				output += '#'

			output += attribute + ' = ' + value + '\n'

	return output.strip('\n\r ')


@app.route('/create', methods = ['GET', 'POST'])
def show_view():

	def show_response(error = None):
		jars = connection.session.query(models.Jar).order_by(models.Jar.name.asc()).all()
		return flask.render_template('generate.html', jars = jars, form = request.form, error = error)

	if request.method == 'GET':
		return show_response()

	if request.method == 'POST':
		entry = models.Entry(jar_id = request.form.get('jar'), version = request.form.get('version'))

		m = entry.validate(request.form)
		if m:
			return show_response(error = m)
		else:
			# connection.session.add(entry)
			# connection.session.commit()
			# return redirect('/conf/' + entry.id)
			return 'yep!'

@app.route('/create/raw', methods = ['POST'])
def preview_generate_file():
	return generateFromIterator(request.form)


@app.route('/create/validate', methods = ['POST'])
def validate_post():
	entry = models.Entry(jar_id = request.form.get('jar'), version = request.form.get('version'))
	m = entry.validate(request.form)
	if m:
		return m
	else:
		return 'OK'
