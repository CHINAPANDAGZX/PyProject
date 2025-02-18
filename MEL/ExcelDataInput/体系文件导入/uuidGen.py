import uuid

for _ in range(10):
    print(str(uuid.uuid4()).replace('-', ''))