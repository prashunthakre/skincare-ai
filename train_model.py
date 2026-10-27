"""
Full All-Rounder Fitzpatrick 17k Multi-Disease Dataset Downloader & Fast Feature-Transfer Trainer
=================================================================================================
Downloads all live clinical images across ALL Fitzpatrick 17k disease classes (Skin Tones I-VI),
merges existing project sample classes, extracts MobileNetV2 deep features, trains a 90+ class
All-Rounder dermatology classifier for 60 epochs with balanced class weighting, and saves the
end-to-end Grad-CAM-compatible model to `backend/model.h5` and `backend/class_indices.json`.
"""
import os
import io
import json
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import pandas as pd
from PIL import Image

CSV_PATH = os.path.join("data", "fitzpatrick17k", "fitzpatrick17k.csv")
ALL_DATA_DIR = os.path.join("data", "fitzpatrick17k_all_classes")
SAMPLE_DIR = "sample_test_images"
MODEL_PATH = os.path.join("backend", "model.h5")
CLASS_INDICES_PATH = os.path.join("backend", "class_indices.json")


def format_disease_name(raw_label: str) -> str:
    """Formats raw Fitzpatrick 17k lowercase label into clean clinical title case."""
    clean = raw_label.strip()
    special_map = {
        "basal cell carcinoma": "Basal Cell Carcinoma",
        "basal cell carcinoma morpheiform": "Basal Cell Carcinoma (Morpheiform)",
        "solid cystic basal cell carcinoma": "Basal Cell Carcinoma (Solid Cystic)",
        "squamous cell carcinoma": "Squamous Cell Carcinoma",
        "melanoma": "Melanoma",
        "malignant melanoma": "Melanoma",
        "superficial spreading melanoma ssm": "Melanoma (Superficial Spreading)",
        "eczema": "Eczema",
        "dyshidrotic eczema": "Dyshidrotic Eczema",
        "allergic contact dermatitis": "Allergic Contact Dermatitis",
        "seborrheic dermatitis": "Seborrheic Dermatitis",
        "perioral dermatitis": "Perioral Dermatitis",
        "atopic dermatitis": "Atopic Dermatitis",
        "psoriasis": "Psoriasis",
        "pustular psoriasis": "Pustular Psoriasis",
        "lichen planus": "Lichen Planus",
        "acne": "Acne Vulgaris",
        "acne vulgaris": "Acne Vulgaris",
        "folliculitis": "Folliculitis",
        "vitiligo": "Vitiligo",
        "urticaria": "Urticaria (Hives)",
        "scabies": "Scabies",
        "actinic keratosis": "Actinic Keratosis",
        "seborrheic keratosis": "Seborrheic Keratoses",
        "dermatofibroma": "Dermatofibroma",
        "keloid": "Keloid",
        "rosacea": "Rosacea",
        "lupus erythematosus": "Lupus Erythematosus",
        "pityriasis rosea": "Pityriasis Rosea",
        "pityriasis rubra pilaris": "Pityriasis Rubra Pilaris",
        "granuloma annulare": "Granuloma Annulare",
        "erythema multiforme": "Erythema Multiforme",
        "mycosis fungoides": "Mycosis Fungoides (Cutaneous Lymphoma)",
        "kaposi sarcoma": "Kaposi Sarcoma",
        "neurofibromatosis": "Neurofibromatosis",
        "prurigo nodularis": "Prurigo Nodularis",
        "tungiasis": "Tungiasis",
        "nematode infection": "Cutaneous Nematode Infection",
        "pediculosis lids": "Pediculosis",
        "sarcoidosis": "Cutaneous Sarcoidosis",
        "scleroderma": "Scleroderma",
        "photodermatoses": "Photodermatoses",
        "hailey hailey disease": "Hailey-Hailey Disease",
        "dariers disease": "Darier Disease",
        "porokeratosis actinic": "Actinic Porokeratosis",
    }
    if clean.lower() in special_map:
        return special_map[clean.lower()]
    return clean.title()


def download_worker(task):
    url, dest_path = task
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000:
        return True
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            img_bytes = resp.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        img = img.resize((224, 224), Image.Resampling.LANCZOS)
        img.save(dest_path, "JPEG", quality=90)
        return True
    except Exception:
        return False


