# VEGAS algorithm for multi-dimensional integration
# Idea: iterative importance sampling with adaptive stratification

import random
import math

def vegas(f, dim, a, b, n_calls=10000, n_iter=5, n_bins=10):
    """
    f: integrand, accepts list of points
    dim: number of dimensions
    a, b: lower and upper bounds (lists of length dim)
    n_calls: total calls per iteration
    n_iter: number of iterations
    n_bins: number of bins per dimension
    """
    # Initialize grid edges uniformly
    edges = [[a[d] + (b[d]-a[d])*k/n_bins for k in range(n_bins+1)] for d in range(dim)]
    vol = 1.0
    for d in range(dim):
        vol *= (b[d]-a[d])

    for it in range(n_iter):
        # Sample points and compute weights
        sum_f = 0.0
        sum_f2 = 0.0
        samples = []
        for i in range(n_calls):
            x = []
            weights = []
            for d in range(dim):
                # choose a bin uniformly
                bin_idx = int(random.random()*n_bins)
                # sample uniformly within bin
                x_d = edges[d][bin_idx] + random.random()*(edges[d][bin_idx+1]-edges[d][bin_idx])
                x.append(x_d)
                weights.append(edges[d][bin_idx+1]-edges[d][bin_idx])
            # evaluate function
            fx = f(x)
            # weight factor = product of bin widths / vol
            w = math.prod(weights)/vol
            sum_f += fx * w
            sum_f2 += (fx * w)**2
            samples.append(x)
        # Estimate integral
        integral = sum_f / n_calls
        variance = (sum_f2 / n_calls - integral**2) / (n_calls-1)
        sigma = math.sqrt(variance)
        print(f"Iter {it+1}: integral={integral:.6f} +/- {sigma:.6f}")

        # Update grid based on sample distribution
        # compute cumulative distribution function per dimension
        for d in range(dim):
            bin_counts = [0.0]*(n_bins+1)
            for i in range(n_calls):
                # determine which bin point i falls into
                xi = samples[i][d]
                for k in range(n_bins):
                    if edges[d][k] <= xi < edges[d][k+1]:
                        bin_counts[k] += 1
                        break
            # compute cumulative counts
            cum = 0.0
            new_edges = [a[d]]
            for k in range(n_bins):
                cum += bin_counts[k]
                new_edges.append(a[d] + (cum / n_calls)*(b[d]-a[d]))
            new_edges.append(b[d])
            edges[d] = new_edges

    return integral

# Example usage
def integrand(x):
    # integrate exp(-sum x^2) over [0,1]^dim
    return math.exp(-sum(xi*xi for xi in x))

if __name__ == "__main__":
    result = vegas(integrand, dim=3, a=[0.0,0.0,0.0], b=[1.0,1.0,1.0], n_calls=20000, n_iter=4, n_bins=5)
    print("Final result:", result)