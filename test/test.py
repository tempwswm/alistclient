import alist.client

client = alist.client.Client("http://127.0.0.1:5244", "admin", "admin", )
client.login()
for i in client.list("/local"):
    print(i)
client.mkdir("/local/test1")
client.mkdir("/local/test2")
client.mkdir("/local/test3")
client.rename("test4", "/local/test2")
client.remove("/local", ["test3"])
info = client.get("/local/a/b.jpg")
print(info)
for i in client.list_setting(0):
    print(i)
for i in client.list_user():
    print(i)
for i in client.list_storage():
    print(i)
print(client.get_storage(1))
client.list_driver()
