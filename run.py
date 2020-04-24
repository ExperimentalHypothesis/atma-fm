from application.notifier import app, notify 

def main():
    notify()
    app.run(host='localhost', port='5555')


if __name__ == "__main__":
	main()