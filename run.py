from application.notifier import app 

def main():
    if not app.config["OS"] == "Windows_NT":
        from application.notifier import notify
        notify()
    app.run(host='localhost', port='5555')


if __name__ == "__main__":
	main()