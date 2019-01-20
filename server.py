import gc

from everyclass.api_server import create_app

app = create_app()

# disable gc and freeze
gc.set_threshold(0)  # 700, 10, 10 as default
gc.freeze()


if __name__ == '__main__':
    app = create_app(outside_container=True)
    app.run(
            host='0.0.0.0',
            port=80
    )
