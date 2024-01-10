import autotrading.machine.upbit_machine as upbit_machine
import pprint
import autotrading.db.mongodb_handler as mongodb_handler


m = upbit_machine.UpbitMachine()

h = mongodb_handler.MongoDBHandler("local","coiner_test","price_info")

cursor = h.find_items(h.get_current_db_name(),h.get_current_collection_name(), {})

pprint.pprint(cursor)


