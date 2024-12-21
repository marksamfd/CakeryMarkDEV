'use client';
import { useState, useEffect } from 'react';
import ProductDetails from '../../components/productDetails';
import Breadcrumb from '../../components/breadcrumb';

/**
 * ShopDetails
 *
 * Fetches product details from the API and displays a detailed view of the product.
 *
 * Handles loading and error states, and allows the user to change the selected image, and
 * increment or decrement the product quantity.
 *
 * @returns {JSX.Element} A JSX element representing a product details page.
 */
export default function ShopDetails() {
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [image, setimage] = useState();
  const [quantity, setQuantity] = useState(1);
  const [stars, setStars] = useState(1);
  const productId = window.location.pathname.split('/')[2];

  useEffect(() => {
    cookieStore
      .get('token')
      .then((cookie) =>
        fetch(`/api/cakery/user/customer/Product/${productId}`, {
          headers: {
            Authorization: `Bearer ${cookie?.value}`,
          },
        }),
      )
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setProduct(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching product details:', error);
        setLoading(false);
      });
  }, [productId]);

  const handleThumbnailClick = (image) => {
    setimage(image);
  };

  /**
   * Handles the increment or decrement of the product quantity when the user
   * clicks on the + or - buttons.
   *
   * @param {string} type - The type of change, either 'increment' or 'decrement'.
   */

  const handleQuantityChange = (type) => {
    setQuantity((prevQuantity) => {
      if (type === 'increment') {
        return prevQuantity + 1;
      } else if (type === 'decrement' && prevQuantity > 1) {
        return prevQuantity - 1;
      }
      return prevQuantity;
    });
  };
  const ratingChanged = (newRating) => {
    cookieStore
      .get('token')
      .then((cookie) =>
        fetch(`/api//cakery/user/customer/Review`, {
          method: 'Post',
          headers: {
            Authorization: `Bearer ${cookie?.value}`,
          },
          body: { rating: newRating, productid: productId },
        }),
      )
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        setProduct(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error fetching product details:', error);
        setLoading(false);
      });
    console.log(newRating);
  };
  console.log(product);
  if (loading) return <p>Loading product details...</p>;
  if (!product) return <p>No product details found.</p>;

  return (
    <>
      <Breadcrumb title="Product Details" />
      <ProductDetails
        product={product}
        image={image}
        handleThumbnailClick={handleThumbnailClick}
        quantity={quantity}
        handleQuantityChange={handleQuantityChange}
        rating={stars}
        handleRatingChange={ratingChanged}
      />
      <br />  
    </>
  );
}
