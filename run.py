# run "python ./run.py" to run the server

from cf_tracker import create_app


def main():
    app = create_app()
    app.run(debug=True)  # run with debug mode turned on


if __name__ == "__main__":
    main()
