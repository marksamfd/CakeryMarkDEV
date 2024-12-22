import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/react';
import OrderItem from '@/app/(customer)/components/orderItem';

describe('OrderItem Component', () => {
  const mockProps = {
    productName: 'Test Cake',
    quantity: 2,
    status: 'Delivered',
    totalPrice: 20,
  };

  it('renders product name', () => {
    render(<OrderItem {...mockProps} />);
    const productName = screen.getByText(/Test Cake/i);
    expect(productName).toBeInTheDocument();
  });

  it('renders product quantity', () => {
    render(<OrderItem {...mockProps} />);
    const quantity = screen.getByText(/Quantity : 2/i);
    expect(quantity).toBeInTheDocument();
  });

  it('renders product status', () => {
    render(<OrderItem {...mockProps} />);
    const status = screen.getByText(/Delivered/i);
    expect(status).toBeInTheDocument();
  });

  it('renders total price', () => {
    render(<OrderItem {...mockProps} />);
    const totalPrice = screen.getByText(/20 EGP/i);
    expect(totalPrice).toBeInTheDocument();
  });
});