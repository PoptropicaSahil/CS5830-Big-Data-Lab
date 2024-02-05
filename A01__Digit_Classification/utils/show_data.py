import matplotlib.pyplot as plt


def plot_image(image, label=None):
    # fig, axes = plt.plot(figsize=(12, 3))
    if label is None:
        plt.title("Plot given figure")
    else:
        plt.title(f"Plot given figure \n Label: {label}")
    plt.imshow(image.numpy().squeeze(), cmap="gray")
    plt.axis("off")
    plt.show()
