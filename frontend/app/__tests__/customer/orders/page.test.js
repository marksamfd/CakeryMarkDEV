import '@testing-library/jest-dom';
import { render } from '@testing-library/react';
import OrdersPage from '@/app/(customer)/orders/page';

describe('OrdersPage Component', () => {
  it('renders the orders title', () => {
    const { container } = render(<OrdersPage />);
    expect(container).toMatchSnapshot();
  });

  it('renders the order list', () => {
    const { container } = render(<OrdersPage />);
    expect(container).toMatchSnapshot();
  });
});