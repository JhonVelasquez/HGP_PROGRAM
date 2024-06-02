from hgp import *


url_sqlite = "sqlite:///./db/hgp.db"
url_mysql = "mysql+pymysql://root:R0ck0!@localhost:3306/hgp_dev"

controllerHGP = Controller(failback_path = url_sqlite)
#controllerHGP.setDB(db_hgp)

#controllerHGP.test_db_dunctions()

controllerHGP.init_visual_main()

