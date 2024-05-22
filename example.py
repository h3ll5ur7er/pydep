from pydep import Consumer, Injectable

class SomeService(Injectable):
    asd = 123

class ProSumer(Injectable):
    __inject__ = [SomeService]

class Instanced(Consumer):
    __inject__ = [ProSumer, SomeService]
    pro_sumer: ProSumer

def test():
    assert Instanced().pro_sumer
    assert ProSumer()
    assert ProSumer()
    assert Instanced().pro_sumer.some_service
    assert Instanced().pro_sumer.some_service.asd == 123
    assert Instanced().pro_sumer.some_service is Instanced().some_service

if __name__ == "__main__":
    test()
