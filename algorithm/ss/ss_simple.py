

from algorithm.simple.gmpy_math import *
from algorithm.pailler.crt_paillier import PaillierKeyPair

def generate_share(data, p_len):
    x0 = get_safe_prime(p_len)
    x1 = sub(data,x0)
    return (x0,x1)



#pailler 乘法三元组的获得
def get_brave_triple(n=32,p_len = 1024):
    #host_1
    a_0,b_0 = get_random_big_num(n),get_random_big_num(n)
    pk, sk = PaillierKeyPair.generate_keypair(n_length=p_len)  # pk send to host_2

    #host_2
    a_1, b_1 = get_random_big_num(n), get_random_big_num(n)
    r = get_random_big_num(n)

    #host_1: a0 b0 encode
    a_0_enc = pk.encrypt(a_0)
    b_0_enc = pk.encrypt(b_0)

    #host_2
    d1 = a_0_enc.mul_scalar(b_1)
    d2 = b_0_enc.mul_scalar(a_1)
    d3 = pk.encrypt(r)
    d = d1.add_encryptnumber(d2).add_encryptnumber(d3)

    #host1
    c_0 = add(mul(a_0, b_0), sk.decrypt(d))
    c_1 = sub(mul(a_1, b_1), r)

    #add
    a = add(a_0,a_1)
    b = add(b_0, b_1)
    c = add(c_0, c_1)


    print("a1:{}, b1:{}".format(a_1, b_1))
    print("a0:{}, b0:{}".format(a_0,b_0))
    print("c0:{}, c1:{}".format(c_0, c_1))
    print("a=a0+a1:{}".format(a))
    print("b=b0+b1:{}".format(b))
    print("c=c0+c1:{}".format(c))
    print("a*b:{}".format(mul(a,b)))
    #a0_enc b0_enc transmit to host_2

    return (a_0,b_0,c_0), (a_1,b_1,c_1)


def ss_add_demo(host_set,guest_set):
    host_data_0, host_data_1 = host_set
    guest_data_0, guest_data_1 = guest_set

    host_gest_0 = add(host_data_0,guest_data_1)
    host_gest_1 = add(host_data_1,guest_data_0)

    host_guset_add = add(host_gest_1,host_gest_0)

    print("host_gest_0:{}".format(host_gest_0))
    print("host_gest_1:{}".format(host_gest_1))
    print("host_guset_add result :{}".format(host_guset_add))

    return host_guset_add



def ss_mul_demo(host_set,guest_set):
    host_data_0, host_data_1 = host_set
    guest_data_0, guest_data_1 = guest_set

    print("triple".center(50,'-'))
    triple_0, triple_1 = get_brave_triple()

    print("mul official".center(50, '-'))
    a_0,b_0,c_0 = triple_0
    a_1,b_1,c_1 = triple_1

    e_0 = (host_data_0, sub(0,a_0))
    e_1 = (host_data_1,sub(0,a_1))
    e = ss_add_demo(e_0,e_1)

    f_0 = (guest_data_0,sub(0,b_0))
    f_1 = (guest_data_1, sub(0, b_1))
    f = ss_add_demo(f_0,f_1)


    z_0_1 = mul(f, a_0)
    z_0_2 = mul(e, b_0)
    z_0 = add(add(z_0_1, z_0_2), c_0)

    z_1_1 = mul(e,f)
    z_1_2 = mul(f, a_1)
    z_1_3 = mul(e, b_1)
    z_1 = add(add(add(z_1_1,z_1_2),z_1_3),c_1)

    z_all = add(z_0,z_1)

    # print(f"a_0:{a_0} b_0:{b_0} c_0:{c_0}")
    # print(f"a_0:{a_1} b_0:{b_1} c_0:{c_1}")
    print("e_0:{};e_1:{}".format(e_0, e_1))
    print("f_0:{};f_1:{}".format(f_0, f_1))
    print("e:{};f:{}".format(e, f))

    print("z_0:{}".format(z_0))
    print("z_1:{}".format(z_1))
    print("z_all:{}".format(z_all))


if __name__ == '__main__':
    d_len=16
    host_data = get_random_big_num(d_len)
    guest_data = get_random_big_num(d_len)
    print("host_data:{}".format(host_data))
    print("guest_data:{}".format(guest_data))
    print("host_data+guest_data:{}".format(add(host_data,guest_data)))
    print("host_data*guest_data:{}".format(mul(host_data,guest_data)))

    print("make share".center(100, '='))
    p_len = 64
    host_data_set = generate_share(host_data, p_len)
    print(f"host_data,{host_data_set}")
    guest_data_set = generate_share(guest_data, p_len)
    print(f"guest_data,{guest_data_set}")

    # ss add demo
    print("add".center(100,'='))
    ss_add_demo(host_data_set, guest_data_set)

    print("mul".center(100,'='))
    ss_mul_demo(host_data_set, guest_data_set)

    # # print(add(host_data_0, host_data_1))
    # print("share add".center(100,'='))
    # join_0 = add(host_data_0,guest_data_0)
    # print(f"host_data_0+guest_data_0:{join_0}")
    # join_1 = add(host_data_1,guest_data_1)
    # print(f"host_data_1+guest_data_1:{join_1}")
    # print(f"host_data+guest_data:{join_1+join_0}")





