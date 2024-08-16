import torch
import time

def gpu_test():
    # Check if CUDA (GPU support) is available
    if torch.cuda.is_available():
        device = torch.device("cuda")
        print("GPU is available. Using:", torch.cuda.get_device_name(0))
    else:
        device = torch.device("cpu")
        print("GPU is not available. Using CPU.")

    # Create a large tensor
    size = 50000
    a = torch.randn(size, size, device=device)
    b = torch.randn(size, size, device=device)

    # Warm-up run
    torch.matmul(a, b)

    # Measure time for matrix multiplication
    start_time = time.time()
    for _ in range(100):
        c = torch.matmul(a, b)
    torch.cuda.synchronize()  # Make sure GPU operations are completed
    end_time = time.time()

    print(f"Time taken for 10 iterations: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    gpu_test()
