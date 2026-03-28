"""Plot a classical walk demo on a spiked cycle graph."""

from cw import run_cycle_demo


def main():
    run_cycle_demo(graph_size=12, start=0, duration=15, num_spikes=6)


if __name__ == "__main__":
    main()
