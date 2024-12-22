import '@testing-library/jest-dom';
import { render, screen, fireEvent } from '@testing-library/react';
import CartItem from '@/app/(customer)/components/cartItem';

describe('CartItem Component', () => {
  const mockProps = {
    cartid: 1,
    productId: 1,
    productname: 'Test Cake',
    cartitemid: 1,
    customcakeid: 1,
    quantity: 2,
    price: 10,
    total: 20,
    onRemove: jest.fn(),
    onIncrease: jest.fn(),
    onDecrease: jest.fn(),
  };

  it('renders product name', () => {
    render(<CartItem {...mockProps} />);
    const productName = screen.getByText(/Test Cake/i);
    expect(productName).toBeInTheDocument();
  });

  it('renders product price', () => {
    render(<CartItem {...mockProps} />);
    const price = screen.getByText(/\$10/i);
    expect(price).toBeInTheDocument();
  });

  it('renders total price', () => {
    render(<CartItem {...mockProps} />);
    const total = screen.getByText(/\$20/i);
    expect(total).toBeInTheDocument();
  });

  it('calls onIncrease when increase button is clicked', () => {
    render(<CartItem {...mockProps} />);
    const increaseButton = screen.getByTitle('Add item');
    fireEvent.click(increaseButton);
    expect(mockProps.onIncrease).toHaveBeenCalled();
  });

  it('calls onDecrease when decrease button is clicked', () => {
    render(<CartItem {...mockProps} />);
    const decreaseButton = screen.getByTitle('decrease item');
    fireEvent.click(decreaseButton);
    expect(mockProps.onDecrease).toHaveBeenCalled();
  });

  it('calls onRemove when remove button is clicked', () => {
    render(<CartItem {...mockProps} />);
    const removeButton = screen.getByTitle('Remove item');
    fireEvent.click(removeButton);
    expect(mockProps.onRemove).toHaveBeenCalled();
  });
});
