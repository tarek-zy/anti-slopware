# Examples

## python

`before/orders.py` is the starting point. `easy/`, `medium/` and `hard/` are the result of `/anti-slopware <level>` on it. `test_orders.py` runs against any of them:

```
python3 examples/verify.py
```

## c

`uaf.c` compiles with no warnings under `-Wall -Wextra` and reads freed memory. The C checks find it by running:

```
cc -g -fsanitize=address,undefined -o uaf examples/c/uaf.c && ./uaf
```

AddressSanitizer reports `heap-use-after-free` at the `printf` line.
