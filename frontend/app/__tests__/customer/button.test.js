import '@testing-library/jest-dom';
import { render, screen, fireEvent } from '@testing-library/react';
import Button from '@/app/(customer)/components/button';

describe('Button Component', () => {
  it('renders button with children', () => {
    render(<Button>Click Me</Button>);
    const button = screen.getByText(/Click Me/i);
    expect(button).toBeInTheDocument();
  });

  it('calls onClick when button is clicked', () => {
    const handleClick = jest.fn();
    render(<Button onClick={handleClick}>Click Me</Button>);
    const button = screen.getByText(/Click Me/i);
    fireEvent.click(button);
    expect(handleClick).toHaveBeenCalled();
  });
});