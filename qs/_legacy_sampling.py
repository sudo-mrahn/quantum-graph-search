"""Internal compatibility helpers for legacy quantum-search sampling APIs."""

from qs._simulation import sample_probability_series


def sample_marked_probability_series(
    adj_mat,
    node_indices,
    maxss,
    total_steps,
    *,
    step_fn,
    probability_fn,
):
    """
    Run the historical multi-marked-node sampling workflow.
    """

    return sample_probability_series(
        adj_mat,
        node_indices,
        maxss,
        total_steps,
        step_fn=step_fn,
        probability_fn=probability_fn,
    )
