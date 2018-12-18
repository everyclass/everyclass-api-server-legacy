from everyclass.api_server import create_app

app = create_app()


if __name__ == '__main__':
    app = create_app(outside_container=True)
    app.run(
            host='0.0.0.0',
            port=80
    )
