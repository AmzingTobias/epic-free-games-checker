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
        assert product_decode.get_title_of_product(
            {"title": "Title"}) == "Title"


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
        assert product_decode.get_description_of_product(
            {"description": "Description"}) == "Description"


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
            product_decode.get_price_of_product(
                {"price": {"totalPrice": {"discountPrice": 0.2}}})

    def test_valid_field_returns_price(self):
        """Test that passing a dictionary with a valid 'price' field returns the correct price."""
        assert product_decode.get_price_of_product(
            {"price": {"totalPrice": {"discountPrice": 1239}}}) == 1239


class TestGetProductThumbnail:
    """Test cases for the get_thumbnail_of_product function."""

    def test_invalid_data_type_raises_exception(self):
        """Test that passing an invalid data type raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_thumbnail_of_product("keyImages")

    def test_missing_field_raises_exception(self):
        """Test that passing a dictionary with a missing 'keyImages' field raises a ProductDecodeException."""
        assert product_decode.get_thumbnail_of_product({"any": "Test"}) is None

    def test_invalid_field_value_raises_exception(self):
        """Test that passing a dictionary with an invalid 'keyImages' field value raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_thumbnail_of_product({"keyImages": 2})

    def test_valid_field_returns_none(self):
        """Test that passing a dictionary with a valid 'keyImages' field returns None, if no image exists with type Thumbnail."""
        sample_data = {"keyImages": [
            {"type": "Image", "url": "invalid"}]}
        assert product_decode.get_thumbnail_of_product(
            sample_data) is None

    def test_valid_field_returns_thumbnail(self):
        """Test that passing a dictionary with a valid 'keyImages' field returns the correct thumbnail."""
        sample_data = {"keyImages": [
            {"type": "Image", "url": "invalid"}, {"type": "Thumbnail", "url": "valid"}]}
        assert product_decode.get_thumbnail_of_product(
            sample_data) == "valid"

    def test_invalid_thumbnail_data_raises_exception(self):
        """Test that passing a dictionary with a valid 'keyImages' field but invalid data type is ignored."""
        sample_data = {"keyImages": [
            {"type": "Image", "url": "invalid"}, {"type": "Thumbnail", "url": 0}]}
        assert product_decode.get_thumbnail_of_product(
            sample_data) is None


class TestProductURL:
    """Test cases for the get_product_url function."""

    def test_invalid_data_type_raises_exception(self):
        """Test that passing an invalid data type raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_product_url("url")

    def test_missing_field_raises_exception(self):
        """Test that passing a dictionary with a missing 'offerMappings' field raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_product_url({"any": "Test"})

    def test_invalid_field_value_raises_exception(self):
        """Test that passing a dictionary with an invalid 'offerMappings' field value raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            product_decode.get_product_url({"offerMappings": 2})

    def test_valid_field_returns_url(self):
        """Test that passing a dictionary with a valid 'pageSlug' field returns the first URL."""
        sample_data = {"offerMappings": [{"pageSlug": "url1"}, {"pageSlug": "url2"}]}
        assert product_decode.get_product_url(sample_data) == "url1"

    def test_invalid_url_data_raises_exception(self):
        """Test that passing a dictionary with a valid 'pageSlug' field but invalid data type raises a ProductDecodeException."""
        with pytest.raises(product_decode.ProductDecodeException):
            sample_data = {"offerMappings": [{"pageSlug": 2}, {"pageSlug": "url2"}]}
            product_decode.get_product_url(sample_data)


class TestDecodeProduct:
    """Test cases for the decode_product function."""

    def test_valid_product_returns_game(self):
        """Test that passing valid product will return a game."""
        test_valid_product = {
            "title": "title",
            "description": "description",
            "price": {"totalPrice": {"discountPrice": 1000}},
            "offerMappings": [{"pageSlug": "url1"}, {"pageSlug": "url2"}],
            "keyImages": [
                {"type": "Image", "url": "invalid"}, {"type": "Thumbnail", "url": "valid"}]
        }
        game = product_decode.decode_product(test_valid_product)
        assert isinstance(game, product_decode.Game)
        assert game.title == "title"
        assert game.description == "description"
        assert game.product_url == "url1"
        assert game.price == 1000
        assert game.thumbnail_url == "valid"

    def test_invalid_product_data_type_returns_none(self):
        """Test that passing invalid data will return None."""
        game = product_decode.decode_product(None)
        assert game is None

    def test_product_missing_field_returns_none(self):
        """Test that passing a product with a missing key field will return None."""
        missing_field_product = {
            "title": "title",
            "price": {"totalPrice": {"discountPrice": 0}},
            "offerMappings": [{"pageSlug": "url1"}, {"pageSlug": "url2"}],
            "keyImages": [
                {"type": "Image", "url": "invalid"}, {"type": "Thumbnail", "url": "valid"}]
        }
        game = product_decode.decode_product(missing_field_product)
        assert game is None

    def test_product_missing_thumbnail_returns_game(self):
        """Test that passing invalid data will return None."""
        test_valid_product = {
            "title": "title",
            "description": "description",
            "price": {"totalPrice": {"discountPrice": 1000}},
            "offerMappings": [{"pageSlug": "url1"}, {"pageSlug": "url2"}],
        }
        game = product_decode.decode_product(test_valid_product)
        assert isinstance(game, product_decode.Game)
        assert game.title == "title"
        assert game.description == "description"
        assert game.product_url == "url1"
        assert game.price == 1000
        assert game.thumbnail_url is None
