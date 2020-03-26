import coroutines
import synchronous


def main():
    coroutines.example_1()
    synchronous.example_1()
    coroutines.example_2()
    synchronous.example_2()
    coroutines.example_3()
    coroutines.example_4()
    coroutines.close_ioloop()


if __name__ == '__main__':
    main()
