from vocabulary_srv import create_app
import os
import shutil

scripts_dir = os.path.dirname(__file__)

shutil.rmtree(os.path.join(scripts_dir, "..", "instance"), ignore_errors=True)
shutil.copytree(os.path.join(scripts_dir, "..", "tests", "testdata"),
                os.path.join(scripts_dir, "..", "instance"))
shutil.copy(os.path.join(scripts_dir, "testconfig.py"),
            os.path.join(scripts_dir, "..", "instance", "config.py"))

os.chdir(os.path.join(scripts_dir, "..", "instance"))
os.environ["FLASK_ENV"] = "development"

app = create_app()
runner = app.test_cli_runner()
result = runner.invoke(app.cli.get_command(cmd_name="init-db", ctx=app))
print(f"Result of init-db: {result}")
print(result.stdout)

if result.exit_code != 0:
    print("init-db had non-zero return status, terminating...")
    import sys; sys.exit()

# Running the app
app.run(use_reloader=False) 
# TODO Find a better fix: app doesn't start with reloader
# when called with make
