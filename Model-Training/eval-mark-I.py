from __future__ import annotations

import os
import numpy as np
from keras.models import load_model
from keras.preprocessing import image
from sklearn.metrics.pairwise import euclidean_distances

# Function to load and preprocess images
def load_and_preprocess_image(img_path, target_size=(160, 160)):
    try:
        img = image.load_img(img_path, target_size=target_size)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0
        return img_array
    except Exception as e:
        print(f"Error loading image {img_path}: {e}")
        return None

# Function to generate embeddings
def generate_embeddings(model, dataset_path):
    embeddings = []
    labels = []

    for class_name in os.listdir(dataset_path):
        class_path = os.path.join(dataset_path, class_name)
        if not os.path.isdir(class_path):
            continue

        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img_array = load_and_preprocess_image(img_path)
            if img_array is None:
                continue
            embedding = model.predict(img_array)
            embeddings.append(embedding[0])
            labels.append(class_name)

    embeddings = np.array(embeddings)
    labels = np.array(labels)
    return embeddings, labels

# Function to calculate intra-cluster distances
def calculate_intra_cluster_distances(embeddings, labels):
    unique_labels = np.unique(labels)
    distances = []

    for label in unique_labels:
        cluster_embeddings = embeddings[labels == label]
        avg_embedding = np.mean(cluster_embeddings, axis=0)
        max_distance = np.max(
            euclidean_distances(
                cluster_embeddings,
                [avg_embedding],
            ),
        )
        distances.append(max_distance)

    return np.array(distances)

# Load the pre-trained FaceNet model
model_path = "facenet_model.h5"
model = load_model(model_path)

# Path to the dataset
dataset_path = "path_to_your_dataset"

# Generate embeddings for the original model
embeddings_original, labels = generate_embeddings(model, dataset_path)

# Load the fine-tuned model
finetuned_model_path = "facenet_model_finetuned.h5"
finetuned_model = load_model(finetuned_model_path)

# Generate embeddings for the fine-tuned model
embeddings_finetuned, _ = generate_embeddings(finetuned_model, dataset_path)

# Calculate intra-cluster distances for both models
intra_distances_original = calculate_intra_cluster_distances(
    embeddings_original,
    labels,
)
intra_distances_finetuned = calculate_intra_cluster_distances(
    embeddings_finetuned,
    labels,
)

# Compare intra-cluster distances
intra_distance_change = intra_distances_finetuned - intra_distances_original

# Output the results
print(f"Intra-Cluster Distance Change: {intra_distance_change}")
print(f"Mean Distance Change: {np.mean(intra_distance_change)}")
print(f"Positive Impact: {np.sum(intra_distance_change < 0)}")
print(f"Negative Impact: {np.sum(intra_distance_change > 0)}")
print(f"Average Impact: {np.sum(intra_distance_change == 0)}")
