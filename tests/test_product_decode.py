import pytest
import product_decode

class TestGetTitleOfProduct:
    """Test cases for the get_title_of_product function."""

    def test_invalid_data_type_raises_exception(self):
        """Test that passing an invalid data type raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_title_of_product("Test")

    def test_missing_field_raises_exception(self):
        """Test that passing a dictionary with a missing 'title' field raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_title_of_product({"any": "Test"})

    def test_invalid_field_value_raises_exception(self):
        """Test that passing a dictionary with an invalid 'title' field value raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_title_of_product({"title": 2})

    def test_valid_field_returns_title(self):
        """Test that passing a dictionary with a valid 'title' field returns the correct title."""
        assert product_decode.get_title_of_product({"title": "Title"}) == "Title"

class TestGetDescriptionOfProduct:
    """Test cases for the get_description_of_product function."""

    def test_invalid_data_type_raises_exception(self):
        """Test that passing an invalid data type raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_description_of_product("Test")

    def test_missing_field_raises_exception(self):
        """Test that passing a dictionary with a missing 'description' field raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_description_of_product({"any": "Test"})

    def test_invalid_field_value_raises_exception(self):
        """Test that passing a dictionary with an invalid 'description' field value raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_description_of_product({"description": 2})

    def test_valid_field_returns_title(self):
        """Test that passing a dictionary with a valid 'description' field returns the correct description."""
        assert product_decode.get_description_of_product({"description": "Description"}) == "Description"

class TestGetPriceOfProduct:
    """Test cases for the get_price_of_product function."""

    def test_invalid_data_type_raises_exception(self):
        """Test that passing an invalid data type raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_price_of_product("Test")

    def test_missing_field_raises_exception(self):
        """Test that passing a dictionary with a missing 'price' field raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_price_of_product({"any": "Test"})

    def test_invalid_field_value_raises_exception(self):
        """Test that passing a dictionary with an invalid 'price' field value raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_price_of_product({"price": {"totalPrice": {"discountPrice": 0.2}}})

    def test_valid_field_returns_price(self):
        """Test that passing a dictionary with a valid 'price' field returns the correct price."""
        assert product_decode.get_price_of_product({"price": {"totalPrice": {"discountPrice": 1239}}}) == 1239
