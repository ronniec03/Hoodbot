"""
GPT4All troubleshooting and fixes for common issues
"""

import os
import sys

def fix_cuda_dll_issues():
    """Set environment variables to avoid CUDA DLL loading issues"""
    os.environ['CUDA_VISIBLE_DEVICES'] = ''
    os.environ['OMP_NUM_THREADS'] = '4'
    os.environ['TOKENIZERS_PARALLELISM'] = 'false'
    
def check_gpt4all_installation():
    """Check if GPT4All is properly installed"""
    try:
        import gpt4all
        print(f"✓ GPT4All version: {gpt4all.__version__}")
        return True
    except ImportError:
        print("✗ GPT4All not installed")
        return False
    except Exception as e:
        print(f"✗ GPT4All import error: {e}")
        return False

def test_model_loading():
    """Test basic model loading"""
    try:
        # Fix CUDA issues first
        fix_cuda_dll_issues()
        
        from gpt4all import GPT4All
        
        print("Testing Orca-Mini-3B model loading...")
        model = GPT4All(
            "orca-mini-3b-gguf2-q4_0.gguf",
            device="cpu",
            n_threads=4,
            allow_download=False  # Don't download, just test loading
        )
        print("✓ Model loaded successfully")
        return True
        
    except Exception as e:
        print(f"✗ Model loading failed: {e}")
        return False

if __name__ == "__main__":
    print("GPT4All Troubleshooting Tool")
    print("=" * 40)
    
    # Check installation
    if not check_gpt4all_installation():
        print("\nTry: pip install --upgrade gpt4all")
        sys.exit(1)
    
    # Fix environment
    fix_cuda_dll_issues()
    print("✓ Environment variables set for CPU mode")
    
    # Test model
    if test_model_loading():
        print("\n✓ All tests passed! Your companion should work now.")
    else:
        print("\n✗ Model loading issues detected.")
        print("Try running: launch_cpu.bat")
