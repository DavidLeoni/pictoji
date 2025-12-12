
"""
A P B
A P C
A P D
"""

def G():
  A
  B
  C
  P = [B, C, D, E, N]

class N:
    def __init__(self, _name=None, _parent=None, **kwargs):
        # private bookkeeping
        object.__setattr__(self, "_name", _name)
        object.__setattr__(self, "_parent", _parent)
        # seed public fields
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, name):
        # auto-create child and remember its name & parent
        child = N(_name=name, _parent=self)
        self.__dict__[name] = child
        return child

    def __setattr__(self, name, value):
        if name.startswith("_"):
            # keep internals out of the public dict
            object.__setattr__(self, name, value)
            return
        # auto-convert dicts into Entities (recursive)
        if isinstance(value, dict):
            ent = N(_name=name, _parent=self)
            for k, v in value.items():
                setattr(ent, k, v)
            self.__dict__[name] = ent
        else:
            self.__dict__[name] = value

# --- callable: always return an Entity ---
    def __call__(self, *args, **kwargs):
        child = N(_name="()", _parent=self)
        # keep metadata private to avoid cycles in repr/export
        object.__setattr__(child, "_call_args", args)
        object.__setattr__(child, "_call_kwargs", kwargs)
        return child

    # --- operators: always return an Entity ---
    def _op(self, symbol, other):
        node = N(_name=symbol, _parent=self)
        object.__setattr__(node, "_op_symbol", symbol)
        object.__setattr__(node, "_op_other", other)
        return node

    def __gt__(self, other):   return self._op(">", other)
    def __lt__(self, other):   return self._op("<", other)
    def __lshift__(self, other): return self._op("<<", other)
    def __rshift__(self, other): return self._op(">>", other)

    # optional reflected shifts if Entity is on the right-hand side
    def __rlshift__(self, other): return self._op("<<", other)
    def __rrshift__(self, other): return self._op(">>", other)


    @property
    def path(self) -> str:
        # dotted path from the root (empty for the root itself)
        parts = []
        node = self
        while node is not None and node._name is not None:
            parts.append(node._name)
            node = node._parent
        return ".".join(reversed(parts))

    def to_dict(self):
        # export a pure-Python structure, stripping internals
        def convert(v):
            if isinstance(v, N):
                return {k: convert(val)
                        for k, val in v.__dict__.items()
                        if not k.startswith("_")}
            return v
        return convert(self)

    def __repr__(self):
        # readable, ignore internals
        public = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return f"EN({public})"



e = N()
e.foo.bar.baz = 123
e.system.network.ip = "10.0.0.1"
e.user = {"name": "Alice", "prefs": {"theme": "dark"}}

print(e.foo.bar._name)     # 'bar'
print(e.foo.bar._parent is e.foo)  # True
print(e.user.prefs.path)   # 'user.prefs'
print(e.user.prefs.theme)  # 'dark'
print(e.to_dict())
# {'foo': {'bar': {'baz': 123}}, 'system': {'network': {'ip': '10.0.0.1'}}, 'user': {'name': 'Alice', 'prefs': {'theme': 'dark'}}}


x = e.alpha(1, mode="x").beta      # callable chaining
y = e.left << 3 >> 1 > 0 < 2       # all return Entity instances

print(isinstance(x, N))  # True
print(isinstance(y, N))  # True
print((e.foo > 10).path)      # '>.?'; exact path reflects chained ops from parent
print(e.to_dict())            # exports only public fields

class E(N):
    pass

class G2:
  U = "uuuuu" 
  E = "eeee"
  W = "wwwww"

class G1:
  A = N("aaaa")
  B = N("bbbb")
  C = N("cccc")
  P = E("pppp")
  goes_to = N("goes to")
  Happy_Tom = N()
  hollywood = N("hollywood")

  A.Q = [B, C, G2.U]

  A.P(3) >> [B, C, G2.U]

  A >> P(3) >> [B, C, G2.U]

  A  >>P(3)>> [B, C, G2.U]

  A  >> "b b" >> C
  A  >> "b b,2" >> C
 

  A  >> (b,2) >> C

  A(b,2) >> C

  A << (b,2) >> C

  A << B

  A  >> ("b b",2)  >> C


  N("Happy Tom") >> E("goes to") >> N("Hollywood")


  A.P >> [B, C, G2.U]
  A.P >> B
  A.P >> C
  A.P.C
  "Happy Tom" "goes to" "hollywood"
  
  Happy_Tom . goes_to(231) . hollywood

  Happy_Tom >> goes_to(231) >> hollywood
  
  Happy_Tom >>goes_to(231)>> hollywood
  

  A.P(3) >> [B, C, G2.U]
  A.P(3, [B, C, G2.U])


class G3:
    A : G2
    A = G2.B

"""
with group as G:
  A.P = [B, C, D, E, N]

with group as K:
  X.Y = G


A.P = [] 
A.P += B
A.P += C
A.P += D
A.P += E
A.P += N
"""