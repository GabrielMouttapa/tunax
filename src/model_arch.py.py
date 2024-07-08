"""
Physical model
"""

import equinox as eqx
import jax.numpy as jnp
from grid import Grid
from case import Case
from typing import Dict

class CloCoefs(eqx.Module):
    clo_coef_dico: Dict[str, float]

class State(eqx.Module):
    """
    Define the state at one time step on one grid.
    """
    grid: Grid
    u: jnp.ndarray

    def closure1(self, case, clo_coefs: CloCoefs):
        alpha = clo_coefs.clo_coef_dico['alpha']
        beta = clo_coefs.clo_coef_dico['beta']
        u_np1_c = self.u[1:-1] + alpha*beta*case.dt/(self.grid.hz[1:-1]**2) * (self.u[2:]-2*self.u[1:-1]+self.u[:-2])
        u_np1_l = self.u[0] + alpha*beta*case.dt/(self.grid.hz[0]**2) * (self.u[1]-2*self.u[0])
        u_np1_d = self.u[-1] + alpha*beta*case.dt/(self.grid.hz[-1]**2) * (-2*self.u[-1]+self.u[-2])
        u_np1 = jnp.concatenate([jnp.array([u_np1_l]), u_np1_c, jnp.array([u_np1_d])])
        return State(self.grid, u_np1)
    
    def cost(self, obs):
        return jnp.sum((self.u-obs.u)**2)

class Experience(eqx.Module):
    """
    Define an experiment
    """
    nt: int
    grid: Grid
    state0: State
    case: Case
    clo_coefs: CloCoefs

    def run(self):
        state = self.state0
        for _ in range(self.nt):
            state = state.closure1(self.case, self.clo_coefs)
        return state
model_arch.py