from flask import Flask, render_template, request, redirect
from core.deployment import Deployment

app = Flask(__name__)

@app.route('/new')
def new_deployment():
    return render_template('new.html')

@app.route('/result', methods=['POST'])
def deploy():
    app_name = request.form.get('appname')
    repo_url = request.form.get('repourl')
    num_threads = request.form.get('numthreads')
    user_app = Deployment(app_name, repo_url, num_threads)
    config = user_app.initialize()
    url = user_app.run(config)
    return redirect(url)

if __name__ == '__main__':
    app.run()   