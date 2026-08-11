import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import shutil

# 1. Define classes and directories
DATA_DIR = "data/IMG_CLASSES"
MODEL_SAVE_PATH = "model.h5"

def build_model(num_classes):
    print("Building MobileNetV2 Transfer Learning Model...")
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Freeze the base model
    base_model.trainable = False
    
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2)(x)
    x = Dense(128, activation='relu')(x)
    predictions = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=predictions)
    # Compile
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), 
                  loss='categorical_crossentropy', 
                  metrics=['accuracy'])
    return model

def main():
    if not os.path.exists(DATA_DIR):
        print(f"Dataset directory not found at {DATA_DIR}. Please place your IMG_CLASSES folder inside the data folder.")
        return

    # ImageDataGenerators with augmentation and validation split
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest',
        validation_split=0.2 # 20% for validation
    )

    batch_size = 32 # Suitable for GTX 1650 4GB

    train_generator = datagen.flow_from_directory(
        directory=DATA_DIR,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training'
    )

    val_generator = datagen.flow_from_directory(
        directory=DATA_DIR,
        target_size=(224, 224),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation'
    )

    num_classes = len(train_generator.class_indices)
    print(f"Found {num_classes} classes: {train_generator.class_indices}")

    model = build_model(num_classes)
    
    # Save class indices to json for inference
    import json
    with open('class_indices.json', 'w') as f:
        json.dump(train_generator.class_indices, f)
    
    print("Starting training (this may take a while)...")
    epochs = 50 # Increased to 50 for better accuracy
    
    # Adding Early Stopping to save time
    from tensorflow.keras.callbacks import EarlyStopping
    early_stop = EarlyStopping(
        monitor='val_accuracy', 
        patience=5,               # Will wait 5 epochs to see if it improves
        restore_best_weights=True # Keeps the weights of the best epoch
    )
    
    model.fit(
        train_generator,
        epochs=epochs,
        validation_data=val_generator,
        callbacks=[early_stop]
    )

    print(f"Saving model to {MODEL_SAVE_PATH}...")
    model.save(MODEL_SAVE_PATH)
    print("Training complete! You can now run the Streamlit app.")

if __name__ == '__main__':
    # Warn user about missing GPU usage optimization
    print("Checking GPUs...")
    print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
    main()
