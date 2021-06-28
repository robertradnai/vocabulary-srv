from vocabulary_srv import create_app
import os
import shutil

scripts_dir = os.path.dirname(__file__)

shutil.rmtree(os.path.join(scripts_dir, "..", "instance"), ignore_errors=True)
shutil.copytree(os.path.join(scripts_dir, "..", "tests", "testdata"), os.path.join(scripts_dir, "..", "instance", "testdata"))

# Cleaning the database
app = create_app(config_filename=os.path.join(scripts_dir, "testconfig.py"))
runner = app.test_cli_runner()
result = runner.invoke(app.cli.get_command(cmd_name="init-db", ctx=app))
print(result.stdout)

# Running the app
app.run(debug=True)
