from show_result import create_app, db

import flask_script
import flask_migrate

# 创建一个app对象
app = create_app("product")
manager = flask_script.Manager(app)

flask_migrate.Migrate(app, db)
manager.add_command("db", flask_migrate.MigrateCommand)

if __name__ == "__main__":
    manager.run()