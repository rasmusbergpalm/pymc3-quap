import arviz as az
import numpy as np
import scipy
import pymc3 as pm


def quap(vars, n_samples=10_000):
    """Finds the quadratic approximation to the posterior, also known as the Laplace approximation.

    NOTE: The quadratic approximation only works well for unimodal and roughly symmetrical posteriors of continuous variables.
    The usual MCMC convergence and mixing statistics (e.g. R-hat, ESS) will NOT tell you anything about how well this approximation fits your actual (unknown) posterior, indeed they'll always be extremely nice since all samples are from exactly the same distribution, the posterior quadratic approximation.
    Use at your own risk.

    See Chapter 4 of "Bayesian Data Analysis" 3rd edition for background.

    Returns an arviz.InferenceData object for compatibility by sampling from the approximated quadratic posterior. Note these are NOT MCMC samples.

    Also returns the exact posterior approximation as a scipy.stats.multivariate_normal distribution.

    Parameters
    ----------
    vars: list
        List of variables to approximate the posterior for.
    n_samples: int
        How many samples to sample from the approximate posterior.

    Returns
    -------
    arviz.InferenceData:
        InferenceData with samples from the approximate posterior
    scipy.stats.multivariate_normal:
        Multivariate normal posterior approximation
    """
    map = pm.find_MAP(vars=vars)
    H = pm.find_hessian(map, vars=vars)
    cov = np.linalg.inv(H)
    mean = np.concatenate([np.atleast_1d(map[v.name]) for v in vars])
    posterior = scipy.stats.multivariate_normal(mean=mean, cov=cov)
    draws = posterior.rvs(n_samples)[np.newaxis, ...]
    samples = {}
    i = 0
    for v in vars:
        var_size = map[v.name].size
        samples[v.name] = draws[:, :, i: i + var_size]
        if var_size == 1:
            samples[v.name] = samples[v.name].squeeze(axis=-1)
        i += var_size
    return az.convert_to_inference_data(samples), posterior
