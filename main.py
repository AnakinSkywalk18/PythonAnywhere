from mysite import create_app

app = create_app()

# Only Executes if File is Run
if __name__ == '__main__':
    app.run(debug=True)