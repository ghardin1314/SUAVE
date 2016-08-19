# converge_root.py
# 
# Created:  Jul 2014, SUAVE Team
# Modified: Aug 2016, T. MacDonald
#
# Added scipy.optimize.root

# ----------------------------------------------------------------------
#  Imports
# ----------------------------------------------------------------------

import scipy.optimize
import numpy as np

from SUAVE.Core.Arrays import array_type

# ----------------------------------------------------------------------
#  Converge Root
# ----------------------------------------------------------------------

def converge_root(segment,state):
    
    unknowns = state.unknowns.pack_array()
    
    try:
        root_finder = segment.settings.root_finder
    except AttributeError:
        root_finder = scipy.optimize.fsolve
    
        
    if root_finder == scipy.optimize.fsolve:
        
        unknowns,infodict,ier,msg = root_finder( iterate,
                                                 unknowns,
                                                 args = [segment,state],
                                                 xtol = state.numerics.tolerance_solution,
                                                 full_output=1)    
        if ier!=1:
            print "Segment did not converge. Segment Tag: " + segment.tag
            print "Error Message:\n" + msg
            segment.state.numerics.converged = False
        else:
            segment.state.numerics.converged = True
            
            

    elif root_finder == scipy.optimize.root:        
    
        sol = root_finder(  iterate,
                            unknowns,
                            args = [segment,state],
                            tol = state.numerics.tolerance_solution,
                            method='lm') 
        if sol.success != True:
            print "Segment did not converge. Segment Tag: " + segment.tag
            print "Message: " + sol.message   
            segment.state.numerics.converged = False
        else:
            segment.state.numerics.converged = True
         
    else:
        raise ValueError('Selected root finder is not supported.')
                            
    return
    
# ----------------------------------------------------------------------
#  Helper Functions
# ----------------------------------------------------------------------
    
def iterate(unknowns,(segment,state)):

    if isinstance(unknowns,array_type):
        state.unknowns.unpack_array(unknowns)
    else:
        state.unknowns = unknowns
        
    segment.process.iterate(segment,state)
    
    residuals = state.residuals.pack_array()
        
    return residuals 