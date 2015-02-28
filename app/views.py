from flask import render_template, redirect, url_for
from app import app
from .forms import SecurityForm
from .finance import pullData, printStock

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = SecurityForm()
    if form.validate_on_submit():
        security = form.security.data
        return redirect(url_for('results', security=security))
    return render_template('index.html',
                           form=form)

@app.route('/results/<security>', methods=['GET', 'POST'])
def results(security):
    sourceCode = pullData(security)
    previewData = sourceCode[:6]
    plotData = printStock(sourceCode)
    return render_template('results.html',
                           security=security,
                           data=previewData)