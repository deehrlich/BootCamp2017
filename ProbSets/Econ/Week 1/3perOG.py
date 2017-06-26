#Solve for steady state and TPI of 3-period OG model

#Import Libraries
import math
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt

#Houshold Paremeters
"""
yrs_lived  = scalar, number of yeras individua lives
S = scalar, number of periods in the model
nvec = numpy array, labor supply
beta_annual = scalar, annual discount factor
beta = scalr, model discount factor
sigma = scalar >= 1, coefficient of relevant risk aversion
"""
yrs_lived = 60
S = 3
nvec = np.array([1.0, 1.0, 0.2])
beta_annual = 0.96
beta = beta_annual ** (yrs_lived / S)
sigma = 3

#Firm Parameters
"""
alpha = 0 < scalar < 1
A = scalar > 0, TFP
delta_annual = 0 < scalar < 1, annual depreciation rate
delta = 0 < scalar < 1, model depreciation rate
"""
alpha = 0.35
A = 1.0
delta_annual = 0.05
delta =  1 - (1-delta_annual) ** (yrs_lived / S)

#TPI Parameters
"""
T = preiod by which Steady State occurs
TPI_tol = epsilon value for distance between K values
"""
T = int(round(10*S))
TPI_tol = 1e-13
xi = 0.3
Bool_graph = True


def get_r(K, L, params):
    A, alpha, delta = params
    r = alpha * A * ((L/K) ** (1 - alpha)) - delta
    return r

def get_w(K, L, params):
    A, alpha = params
    return (1 - alpha) * A * ((K / L) ** alpha)

def get_K(bvec):
    return bvec.sum()

def get_Y(K, L, params):
    A, alpha = params
    return A * (K ** alpha) * (L ** (1 - alpha))

def get_L(nvec):
    return nvec.sum()

def get_c(bt, btp1, r, w, n):
    c = (1 + r) * bt + w * n - btp1
    return c

def get_Csum(cvec):
    return cvec.sum()

def get_MU(c, sigma):
    MU_c = c ** (-sigma)
    return MU_c

def get_EulErrs(bvec, *args):

    if len(args) !=3:
        b2, b3 = bvec
        beta, sigma, nvec, alpha, A, delta = args
        r_params = [A, alpha, delta]
        w_params = [A, alpha]

        L = get_L(nvec)
        K = get_K(bvec)
        r = get_r(K, L, r_params)
        w = get_w(K, L, w_params)

        c1 = get_c(0.0, b2, 0.0, w, nvec[0])
        c2 = get_c(b2, b3, r, w, nvec[1])
        c3 = get_c(b3, 0.0, r, w, nvec[2])
        MUc1 = get_MU(c1, sigma)
        MUc2 = get_MU(c2, sigma)
        MUc3 = get_MU(c3, sigma)
        error1 = MUc1 - beta * (1 + r) * MUc2
        error2 = MUc2 - beta * (1 + r) * MUc3

    else:
        b2, b3 = bvec
        r, w, b_args = args
        beta, sigma, nvec, alpha, A, delta = b_args
        c1 = get_c(0.0, b2, 0.0, w[0], nvec[0])
        c2 = get_c(b2, b3, r[0], w[1], nvec[1])
        c3 = get_c(b3, 0.0, r[1], w[2], nvec[2])
        MUc1 = get_MU(c1, sigma)
        MUc2 = get_MU(c2, sigma)
        MUc3 = get_MU(c3, sigma)
        error1 = MUc1 - beta * (1 + r[0]) * MUc2
        error2 = MUc2 - beta * (1 + r[1]) * MUc3

    errors = np.array([error1, error2])
    return errors

def get_SS(bvec_init, b_args):

    beta, sigma, nvec, alpha, A, delta = b_args
    r_params = [A, alpha, delta]
    w_params = [A, alpha]

    b_result = opt.root(get_EulErrs, bvec_init, args=(b_args))
    #print(b_result)
    print('Roots: ', b_result.x)

    b_ss = b_result.x
    L_ss = get_L(nvec)
    K_ss = get_K(b_ss)
    r_ss = get_r(K_ss, L_ss, r_params)
    w_ss = get_w(K_ss, L_ss, w_params)
    c1_ss = get_c(0.0, b_ss[0], 0.0, w_ss, nvec[0])
    c2_ss = get_c(b_ss[0], b_ss[1], r_ss, w_ss, nvec[1])
    c3_ss = get_c(b_ss[1], 0.0, r_ss, w_ss, nvec[2])
    cvec_ss = np.array([c1_ss, c2_ss, c3_ss])
    C_ss = get_Csum(cvec_ss)
    Y_ss = get_Y(K_ss, L_ss, w_params)

    ss = (b_ss, L_ss, K_ss, r_ss, w_ss, cvec_ss, C_ss, Y_ss)
    return ss


