import os
import tensorflow as tf
from train_model import build_model

try:
    print("Building model architecture locally...")
    model = build_model(10)  # 10 classes
    
    print("Loading weights from model.h5...")
    model.load_weights('model.h5', by_name=True, skip_mismatch=True)
    
    print("Weights loaded successfully!")
    print("Saving native Keras 2 model...")
    model.save('model_fixed.h5')
    print("Saved as model_fixed.h5")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