def download_all_fitzpatrick_classes():
    df = pd.read_csv(CSV_PATH)
    # All live Atlas Dermatologico URLs across all Fitzpatrick 17k classes (3,905 images across 91 diseases)
    atlas_df = df[df["url"].notna() & df["url"].str.contains("atlas", case=False)].copy()
    atlas_df["clean_class"] = atlas_df["label"].apply(format_disease_name)

    os.makedirs(ALL_DATA_DIR, exist_ok=True)

    # Also copy existing curated project images from data/IMG_CLASSES and sample_test_images
    sample_map = {
        "1_Eczema": "Eczema",
        "2_Melanocytic_Nevi": "Melanocytic Nevi",
        "3_Psoriasis": "Psoriasis",
        "4_Basal_Cell_Carcinoma": "Basal Cell Carcinoma",
        "5_Fungal_Infections": "Fungal Infections (Tinea)",
        "6_Viral_Warts": "Viral Infections (Warts)",
    }
    if os.path.exists(SAMPLE_DIR):
        for s_folder, c_name in sample_map.items():
            src_d = os.path.join(SAMPLE_DIR, s_folder)
            dst_d = os.path.join(ALL_DATA_DIR, c_name)
            os.makedirs(dst_d, exist_ok=True)
            if os.path.exists(src_d):
                for f in os.listdir(src_d):
                    if f.lower().endswith((".jpg", ".jpeg", ".png")):
                        shutil.copy2(os.path.join(src_d, f), os.path.join(dst_d, f"curated_{f}"))

    tasks = []
    for _, row in atlas_df.iterrows():
        c_name = row["clean_class"]
        c_dir = os.path.join(ALL_DATA_DIR, c_name)
        os.makedirs(c_dir, exist_ok=True)
        md5 = row["md5hash"]
        st_scale = row["fitzpatrick_scale"]
        dest = os.path.join(c_dir, f"fitz_st{st_scale}_{md5[:10]}.jpg")
        tasks.append((row["url"], dest))

    print(f"Downloading/verifying {len(tasks)} Fitzpatrick 17k clinical images across {atlas_df['clean_class'].nunique()} diseases using 40 threads...")
    ok = 0
    with ThreadPoolExecutor(max_workers=40) as ex:
        futures = [ex.submit(download_worker, t) for t in tasks]
        for idx, fut in enumerate(as_completed(futures), 1):
            if fut.result():
                ok += 1
            if idx % 500 == 0 or idx == len(tasks):
                print(f"  Progress: {idx}/{len(tasks)} processed ({ok} valid images ready)...")

    print(f"Total verified clinical images across all classes: {ok}")


