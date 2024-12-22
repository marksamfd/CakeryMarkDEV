import '@testing-library/jest-dom';
import { render, screen, fireEvent } from '@testing-library/react';
import ProductDetails from '@/app/(customer)/components/productDetails';

describe('ProductDetails Component', () => {
  const mockProps = {
    product: {
      name: 'Test Cake',
      price: 10,
      description: 'Delicious cake',
      category: 'Cakes',
      image: '/path/to/image.jpg',
    },
    image: '/path/to/image.jpg',
    handleThumbnailClick: jest.fn(),
    quantity: 1,
    handleQuantityChange: jest.fn(),
    rating: 5,
    handleRatingChange: jest.fn(),
  };

  it('renders product name', () => {
    render(<ProductDetails {...mockProps} />);
    const productName = screen.getByText(/Test Cake/i);
    expect(productName).toBeInTheDocument();
  });

  it('renders product price', () => {
    render(<ProductDetails {...mockProps} />);
    const price = screen.getByText(/\$10/i);
    expect(price).toBeInTheDocument();
  });

  it('renders product description', () => {
    render(<ProductDetails {...mockProps} />);
    const description = screen.getByText(/Delicious cake/i);
    expect(description).toBeInTheDocument();
  });

  it('calls handleQuantityChange when quantity is changed', () => {
    render(<ProductDetails {...mockProps} />);
    const incrementButton = screen.getByText('+');
    fireEvent.click(incrementButton);
    expect(mockProps.handleQuantityChange).toHaveBeenCalled();
  });

});