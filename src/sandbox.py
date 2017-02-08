class Num(object):
    def __init__(self,val):
        self.val = val

    def __eq__(self, other):
        return self.val == other.val

nums = [ Num(1), Num(2), Num(3), Num(4), Num(1) ]


print(Num(6) in nums)
print(Num(4) ==  Num(4))