def train_allrounder_model():
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
    from tensorflow.keras.models import Model
    from PIL import ImageOps

    # Gather all classes that have at least 3 valid images
    class_folders = sorted([
        d for d in os.listdir(ALL_DATA_DIR)
        if os.path.isdir(os.path.join(ALL_DATA_DIR, d))
        and len([f for f in os.listdir(os.path.join(ALL_DATA_DIR, d)) if f.endswith((".jpg", ".jpeg", ".png"))]) >= 3
    ])

    num_classes = len(class_folders)
    class_to_idx = {c_name: idx for idx, c_name in enumerate(class_folders)}
    print(f"Training All-Rounder Model across {num_classes} distinct dermatological diseases!")

    # Load all images into memory (preprocessed identically to backend/model.py)
    X_list = []
    y_list = []

    for c_name in class_folders:
        c_idx = class_to_idx[c_name]
        c_dir = os.path.join(ALL_DATA_DIR, c_name)
        files = [f for f in os.listdir(c_dir) if f.endswith((".jpg", ".jpeg", ".png"))]
        for fname in files:
            fpath = os.path.join(c_dir, fname)
            try:
                img = Image.open(fpath).convert("RGB")
                try:
                    img = ImageOps.autocontrast(img, cutoff=0.5)
                except Exception:
                    pass
                img = img.resize((224, 224), Image.Resampling.LANCZOS)
                arr = np.array(img, dtype=np.float32) / 255.0
                X_list.append(arr)
                y_list.append(c_idx)
                # For minority classes (<30 images), also add horizontal flip to balance representation
                if len(files) < 30:
                    arr_flip = np.fliplr(arr)
                    X_list.append(arr_flip)
                    y_list.append(c_idx)
            except Exception:
                continue

    X_all = np.array(X_list, dtype=np.float32)
    y_all = np.array(y_list, dtype=np.int32)
    print(f"Prepared training tensor: X={X_all.shape}, y={y_all.shape} across {num_classes} classes.")

    # Shuffle dataset
    rng = np.random.default_rng(42)
    perm = rng.permutation(len(X_all))
    X_all = X_all[perm]
    y_all = y_all[perm]

    # Step 1: Build MobileNetV2 Feature Extractor (flat layers for Grad-CAM compatibility)
    print("Building MobileNetV2 base model and extracting deep feature representations...")
    base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False

    gap_layer = GlobalAveragePooling2D(name="global_avg_pool")
    feat_extractor = Model(inputs=base_model.input, outputs=gap_layer(base_model.output))

    # Extract 1280-dim features in fast batches
    features = feat_extractor.predict(X_all, batch_size=64, verbose=1)
    print(f"Extracted feature matrix: {features.shape}")

    # Step 2: Train high-capacity multi-disease classification head on extracted features
    feat_input = tf.keras.Input(shape=(1280,))
    bn1 = BatchNormalization(name="head_bn")(feat_input)
    drop1 = Dropout(0.25, name="head_drop1")(bn1)
    dense1 = Dense(512, activation="relu", name="head_dense1")(drop1)
    bn2 = BatchNormalization(name="head_bn2")(dense1)
    drop2 = Dropout(0.20, name="head_drop2")(bn2)
    out_layer = Dense(num_classes, activation="softmax", name="predictions")(drop2)

    head_model = Model(inputs=feat_input, outputs=out_layer)

    # Compute mild balanced sample weights so rare diseases and common diseases both learn well
    class_counts = np.bincount(y_all, minlength=num_classes)
    class_weights = {
        i: float(np.clip(len(y_all) / (num_classes * max(class_counts[i], 1)), 0.5, 4.0))
        for i in range(num_classes)
    }

    y_cat = tf.keras.utils.to_categorical(y_all, num_classes=num_classes)

    lr_schedule = tf.keras.optimizers.schedules.CosineDecay(
        initial_learning_rate=3e-3,
        decay_steps=60 * (len(X_all) // 64 + 1),
        alpha=1e-2
    )
    head_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=lr_schedule),
        loss="categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.TopKCategoricalAccuracy(k=3, name="top3_acc")]
    )

    print(f"Training All-Rounder {num_classes}-Class Dermatology Classifier Head (60 Epochs)...")
    head_model.fit(
        features,
        y_cat,
        batch_size=64,
        epochs=60,
        validation_split=0.12,
        class_weight=class_weights,
        verbose=1
    )

    # Step 3: Assemble Full End-to-End Model (Input -> MobileNetV2 -> GAP -> Head) for Grad-CAM + Inference
    x = gap_layer(base_model.output)
    x = head_model.get_layer("head_bn")(x)
    x = head_model.get_layer("head_drop1")(x)
    x = head_model.get_layer("head_dense1")(x)
    x = head_model.get_layer("head_bn2")(x)
    x = head_model.get_layer("head_drop2")(x)
    preds = head_model.get_layer("predictions")(x)

    full_model = Model(inputs=base_model.input, outputs=preds)
    full_model.save(MODEL_PATH)
    print(f"Saved full end-to-end {num_classes}-Class All-Rounder model to {MODEL_PATH}!")

    # Save updated class_indices.json
    with open(CLASS_INDICES_PATH, "w", encoding="utf-8") as f:
        json.dump(class_to_idx, f, indent=2)
    print(f"Saved {num_classes} disease classes to {CLASS_INDICES_PATH}!")


if __name__ == "__main__":
    download_all_fitzpatrick_classes()
    train_allrounder_model()

