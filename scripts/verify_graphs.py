#!/usr/bin/env python3
"""Integrity-check every .pt graph in a store by actually loading it.

A size floor is not enough. A network-filesystem write failure once left
qwen3-8b-taboo-04-blue.pt at 256 MB against a 305-322 MB sibling range, so a
200 MB threshold passed a file whose zip central directory was never written.
Only Graph.from_pt tells the truth.

Exit status is 1 when a corrupt file is found and left in place, 0 otherwise.
"""
import argparse
import glob
import os
import sys
from concurrent.futures import ProcessPoolExecutor

import torch

from circuit_tracer.graph import Graph


def check(path):
    """Two artifact kinds share a graph store and they need different loaders.

    `<slug>_graph.pt` is a Graph. `<slug>_graph.pt.baseline.pt` is the baseline
    activation cache the refusal builder writes next to it, a bare torch.save of
    tensors rather than a Graph, so Graph.from_pt raises
    "'Tensor' object has no attribute 'get'" on a perfectly healthy file.

    That false positive was destructive rather than merely noisy. The glob below
    matches anything ending in .pt, so on refusal every sidecar was reported
    CORRUPT and --delete removed it. compute_or_load_graph counts a cache hit
    only when the .pt AND .baseline.pt AND .baseline.json are all present, so a
    single documented "verify before teardown" run would have silently
    invalidated the whole store. ELK never saw it because its builder writes
    no sidecars.

    Both kinds are still checked. Both are bare torch.save writes, so both are
    exposed to the same truncated-footer failure this script exists to catch.
    """
    try:
        if path.endswith(".baseline.pt"):
            torch.load(path, weights_only=False, map_location="cpu")
            return (path, True, f"baseline cache, {os.path.getsize(path) / 2**20:.0f} MB")
        g = Graph.from_pt(path)
        n = int(g.adjacency_matrix.shape[0])
        return (path, True, f"{n} nodes, {os.path.getsize(path) / 2**20:.0f} MB")
    except Exception as e:  # truncated write, bad footer, anything
        return (path, False, f"{type(e).__name__}: {str(e)[:70]}")


def parse_args(argv=None):
    lines = __doc__.strip().split("\n\n")
    parser = argparse.ArgumentParser(
        description=lines[0],
        epilog="\n\n".join(lines[1:]),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("graphs_dir", help="directory holding the *.pt graph store")
    parser.add_argument("--delete", action="store_true",
                        help="remove every file that fails to load")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    d = args.graphs_dir
    delete = args.delete
    files = sorted(glob.glob(os.path.join(d, "*.pt")))
    if not files:
        print(f"no .pt files under {d}")
        return 1

    with ProcessPoolExecutor(16) as ex:
        results = list(ex.map(check, files))

    bad = [r for r in results if not r[1]]
    print(f"checked {len(results)}   ok {len(results) - len(bad)}   CORRUPT {len(bad)}")
    for path, _, why in bad:
        print(f"  CORRUPT {os.path.basename(path)}  {why}")
        if delete:
            os.remove(path)
            print("          deleted")
    return 1 if (bad and not delete) else 0


if __name__ == "__main__":
    sys.exit(main())
