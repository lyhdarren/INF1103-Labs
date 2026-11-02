from .product import Product

# ======================
# DIGITAL PRODUCT
# ======================
class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock, downloadable_size):
        super().__init__(product_id, name, price, stock)
        self.__downloadsize = downloadable_size

    def get_download_size(self) -> float:
        return self.__downloadsize

    def display_information(self):
        super().display_information()
        print(f"Type: Digital | Download Size: {self.__downloadsize} MB")

    def get_fulfillment_info(self) -> str:
        return f"Delivered electronically ({self.__downloadsize} MB download)."
