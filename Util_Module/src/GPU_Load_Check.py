import torch

def gpu_load_check():
    print("PyTorch Version:", torch.__version__)
    print("CUDA Available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("Device Name:", torch.cuda.get_device_name(0))
        print("CUDA Version:", torch.version.cuda)

if __name__ == '__main__':
    gpu_load_check()