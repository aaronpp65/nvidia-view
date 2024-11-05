# python gpu_test.py --size 50000 --n 100

import torch
import time
import argparse

def gpu_test(size: int = 50000, n: int = 100) -> None:
    """
    Function to run matrix multiplication on GPU.
    size: size of the square matrix
    n: number of iterations to perform matrix multiplication
    """
    # Check if CUDA (GPU support) is available
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("GPU is available. Using:", torch.cuda.get_device_name(0))
    else:
        device = torch.device("cpu")
        print("GPU is not available. Using CPU.")

    # Create a large tensor
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)

    # Warm-up run
    torch.matmul(a, b)

    # Measure time for matrix multiplication
    start_time = time.time()
    for _ in range(n):
        c = torch.matmul(a, b)
    torch.cuda.synchronize()  # Make sure GPU operations are completed
    end_time = time.time()

    print(f"Time taken for {n} iterations: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run matrix multiplication on GPU.")
    parser.add_argument("--size", type=int, required=True, help="Size of the square matrix")
    parser.add_argument("--n", type=int, required=True, help="Number of iterations to perform matrix multiplication")
    args = parser.parse_args()

    gpu_test(args.size, args.n)
