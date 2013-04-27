# coding: braces

def foo(x, y) {
    return x + y
}

def main() {
    for i in range(10) {
        print "%s, %s" % (i * 2,
            i * 3)
    }
}

if __name__ == '__main__' {
    main()
}
