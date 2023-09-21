import argparse


def fast_pow(x: int, y: int) -> float:
    if y == 0:
        return 1
    if y == -1:
        return 1. / x
    p = fast_pow(x, y // 2)
    p *= p
    if y % 2:
        p *= x
    return p


def prime_checker(number: int) -> bool:
    if number < 1:
        return False
    elif number > 1:
        if number == 2:
            return True
        for i in range(2, number):
            return number % i != 0


def primitive_check(g: int, p: int, roots: list[int]) -> bool:
    for i in range(1, p):
        roots.append(pow(g, i) % p)
    for i in range(1, p):
        if roots.count(i) > 1:
            roots.clear()
            return False
        return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p")
    parser.add_argument("-a")
    parser.add_argument("-Xa")
    parser.add_argument("-Yb")
    parser.add_argument("-k")
    args = parser.parse_args()

    roots = []
    # if not prime_checker(args.p):
    #     print("Number Is Not Prime, Please Enter Again!")
    #
    # if primitive_check(G, P, l) == -1:
    #     print(f"Number Is Not A Primitive Root Of {P}, Please Try Again!")
    #     continue
    #     break
    #
    # # Private Keys
    # x1, x2 = int(input("Enter The Private Key Of User 1 : ")), int(
    #     input("Enter The Private Key Of User 2 : ")
    # )
    # while 1:
    #     if x1 >= P or x2 >= P:
    #         print(f"Private Key Of Both The Users Should Be Less Than {P}!")
    #         continue
    #     break
    #
    # # Calculate Public Keys
    # y1, y2 = pow(G, x1) % P, pow(G, x2) % P
    #
    # # Generate Secret Keys
    # k1, k2 = pow(y2, x1) % P, pow(y1, x2) % P
    #
    # print(f"\nSecret Key For User 1 Is {k1}\nSecret Key For User 2 Is {k2}\n")
    #
    # if k1 == k2:
    #     print("Keys Have Been Exchanged Successfully")
    # else:
    #     print("Keys Have Not Been Exchanged Successfully")
