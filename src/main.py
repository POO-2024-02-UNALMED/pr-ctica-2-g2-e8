from app.database.Repository import Repository
from app.classes.WithId import WithId

if __name__ == "__main__":
    Repository.create_temp_directory()
    Repository.set_debug_mode(True)

    class Test(WithId):
        def __init__(self, id):
            super().__init__(id)

    test = Test("test")
    Repository.save(test)
    test = Repository.load("Test", "test")
    print(test.get_id())