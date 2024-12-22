import '@testing-library/jest-dom';
import { render, screen, fireEvent } from '@testing-library/react';
import CheckoutInputField from '@/app/(customer)/components/checkoutInput';

describe('CheckoutInputField Component', () => {
  it('renders input field with label', () => {
    render(<CheckoutInputField label="Name" />);
    const label = screen.getByText(/Name/i);
    expect(label).toBeInTheDocument();
  });
});