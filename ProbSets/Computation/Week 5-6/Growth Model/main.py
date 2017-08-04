#======================================================================
#
#     This routine solves an infinite horizon growth model
#     with dynamic programming and sparse grids
#
#     The model is described in Scheidegger & Bilionis (2017)
#     https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2927400
#
#     external libraries needed:
#     - IPOPT (https://projects.coin-or.org/Ipopt)
#     - PYIPOPT (https://github.com/xuy/pyipopt)
#     - TASMANIAN (http://tasmanian.ornl.gov/)
#
#     Simon Scheidegger, 11/16 ; 07/17
#======================================================================

import nonlinear_solver_initial as solver     #solves opt. problems for terminal VF
import nonlinear_solver_iterate as solviter   #solves opt. problems during VFI
from parameters import *                      #parameters of model
import interpolation as interpol              #interface to sparse grid library/terminal VF
import interpolation_iter as interpol_iter    #interface to sparse grid library/iteration
import postprocessing as post                 #computes the L2 and Linfinity error of the model

import TasmanianSG                            #sparse grid library
import numpy as np


#======================================================================
# Start with Value Function Iteration

# terminal value function
valnew = [TasmanianSG.TasmanianSparseGrid()]*5
if (numstart==0):
    for i in range(len(theta)):
        valnew[i] = interpol.sparse_grid(n_agents, iDepth)
        valnew[i].write("valnew_1." + str(numstart) + "_" + str(theta[i]) + ".txt") #write file to disk for restart

# value function during iteration
else:
    for i in range(len(theta)):
        valnew[i].read("valnew_1." + str(numstart) + "_" + str(theta[i])  + ".txt")  #write file to disk for restart

valold = [TasmanianSG.TasmanianSparseGrid()]*5
valold=valnew

for i in range(numstart, numits):
    valnew=[TasmanianSG.TasmanianSparseGrid()]*5
    for j in range(len(theta)):
        valnew[j]=interpol_iter.sparse_grid_iter(n_agents, iDepth, valold, theta_range[j])
        valold[j]=valnew[j]
        valnew[j].write("valnew_1." + str(j+1) + ".txt")


#======================================================================
print "==============================================================="
print " "
print " Computation of a growth model of dimension ", n_agents ," finished after ", numits, " steps"
print " "
print "==============================================================="
#======================================================================

# compute errors
avg_err=post.ls_error(n_agents, numstart, numits, No_samples)

#======================================================================
print "==============================================================="
print " "
print " Errors are computed -- see errors.txt"
print " "
print "==============================================================="
#======================================================================
