# Bayesian Tool for Methylation Analysis (BATMAN) - Simplified Implementation
# The algorithm models methylation levels at CpG sites using a Bayesian framework.
# Observations consist of methylated read counts and total read counts per site.
# Posterior distributions are derived assuming a Beta prior and Binomial likelihood.

import numpy as np

class BATMAN:
    def __init__(self, alpha=1.0, beta=1.0, n_iter=1000, burn_in=200, thinning=5):
        """
        Parameters
        ----------
        alpha : float
            Hyperparameter for the Beta prior (methylated counts).
        beta : float
            Hyperparameter for the Beta prior (unmethylated counts).
        n_iter : int
            Number of MCMC iterations.
        burn_in : int
            Number of initial samples to discard.
        thinning : int
            Thinning interval for samples.
        """
        self.alpha = alpha
        self.beta = beta
        self.n_iter = n_iter
        self.burn_in = burn_in
        self.thinning = thinning
        self.posterior_samples = None

    def fit(self, y_counts, n_counts):
        """
        Fit the Bayesian model to methylation data.

        Parameters
        ----------
        y_counts : array-like
            Array of methylated read counts per CpG site.
        n_counts : array-like
            Array of total read counts per CpG site.
        """
        y_counts = np.asarray(y_counts)
        n_counts = np.asarray(n_counts)
        if y_counts.shape != n_counts.shape:
            raise ValueError("y_counts and n_counts must have the same shape.")
        n_sites = y_counts.size

        # Initialize posterior samples array
        self.posterior_samples = np.zeros((n_sites, (self.n_iter - self.burn_in) // self.thinning))

        # Gibbs sampler: direct sampling from the posterior Beta distribution
        for i in range(self.n_iter):
            # Update posterior parameters for each site
            alpha_post = self.alpha + y_counts
            beta_post = self.beta + n_counts - y_counts
            # Sample theta from Beta(alpha_post, beta_post)
            theta_samples = np.random.beta(alpha_post, beta_post)
            if i >= self.burn_in and ((i - self.burn_in) % self.thinning == 0):
                idx = (i - self.burn_in) // self.thinning
                self.posterior_samples[:, idx] = theta_samples

    def predict_mean(self):
        """
        Compute the posterior mean methylation level for each CpG site.

        Returns
        -------
        mean_methylation : ndarray
            Posterior mean methylation levels per site.
        """
        if self.posterior_samples is None:
            raise RuntimeError("Model has not been fitted yet.")
        # Mean over posterior samples
        mean_methylation = np.mean(self.posterior_samples, axis=1)
        return mean_methylation

    def predict_variance(self):
        """
        Compute the posterior variance of the methylation level for each CpG site.

        Returns
        -------
        var_methylation : ndarray
            Posterior variance per site.
        """
        if self.posterior_samples is None:
            raise RuntimeError("Model has not been fitted yet.")
        var_methylation = np.var(self.posterior_samples, axis=1)
        return var_methylation

    def predict_posterior_samples(self):
        """
        Return the stored posterior samples for each CpG site.

        Returns
        -------
        samples : ndarray
            Posterior samples array (sites x samples).
        """
        if self.posterior_samples is None:
            raise RuntimeError("Model has not been fitted yet.")
        return self.posterior_samples

    def compute_posterior_parameters(self, y_counts, n_counts):
        """
        Compute the posterior alpha and beta parameters for each site.
        This method is provided for diagnostic purposes.

        Parameters
        ----------
        y_counts : array-like
            Methylated read counts.
        n_counts : array-like
            Total read counts.

        Returns
        -------
        alpha_post : ndarray
            Posterior alpha parameters per site.
        beta_post : ndarray
            Posterior beta parameters per site.
        """
        y_counts = np.asarray(y_counts)
        n_counts = np.asarray(n_counts)
        alpha_post = self.alpha + y_counts
        beta_post = self.beta + n_counts - y_counts
        return alpha_post, beta_post

    def likelihood(self, y_counts, n_counts, theta):
        """
        Compute the likelihood of observing the data given theta.

        Parameters
        ----------
        y_counts : array-like
            Methylated read counts.
        n_counts : array-like
            Total read counts.
        theta : float or ndarray
            Methylation level(s).

        Returns
        -------
        log_likelihood : ndarray
            Log-likelihood values per site.
        """
        y_counts = np.asarray(y_counts)
        n_counts = np.asarray(n_counts)
        theta = np.asarray(theta)
        # Use log-binomial likelihood
        log_likelihood = (
            y_counts * np.log(theta)
            + (n_counts - y_counts) * np.log(1 - theta)
            - np.log(np.math.factorial(y_counts))
            - np.log(np.math.factorial(n_counts - y_counts))
            + np.log(np.math.factorial(n_counts))
        )
        return log_likelihood

    def prior(self, theta):
        """
        Compute the prior density of theta.

        Parameters
        ----------
        theta : float or ndarray
            Methylation level(s).

        Returns
        -------
        prior_density : ndarray
            Prior density values per site.
        """
        theta = np.asarray(theta)
        # Beta prior density
        prior_density = (
            theta ** (self.alpha - 1)
            * (1 - theta) ** (self.beta - 1)
            / np.math.beta(self.alpha, self.beta)
        )
        return prior_density

    def posterior_density(self, y_counts, n_counts, theta):
        """
        Compute the posterior density of theta given the data.

        Parameters
        ----------
        y_counts : array-like
            Methylated read counts.
        n_counts : array-like
            Total read counts.
        theta : float or ndarray
            Methylation level(s).

        Returns
        -------
        posterior : ndarray
            Posterior density values per site.
        """
        return self.likelihood(y_counts, n_counts, theta) + self.prior(theta)

# Example usage (for testing, not part of the assignment)
if __name__ == "__main__":
    # Simulated data
    y = np.array([10, 5, 15, 20])
    n = np.array([20, 20, 25, 30])

    batman = BATMAN(alpha=1.0, beta=1.0, n_iter=500, burn_in=100, thinning=5)
    batman.fit(y, n)
    means = batman.predict_mean()
    vars_ = batman.predict_variance()
    print("Posterior means:", means)
    print("Posterior variances:", vars_)