def get_Kpath_guess(K_init, K_ss, T):
    Kpath = np.linspace(K_init, K_ss, T)
    Kpath = np.append(Kpath, Kpath[T-1])
    return Kpath

def get_bpath(rpath, wpath, bvec_init, b_args):

    bpath = np.zeros((T,2))
    b2 = bvec_init[0]
    b3 = (wpath[0] + (1+rpath[0])*bvec_init[0] - 0.2*wpath[1]*(beta*(1+rpath[1]))**(-1/sigma))/(1+ (1+rpath[1])*(beta*(1+rpath[1]))**(-1/sigma))

    bpath[0] = bvec_init
    bpath[1,1] = b3

    for i in range(1,T-1):
        r = np.array([rpath[i], rpath[i+1]])
        w = np.array([wpath[i-1], wpath[i], wpath[i+1]])
        b_i = opt.root(get_EulErrs, bvec_init, args=(r, w, b_args))
        bpath[i,0] = b_i.x[0]
        bpath[i+1,1] = b_i.x[1]

    return bpath

def TPI_graph(Kpath):
    periods = np.linspace(1, len(Kpath), len(Kpath))
    plt.plot(periods, Kpath)
    plt.xlabel("Period t")
    plt.ylabel("$K_t$")
    plt.title('Time path for $K_t$')
    plt.savefig("TPIgraph.jpeg")
    plt.show()

def get_PathErrs(Kpath, Kprime):
    return math.sqrt(np.sum((Kpath-Kprime)**2))

def get_Kpath(bpath):
    return bpath.sum(axis=1)

def get_TPI(bvec_init, TPI_args, Bool_graph=True):

    beta, sigma, nvec, alpha, A, delta, T, TPI_tol, xi = TPI_args
    r_params = [A, alpha, delta]
    w_params = [A, alpha]

    #Step 1: Find Steady State
    b_args = (beta, sigma, nvec, alpha, A, delta)
    b_ss, L_ss, K_ss, r_ss, w_ss, cvec_ss, C_ss, Y_ss = get_SS(bvec_init, b_args)

    #Step 2: Guess K path
    b2_init = 0.8 * b_ss[0]
    b3_init = 1.1 * b_ss[1]
    bvec_init = np.array([b2_init, b3_init])
    K_init = bvec_init.sum()
    Kpath = get_Kpath_guess(K_init, K_ss, T)
    Kprime = Kpath.copy()

    err_TPI = 1
    iter_num = 0
    L = get_L(nvec)

    while err_TPI > TPI_tol:

        Kpath = xi * Kprime + (1 - xi) * Kpath

        #Step 3: Get HH Decisions and solve for new kpath
        rpath = get_r(Kpath, L, r_params)
        wpath = get_w(Kpath, L, w_params)
        bpath = get_bpath(rpath, wpath, bvec_init, b_args)

        #Step 4: Get new K path and errors
        Kprime  = get_Kpath(bpath)
        err_TPI = get_PathErrs(Kpath, Kprime)
        iter_num += 1

    #Graph
    if Bool_graph == True:
        TPI_graph(Kpath)

    return Kpath, iter_num


"""Problem 1 """
b2_init = 0.10
b3_init = 0.10
bvec_init = np.array([b2_init, b3_init])
b_args = (beta, sigma, nvec, alpha, A, delta)
get_SS(bvec_init, b_args)


"""Problem 2"""
beta = 0.55
b_args = (beta, sigma, nvec, alpha, A, delta)
get_SS(bvec_init, b_args)


"""Problem 3"""
beta = beta_annual ** (yrs_lived / S)
TPI_args = (beta, sigma, nvec, alpha, A, delta, T, TPI_tol, xi)
Kpath, iter_num  = get_TPI(bvec_init, TPI_args, Bool_graph=True)
print("Iterations until convergence:", iter_num)


"""Problem 4"""
TPI_tol = 0.0001
TPI_args = (beta, sigma, nvec, alpha, A, delta, T, TPI_tol, xi)
Kpath, iter_num  = get_TPI(bvec_init, TPI_args, Bool_graph=True)
print("Iterations until convergence:",iter_num)
