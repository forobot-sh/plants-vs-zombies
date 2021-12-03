import turtle

if __name__ == '__main__':
    a_list = [1, 2, 3, 4, 6, 5, 3]
    # print(a_list + a_list)
    # print(a_list * 2)
    # print(a_list[2:])
    # print(a_list[:3])
    # print(a_list[-1])
    # if 'b' in a_list:
    #     a_list.remove('b')
    # print('b' in a_list)
    # print(1 in a_list)
    # a_list.append(8)
    # print(a_list)
    a_list.sort()
    print(a_list)
    # a_list.reverse()
    # print(a_list)
    # print(a_list.index(3))
    a_list.remove(3)
    # print(a_list)
    t = turtle.Turtle()

    turtle.setup(650, 350, 200, 200)
    turtle.penup()
    turtle.fd(-250)
    turtle.pendown()
    turtle.color("purple")
    turtle.pensize(25)
    turtle.seth(-40)
    for i in range(4):
        turtle.circle(40, 80)
        turtle.circle(-40, 80)
    turtle.circle(40, 80 / 2)
    turtle.fd(40)
    turtle.circle(16, 180)
    turtle.fd(40 * 2 / 3)
    turtle.done()
