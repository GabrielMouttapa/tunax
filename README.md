# Description
This package is a framework to calibration physical closures of the vertical components of global ocean models. The closures are called by a one dimentional column model (`src/model.py`), the closures are located in `src/closres/`. The parameters of these closures are calibrated using the "observations" in the folder `obs/`, typically the observations are outputs of LES ('Large Eddy Simulations'). The code is written in jax to obtain the differentiability.

# Example of use
One can find an example of simple usage of the code in `notebooks/k-epsilon_Kato-Phillips` : this shows the calibration of one parameter of $k-\varepsilon$ with a perfect model based on the idealized case of Kato-Phillips.